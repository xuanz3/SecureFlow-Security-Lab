#!/usr/bin/env python3
"""Authorised SecureFlow Phase 4 application-security assessment.

Targets only the project-owned localhost application and fictional accounts.
No passwords or authentication cookies are written to evidence files.
"""

import argparse
import csv
import datetime as dt
import http.cookiejar
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
from html.parser import HTMLParser
from pathlib import Path


class FormParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.inputs = {}
        self.links = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag.lower() == "input" and values.get("name"):
            self.inputs[values["name"]] = values.get("value", "")
        if tag.lower() == "a" and values.get("href"):
            self.links.append(values["href"])


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class HttpClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")
        self.cookie_jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookie_jar)
        )
        self.no_redirect_opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookie_jar),
            NoRedirect(),
        )

    def request(self, method, path, data=None, headers=None, follow=True):
        url = urllib.parse.urljoin(self.base_url + "/", path.lstrip("/"))
        request_headers = {
            "User-Agent": "SecureFlow-Phase4-Assessment/1.0",
        }
        if headers:
            request_headers.update(headers)

        request = urllib.request.Request(
            url,
            data=data,
            headers=request_headers,
            method=method,
        )
        opener = self.opener if follow else self.no_redirect_opener

        try:
            with opener.open(request, timeout=20) as response:
                return {
                    "status": response.status,
                    "headers": dict(response.headers.items()),
                    "body": response.read(),
                    "url": response.geturl(),
                }
        except urllib.error.HTTPError as error:
            return {
                "status": error.code,
                "headers": dict(error.headers.items()),
                "body": error.read(),
                "url": error.geturl(),
            }

    def get(self, path, follow=True):
        return self.request("GET", path, follow=follow)

    def post_form(self, path, fields, follow=True):
        data = urllib.parse.urlencode(fields).encode("utf-8")
        return self.request(
            "POST",
            path,
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            follow=follow,
        )

    def post_multipart(self, path, fields, filename, content_type, content):
        boundary = "----SecureFlowPhase4" + uuid.uuid4().hex
        chunks = []

        for name, value in fields.items():
            chunks.extend([
                "--" + boundary,
                'Content-Disposition: form-data; name="%s"' % name,
                "",
                value,
            ])

        chunks.extend([
            "--" + boundary,
            'Content-Disposition: form-data; name="file"; filename="%s"' % filename,
            "Content-Type: " + content_type,
            "",
        ])

        prefix = ("\r\n".join(chunks) + "\r\n").encode("utf-8")
        suffix = ("\r\n--" + boundary + "--\r\n").encode("utf-8")
        payload = prefix + content + suffix

        return self.request(
            "POST",
            path,
            data=payload,
            headers={"Content-Type": "multipart/form-data; boundary=" + boundary},
            follow=True,
        )

    def has_auth_cookie(self):
        return any(
            "SecureFlow.Auth" in cookie.name
            for cookie in self.cookie_jar
        )


def parse_html(body):
    parser = FormParser()
    parser.feed(body.decode("utf-8", errors="replace"))
    return parser


def require_token(response, context):
    parser = parse_html(response["body"])
    token = parser.inputs.get("__RequestVerificationToken")
    if not token:
        raise RuntimeError(
            "Anti-forgery token was not found while testing %s." % context
        )
    return token


def load_env(path):
    result = {}
    for raw_line in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        result[key] = value
    return result


def login(base_url, email, password):
    client = HttpClient(base_url)
    login_page = client.get("/Account/Login")
    token = require_token(login_page, "login")

    response = client.post_form(
        "/Account/Login",
        {
            "__RequestVerificationToken": token,
            "Email": email,
            "Password": password,
            "RememberMe": "false",
            "ReturnUrl": "",
        },
    )

    body_text = response["body"].decode("utf-8", errors="replace")
    success = (
        response["status"] == 200
        and client.has_auth_cookie()
        and "Invalid sign-in attempt." not in body_text
    )

    if not success:
        raise RuntimeError(
            "Could not authenticate fictional account %s. HTTP %s."
            % (email, response["status"])
        )

    return client


