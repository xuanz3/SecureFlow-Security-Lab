#!/usr/bin/env python3
"""Close Phase 6 recovery risks after validated exercise evidence exists."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def replace_table_row(path: Path, prefix: str, replacement: str) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    matches = [
        index for index, line in enumerate(lines)
        if line.startswith(prefix)
    ]
    if len(matches) != 1:
        raise RuntimeError(
            f"Expected one table row starting {prefix!r} in {path}, "
            f"found {len(matches)}"
        )
    lines[matches[0]] = replacement
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def regenerate_risk_markdown(register: dict, path: Path) -> None:
    lines = [
        "# SecureFlow Risk Register",
        "",
        "## Scope and method",
        "",
        "This is a project-level portfolio risk self-assessment. It is not an",
        "enterprise risk assessment, certification, regulatory compliance statement",
        "or substitute for production threat, business-impact and legal analysis.",
        "",
        "Likelihood and impact use a 1–5 scale. Score equals likelihood multiplied by",
        "impact. Bands are Low 1–4, Moderate 5–9, High 10–14 and Extreme 15–25.",
        "",
        "| ID | Risk | Inherent | Residual | Status | Treatment |",
        "|---|---|---:|---:|---|---|",
    ]
    for risk in register["risks"]:
        lines.append(
            f'| {risk["id"]} | {risk["title"]} | '
            f'{risk["inherent_score"]} | {risk["residual_score"]} | '
            f'{risk["status"]} | {risk["treatment"]} |'
        )

    lines.extend(["", "## Evidence and control detail", ""])
    for risk in register["risks"]:
        lines.extend(
            [
                f'### {risk["id"]} — {risk["title"]}',
                "",
                f'- Asset: {risk["asset"]}',
                f'- Threat: {risk["threat"]}',
                "- Controls:",
            ]
        )
        lines.extend(f"  - {item}" for item in risk["controls"])
        lines.append("- Evidence:")
        lines.extend(
            f"  - [`{item}`](../{item})"
            for item in risk["evidence"]
        )
        lines.extend(
            [
                f'- Owner: {risk["owner"]}',
                f'- Residual treatment decision: {risk["treatment"]}',
                "",
            ]
        )

    path.write_text("\n".join(lines), encoding="utf-8")


def update_validator(path: Path) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    if any(
        line.strip() == "if open_treatments:"
        for line in lines
    ):
        return

    start = next(
        (
            index for index, line in enumerate(lines)
            if "if set(open_treatments) !=" in line
        ),
        None,
    )
    if start is None:
        raise RuntimeError(
            "Governance validator open-treatment rule was not found."
        )

    end = None
    for index in range(start + 1, min(start + 10, len(lines))):
        if lines[index] == "        )":
            end = index
            break
    if end is None:
        raise RuntimeError(
            "Governance validator open-treatment block is malformed."
        )

    replacement = [
        "    if open_treatments:",
        "        errors.append(",
        '            "expected no open recovery treatments after Issue #32"',
        "        )",
    ]
    lines[start : end + 1] = replacement
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()

    root = Path(args.root)
    recovery_report = (
        root / "recovery/PHASE6_RECOVERY_EXERCISE_REPORT.md"
    )
    recovery_validation = root / "docs/PHASE6_RECOVERY_VALIDATION.md"
    if not recovery_report.is_file():
        raise RuntimeError("Recovery report is missing.")
    if not recovery_validation.is_file():
        raise RuntimeError("Recovery validation is missing.")

    register_path = root / "governance/risk-register.json"
    register = json.loads(
        register_path.read_text(encoding="utf-8")
    )
    risks = {
        item["id"]: item for item in register["risks"]
    }

    r8 = risks["R-08"]
    r8["controls"] = [
        "Persistent PostgreSQL volume",
        "Custom-format database backup with SHA-256 validation",
        "Clean-volume restore with schema and row-count comparison",
        "Measured local recovery exercise and failure runbook",
    ]
    r8["residual_likelihood"] = 1
    r8["residual_impact"] = 5
    r8["residual_score"] = 5
    r8["treatment"] = (
        "Retain scheduled restore testing and add encrypted off-site "
        "retention before production."
    )
    r8["status"] = "Mitigated with residual risk"
    r8["evidence"] = [
        "infrastructure/docker/compose.yml",
        "recovery/PHASE6_RECOVERY_EXERCISE_REPORT.md",
        "docs/PHASE6_RECOVERY_VALIDATION.md",
        "recovery/runbooks/DATABASE_BACKUP_RESTORE.md",
    ]

    r9 = risks["R-09"]
    r9["controls"] = [
        "Versioned Git releases",
        "Published container images and provenance",
        "Exact known-good image identity verification",
        "Controlled candidate failure and measured rollback exercise",
    ]
    r9["residual_likelihood"] = 1
    r9["residual_impact"] = 4
    r9["residual_score"] = 4
    r9["treatment"] = (
        "Retain immutable known-good image references and rehearse "
        "rollback after material deployment changes."
    )
    r9["status"] = "Mitigated"
    r9["evidence"] = [
        ".github/workflows/publish-image.yml",
        "recovery/PHASE6_RECOVERY_EXERCISE_REPORT.md",
        "docs/PHASE6_RECOVERY_VALIDATION.md",
        "recovery/runbooks/APPLICATION_ROLLBACK.md",
    ]

    register_path.write_text(
        json.dumps(register, indent=2),
        encoding="utf-8",
    )
    regenerate_risk_markdown(
        register,
        root / "governance/RISK_REGISTER.md",
    )

    replace_table_row(
        root / "governance/NIST_CSF_2_0_PROFILE.md",
        "| Recover |",
        "| Recover | A PostgreSQL backup was validated and restored into a clean volume, and a controlled failing candidate image was rolled back to an exact known-good image. | Established for the local exercise | `recovery/PHASE6_RECOVERY_EXERCISE_REPORT.md`; `docs/PHASE6_RECOVERY_VALIDATION.md` | Add encrypted off-site retention, scheduled exercises and organisation-approved RPO/RTO before production. |",
    )
    replace_table_row(
        root / "governance/ESSENTIAL_EIGHT_GAP_REVIEW.md",
        "| Regular backups |",
        "| Regular backups | Relevant | Demonstrated for the local exercise | Backup integrity, clean restore and measured recovery were verified locally; enterprise scheduling, encryption, off-site retention and organisational coverage remain outside scope. | Retain scheduled restore testing and add production retention controls before deployment. |",
    )
    replace_table_row(
        root / "governance/GOVERNANCE_ACTION_PLAN.md",
        "| 1 | Execute PostgreSQL backup",
        "| 1 | Execute PostgreSQL backup and clean restore with integrity checks and measured recovery time. | R-08; NIST Recover; Essential Eight regular backups | Project owner | Completed in Issue #32 | `recovery/PHASE6_RECOVERY_EXERCISE_REPORT.md`; `docs/PHASE6_RECOVERY_VALIDATION.md` |",
    )
    replace_table_row(
        root / "governance/GOVERNANCE_ACTION_PLAN.md",
        "| 1 | Execute rollback",
        "| 1 | Execute rollback from a deliberately changed application image to a known-good version. | R-09; NIST Recover | Project owner | Completed in Issue #32 | `recovery/PHASE6_RECOVERY_EXERCISE_REPORT.md`; `recovery/runbooks/APPLICATION_ROLLBACK.md` |",
    )

    governance_readme = root / "governance/README.md"
    text = governance_readme.read_text(encoding="utf-8")
    old = (
        "Issue #32 will supply measured backup, restore and rollback evidence. "
        "Issue #33\nwill publish the final management report, technical report, "
        "evidence navigation,\nfinal screenshots and v1.0 release."
    )
    new = (
        "Issue #32 supplies measured backup, clean restore and exact-image "
        "rollback evidence.\nIssue #33 will publish the final management report, "
        "technical report, evidence\nnavigation, final screenshots and v1.0 release."
    )
    if old in text:
        text = text.replace(old, new)
    elif new not in text:
        raise RuntimeError(
            "Governance README recovery status block was not found."
        )
    governance_readme.write_text(text, encoding="utf-8")

    update_validator(
        root
        / "security-assessment/tools/validate_phase6_governance.py"
    )

    print("PASS: R-08 and R-09 updated from open treatment.")
    print("PASS: NIST Recover profile updated.")
    print("PASS: Essential Eight regular backups review updated.")
    print("PASS: governance validator now expects no open treatments.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(
            f"Recovery governance finalisation failed: {error}",
            file=sys.stderr,
        )
        sys.exit(1)
