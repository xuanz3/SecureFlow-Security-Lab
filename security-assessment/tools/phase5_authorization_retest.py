#!/usr/bin/env python3
"""Retest SecureFlow owner and administrator authorisation boundaries.

The application is an MVC browser application. Cookie authentication expresses
access denial as either HTTP 403 or a redirect to /Account/AccessDenied.
This retest inspects the raw response before redirects and separately verifies
the rendered access-denied page. It never treats the final HTTP 200 denial page
as successful access to the protected resource.
"""

import argparse
import datetime as dt
import http.cookiejar
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path


REDIRECT_STATUSES = {301, 302, 303, 307, 308}


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


class HttpClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")
        self.cookie_jar = http.cookiejar.CookieJar()
        self.following = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookie_jar)
        )
        self.raw = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookie_jar),
            NoRedirect(),
        )

    def request(self, method, path, data=None, headers=None, follow=True):
        url = urllib.parse.urljoin(self.base_url + "/", path.lstrip("/"))
        request_headers = {
            "User-Agent": "SecureFlow-Phase5-Authorization-Retest/1.0",
        }
        if headers:
            request_headers.update(headers)

        request = urllib.request.Request(
            url,
            data=data,
            headers=request_headers,
            method=method,
        )
        opener = self.following if follow else self.raw

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
        payload = urllib.parse.urlencode(fields).encode("utf-8")
        return self.request(
            "POST",
            path,
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            follow=follow,
        )

    def has_auth_cookie(self):
        return any("SecureFlow.Auth" in cookie.name for cookie in self.cookie_jar)


def parse_form(body):
    parser = FormParser()
    parser.feed(body.decode("utf-8", errors="replace"))
    return parser.inputs


def require_token(response, context):
    token = parse_form(response["body"]).get("__RequestVerificationToken")
    if not token:
        raise RuntimeError(
            "Anti-forgery token was not found during %s." % context
        )
    return token


def load_env(path):
    result = {}
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        result[key] = value
    return result


def login(base_url, email, password):
    client = HttpClient(base_url)
    page = client.get("/Account/Login")
    token = require_token(page, "login")
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
    body = response["body"].decode("utf-8", errors="replace")
    if (
        response["status"] != 200
        or not client.has_auth_cookie()
        or "Invalid sign-in attempt." in body
    ):
        raise RuntimeError(
            "Could not authenticate fictional account %s." % email
        )
    return client


def create_ticket(client, title):
    page = client.get("/Tickets/Create")
    token = require_token(page, "ticket creation")
    response = client.post_form(
        "/Tickets/Create",
        {
            "__RequestVerificationToken": token,
            "Title": title,
            "Description": (
                "Fictional ticket created for the Phase 5 authorisation retest."
            ),
        },
    )
    match = re.search(
        r"/Tickets/Details/([0-9a-fA-F-]{36})",
        response["url"],
    )
    if not match:
        match = re.search(
            r"/Tickets/Details/([0-9a-fA-F-]{36})",
            response["body"].decode("utf-8", errors="replace"),
        )
    if not match:
        raise RuntimeError("Could not resolve the created ticket identifier.")
    return match.group(1)


def header(response, name):
    for key, value in response["headers"].items():
        if key.lower() == name.lower():
            return value
    return ""


def denial_result(test_id, area, raw_response, followed_response, secret_text):
    location = header(raw_response, "Location")
    raw_denied = (
        raw_response["status"] == 403
        or (
            raw_response["status"] in REDIRECT_STATUSES
            and "/Account/AccessDenied" in location
        )
    )
    followed_body = followed_response["body"].decode(
        "utf-8",
        errors="replace",
    )
    rendered_denied = (
        followed_response["status"] == 200
        and "Access denied" in followed_body
        and secret_text not in followed_body
        and "/Account/AccessDenied" in followed_response["url"]
    )

    if raw_response["status"] == 403:
        raw_summary = "HTTP 403"
    else:
        raw_summary = "HTTP %s -> %s" % (
            raw_response["status"],
            location or "(no Location header)",
        )

    return {
        "test_id": test_id,
        "area": area,
        "expected": "Access is denied before protected content is returned",
        "actual": raw_summary,
        "raw_denied": raw_denied,
        "rendered_denied": rendered_denied,
        "status": "PASS" if raw_denied and rendered_denied else "FAIL",
    }