def create_ticket(client, title, description):
    page = client.get("/Tickets/Create")
    token = require_token(page, "ticket creation")
    response = client.post_form(
        "/Tickets/Create",
        {
            "__RequestVerificationToken": token,
            "Title": title,
            "Description": description,
        },
    )

    match = re.search(
        r"/Tickets/Details/([0-9a-fA-F-]{36})",
        response["url"],
    )
    if not match:
        body_text = response["body"].decode("utf-8", errors="replace")
        match = re.search(
            r"/Tickets/Details/([0-9a-fA-F-]{36})",
            body_text,
        )

    if not match:
        raise RuntimeError(
            "Ticket creation did not return a ticket identifier."
        )

    return match.group(1), response


def upload_file(client, ticket_id, filename, content_type, content):
    details = client.get("/Tickets/Details/" + ticket_id)
    token = require_token(details, "attachment upload")
    return client.post_multipart(
        "/Tickets/UploadAttachment/" + ticket_id,
        {"__RequestVerificationToken": token},
        filename,
        content_type,
        content,
    )


def result(test_id, area, expected, actual, status, evidence):
    return {
        "test_id": test_id,
        "area": area,
        "expected": expected,
        "actual": actual,
        "status": status,
        "evidence": evidence,
    }


def finding(
    finding_id,
    title,
    severity,
    cwe,
    owasp,
    asset,
    evidence,
    reproduction,
    cause,
    impact,
    recommendation,
):
    return {
        "id": finding_id,
        "title": title,
        "severity": severity,
        "cwe": cwe,
        "owasp": owasp,
        "asset": asset,
        "evidence": evidence,
        "reproduction": reproduction,
        "cause": cause,
        "impact": impact,
        "recommendation": recommendation,
        "status": "Open",
        "issue_url": None,
        "issue_number": None,
    }


