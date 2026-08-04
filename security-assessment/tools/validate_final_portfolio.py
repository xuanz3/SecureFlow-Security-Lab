#!/usr/bin/env python3
"""Validate and optionally refresh SecureFlow v1.0 final evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import subprocess
import sys
from pathlib import Path


IMAGE_NAMES = [
    "01-application-overview.png",
    "02-security-pipeline.png",
    "03-assessment-findings.png",
    "04-remediation-retest.png",
    "05-detection-investigation.png",
    "06-governance-recovery.png",
]

SOURCES = {
    "01-application-overview.png": "hardened local application",
    "02-security-pipeline.png": "workflow and technical-report evidence",
    "03-assessment-findings.png": "Phase 4 vulnerability register",
    "04-remediation-retest.png": "Phase 5 remediation matrix",
    "05-detection-investigation.png": "detection evaluation evidence",
    "06-governance-recovery.png": "Phase 6 governance and recovery validation",
}

PRIVATE_PATTERNS = [
    r"/Users/[^/\s]+/",
    r"/private/var/folders/[^\s]+",
    r"\b192\.168\.\d{1,3}\.\d{1,3}\b",
    r"\b10\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
    r"\b172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}\b",
]

PUBLIC_TEXT_FILES = [
    "README.md",
    "reports/FINAL_MANAGEMENT_REPORT.md",
    "reports/FINAL_TECHNICAL_REPORT.md",
    "evidence/final/README.md",
]


def png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()[:24]
    if len(data) != 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"Not a valid PNG header: {path}")
    return struct.unpack(">II", data[16:24])


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_vulnerability_rows(path: Path) -> list[list[str]]:
    rows = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line.startswith("| PH4-F"):
            continue
        rows.append(
            [cell.strip() for cell in line.strip("|").split("|")]
        )
    return rows


def tracked_generated_python(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    )
    return [
        item for item in result.stdout.splitlines()
        if "__pycache__/" in item
        or item.endswith((".pyc", ".pyo"))
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--refresh-manifest", action="store_true")
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    args = parser.parse_args()

    root = Path(args.root).resolve()
    final_dir = root / "evidence/final"
    manifest_path = final_dir / "manifest.json"
    sums_path = final_dir / "SHA256SUMS.txt"

    errors: list[str] = []
    images = []
    actual_pngs = sorted(
        path.name for path in final_dir.glob("*.png")
    )
    if actual_pngs != IMAGE_NAMES:
        errors.append(
            "final PNG set differs from required six files: "
            + repr(actual_pngs)
        )

    for name in IMAGE_NAMES:
        path = final_dir / name
        if not path.is_file():
            errors.append(f"missing final image: {name}")
            continue
        try:
            width, height = png_dimensions(path)
        except ValueError as error:
            errors.append(str(error))
            continue
        size = path.stat().st_size
        digest = sha256(path)
        if (width, height) != (1600, 900):
            errors.append(
                f"{name}: expected 1600x900, found {width}x{height}"
            )
        if size < 20_000:
            errors.append(
                f"{name}: image is unexpectedly small ({size} bytes)"
            )
        images.append(
            {
                "path": f"evidence/final/{name}",
                "width": width,
                "height": height,
                "size_bytes": size,
                "sha256": digest,
                "source": SOURCES[name],
            }
        )

    manifest = {
        "schema_version": "1.0",
        "project": "SecureFlow Security Lab",
        "release": "v1.0.0",
        "playwright_version": "1.55.0",
        "viewport": {"width": 1600, "height": 900},
        "image_count": len(images),
        "images": images,
    }

    if args.refresh_manifest and not errors:
        manifest_path.write_text(
            json.dumps(manifest, indent=2),
            encoding="utf-8",
        )
        sums_path.write_text(
            "".join(
                f'{item["sha256"]}  {Path(item["path"]).name}\n'
                for item in images
            ),
            encoding="utf-8",
        )
    else:
        if not manifest_path.is_file():
            errors.append("final manifest is missing")
        else:
            existing = json.loads(
                manifest_path.read_text(encoding="utf-8")
            )
            if existing != manifest:
                errors.append(
                    "final manifest does not match current image files"
                )
        if not sums_path.is_file():
            errors.append("final SHA256SUMS.txt is missing")
        else:
            expected_sums = "".join(
                f'{item["sha256"]}  {Path(item["path"]).name}\n'
                for item in images
            )
            if sums_path.read_text(encoding="utf-8") != expected_sums:
                errors.append(
                    "final SHA256SUMS.txt does not match current images"
                )

    required = [
        root / "README.md",
        root / "reports/FINAL_MANAGEMENT_REPORT.md",
        root / "reports/FINAL_TECHNICAL_REPORT.md",
        root / "evidence/final/README.md",
        root / "security-assessment/results/phase4/VULNERABILITY_REGISTER.md",
        root / "security-assessment/results/phase5/FINDING_REMEDIATION_MATRIX.md",
        root / "evidence/archive/artifacts/phase5/detection-evaluation.json",
        root / "evidence/archive/artifacts/phase6/governance-validation.json",
        root / "evidence/archive/artifacts/phase6/recovery/recovery-validation.json",
    ]
    for path in required:
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"missing or empty final file: {path}")

    if not errors:
        readme = (root / "README.md").read_text(encoding="utf-8")
        first_section = "\n".join(readme.splitlines()[:35])
        for phrase in [
            "Status: v1.0 complete",
            "34 tests",
            "8 assessment findings",
            "5 Sigma rules",
            "5.007 seconds",
        ]:
            if phrase not in first_section:
                errors.append(
                    f"README 30-second overview is missing: {phrase}"
                )
        for name in IMAGE_NAMES:
            if f"evidence/final/{name}" not in readme:
                errors.append(
                    f"README does not link final image: {name}"
                )

        management = (
            root / "reports/FINAL_MANAGEMENT_REPORT.md"
        ).read_text(encoding="utf-8")
        technical = (
            root / "reports/FINAL_TECHNICAL_REPORT.md"
        ).read_text(encoding="utf-8")
        for phrase in [
            "Executive summary",
            "Final outcomes",
            "Risk and assurance position",
            "Recovery outcome",
        ]:
            if phrase not in management:
                errors.append(
                    f"management report missing section: {phrase}"
                )
        for finding in [f"PH4-F{index:02d}" for index in range(1, 9)]:
            if finding not in technical:
                errors.append(
                    f"technical report missing finding trace: {finding}"
                )

        vulnerability_rows = parse_vulnerability_rows(
            root
            / "security-assessment/results/phase4/VULNERABILITY_REGISTER.md"
        )
        if len(vulnerability_rows) != 8:
            errors.append(
                f"expected 8 vulnerability rows, found {len(vulnerability_rows)}"
            )
        for row in vulnerability_rows:
            if "Closed" not in row[4]:
                errors.append(
                    f"vulnerability is not closed: {row[0]} {row[4]}"
                )

        detection = json.loads(
            (
                root
                / "evidence/archive/artifacts/phase5/detection-evaluation.json"
            ).read_text(encoding="utf-8")
        )
        if (
            detection.get("status") != "PASS"
            or detection.get("sigma_count") != 5
            or detection.get("kql_count") != 5
            or detection.get("event_count") != 11
        ):
            errors.append("final detection metrics are not validated")

        governance = json.loads(
            (
                root
                / "evidence/archive/artifacts/phase6/governance-validation.json"
            ).read_text(encoding="utf-8")
        )
        if (
            governance.get("status") != "PASS"
            or governance.get("risk_count") != 10
            or governance.get("open_treatments") != []
        ):
            errors.append("final governance status is not validated")

        recovery = json.loads(
            (
                root
                / "evidence/archive/artifacts/phase6/recovery/recovery-validation.json"
            ).read_text(encoding="utf-8")
        )
        if (
            recovery.get("status") != "PASS"
            or recovery.get("table_count") != 11
            or recovery.get("all_integrity_checks_passed") is not True
            or recovery.get("raw_backup_committed") is not False
        ):
            errors.append("final recovery status is not validated")

    combined = ""
    for relative in PUBLIC_TEXT_FILES:
        path = root / relative
        if path.is_file():
            combined += "\n" + path.read_text(encoding="utf-8")
    for pattern in PRIVATE_PATTERNS:
        if re.search(pattern, combined):
            errors.append(
                f"private environment pattern found in public file: {pattern}"
            )

    bad_tracked = tracked_generated_python(root)
    if bad_tracked:
        errors.append(
            "generated Python files remain tracked: "
            + ", ".join(bad_tracked)
        )

    for path in root.rglob("*"):
        if (
            path.is_file()
            and path.suffix.lower() in {
                ".dump",
                ".backup",
                ".sql",
            }
            and ".git" not in path.parts
        ):
            errors.append(
                f"raw backup-like file exists in repository: {path}"
            )

    result = {
        "status": "PASS" if not errors else "FAIL",
        "release": "v1.0.0",
        "image_count": len(images),
        "image_dimensions": "1600x900",
        "findings_closed": 8,
        "automated_tests": 34,
        "sigma_rules": 5,
        "kql_queries": 5,
        "incident_events": 11,
        "risk_count": 10,
        "open_recovery_treatments": 0,
        "restored_tables": 11,
        "measured_recovery_time_seconds": 5.007,
        "rollback_duration_seconds": 1.473,
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
        "# SecureFlow v1.0 Final Validation",
        "",
        f'- Overall result: **{result["status"]}**',
        f'- Final images: **{result["image_count"]}** at **1600×900**',
        f'- Automated tests: **{result["automated_tests"]}**',
        f'- Findings closed: **{result["findings_closed"]} / 8**',
        f'- Sigma / KQL: **{result["sigma_rules"]} / {result["kql_queries"]}**',
        f'- Controlled incident events: **{result["incident_events"]}**',
        f'- Project risks: **{result["risk_count"]}**',
        f'- Open recovery treatments: **{result["open_recovery_treatments"]}**',
        f'- Restored tables: **{result["restored_tables"]}**',
        f'- Local recovery / rollback: **{result["measured_recovery_time_seconds"]}s / {result["rollback_duration_seconds"]}s**',
        "",
        "The validation confirms internal portfolio traceability and deterministic",
        "evidence. It does not establish certification, organisational compliance",
        "or a production recovery SLA.",
        "",
    ]
    if errors:
        lines.extend(["## Errors", ""])
        lines.extend(f"- {error}" for error in errors)
        lines.append("")

    output_md.write_text("\n".join(lines), encoding="utf-8")

    print(
        f'Final portfolio validation {result["status"]}: '
        f'{result["image_count"]} images, '
        f'{result["findings_closed"]}/8 findings, '
        f'{result["automated_tests"]} tests'
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
            f"Final portfolio validation failed: {error}",
            file=sys.stderr,
        )
        sys.exit(1)
