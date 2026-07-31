#!/usr/bin/env python3
"""Create or reuse GitHub finding issues and link local finding records."""

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path


def run(args, input_text=None):
    result = subprocess.run(
        args,
        input=input_text,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise RuntimeError(
            "Command failed: %s\n%s"
            % (" ".join(args), result.stderr)
        )
    return result.stdout


def issue_body(item):
    return """## Finding

**{id} — {title}**

- Severity: **{severity}**
- Status: **Open**
- Asset: `{asset}`
- CWE: {cwe}
- OWASP: {owasp}
- Parent assessment: #23

## Evidence

{evidence}

## Safe reproduction

{reproduction}

## Technical cause

{cause}

## Impact

{impact}

## Recommendation

{recommendation}

## Safety boundary

Testing was restricted to project-owned localhost containers and fictional data.
""".format(**item)


def update_markdown(path, issue_url):
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        "- GitHub issue: Pending",
        "- GitHub issue: %s" % issue_url,
    )
    path.write_text(text, encoding="utf-8")


def write_registers(results_dir, findings):
    md = [
        "# Phase 4 Vulnerability Register",
        "",
        "| ID | Severity | Finding | CWE | Status | GitHub issue |",
        "|---|---|---|---|---|---|",
    ]

    for item in findings:
        md.append(
            "| {id} | {severity} | {title} | {cwe} | {status} | [#{issue_number}]({issue_url}) |".format(
                **item
            )
        )

    md.extend([
        "",
        "## Register rules",
        "",
        "- Findings remain open until a remediation PR is merged and a retest is recorded.",
        "- Deliberately insecure Terraform fixtures are training evidence and are not application findings.",
        "- Severity is a portfolio estimate for the local reference environment.",
        "",
    ])

    (results_dir / "VULNERABILITY_REGISTER.md").write_text(
        "\n".join(md),
        encoding="utf-8",
    )

    with (results_dir / "VULNERABILITY_REGISTER.csv").open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "id",
                "severity",
                "title",
                "asset",
                "cwe",
                "owasp",
                "status",
                "issue_number",
                "issue_url",
            ],
        )
        writer.writeheader()
        for item in findings:
            writer.writerow({
                key: item.get(key, "")
                for key in writer.fieldnames
            })


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--results-dir", required=True)
    args = parser.parse_args()

    repo_root = Path(args.repo_root)
    results_dir = Path(args.results_dir)
    findings_path = results_dir / "findings.json"
    findings = json.loads(findings_path.read_text(encoding="utf-8"))

    severity_labels = {
        "Low": "severity-low",
        "Medium": "severity-medium",
        "High": "severity-high",
        "Critical": "severity-critical",
    }

    for item in findings:
        search = run([
            "gh", "issue", "list",
            "--repo", args.repo,
            "--state", "all",
            "--search", "%s in:title" % item["id"],
            "--limit", "10",
            "--json", "number,url,title",
        ])
        candidates = json.loads(search)

        match = None
        for candidate in candidates:
            if item["id"] in candidate.get("title", ""):
                match = candidate
                break

        if match is None:
            payload = {
                "title": "[Phase 4 Finding %s] %s"
                % (item["id"], item["title"]),
                "body": issue_body(item),
                "labels": [
                    "security-finding",
                    "phase-4",
                    severity_labels[item["severity"]],
                ],
                "milestone": 4,
            }

            created = json.loads(run([
                "gh", "api",
                "--method", "POST",
                "repos/%s/issues" % args.repo,
                "--input", "-",
            ], json.dumps(payload)))

            match = {
                "number": created["number"],
                "url": created["html_url"],
                "title": created["title"],
            }

        item["issue_number"] = match["number"]
        item["issue_url"] = match["url"]
        update_markdown(
            repo_root
            / "security-assessment/findings/%s.md" % item["id"],
            match["url"],
        )
        print("%s -> #%s" % (item["id"], match["number"]))

    findings_path.write_text(
        json.dumps(findings, indent=2),
        encoding="utf-8",
    )
    write_registers(results_dir, findings)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("Finding issue publication failed: %s" % error, file=sys.stderr)
        sys.exit(1)