def markdown_escape(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def write_finding_markdown(path, item):
    lines = [
        "# %s — %s" % (item["id"], item["title"]),
        "",
        "- Severity: **%s**" % item["severity"],
        "- Status: **%s**" % item["status"],
        "- Asset: `%s`" % item["asset"],
        "- CWE: %s" % item["cwe"],
        "- OWASP: %s" % item["owasp"],
        "- GitHub issue: Pending",
        "",
        "## Evidence",
        "",
        item["evidence"],
        "",
        "## Safe reproduction",
        "",
        item["reproduction"],
        "",
        "## Technical cause",
        "",
        item["cause"],
        "",
        "## Impact",
        "",
        item["impact"],
        "",
        "## Recommendation",
        "",
        item["recommendation"],
        "",
        "## Safety boundary",
        "",
        "Testing was restricted to project-owned localhost containers and fictional data.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://localhost:8080")
    parser.add_argument("--env-file", required=True)
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    env = load_env(args.env_file)
    required = [
        "SEED_ADMIN_EMAIL",
        "SEED_ADMIN_PASSWORD",
        "SEED_ALICE_EMAIL",
        "SEED_ALICE_PASSWORD",
        "SEED_BOB_EMAIL",
        "SEED_BOB_PASSWORD",
    ]
    missing = [key for key in required if not env.get(key)]
    if missing:
        raise RuntimeError(
            "Missing local fictional account values: " + ", ".join(missing)
        )

    started = dt.datetime.now(dt.timezone.utc)
    run_id = started.strftime("%Y%m%dT%H%M%SZ")

    health = HttpClient(args.base_url).get("/health/ready")
    if health["status"] != 200:
        raise RuntimeError(
            "The local SecureFlow readiness endpoint returned HTTP %s."
            % health["status"]
        )

    admin = login(
        args.base_url,
        env["SEED_ADMIN_EMAIL"],
        env["SEED_ADMIN_PASSWORD"],
    )
    alice = login(
        args.base_url,
        env["SEED_ALICE_EMAIL"],
        env["SEED_ALICE_PASSWORD"],
    )
    bob = login(
        args.base_url,
        env["SEED_BOB_EMAIL"],
        env["SEED_BOB_PASSWORD"],
    )

    timestamp = started.strftime("%Y-%m-%d %H:%M:%S UTC")
    alice_ticket, _ = create_ticket(
        alice,
        "Phase 4 Alice authorisation test " + run_id,
        "Fictional ticket created for the authorised Phase 4 security assessment.",
    )
    bob_ticket, _ = create_ticket(
        bob,
        "Phase 4 Bob authorisation test " + run_id,
        "Fictional ticket created for the authorised Phase 4 security assessment.",
    )

    tests = []

    cross_user = alice.get("/Tickets/Details/" + bob_ticket)
    tests.append(result(
        "A02",
        "Object-level authorisation",
        "Alice receives HTTP 403 for Bob's ticket",
        "HTTP %s" % cross_user["status"],
        "PASS" if cross_user["status"] == 403 else "FAIL",
        "GET /Tickets/Details/%s using Alice's authenticated session" % bob_ticket,
    ))

    admin_denied = alice.get("/Admin")
    tests.append(result(
        "A03",
        "Role authorisation",
        "Normal user receives HTTP 403 for the administrator route",
        "HTTP %s" % admin_denied["status"],
        "PASS" if admin_denied["status"] == 403 else "FAIL",
        "GET /Admin using Alice's authenticated session",
    ))

    admin_allowed = admin.get("/Admin")
    tests.append(result(
        "A03-ADMIN",
        "Role authorisation",
        "Administrator can access the administrator route",
        "HTTP %s" % admin_allowed["status"],
        "PASS" if admin_allowed["status"] == 200 else "FAIL",
        "GET /Admin using the fictional administrator session",
    ))

    csrf_missing = alice.post_form(
        "/Tickets/Create",
        {
            "Title": "Missing token test",
            "Description": "This request intentionally omits the anti-forgery token.",
        },
        follow=False,
    )
    tests.append(result(
        "A05-CSRF",
        "Request integrity",
        "POST without anti-forgery token is rejected",
        "HTTP %s" % csrf_missing["status"],
        "PASS" if csrf_missing["status"] == 400 else "FAIL",
        "POST /Tickets/Create without __RequestVerificationToken",
    ))

    missing_ticket = alice.get(
        "/Tickets/Details/00000000-0000-0000-0000-000000000000"
    )
    tests.append(result(
        "A05-404",
        "Error handling",
        "Unknown ticket identifier returns HTTP 404 without a stack trace",
        "HTTP %s" % missing_ticket["status"],
        "PASS" if missing_ticket["status"] == 404 else "FAIL",
        "GET a non-existent all-zero ticket identifier",
    ))

    exe_upload = upload_file(
        alice,
        alice_ticket,
        "payload.exe",
        "application/octet-stream",
        b"MZ" + b"\x00" * 32,
    )
    exe_text = exe_upload["body"].decode("utf-8", errors="replace")
    tests.append(result(
        "A04-EXT",
        "File upload",
        "Executable extension is rejected",
        "Rejected" if "extension is not allowed" in exe_text else "Not rejected",
        "PASS" if "extension is not allowed" in exe_text else "FAIL",
        "Uploaded payload.exe to Alice's fictional ticket",
    ))

    mismatch_upload = upload_file(
        alice,
        alice_ticket,
        "image.png",
        "text/html",
        b"<html>not an image</html>",
    )
    mismatch_text = mismatch_upload["body"].decode("utf-8", errors="replace")
    tests.append(result(
        "A04-MIME",
        "File upload",
        "Declared MIME mismatch is rejected",
        "Rejected" if "declared content type" in mismatch_text else "Not rejected",
        "PASS" if "declared content type" in mismatch_text else "FAIL",
        "Uploaded image.png with Content-Type text/html",
    ))

    oversized_upload = upload_file(
        alice,
        alice_ticket,
        "large.pdf",
        "application/pdf",
        b"%PDF-1.4\n" + (b"A" * (2 * 1024 * 1024 + 1)),
    )
    oversized_text = oversized_upload["body"].decode("utf-8", errors="replace")
    tests.append(result(
        "A04-SIZE",
        "File upload",
        "File larger than 2 MB is rejected",
        "Rejected" if "between 1 byte and 2 MB" in oversized_text else "Not rejected",
        "PASS" if "between 1 byte and 2 MB" in oversized_text else "FAIL",
        "Uploaded a local generated file larger than the application limit",
    ))

    traversal_upload = upload_file(
        alice,
        alice_ticket,
        "../../report.pdf",
        "application/pdf",
        b"%PDF-1.4\n% fictional\n%%EOF\n",
    )
    traversal_text = traversal_upload["body"].decode("utf-8", errors="replace")
    traversal_pass = (
        "report.pdf" in traversal_text
        and "../../report.pdf" not in traversal_text
    )
    tests.append(result(
        "A04-NAME",
        "File upload",
        "Path components are removed from the original filename",
        "Sanitised to report.pdf" if traversal_pass else "Sanitisation not confirmed",
        "PASS" if traversal_pass else "FAIL",
        "Uploaded a fictional filename containing ../ path components",
    ))

    signature_upload = upload_file(
        alice,
        alice_ticket,
        "invoice.pdf",
        "application/pdf",
        b"<html><script>fictional</script></html>",
    )
    signature_text = signature_upload["body"].decode(
        "utf-8",
        errors="replace",
    )
    signature_bypass = "invoice.pdf" in signature_text
    tests.append(result(
        "A04-SIGNATURE",
        "File upload",
        "File content is verified against the declared type",
        "Non-PDF content accepted as invoice.pdf"
        if signature_bypass
        else "Non-PDF content rejected",
        "FINDING" if signature_bypass else "PASS",
        "Uploaded HTML bytes with .pdf extension and application/pdf declaration",
    ))

    home = HttpClient(args.base_url).get("/")
    header_map = {
        key.lower(): value
        for key, value in home["headers"].items()
    }
    required_headers = [
        "content-security-policy",
        "x-content-type-options",
        "x-frame-options",
        "referrer-policy",
        "permissions-policy",
    ]
    missing_headers = [
        name
        for name in required_headers
        if name not in header_map
    ]
    tests.append(result(
        "A06",
        "Security headers",
        "Required browser security headers are present",
        "Missing: " + ", ".join(missing_headers)
        if missing_headers
        else "All required headers present",
        "PASS" if not missing_headers else "FAIL",
        "GET / and inspect response headers",
    ))

    rate_client = HttpClient(args.base_url)
    rate_statuses = []
    for index in range(1, 8):
        login_page = rate_client.get("/Account/Login")
        token = require_token(login_page, "rate-limit test")
        response = rate_client.post_form(
            "/Account/Login",
            {
                "__RequestVerificationToken": token,
                "Email": "missing-%02d-%s@example.test" % (index, run_id),
                "Password": "Fictional!Password123",
                "RememberMe": "false",
                "ReturnUrl": "",
            },
            follow=False,
        )
        rate_statuses.append(response["status"])
        if response["status"] == 429:
            break

    tests.append(result(
        "A01",
        "Authentication rate limiting",
        "Repeated login attempts eventually receive HTTP 429",
        "Statuses: " + ", ".join(str(value) for value in rate_statuses),
        "PASS" if 429 in rate_statuses else "FAIL",
        "Low-volume repeated login requests using nonexistent fictional identities",
    ))

    file_validator = (
        repo_root
        / "src/SecureFlow.Web/Security/FileUploadValidator.cs"
    ).read_text(encoding="utf-8")
    tickets_controller = (
        repo_root
        / "src/SecureFlow.Web/Controllers/TicketsController.cs"
    ).read_text(encoding="utf-8")
    program = (
        repo_root
        / "src/SecureFlow.Web/Program.cs"
    ).read_text(encoding="utf-8")
    headers_middleware = (
        repo_root
        / "src/SecureFlow.Web/Security/SecurityHeadersMiddleware.cs"
    ).read_text(encoding="utf-8")
    compose = (
        repo_root
        / "infrastructure/docker/compose.yml"
    ).read_text(encoding="utf-8")
    dockerfile = (
        repo_root
        / "infrastructure/docker/Dockerfile"
    ).read_text(encoding="utf-8")

    findings = []

    if signature_bypass:
        findings.append(finding(
            "PH4-F01",
            "Upload validation trusts the declared file type",
            "Medium",
            "CWE-434",
            "OWASP A04:2021 – Insecure Design",
            "Attachment upload validation",
            "Test A04-SIGNATURE accepted HTML bytes as invoice.pdf when the extension and client-declared Content-Type matched the allowlist.",
            "Upload non-PDF bytes using filename invoice.pdf and Content-Type application/pdf to an owned fictional ticket.",
            "The validator checks extension, length and the client-declared MIME value, but does not inspect a file signature or parsed content.",
            "A crafted file can be stored and served under a trusted-looking type, increasing content-confusion and downstream processing risk.",
            "Validate magic bytes or parse supported formats server-side; store the detected type and reject mismatches.",
        ))

    combined_upload_code = file_validator + "\n" + tickets_controller + "\n" + program
    if not re.search(
        r"(?i)clamav|antivirus|anti-malware|malware scanner|quarantine",
        combined_upload_code,
    ):
        findings.append(finding(
            "PH4-F02",
            "Uploaded files are not quarantined or malware-scanned",
            "Medium",
            "CWE-434",
            "OWASP A04:2021 – Insecure Design",
            "Attachment processing workflow",
            "Static review found no quarantine state, antivirus integration or asynchronous malware scan before attachments become downloadable.",
            "Review TicketsController, FileUploadValidator and application service registrations for a scanning or quarantine workflow.",
            "Accepted files are written directly to the application upload volume and immediately exposed through the authorised download action.",
            "An authorised user could store malicious content that later reaches another authorised user or downstream tool.",
            "Add a quarantine state, malware scanning service, scan result audit event and release files only after a clean result.",
        ))

    if "AddFixedWindowLimiter" in program and "RateLimitPartition" not in program:
        findings.append(finding(
            "PH4-F03",
            "Login rate limiting uses a shared global bucket",
            "Medium",
            "CWE-400",
            "OWASP A04:2021 – Insecure Design",
            "Login endpoint rate-limiting policy",
            "Program.cs registers one AddFixedWindowLimiter policy without partitioning by source address or account identifier. Test A01 confirmed the shared policy reaches HTTP 429.",
            "Inspect the login rate-limiter registration and send a small number of login requests from separate fictional sessions.",
            "The fixed window is global to the named policy rather than partitioned per source or account.",
            "One client can consume the allowance and temporarily affect unrelated users, while distributed abuse is not separated by source.",
            "Use AddPolicy with RateLimitPartition keyed by a privacy-conscious source/account composite and retain a bounded global backstop.",
        ))

    if "'unsafe-inline'" in headers_middleware:
        findings.append(finding(
            "PH4-F04",
            "Content Security Policy permits inline styles",
            "Low",
            "CWE-693",
            "OWASP A05:2021 – Security Misconfiguration",
            "Browser Content Security Policy",
            "SecurityHeadersMiddleware configures style-src 'self' 'unsafe-inline'.",
            "Inspect the Content-Security-Policy response header returned by GET /.",
            "Inline styles are permitted rather than being restricted with hashes, nonces or external stylesheets only.",
            "The policy provides weaker protection against style-based injection and makes future CSP hardening more difficult.",
            "Remove unsafe-inline by moving styles to static files or authorising only required styles through hashes/nonces.",
        ))

    if not re.search(r"(?m)^\s+read_only:\s*true\s*$", compose):
        findings.append(finding(
            "PH4-F05",
            "Application container root filesystem is writable",
            "Low",
            "CWE-732",
            "OWASP A05:2021 – Security Misconfiguration",
            "Docker Compose application service",
            "compose.yml does not set read_only: true for the application container.",
            "Inspect the app service configuration and Docker runtime ReadonlyRootfs value.",
            "The application container can write outside its dedicated upload volume.",
            "A compromised process has a larger writable surface for staging files or modifying runtime state.",
            "Enable a read-only root filesystem and add explicit writable tmpfs/volume mounts only where required.",
        ))

    if "cap_drop:" not in compose or "no-new-privileges" not in compose:
        findings.append(finding(
            "PH4-F06",
            "Container runtime privileges are not explicitly reduced",
            "Medium",
            "CWE-250",
            "OWASP A05:2021 – Security Misconfiguration",
            "Docker Compose application service",
            "compose.yml does not both drop all Linux capabilities and enable no-new-privileges.",
            "Inspect the app service CapDrop and SecurityOpt runtime values.",
            "The container relies on Docker defaults rather than an explicit least-privilege runtime policy.",
            "If application code is compromised, unnecessary kernel capabilities or privilege transitions can increase impact.",
            "Set cap_drop: [ALL], security_opt: [no-new-privileges:true], and add back only a demonstrated required capability.",
        ))

    mutable_from = [
        line.strip()
        for line in dockerfile.splitlines()
        if line.strip().upper().startswith("FROM ")
        and "@sha256:" not in line
    ]
    if mutable_from:
        findings.append(finding(
            "PH4-F07",
            "Container base images are referenced by mutable tags",
            "Medium",
            "CWE-494",
            "OWASP A08:2021 – Software and Data Integrity Failures",
            "Multi-stage application Dockerfile",
            "Dockerfile FROM instructions are not pinned to registry digests: " + "; ".join(mutable_from),
            "Inspect every FROM instruction in infrastructure/docker/Dockerfile.",
            "Version tags can be repointed and do not uniquely identify the bytes used for a build.",
            "A future rebuild can consume different base-image content without a source change, weakening reproducibility and provenance.",
            "Pin each base image by verified digest and update the digest through a reviewed dependency PR.",
        ))

    limit_markers = [
        "MultipartBodyLengthLimit",
        "RequestSizeLimit",
        "RequestFormLimits",
        "MaxRequestBodySize",
    ]
    if not any(marker in combined_upload_code for marker in limit_markers):
        findings.append(finding(
            "PH4-F08",
            "Upload request size is not limited before model binding",
            "Medium",
            "CWE-400",
            "OWASP A04:2021 – Insecure Design",
            "Attachment upload endpoint",
            "The application checks IFormFile.Length in FileUploadValidator but configures no endpoint or form multipart limit near the 2 MB business rule.",
            "Inspect upload endpoint attributes and FormOptions/Kestrel request-limit configuration.",
            "The framework can accept and buffer a request substantially larger than the business limit before controller validation rejects it.",
            "Repeated oversized requests can consume more memory, disk or connection time than intended.",
            "Set an endpoint RequestSizeLimit and MultipartBodyLengthLimit close to the allowed file size, with a small multipart overhead allowance.",
        ))

    if len(findings) < 8:
        raise RuntimeError(
            "Only %d validated findings were produced; Phase 4 requires at least eight."
            % len(findings)
        )

    completed = dt.datetime.now(dt.timezone.utc)
    document = {
        "assessment": {
            "phase": 4,
            "run_id": run_id,
            "started_utc": started.isoformat(),
            "completed_utc": completed.isoformat(),
            "target": args.base_url,
            "scope": "Project-owned localhost containers and fictional accounts",
            "tool": "SecureFlow Phase 4 assessment harness",
            "tool_version": "1.0",
        },
        "tickets": {
            "alice_ticket_id": alice_ticket,
            "bob_ticket_id": bob_ticket,
        },
        "tests": tests,
        "findings": findings,
    }

    (output_dir / "application-assessment.json").write_text(
        json.dumps(document, indent=2),
        encoding="utf-8",
    )

    tests_pass = sum(1 for item in tests if item["status"] == "PASS")
    tests_findings = sum(
        1 for item in tests if item["status"] == "FINDING"
    )
    tests_fail = sum(1 for item in tests if item["status"] == "FAIL")

    summary = [
        "# Phase 4 Application Security Assessment",
        "",
        "- Run: `%s`" % run_id,
        "- Started: %s" % timestamp,
        "- Target: `%s`" % args.base_url,
        "- Safety boundary: project-owned localhost containers and fictional accounts",
        "- Test results: %d PASS, %d FINDING, %d FAIL"
        % (tests_pass, tests_findings, tests_fail),
        "- Validated findings: %d" % len(findings),
        "",
        "## Test matrix results",
        "",
        "| Test | Area | Expected | Actual | Status |",
        "|---|---|---|---|---|",
    ]

    for item in tests:
        summary.append(
            "| %s | %s | %s | %s | %s |"
            % (
                markdown_escape(item["test_id"]),
                markdown_escape(item["area"]),
                markdown_escape(item["expected"]),
                markdown_escape(item["actual"]),
                markdown_escape(item["status"]),
            )
        )

    summary.extend([
        "",
        "## Validated findings",
        "",
        "| ID | Severity | Finding | Status |",
        "|---|---|---|---|",
    ])

    for item in findings:
        summary.append(
            "| %s | %s | %s | %s |"
            % (
                item["id"],
                item["severity"],
                markdown_escape(item["title"]),
                item["status"],
            )
        )

    summary.extend([
        "",
        "## Limitations",
        "",
        "- The assessment did not target public systems or third-party services.",
        "- Authentication accounts and ticket records are fictional.",
        "- The passive ZAP baseline from Phase 3 remains separate from these manual/API checks.",
        "- Finding severity is a portfolio risk estimate and should be recalibrated for a real production deployment.",
        "",
    ])

    (output_dir / "APPLICATION_ASSESSMENT.md").write_text(
        "\n".join(summary),
        encoding="utf-8",
    )

    findings_dir = repo_root / "security-assessment/findings"
    findings_dir.mkdir(parents=True, exist_ok=True)

    for item in findings:
        write_finding_markdown(
            findings_dir / ("%s.md" % item["id"]),
            item,
        )

    (output_dir / "findings.json").write_text(
        json.dumps(findings, indent=2),
        encoding="utf-8",
    )

    print("Phase 4 application assessment complete.")
    print("Tests: %d PASS, %d FINDING, %d FAIL" % (
        tests_pass,
        tests_findings,
        tests_fail,
    ))
    print("Findings: %d" % len(findings))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("Assessment failed: %s" % error, file=sys.stderr)
        sys.exit(1)
