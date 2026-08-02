#!/usr/bin/env python3
"""Validate SecureFlow Phase 6 governance content."""

import argparse
import json
import re
import sys
from pathlib import Path


NIST_FUNCTIONS = [
    "Govern",
    "Identify",
    "Protect",
    "Detect",
    "Respond",
    "Recover",
]

ESSENTIAL_EIGHT = [
    "Application control",
    "Patch applications",
    "Configure Microsoft Office macro settings",
    "User application hardening",
    "Restrict administrative privileges",
    "Patch operating systems",
    "Multi-factor authentication",
    "Regular backups",
]

FORBIDDEN_CLAIMS = [
    r"\bNIST certified\b",
    r"\bNIST compliant\b",
    r"\bASD certified\b",
    r"\bEssential Eight compliant\b",
    r"\bMaturity Level (?:One|Two|Three|1|2|3) achieved\b",
]

PRIVATE_PATTERNS = [
    r"/Users/[^/\s]+/",
    r"\b192\.168\.\d{1,3}\.\d{1,3}\b",
    r"\b10\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
    r"\b172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}\b",
]


def score_band(score):
    if score <= 4:
        return "Low"
    if score <= 9:
        return "Moderate"
    if score <= 14:
        return "High"
    return "Extreme"


def validate_risks(root, register):
    errors = []
    risks = register.get("risks", [])

    if len(risks) != 10:
        errors.append(f"expected 10 risks, found {len(risks)}")

    ids = [risk.get("id") for risk in risks]
    if len(set(ids)) != len(ids):
        errors.append("risk identifiers are not unique")

    for risk in risks:
        risk_id = risk.get("id", "(missing)")
        expected_inherent = (
            risk.get("inherent_likelihood", 0)
            * risk.get("inherent_impact", 0)
        )
        expected_residual = (
            risk.get("residual_likelihood", 0)
            * risk.get("residual_impact", 0)
        )

        if risk.get("inherent_score") != expected_inherent:
            errors.append(f"{risk_id}: incorrect inherent score")
        if risk.get("residual_score") != expected_residual:
            errors.append(f"{risk_id}: incorrect residual score")

        for key in [
            "title",
            "asset",
            "threat",
            "treatment",
            "owner",
            "status",
        ]:
            if not str(risk.get(key, "")).strip():
                errors.append(f"{risk_id}: missing {key}")

        controls = risk.get("controls", [])
        evidence = risk.get("evidence", [])
        if not controls:
            errors.append(f"{risk_id}: no controls")
        if not evidence:
            errors.append(f"{risk_id}: no evidence")

        for relative in evidence:
            path = root / relative
            if not path.is_file():
                errors.append(
                    f"{risk_id}: evidence path does not exist: {relative}"
                )

        risk["inherent_band"] = score_band(risk["inherent_score"])
        risk["residual_band"] = score_band(risk["residual_score"])

    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    args = parser.parse_args()

    root = Path(args.root)
    governance = root / "governance"
    required = [
        governance / "README.md",
        governance / "RISK_REGISTER.md",
        governance / "risk-register.json",
        governance / "NIST_CSF_2_0_PROFILE.md",
        governance / "ESSENTIAL_EIGHT_GAP_REVIEW.md",
        governance / "GOVERNANCE_ACTION_PLAN.md",
        governance / "FRAMEWORK_REFERENCES.md",
    ]

    errors = []
    for path in required:
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"missing or empty required file: {path}")

    if errors:
        raise RuntimeError("; ".join(errors))

    register = json.loads(
        (governance / "risk-register.json").read_text(encoding="utf-8")
    )
    errors.extend(validate_risks(root, register))

    nist_text = (
        governance / "NIST_CSF_2_0_PROFILE.md"
    ).read_text(encoding="utf-8")
    for function in NIST_FUNCTIONS:
        if function not in nist_text:
            errors.append(f"NIST profile missing function: {function}")

    e8_text = (
        governance / "ESSENTIAL_EIGHT_GAP_REVIEW.md"
    ).read_text(encoding="utf-8")
    for strategy in ESSENTIAL_EIGHT:
        if strategy not in e8_text:
            errors.append(
                f"Essential Eight review missing strategy: {strategy}"
            )

    combined = "\n".join(
        path.read_text(encoding="utf-8") for path in required
        if path.suffix in {".md", ".json"}
    )

    for pattern in FORBIDDEN_CLAIMS:
        if re.search(pattern, combined, re.IGNORECASE):
            errors.append(f"forbidden certification/compliance claim: {pattern}")

    for pattern in PRIVATE_PATTERNS:
        if re.search(pattern, combined):
            errors.append(f"private environment pattern found: {pattern}")

    normalised_e8 = " ".join(e8_text.split())
    if not re.search(
        r"no\s+Maturity\s+Level\s+One,\s+Two\s+or\s+Three"
        r"\s+claim\s+is\s+made",
        normalised_e8,
        re.IGNORECASE,
    ):
        errors.append("Essential Eight maturity claim boundary is missing")

    open_treatments = [
        risk["id"]
        for risk in register["risks"]
        if risk["status"] == "Open treatment"
    ]
    if open_treatments:
        errors.append(
            "expected no open recovery treatments after Issue #32"
        )

    payload = {
        "status": "PASS" if not errors else "FAIL",
        "risk_count": len(register["risks"]),
        "nist_functions": NIST_FUNCTIONS,
        "essential_eight_strategies": ESSENTIAL_EIGHT,
        "open_treatments": open_treatments,
        "all_evidence_paths_exist": not any(
            "evidence path does not exist" in error for error in errors
        ),
        "claim_boundary_validated": not any(
            "forbidden certification" in error for error in errors
        ),
        "errors": errors,
    }

    output_json = Path(args.output_json)
    output_md = Path(args.output_md)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)

    output_json.write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )

    lines = [
        "# Phase 6 Governance Validation",
        "",
        f'- Overall result: **{payload["status"]}**',
        f'- Risks validated: **{payload["risk_count"]}**',
        f'- NIST CSF functions represented: **{len(NIST_FUNCTIONS)}**',
        f'- Essential Eight strategies reviewed: **{len(ESSENTIAL_EIGHT)}**',
        f'- Open treatments: **{", ".join(open_treatments)}**',
        f'- Evidence paths resolve: **{payload["all_evidence_paths_exist"]}**',
        f'- Claim boundary validated: **{payload["claim_boundary_validated"]}**',
        "",
        "## Interpretation",
        "",
        "The governance artefacts are internally consistent and evidence-linked.",
        "This validation does not establish certification, regulatory compliance or",
        "an Essential Eight maturity level.",
        "",
    ]
    if errors:
        lines.extend(["## Errors", ""])
        lines.extend(f"- {error}" for error in errors)
        lines.append("")

    output_md.write_text("\n".join(lines), encoding="utf-8")

    print(
        f'Governance validation {payload["status"]}: '
        f'{payload["risk_count"]} risks, '
        f'{len(NIST_FUNCTIONS)} CSF functions, '
        f'{len(ESSENTIAL_EIGHT)} Essential Eight strategies'
    )
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Governance validation failed: {error}", file=sys.stderr)
        sys.exit(1)
