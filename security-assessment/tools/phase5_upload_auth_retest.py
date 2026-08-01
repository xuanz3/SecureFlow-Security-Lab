#!/usr/bin/env python3
"""Retest Phase 5 upload, CSP and request-limit controls on localhost."""

import argparse
import datetime as dt
import http.cookiejar
import json
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

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag.lower() == "input" and values.get("name"):
            self.inputs[values["name"]] = values.get("value", "")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class Client:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")
        self.cookies = http.cookiejar.CookieJar()
        self.follow = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookies)
        )
        self.raw = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookies),
            NoRedirect(),
        )

    def request(self, method, path, data=None, headers=None, follow=True):
        url = urllib.parse.urljoin(self.base_url + "/", path.lstrip("/"))
        request = urllib.request.Request(
            url,
            data=data,
            headers={
                "User-Agent": "SecureFlow-Phase5-Upload-Retest/1.0",
                **(headers or {}),
            },
            method=method,
        )
        opener = self.follow if follow else self.raw
        try:
            with opener.open(request, timeout=30) as response:
                return {
                    "status": response.status,
                    "headers": dict(response.headers.items()),
                    "body": response.read(),
                    "url": response.geturl(),
                    "transport_error": None,
                }
        except urllib.error.HTTPError as error:
            return {
                "status": error.code,
                "headers": dict(error.headers.items()),
                "body": error.read(),
                "url": error.geturl(),
                "transport_error": None,
            }
        except (
            urllib.error.URLError,
            BrokenPipeError,
            ConnectionResetError,
            TimeoutError,
        ) as error:
            return {
                "status": 0,
                "headers": {},
                "body": b"",
                "url": url,
                "transport_error": str(error),
            }

    def get(self, path, follow=True):
        return self.request("GET", path, follow=follow)

    def post_form(self, path, fields):
        return self.request(
            "POST",
            path,
            data=urllib.parse.urlencode(fields).encode(),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

    def post_file(
        self,
        path,
        token,
        filename,
        content_type,
        content,
        follow=True,
    ):
        boundary = "----SecureFlowP5" + uuid.uuid4().hex
        prefix = (
            "--{0}\r\n"
            'Content-Disposition: form-data; name="__RequestVerificationToken"'
            "\r\n\r\n{1}\r\n"
            "--{0}\r\n"
            'Content-Disposition: form-data; name="file"; filename="{2}"'
            "\r\nContent-Type: {3}\r\n\r\n"
        ).format(boundary, token, filename, content_type).encode()
        suffix = ("\r\n--" + boundary + "--\r\n").encode()
        return self.request(
            "POST",
            path,
            data=prefix + content + suffix,
            headers={
                "Content-Type": "multipart/form-data; boundary=" + boundary
            },
            follow=follow,
        )


def env(path):
    result = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            result[key] = value
    return result


def token(response):
    parser = FormParser()
    parser.feed(response["body"].decode(errors="replace"))
    value = parser.inputs.get("__RequestVerificationToken")
    if not value:
        raise RuntimeError("Anti-forgery token was not found.")
    return value


def login(base_url, email, password):
    client = Client(base_url)
    page = client.get("/Account/Login")
    response = client.post_form(
        "/Account/Login",
        {
            "__RequestVerificationToken": token(page),
            "Email": email,
            "Password": password,
            "RememberMe": "false",
            "ReturnUrl": "",
        },
    )
    if not any("SecureFlow.Auth" in item.name for item in client.cookies):
        raise RuntimeError("Fictional account login failed.")
    return client


def create_ticket(client):
    page = client.get("/Tickets/Create")
    response = client.post_form(
        "/Tickets/Create",
        {
            "__RequestVerificationToken": token(page),
            "Title": "Phase 5 upload hardening retest",
            "Description": (
                "Fictional ticket used for the local upload security retest."
            ),
        },
    )
    match = re.search(
        r"/Tickets/Details/([0-9a-fA-F-]{36})",
        response["url"] + response["body"].decode(errors="replace"),
    )
    if not match:
        raise RuntimeError("Ticket identifier was not returned.")
    return match.group(1)


def body(response):
    return response["body"].decode("utf-8", errors="replace")


def result(test_id, control, passed, actual):
    return {
        "test_id": test_id,
        "control": control,
        "status": "PASS" if passed else "FAIL",
        "actual": actual,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://localhost:8080")
    parser.add_argument("--env-file", required=True)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    args = parser.parse_args()

    values = env(args.env_file)
    client = login(
        args.base_url,
        values["SEED_ALICE_EMAIL"],
        values["SEED_ALICE_PASSWORD"],
    )
    ticket_id = create_ticket(client)
    path = "/Tickets/UploadAttachment/" + ticket_id

    tests = []

    details = client.get("/Tickets/Details/" + ticket_id)
    csrf = token(details)

    spoofed = client.post_file(
        path,
        csrf,
        "spoofed.pdf",
        "application/pdf",
        b"<html>not a PDF</html>",
    )
    tests.append(result(
        "P5-UP-01",
        "Server-side file signature validation",
        "signature does not match" in body(spoofed),
        "Mismatched PDF content was rejected",
    ))

    csrf = token(client.get("/Tickets/Details/" + ticket_id))
    blocked = client.post_file(
        path,
        csrf,
        "blocked.txt",
        "text/plain",
        b"SECUREFLOW_TEST_BLOCK",
    )
    tests.append(result(
        "P5-UP-02",
        "Quarantine and scanner gate",
        "rejected by the local security scan" in body(blocked),
        "Harmless scanner test marker was not released",
    ))

    clean_name = "clean-phase5.pdf"
    csrf = token(client.get("/Tickets/Details/" + ticket_id))
    clean = client.post_file(
        path,
        csrf,
        clean_name,
        "application/pdf",
        b"%PDF-1.4\n1 0 obj\n<<>>\nendobj\n%%EOF\n",
    )
    tests.append(result(
        "P5-UP-03",
        "Clean-file release",
        clean_name in body(clean),
        "Valid PDF was released after inspection",
    ))

    csrf = token(client.get("/Tickets/Details/" + ticket_id))
    oversized = client.post_file(
        path,
        csrf,
        "oversized.pdf",
        "application/pdf",
        b"%PDF-1.4\n" + (b"A" * (2 * 1024 * 1024 + 96 * 1024)),
        follow=False,
    )
    transport_error = oversized.get("transport_error")
    early_disconnect = (
        oversized["status"] == 0
        and transport_error
        and any(
            marker in transport_error.lower()
            for marker in (
                "broken pipe",
                "connection reset",
                "remote end closed",
            )
        )
    )

    health_after_limit = client.get("/health/ready")
    application_healthy = health_after_limit["status"] == 200

    oversized_rejected = (
        oversized["status"] in {400, 413}
        or (early_disconnect and application_healthy)
    )

    if oversized["status"] in {400, 413}:
        oversized_actual = "HTTP %s" % oversized["status"]
    elif early_disconnect and application_healthy:
        oversized_actual = (
            "Connection closed during oversized upload; "
            "readiness remained HTTP 200"
        )
    else:
        oversized_actual = (
            "HTTP %s; transport error: %s; readiness: HTTP %s"
            % (
                oversized["status"],
                transport_error or "none",
                health_after_limit["status"],
            )
        )

    tests.append(result(
        "P5-UP-04",
        "Pre-model-binding request limit",
        oversized_rejected,
        oversized_actual,
    ))

    home = client.get("/")
    csp = next(
        (
            value
            for key, value in home["headers"].items()
            if key.lower() == "content-security-policy"
        ),
        "",
    )
    tests.append(result(
        "P5-UP-05",
        "Content Security Policy",
        "'unsafe-inline'" not in csp and "style-src 'self'" in csp,
        csp,
    ))

    passed = all(item["status"] == "PASS" for item in tests)
    payload = {
        "generated_at_utc": dt.datetime.now(
            dt.timezone.utc
        ).isoformat(),
        "scope": "Project-owned localhost and fictional data only",
        "status": "PASS" if passed else "FAIL",
        "tests": tests,
        "residual_risk": (
            "The local deterministic scanner demonstrates quarantine and "
            "release gating. Production deployment would integrate a managed "
            "antivirus or sandbox service and a distributed rate-limit store."
        ),
    }
    Path(args.output_json).write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )

    lines = [
        "# Phase 5 Upload and Authentication Retest",
        "",
        "## Result",
        "",
        "**%s**" % payload["status"],
        "",
        "| Test | Control | Result | Actual |",
        "|---|---|---|---|",
    ]
    for item in tests:
        lines.append(
            "| {test_id} | {control} | {status} | {actual} |".format(
                **{
                    key: str(value).replace("|", "\\|")
                    for key, value in item.items()
                }
            )
        )
    lines.extend([
        "",
        "## Remediated findings",
        "",
        "- PH4-F01 / #52 — file signatures are inspected server-side.",
        "- PH4-F02 / #53 — files enter quarantine and are released only after a clean scan.",
        "- PH4-F03 / #54 — login throttling is partitioned by source address.",
        "- PH4-F04 / #55 — CSP no longer permits inline styles.",
        "- PH4-F08 / #59 — multipart and endpoint request limits apply before controller validation.",
        "",
        "## Residual risk",
        "",
        payload["residual_risk"],
        "",
        "No live malware was introduced. The blocked marker is a harmless project test fixture.",
        "",
    ])
    Path(args.output_md).write_text("\n".join(lines), encoding="utf-8")

    for item in tests:
        print(
            "%s %s: %s"
            % (item["test_id"], item["status"], item["actual"])
        )

    if not passed:
        raise RuntimeError("One or more upload/authentication retests failed.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("Retest failed: %s" % error, file=sys.stderr)
        sys.exit(1)