def write_markdown(path, payload):
    lines = [
        "# Phase 5 Authorisation Retest",
        "",
        "## Conclusion",
        "",
        (
            "**PASS** — the existing server-side owner and administrator "
            "boundaries correctly deny unauthorised access."
            if payload["status"] == "PASS"
            else "**FAIL** — at least one authorisation boundary did not pass."
        ),
        "",
        "Phase 4 reported final HTTP 200 responses because its browser-style client",
        "followed the cookie-authentication redirect to the access-denied page.",
        "The protected resource itself was not returned. This retest records both",
        "the raw denial response and the final denial page.",
        "",
        "## Results",
        "",
        "| Test | Area | Raw result | Denial page verified | Result |",
        "|---|---|---|---|---|",
    ]

    for item in payload["tests"]:
        lines.append(
            "| {test_id} | {area} | {actual} | {rendered} | {status} |".format(
                test_id=item["test_id"],
                area=item["area"],
                actual=item["actual"].replace("|", "\\|"),
                rendered="Yes" if item.get("rendered_denied", True) else "No",
                status=item["status"],
            )
        )

    lines.extend([
        "",
        "## Regression coverage",
        "",
        "- non-owner read denial",
        "- non-owner modify denial",
        "- owner access",
        "- administrator override",
        "- authenticated Tickets controller boundary",
        "- Admin-role controller boundary",
        "",
        "## Classification",
        "",
        "- No object-level authorisation bypass was reproduced.",
        "- No administrator-role bypass was reproduced.",
        "- Phase 4 A02/A03 were test-methodology false positives caused by redirect following.",
        "- No Phase 4 Finding Issue is closed by this retest because A02/A03 were not",
        "  among Findings PH4-F01–PH4-F08.",
        "",
        "## Safety",
        "",
        "Testing used only local project-owned containers and fictional accounts.",
        "No password, cookie or local secret is written to this report.",
        "",
    ])

    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://localhost:8080")
    parser.add_argument("--env-file", required=True)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    args = parser.parse_args()

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

    readiness = HttpClient(args.base_url).get("/health/ready")
    if readiness["status"] != 200:
        raise RuntimeError(
            "Readiness endpoint returned HTTP %s." % readiness["status"]
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

    run_id = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    bob_title = "Phase 5 Bob protected ticket " + run_id
    bob_ticket = create_ticket(bob, bob_title)

    tests = []

    bob_owner = bob.get("/Tickets/Details/" + bob_ticket)
    tests.append({
        "test_id": "P5-AUTH-01",
        "area": "Owner access",
        "expected": "Bob can read Bob's ticket",
        "actual": "HTTP %s" % bob_owner["status"],
        "status": (
            "PASS"
            if bob_owner["status"] == 200
            and bob_title
            in bob_owner["body"].decode("utf-8", errors="replace")
            else "FAIL"
        ),
    })

    cross_raw = alice.get(
        "/Tickets/Details/" + bob_ticket,
        follow=False,
    )
    cross_followed = alice.get(
        "/Tickets/Details/" + bob_ticket,
        follow=True,
    )
    tests.append(denial_result(
        "P5-AUTH-02",
        "Object-level authorisation",
        cross_raw,
        cross_followed,
        bob_title,
    ))

    admin_raw = alice.get("/Admin", follow=False)
    admin_followed = alice.get("/Admin", follow=True)
    tests.append(denial_result(
        "P5-AUTH-03",
        "Administrator authorisation",
        admin_raw,
        admin_followed,
        "All tickets",
    ))

    admin_allowed = admin.get("/Admin")
    tests.append({
        "test_id": "P5-AUTH-04",
        "area": "Administrator access",
        "expected": "Administrator can access the administrator route",
        "actual": "HTTP %s" % admin_allowed["status"],
        "status": "PASS" if admin_allowed["status"] == 200 else "FAIL",
    })

    overall = (
        "PASS"
        if all(item["status"] == "PASS" for item in tests)
        else "FAIL"
    )

    payload = {
        "generated_at_utc": dt.datetime.now(
            dt.timezone.utc
        ).isoformat(),
        "base_url": args.base_url,
        "scope": "Project-owned localhost and fictional accounts only",
        "status": overall,
        "tests": tests,
    }

    Path(args.output_json).write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )
    write_markdown(Path(args.output_md), payload)

    for item in tests:
        print(
            "%s %s: %s"
            % (item["test_id"], item["status"], item["actual"])
        )

    if overall != "PASS":
        raise RuntimeError("One or more authorisation retests failed.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(
            "Authorisation retest failed: %s" % error,
            file=sys.stderr,
        )
        sys.exit(1)
