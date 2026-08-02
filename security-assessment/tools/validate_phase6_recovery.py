#!/usr/bin/env python3
"""Validate committed SecureFlow Phase 6 recovery evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


PRIVATE_PATTERNS = [
    r"/Users/[^/\s]+/",
    r"/private/var/folders/[^\s]+",
    r"\b192\.168\.\d{1,3}\.\d{1,3}\b",
    r"\b10\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
    r"\b172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}\b",
]

RAW_BACKUP_SUFFIXES = {
    ".dump",
    ".backup",
    ".sql",
    ".tar",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    args = parser.parse_args()

    root = Path(args.root)
    evidence = (
        root / "evidence/archive/artifacts/phase6/recovery"
    )
    report = root / "recovery/PHASE6_RECOVERY_EXERCISE_REPORT.md"
    required = {
        "exercise": evidence / "recovery-exercise.json",
        "source": evidence / "source-database-summary.json",
        "restored": evidence / "restored-database-summary.json",
        "backup": evidence / "backup-manifest.json",
        "rollback": evidence / "rollback-evidence.json",
    }

    errors: list[str] = []
    for name, path in required.items():
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"missing or empty {name} evidence: {path}")
    if not report.is_file() or report.stat().st_size == 0:
        errors.append(f"missing or empty recovery report: {report}")

    if errors:
        raise RuntimeError("; ".join(errors))

    exercise = load(required["exercise"])
    source = load(required["source"])
    restored = load(required["restored"])
    backup = load(required["backup"])
    rollback = load(required["rollback"])

    if exercise.get("status") != "PASS":
        errors.append("exercise status is not PASS")

    checks = exercise.get("checks", {})
    required_checks = [
        "backup_archive_valid",
        "clean_target_confirmed",
        "table_set_and_row_counts_match",
        "schema_fingerprint_matches",
        "recovery_marker_restored_once",
        "restored_application_ready",
        "controlled_candidate_failed",
        "known_good_image_restored",
        "database_intact_after_rollback",
    ]
    for name in required_checks:
        if checks.get(name) is not True:
            errors.append(f"required recovery check failed: {name}")

    if source != restored:
        errors.append("source and restored database summaries differ")

    if source.get("recovery_marker_count") != 1:
        errors.append("source recovery marker count is not one")
    if restored.get("recovery_marker_count") != 1:
        errors.append("restored recovery marker count is not one")

    sha256 = str(backup.get("sha256", ""))
    if not re.fullmatch(r"[0-9a-f]{64}", sha256):
        errors.append("backup SHA-256 is invalid")
    if int(backup.get("size_bytes", 0)) < 1024:
        errors.append("backup size is unexpectedly small")
    if int(backup.get("archive_entry_count", 0)) < 1:
        errors.append("backup archive contains no entries")
    if backup.get("raw_archive_committed") is not False:
        errors.append("raw archive commitment boundary is invalid")

    if exercise.get(
        "clean_target_initial_public_table_count"
    ) != 0:
        errors.append("restore target was not clean")
    if exercise.get("restored_readiness_http_status") != 200:
        errors.append("restored application was not ready")
    if float(exercise.get("measured_recovery_time_seconds", -1)) < 0:
        errors.append("measured recovery time is invalid")
    if float(exercise.get("restore_duration_seconds", -1)) < 0:
        errors.append("restore duration is invalid")

    if rollback.get("candidate_state") != "exited":
        errors.append("controlled candidate did not exit")
    if rollback.get("candidate_exit_code") != 42:
        errors.append("controlled candidate exit code is not 42")
    if rollback.get("candidate_readiness_http_status") == 200:
        errors.append("controlled candidate unexpectedly became ready")
    if rollback.get("rollback_readiness_http_status") != 200:
        errors.append("rollback application was not ready")
    if rollback.get("image_identity_match") is not True:
        errors.append("known-good image identity did not match")
    if rollback.get(
        "database_intact_after_rollback"
    ) is not True:
        errors.append("database integrity changed after rollback")
    if float(rollback.get("rollback_duration_seconds", -1)) < 0:
        errors.append("rollback duration is invalid")

    for path in root.rglob("*"):
        if (
            path.is_file()
            and path.suffix.lower() in RAW_BACKUP_SUFFIXES
            and ".git" not in path.parts
        ):
            errors.append(f"raw backup-like file is committed: {path}")

    combined = "\n".join(
        [
            required[name].read_text(encoding="utf-8")
            for name in required
        ]
        + [report.read_text(encoding="utf-8")]
    )
    for pattern in PRIVATE_PATTERNS:
        if re.search(pattern, combined):
            errors.append(
                f"private local environment pattern found: {pattern}"
            )

    report_text = report.read_text(encoding="utf-8")
    for phrase in [
        "Failure handling",
        "not production commitments",
        "Raw backup archive committed: **No**",
    ]:
        if phrase not in report_text:
            errors.append(
                f"recovery report is missing required boundary: {phrase}"
            )

    result = {
        "status": "PASS" if not errors else "FAIL",
        "table_count": source.get("table_count"),
        "backup_sha256": sha256,
        "backup_size_bytes": backup.get("size_bytes"),
        "measured_recovery_time_seconds": exercise.get(
            "measured_recovery_time_seconds"
        ),
        "rollback_duration_seconds": rollback.get(
            "rollback_duration_seconds"
        ),
        "all_integrity_checks_passed": all(
            checks.get(name) is True for name in required_checks
        ),
        "raw_backup_committed": False,
        "errors": errors,
    }

    output_json = Path(args.output_json)
    output_md = Path(args.output_md)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(
        json.dumps(result, indent=2),
        encoding="utf-8",
    )

    lines = [
        "# Phase 6 Recovery Validation",
        "",
        f'- Overall result: **{result["status"]}**',
        f'- Public tables verified: **{result["table_count"]}**',
        f'- Backup size: **{result["backup_size_bytes"]} bytes**',
        f'- Measured local recovery time: **{result["measured_recovery_time_seconds"]} seconds**',
        f'- Measured rollback time: **{result["rollback_duration_seconds"]} seconds**',
        f'- Integrity checks: **{result["all_integrity_checks_passed"]}**',
        "- Raw backup committed: **False**",
        "",
        "The measured values apply only to the controlled local exercise and are",
        "not production RPO/RTO commitments.",
        "",
    ]
    if errors:
        lines.extend(["## Errors", ""])
        lines.extend(f"- {error}" for error in errors)
        lines.append("")

    output_md.write_text("\n".join(lines), encoding="utf-8")

    print(
        f'Recovery validation {result["status"]}: '
        f'{result["table_count"]} tables, '
        f'RTO {result["measured_recovery_time_seconds"]}s, '
        f'rollback {result["rollback_duration_seconds"]}s'
    )
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(
            f"Recovery validation failed: {error}",
            file=sys.stderr,
        )
        sys.exit(1)
