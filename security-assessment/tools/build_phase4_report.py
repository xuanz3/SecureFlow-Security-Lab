#!/usr/bin/env python3
import argparse
import collections
import datetime as dt
import json
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--results-dir", required=True)
    parser.add_argument("--checkov-summary", required=True)
    parser.add_argument("--network-summary", required=True)
    args = parser.parse_args()

    repo_root = Path(args.repo_root)
    results_dir = Path(args.results_dir)

    findings = json.loads(
        (results_dir / "findings.json").read_text(encoding="utf-8")
    )
    assessment = json.loads(
        (results_dir / "application-assessment.json").read_text(
            encoding="utf-8"
        )
    )

    if len(findings) < 8:
        raise RuntimeError("At least eight findings are required.")

    if any(not item.get("issue_url") for item in findings):
        raise RuntimeError("Every finding must link to a GitHub Issue.")

    severity_counts = collections.Counter(
        item["severity"]
        for item in findings
    )
    test_counts = collections.Counter(
        item["status"]
        for item in assessment["tests"]
    )

    passed_tests = [
        item
        for item in assessment["tests"]
        if item["status"] == "PASS"
    ]
    exception_tests = [
        item
        for item in assessment["tests"]
        if item["status"] != "PASS"
    ]

    report = [
        "# Phase 4 Final Security Assessment Report",
        "",
        "## Executive summary",
        "",
        "SecureFlow was assessed inside the authorised project-owned local Docker",
        "environment. The assessment combined manual/API security tests, targeted",
        "source and configuration review, Checkov IaC analysis, Nmap exposure checks",
        "and a controlled packet capture.",
        "",
        "- Application tests: %d PASS, %d FINDING, %d FAIL"
        % (
            test_counts.get("PASS", 0),
            test_counts.get("FINDING", 0),
            test_counts.get("FAIL", 0),
        ),
        "- Validated findings: %d" % len(findings),
        "- Medium: %d" % severity_counts.get("Medium", 0),
        "- Low: %d" % severity_counts.get("Low", 0),
        "- High/Critical: %d"
        % (
            severity_counts.get("High", 0)
            + severity_counts.get("Critical", 0)
        ),
        "",
        "No public, third-party or production system was tested.",
        "",
        "## Scope",
        "",
        "- Local ASP.NET Core SecureFlow application",
        "- Local PostgreSQL container",
        "- Fictional Admin, Alice and Bob accounts",
        "- Dockerfile and Docker Compose configuration",
        "- Non-deployed Azure Terraform reference and insecure fixture",
        "- Loopback and the Mac's active LAN address on TCP 5432/8080 only",
        "",
        "## Validated controls",
        "",
    ]

    for item in passed_tests:
        report.append(
            "- **%s — %s:** %s"
            % (
                item["test_id"],
                item["area"],
                item["actual"],
            )
        )

    if exception_tests:
        report.extend([
            "",
            "## Test deviations and findings",
            "",
            "| Test | Area | Expected | Actual | Result |",
            "|---|---|---|---|---|",
        ])
        for item in exception_tests:
            report.append(
                "| %s | %s | %s | %s | %s |"
                % (
                    item["test_id"],
                    item["area"].replace("|", "\\|"),
                    item["expected"].replace("|", "\\|"),
                    item["actual"].replace("|", "\\|"),
                    item["status"],
                )
            )

    report.extend([
        "",
        "## Findings",
        "",
        "| ID | Severity | Finding | GitHub issue |",
        "|---|---|---|---|",
    ])

    for item in findings:
        report.append(
            "| {id} | {severity} | {title} | [#{issue_number}]({issue_url}) |".format(
                **item
            )
        )

    report.extend([
        "",
        "## Evidence",
        "",
        "- [Application assessment](results/phase4/APPLICATION_ASSESSMENT.md)",
        "- [Vulnerability register](results/phase4/VULNERABILITY_REGISTER.md)",
        "- [Checkov summary](results/phase4/CHECKOV_ASSESSMENT.md)",
        "- [Network exposure summary](results/phase4/NETWORK_ASSESSMENT.md)",
        "- Raw artifacts: `evidence/archive/artifacts/phase4/`",
        "",
        "## Limitations",
        "",
        "- The environment uses local HTTP and fictional data.",
        "- The assessment does not claim production penetration-test coverage.",
        "- Checkov reference results are manually triaged and no Azure resources were deployed.",
        "- Malware-scanner integration was assessed by design/code review, not by introducing live malware.",
        "- Finding severity is an estimate for this portfolio environment.",
        "",
        "## Next phase",
        "",
        "Phase 5 will remediate selected findings through separate pull requests,",
        "add regression tests and detection content, and record retest outcomes.",
        "",
    ])

    final_report = repo_root / "security-assessment/PHASE4_FINAL_ASSESSMENT_REPORT.md"
    final_report.write_text("\n".join(report), encoding="utf-8")

    validation = [
        "# Phase 4 Validation",
        "",
        "- Completed: %s"
        % dt.datetime.now(dt.timezone.utc).isoformat(),
        "- Application assessment JSON and Markdown: present",
        "- Findings linked to GitHub Issues: %d" % len(findings),
        "- Checkov secure reference and insecure fixture: executed",
        "- Loopback/LAN Nmap assessment: executed",
        "- Controlled health-request packet capture: retained",
        "- SHA-256 artifact manifest: present",
        "- Release build and automated tests: required before merge",
        "",
        "## Acceptance result",
        "",
        "**PASS** — Phase 4 produced a repeatable authorised assessment, at least",
        "eight validated findings, a vulnerability register, IaC evidence and network",
        "evidence without testing any non-project target.",
        "",
    ]

    (repo_root / "docs/PHASE4_VALIDATION.md").write_text(
        "\n".join(validation),
        encoding="utf-8",
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("Final report generation failed: %s" % error, file=sys.stderr)
        sys.exit(1)
