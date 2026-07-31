#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path


def runners(document):
    if isinstance(document, list):
        return document
    if isinstance(document, dict):
        return [document]
    return []


def extract(document):
    passed = []
    failed = []
    skipped = []

    for runner in runners(document):
        results = runner.get("results", {})
        passed.extend(results.get("passed_checks", []) or [])
        failed.extend(results.get("failed_checks", []) or [])
        skipped.extend(results.get("skipped_checks", []) or [])

    return passed, failed, skipped


def check_name(item):
    return (
        item.get("check_id", "unknown"),
        item.get("check_name", "Unnamed check"),
        item.get("resource", "unknown resource"),
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference", required=True)
    parser.add_argument("--fixture", required=True)
    parser.add_argument("--image", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    reference = json.loads(Path(args.reference).read_text(encoding="utf-8"))
    fixture = json.loads(Path(args.fixture).read_text(encoding="utf-8"))

    ref_pass, ref_fail, ref_skip = extract(reference)
    fix_pass, fix_fail, fix_skip = extract(fixture)

    if not fix_fail:
        raise RuntimeError(
            "The deliberately insecure fixture did not produce Checkov failures."
        )

    lines = [
        "# Phase 4 Checkov Assessment",
        "",
        "- Checkov image: `%s`" % args.image,
        "- Azure reference: %d passed, %d failed, %d skipped"
        % (len(ref_pass), len(ref_fail), len(ref_skip)),
        "- Deliberately insecure fixture: %d passed, %d failed, %d skipped"
        % (len(fix_pass), len(fix_fail), len(fix_skip)),
        "",
        "## Secure-reference triage",
        "",
        "The reference is non-deployed example code. Any remaining Checkov results are",
        "retained for manual triage rather than silently suppressed.",
        "",
        "| Check | Resource |",
        "|---|---|",
    ]

    for item in ref_fail[:20]:
        check_id, name, resource = check_name(item)
        lines.append(
            "| %s — %s | `%s` |" % (
                check_id,
                name.replace("|", "\\|"),
                resource,
            )
        )

    if not ref_fail:
        lines.append("| None | Reference produced no failed checks |")

    lines.extend([
        "",
        "## Insecure-fixture detection",
        "",
        "| Check | Resource |",
        "|---|---|",
    ])

    for item in fix_fail[:30]:
        check_id, name, resource = check_name(item)
        lines.append(
            "| %s — %s | `%s` |" % (
                check_id,
                name.replace("|", "\\|"),
                resource,
            )
        )

    lines.extend([
        "",
        "## Interpretation",
        "",
        "- Fixture failures are expected evidence, not unresolved application findings.",
        "- No Azure resources were created.",
        "- The reference and fixture remain inside the repository for repeatable review.",
        "",
    ])

    Path(args.output).write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("Checkov summary failed: %s" % error, file=sys.stderr)
        sys.exit(1)
