#!/usr/bin/env python3
"""Validate least-privilege GitHub Actions policy without external packages."""

import argparse
import json
import re
import sys
from pathlib import Path


SHA_ACTION = re.compile(r"^[^@\s]+@[0-9a-fA-F]{40}$")
WORKFLOW_SUFFIXES = {".yml", ".yaml"}


def top_level_permissions(lines):
    for index, raw in enumerate(lines):
        line = raw.rstrip()
        if line.startswith((" ", "\t")):
            continue

        if line == "permissions:":
            permissions = {}
            for child in lines[index + 1 :]:
                stripped = child.rstrip()

                if not stripped or stripped.lstrip().startswith("#"):
                    continue

                if not child.startswith((" ", "\t")):
                    break

                match = re.match(
                    r"^\s{2,}([A-Za-z0-9_-]+):\s*([A-Za-z-]+)\s*$",
                    child,
                )
                if match:
                    permissions[match.group(1)] = match.group(2)

            return permissions

        if line.startswith("permissions:"):
            value = line.split(":", 1)[1].strip()
            return {"__scalar__": value}

    return None


def validate_workflow(path):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    errors = []
    actions = []

    permissions = top_level_permissions(lines)
    if permissions is None:
        errors.append("missing top-level permissions declaration")
    elif permissions.get("__scalar__") in {"write-all", "read-all"}:
        errors.append(
            "scalar read-all/write-all permissions are not permitted"
        )
    else:
        for name, value in permissions.items():
            if value not in {"read", "write", "none"}:
                errors.append(
                    f"unsupported permission value {name}: {value}"
                )

    for index, raw in enumerate(lines):
        stripped = raw.strip()

        if stripped.startswith("uses:"):
            reference = stripped.split(":", 1)[1].strip()
            actions.append(reference)

            if reference.startswith(("./", "docker://")):
                continue

            if not SHA_ACTION.fullmatch(reference):
                errors.append(
                    f"line {index + 1}: action is not pinned to a 40-character SHA: "
                    f"{reference}"
                )

            if reference.startswith("actions/checkout@"):
                window = "\n".join(lines[index + 1 : index + 12])
                if not re.search(
                    r"persist-credentials:\s*false",
                    window,
                    re.IGNORECASE,
                ):
                    errors.append(
                        f"line {index + 1}: checkout must disable persisted credentials"
                    )

    if not actions:
        errors.append("workflow contains no action references")

    return {
        "workflow": path.as_posix(),
        "permissions": permissions,
        "actions": actions,
        "errors": errors,
        "status": "PASS" if not errors else "FAIL",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--workflow-dir",
        default=".github/workflows",
    )
    parser.add_argument("--output")
    args = parser.parse_args()

    workflow_dir = Path(args.workflow_dir)
    files = sorted(
        path
        for path in workflow_dir.iterdir()
        if path.is_file() and path.suffix.lower() in WORKFLOW_SUFFIXES
    )

    if not files:
        raise RuntimeError("No GitHub Actions workflows were found.")

    results = [validate_workflow(path) for path in files]
    overall = "PASS" if all(
        item["status"] == "PASS" for item in results
    ) else "FAIL"

    payload = {
        "status": overall,
        "workflow_count": len(results),
        "policy": {
            "top_level_permissions_required": True,
            "write_all_forbidden": True,
            "actions_require_full_commit_sha": True,
            "checkout_persist_credentials": False,
        },
        "workflows": results,
    }

    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(payload, indent=2),
            encoding="utf-8",
        )

    for item in results:
        print(
            f'{item["status"]}: {item["workflow"]} '
            f'({len(item["actions"])} actions)'
        )
        for error in item["errors"]:
            print(f"  - {error}")

    if overall != "PASS":
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Workflow policy validation failed: {error}", file=sys.stderr)
        sys.exit(1)
