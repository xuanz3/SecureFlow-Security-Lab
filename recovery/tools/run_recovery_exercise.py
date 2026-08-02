#!/usr/bin/env python3
"""Run an isolated SecureFlow database restore and image rollback exercise."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import secrets
import shutil
import socket
import string
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from typing import Any


def run(
    command: list[str],
    *,
    cwd: Path | None = None,
    input_bytes: bytes | None = None,
    check: bool = True,
    text: bool = False,
) -> subprocess.CompletedProcess:
    result = subprocess.run(
        command,
        cwd=cwd,
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        text=text,
    )
    if check and result.returncode != 0:
        stdout = result.stdout if text else result.stdout.decode(
            "utf-8", errors="replace"
        )
        stderr = result.stderr if text else result.stderr.decode(
            "utf-8", errors="replace"
        )
        raise RuntimeError(
            "Command failed: "
            + " ".join(command)
            + f"\nstdout:\n{stdout}\nstderr:\n{stderr}"
        )
    return result


def random_password(length: int = 28) -> str:
    alphabet = string.ascii_letters + string.digits
    return (
        "".join(secrets.choice(alphabet) for _ in range(length))
        + "Aa9!"
    )


def allocate_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def write_env(path: Path, values: dict[str, str]) -> None:
    lines = [f"{key}={value}" for key, value in values.items()]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    os.chmod(path, 0o600)


def compose_command(
    compose_file: Path,
    project: str,
    env_file: Path,
    *arguments: str,
) -> list[str]:
    return [
        "docker",
        "compose",
        "--project-name",
        project,
        "--env-file",
        str(env_file),
        "-f",
        str(compose_file),
        *arguments,
    ]


def compose(
    compose_file: Path,
    project: str,
    env_file: Path,
    *arguments: str,
    input_bytes: bytes | None = None,
    check: bool = True,
    text: bool = False,
) -> subprocess.CompletedProcess:
    return run(
        compose_command(
            compose_file,
            project,
            env_file,
            *arguments,
        ),
        input_bytes=input_bytes,
        check=check,
        text=text,
    )


def wait_http(url: str, timeout: float = 150.0) -> int:
    deadline = time.monotonic() + timeout
    last_status = 0
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=4) as response:
                last_status = int(response.status)
                if last_status == 200:
                    return last_status
        except urllib.error.HTTPError as error:
            last_status = int(error.code)
        except Exception:
            last_status = 0
        time.sleep(1)
    raise RuntimeError(
        f"HTTP readiness did not reach 200 within {timeout}s: "
        f"{url}; last status={last_status}"
    )


def http_status(url: str) -> int:
    try:
        with urllib.request.urlopen(url, timeout=4) as response:
            return int(response.status)
    except urllib.error.HTTPError as error:
        return int(error.code)
    except Exception:
        return 0


def wait_db(
    compose_file: Path,
    project: str,
    env_file: Path,
    timeout: float = 120.0,
) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        result = compose(
            compose_file,
            project,
            env_file,
            "exec",
            "-T",
            "db",
            "pg_isready",
            "-U",
            "secureflow",
            "-d",
            "secureflow",
            check=False,
            text=True,
        )
        if result.returncode == 0:
            return
        time.sleep(1)
    raise RuntimeError("PostgreSQL did not become ready.")


def psql(
    compose_file: Path,
    project: str,
    env_file: Path,
    query: str,
) -> str:
    result = compose(
        compose_file,
        project,
        env_file,
        "exec",
        "-T",
        "db",
        "psql",
        "-v",
        "ON_ERROR_STOP=1",
        "-U",
        "secureflow",
        "-d",
        "secureflow",
        "-At",
        "-c",
        query,
        text=True,
    )
    return result.stdout.strip()


def quote_identifier(value: str) -> str:
    return '"' + value.replace('"', '""') + '"'


def database_summary(
    compose_file: Path,
    project: str,
    env_file: Path,
    marker: str,
) -> dict[str, Any]:
    table_output = psql(
        compose_file,
        project,
        env_file,
        """
SELECT tablename
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY tablename;
""",
    )
    tables = [line for line in table_output.splitlines() if line]
    counts: dict[str, int] = {}
    for table in tables:
        value = psql(
            compose_file,
            project,
            env_file,
            f"SELECT COUNT(*) FROM {quote_identifier(table)};",
        )
        counts[table] = int(value)

    column_output = psql(
        compose_file,
        project,
        env_file,
        """
SELECT
    table_name || '|' ||
    ordinal_position::text || '|' ||
    column_name || '|' ||
    data_type || '|' ||
    is_nullable || '|' ||
    COALESCE(column_default, '')
FROM information_schema.columns
WHERE table_schema = 'public'
ORDER BY table_name, ordinal_position;
""",
    )
    schema_fingerprint = hashlib.sha256(
        column_output.encode("utf-8")
    ).hexdigest()

    marker_count = int(
        psql(
            compose_file,
            project,
            env_file,
            """
SELECT COUNT(*)
FROM "SecurityAuditEvents"
WHERE "CorrelationId" = '"""
            + marker.replace("'", "''")
            + """';
""",
        )
    )

    return {
        "table_count": len(tables),
        "tables": tables,
        "row_counts": counts,
        "schema_fingerprint_sha256": schema_fingerprint,
        "recovery_marker_count": marker_count,
    }


def wait_candidate_exit(
    compose_file: Path,
    project: str,
    env_file: Path,
    timeout: float = 45.0,
) -> tuple[str, int]:
    deadline = time.monotonic() + timeout
    last_status = "unknown"
    while time.monotonic() < deadline:
        container = compose(
            compose_file,
            project,
            env_file,
            "ps",
            "-a",
            "-q",
            "app",
            text=True,
        ).stdout.strip()
        if container:
            status = run(
                [
                    "docker",
                    "inspect",
                    "--format",
                    "{{.State.Status}}|{{.State.ExitCode}}",
                    container,
                ],
                text=True,
            ).stdout.strip()
            if "|" in status:
                last_status, exit_code = status.split("|", 1)
                if last_status == "exited":
                    return last_status, int(exit_code)
        time.sleep(1)
    raise RuntimeError(
        "Controlled candidate did not exit as expected; "
        f"last status={last_status}"
    )


def safe_down(
    compose_file: Path,
    project: str,
    env_file: Path,
) -> None:
    if not env_file.exists():
        return
    compose(
        compose_file,
        project,
        env_file,
        "down",
        "--volumes",
        "--remove-orphans",
        check=False,
        text=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    output_dir = Path(args.output_dir).resolve()
    report_path = Path(args.report).resolve()
    compose_file = repo_root / "recovery/compose.exercise.yml"

    if not compose_file.is_file():
        raise RuntimeError("Recovery Compose file is missing.")

    output_dir.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    suffix = uuid.uuid4().hex[:10]
    source_project = f"sfrsrc{suffix}"
    restore_project = f"sfrdst{suffix}"
    known_good_image = f"secureflow-recovery-known-good:{suffix}"
    candidate_image = f"secureflow-recovery-candidate:{suffix}"
    marker = f"PHASE6-RECOVERY-{uuid.uuid4()}"

    commit = run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_root,
        text=True,
    ).stdout.strip()

    started_at = dt.datetime.now(dt.timezone.utc)
    source_env: Path | None = None
    restore_env: Path | None = None
    work_dir: Path | None = None

    try:
        temp_context = tempfile.TemporaryDirectory(
            prefix="secureflow-recovery-exercise."
        )
        work_dir = Path(temp_context.name)
        source_env = work_dir / "source.env"
        restore_env = work_dir / "restore.env"
        backup_path = work_dir / "secureflow.dump"
        candidate_dockerfile = work_dir / "Dockerfile.candidate"

        common_secrets = {
            "POSTGRES_PASSWORD": random_password(),
            "SEED_ADMIN_EMAIL": "admin@example.test",
            "SEED_ADMIN_PASSWORD": random_password(),
            "SEED_ALICE_EMAIL": "alice@example.test",
            "SEED_ALICE_PASSWORD": random_password(),
            "SEED_BOB_EMAIL": "bob@example.test",
            "SEED_BOB_PASSWORD": random_password(),
        }

        source_port = allocate_port()
        restore_port = allocate_port()
        while restore_port == source_port:
            restore_port = allocate_port()

        source_values = {
            **common_secrets,
            "RECOVERY_APP_PORT": str(source_port),
            "SECUREFLOW_IMAGE": known_good_image,
        }
        restore_values = {
            **common_secrets,
            "RECOVERY_APP_PORT": str(restore_port),
            "SECUREFLOW_IMAGE": known_good_image,
        }
        write_env(source_env, source_values)
        write_env(restore_env, restore_values)

        build_started = time.monotonic()
        run(
            [
                "docker",
                "build",
                "--file",
                "infrastructure/docker/Dockerfile",
                "--tag",
                known_good_image,
                "--label",
                f"org.opencontainers.image.revision={commit}",
                "--label",
                "org.opencontainers.image.version=phase6-known-good",
                ".",
            ],
            cwd=repo_root,
        )
        known_good_build_seconds = time.monotonic() - build_started
        known_good_id = run(
            [
                "docker",
                "image",
                "inspect",
                "--format",
                "{{.Id}}",
                known_good_image,
            ],
            text=True,
        ).stdout.strip()

        candidate_dockerfile.write_text(
            "ARG BASE_IMAGE\n"
            "FROM ${BASE_IMAGE}\n"
            'LABEL org.opencontainers.image.version="'
            'phase6-controlled-failing-candidate"\n'
            'ENTRYPOINT ["sh","-c","echo controlled-candidate-failure '
            '>&2; exit 42"]\n',
            encoding="utf-8",
        )
        run(
            [
                "docker",
                "build",
                "--file",
                str(candidate_dockerfile),
                "--build-arg",
                f"BASE_IMAGE={known_good_image}",
                "--tag",
                candidate_image,
                str(work_dir),
            ]
        )
        candidate_id = run(
            [
                "docker",
                "image",
                "inspect",
                "--format",
                "{{.Id}}",
                candidate_image,
            ],
            text=True,
        ).stdout.strip()

        compose(
            compose_file,
            source_project,
            source_env,
            "up",
            "-d",
            "db",
            "app",
        )
        wait_db(compose_file, source_project, source_env)
        source_url = f"http://127.0.0.1:{source_port}/health/ready"
        wait_http(source_url)

        psql(
            compose_file,
            source_project,
            source_env,
            """
INSERT INTO "SecurityAuditEvents"
(
    "EventType",
    "Outcome",
    "CorrelationId",
    "SourceAddress",
    "OccurredAtUtc"
)
VALUES
(
    'RecoveryExercise',
    'SourceMarker',
    '"""
            + marker.replace("'", "''")
            + """',
    'local-recovery-source',
    NOW()
);
""",
        )
        source_summary = database_summary(
            compose_file,
            source_project,
            source_env,
            marker,
        )
        if source_summary["recovery_marker_count"] != 1:
            raise RuntimeError("Source recovery marker was not recorded once.")

        backup_started = time.monotonic()
        dump_result = compose(
            compose_file,
            source_project,
            source_env,
            "exec",
            "-T",
            "db",
            "pg_dump",
            "-U",
            "secureflow",
            "-d",
            "secureflow",
            "--format=custom",
            "--compress=6",
            "--no-owner",
            "--no-acl",
        )
        backup_seconds = time.monotonic() - backup_started
        backup_bytes = dump_result.stdout
        if len(backup_bytes) < 1024:
            raise RuntimeError("Backup archive is unexpectedly small.")
        backup_path.write_bytes(backup_bytes)
        backup_sha256 = hashlib.sha256(backup_bytes).hexdigest()

        list_result = compose(
            compose_file,
            source_project,
            source_env,
            "exec",
            "-T",
            "db",
            "sh",
            "-c",
            "cat >/tmp/secureflow.dump && "
            "pg_restore --list /tmp/secureflow.dump; "
            "status=$?; rm -f /tmp/secureflow.dump; exit $status",
            input_bytes=backup_bytes,
            text=False,
        )
        archive_list = list_result.stdout.decode(
            "utf-8", errors="replace"
        )
        archive_entries = len(
            [
                line
                for line in archive_list.splitlines()
                if line and not line.startswith(";")
            ]
        )
        if archive_entries == 0:
            raise RuntimeError("Backup archive list contains no entries.")

        recovery_started = time.monotonic()
        compose(
            compose_file,
            restore_project,
            restore_env,
            "up",
            "-d",
            "db",
        )
        wait_db(compose_file, restore_project, restore_env)
        initial_tables = int(
            psql(
                compose_file,
                restore_project,
                restore_env,
                """
SELECT COUNT(*)
FROM pg_tables
WHERE schemaname = 'public';
""",
            )
        )
        if initial_tables != 0:
            raise RuntimeError(
                "Clean restore target already contains public tables."
            )

        restore_started = time.monotonic()
        compose(
            compose_file,
            restore_project,
            restore_env,
            "exec",
            "-T",
            "db",
            "sh",
            "-c",
            "cat >/tmp/secureflow.dump && "
            "pg_restore -U secureflow -d secureflow "
            "--no-owner --no-acl --exit-on-error "
            "/tmp/secureflow.dump; "
            "status=$?; rm -f /tmp/secureflow.dump; exit $status",
            input_bytes=backup_bytes,
        )
        restore_seconds = time.monotonic() - restore_started

        compose(
            compose_file,
            restore_project,
            restore_env,
            "up",
            "-d",
            "app",
        )
        restore_url = (
            f"http://127.0.0.1:{restore_port}/health/ready"
        )
        final_restore_status = wait_http(restore_url)
        measured_rto_seconds = time.monotonic() - recovery_started

        restored_summary = database_summary(
            compose_file,
            restore_project,
            restore_env,
            marker,
        )
        summaries_match = source_summary == restored_summary
        if not summaries_match:
            raise RuntimeError(
                "Restored database summary does not match the source."
            )

        restore_values["SECUREFLOW_IMAGE"] = candidate_image
        write_env(restore_env, restore_values)
        compose(
            compose_file,
            restore_project,
            restore_env,
            "up",
            "-d",
            "--no-deps",
            "--force-recreate",
            "app",
        )
        candidate_state, candidate_exit_code = wait_candidate_exit(
            compose_file,
            restore_project,
            restore_env,
        )
        candidate_http_status = http_status(restore_url)
        if candidate_exit_code != 42 or candidate_http_status == 200:
            raise RuntimeError(
                "Controlled candidate failure was not observed correctly."
            )

        rollback_started = time.monotonic()
        restore_values["SECUREFLOW_IMAGE"] = known_good_image
        write_env(restore_env, restore_values)
        compose(
            compose_file,
            restore_project,
            restore_env,
            "up",
            "-d",
            "--no-deps",
            "--force-recreate",
            "app",
        )
        rollback_http_status = wait_http(restore_url)
        rollback_seconds = time.monotonic() - rollback_started

        running_container = compose(
            compose_file,
            restore_project,
            restore_env,
            "ps",
            "-q",
            "app",
            text=True,
        ).stdout.strip()
        if not running_container:
            raise RuntimeError(
                "Rollback application container was not found."
            )
        running_image_id = run(
            [
                "docker",
                "inspect",
                "--format",
                "{{.Image}}",
                running_container,
            ],
            text=True,
        ).stdout.strip()
        image_identity_match = running_image_id == known_good_id
        if not image_identity_match:
            raise RuntimeError(
                "Running rollback image does not match known-good image."
            )

        post_rollback_summary = database_summary(
            compose_file,
            restore_project,
            restore_env,
            marker,
        )
        database_intact_after_rollback = (
            post_rollback_summary == restored_summary
        )
        if not database_intact_after_rollback:
            raise RuntimeError(
                "Database integrity changed during rollback."
            )

        finished_at = dt.datetime.now(dt.timezone.utc)

        backup_manifest = {
            "format": "PostgreSQL custom archive",
            "raw_archive_committed": False,
            "sha256": backup_sha256,
            "size_bytes": len(backup_bytes),
            "archive_entry_count": archive_entries,
            "backup_duration_seconds": round(backup_seconds, 3),
        }
        rollback_evidence = {
            "candidate_image_id": candidate_id,
            "known_good_image_id": known_good_id,
            "candidate_state": candidate_state,
            "candidate_exit_code": candidate_exit_code,
            "candidate_readiness_http_status": candidate_http_status,
            "rollback_readiness_http_status": rollback_http_status,
            "running_image_id_after_rollback": running_image_id,
            "image_identity_match": image_identity_match,
            "database_intact_after_rollback":
                database_intact_after_rollback,
            "rollback_duration_seconds": round(rollback_seconds, 3),
        }
        exercise = {
            "exercise_id": "P6-RECOVERY-001",
            "status": "PASS",
            "scope": (
                "Project-owned isolated local Docker Compose environments"
            ),
            "source_commit": commit,
            "started_at_utc": started_at.isoformat(),
            "finished_at_utc": finished_at.isoformat(),
            "known_good_build_seconds": round(
                known_good_build_seconds, 3
            ),
            "clean_target_initial_public_table_count": initial_tables,
            "restore_duration_seconds": round(restore_seconds, 3),
            "measured_recovery_time_seconds": round(
                measured_rto_seconds, 3
            ),
            "observed_fixture_rpo_seconds": 0,
            "restored_readiness_http_status": final_restore_status,
            "checks": {
                "backup_archive_valid": archive_entries > 0,
                "clean_target_confirmed": initial_tables == 0,
                "table_set_and_row_counts_match": (
                    source_summary["tables"]
                    == restored_summary["tables"]
                    and source_summary["row_counts"]
                    == restored_summary["row_counts"]
                ),
                "schema_fingerprint_matches": (
                    source_summary["schema_fingerprint_sha256"]
                    == restored_summary["schema_fingerprint_sha256"]
                ),
                "recovery_marker_restored_once": (
                    restored_summary["recovery_marker_count"] == 1
                ),
                "restored_application_ready": (
                    final_restore_status == 200
                ),
                "controlled_candidate_failed": (
                    candidate_exit_code == 42
                    and candidate_http_status != 200
                ),
                "known_good_image_restored": image_identity_match,
                "database_intact_after_rollback":
                    database_intact_after_rollback,
            },
            "limitations": [
                "Measured times apply only to this local controlled dataset.",
                "The raw backup was deleted and is not committed.",
                "Production requires encrypted off-site retention and approved RPO/RTO.",
                "The candidate image is a controlled failing fixture, not a historical production defect.",
            ],
        }

        files = {
            "source-database-summary.json": source_summary,
            "restored-database-summary.json": restored_summary,
            "backup-manifest.json": backup_manifest,
            "rollback-evidence.json": rollback_evidence,
            "recovery-exercise.json": exercise,
        }
        for name, value in files.items():
            (output_dir / name).write_text(
                json.dumps(value, indent=2),
                encoding="utf-8",
            )

        report = [
            "# Phase 6 Backup, Restore and Rollback Exercise",
            "",
            "## Result",
            "",
            "**PASS** — a PostgreSQL custom-format backup was validated,",
            "restored into a clean isolated database volume, served by the",
            "known-good application image and retained through a controlled",
            "candidate failure and image rollback.",
            "",
            "## Scope",
            "",
            "- Project-owned local Docker environments only",
            "- Two unique Compose projects and independent database volumes",
            "- Fictional seeded identities and one deterministic audit marker",
            "- No existing development database or volume used as a target",
            "",
            "## Measured results",
            "",
            f"- Backup archive size: **{len(backup_bytes)} bytes**",
            f"- Backup archive entries: **{archive_entries}**",
            f"- Backup duration: **{backup_seconds:.3f} seconds**",
            f"- Restore duration: **{restore_seconds:.3f} seconds**",
            f"- Measured local recovery time: **{measured_rto_seconds:.3f} seconds**",
            f"- Rollback duration: **{rollback_seconds:.3f} seconds**",
            f"- Restored application readiness: **HTTP {final_restore_status}**",
            "",
            "## Integrity verification",
            "",
            f"- Public tables: **{source_summary['table_count']}**",
            "- Source and restored table sets: **MATCH**",
            "- Every public-table row count: **MATCH**",
            "- Schema fingerprint: **MATCH**",
            "- Recovery marker: **restored exactly once**",
            "- Database after rollback: **UNCHANGED**",
            "",
            "## Rollback verification",
            "",
            "- Controlled candidate state: **exited**",
            f"- Controlled candidate exit code: **{candidate_exit_code}**",
            f"- Candidate readiness status: **HTTP {candidate_http_status} / unavailable**",
            f"- Rollback readiness status: **HTTP {rollback_http_status}**",
            "- Running image identity equals recorded known-good image: **YES**",
            "",
            "## Evidence handling",
            "",
            f"- Backup SHA-256: `{backup_sha256}`",
            "- Raw backup archive committed: **No**",
            "- Temporary passwords and Compose project identifiers committed: **No**",
            "- Evidence contains summaries, timing and immutable image identities only.",
            "",
            "## Failure handling",
            "",
            "The committed runbooks require the exercise to stop without merge when",
            "archive validation, clean-target checks, restore, integrity comparison,",
            "application readiness or exact-image rollback verification fails.",
            "",
            "## Limitations",
            "",
            "The observed zero-second fixture RPO and measured recovery time apply",
            "only to this local exercise. They are not production commitments.",
            "Production use requires encrypted off-site backups, retention policy,",
            "scheduled restore tests, monitored rollback and approved RPO/RTO.",
            "",
        ]
        report_path.write_text(
            "\n".join(report),
            encoding="utf-8",
        )

        print("PASS: backup archive validated")
        print("PASS: clean restore target verified")
        print("PASS: schema and all row counts matched")
        print("PASS: restored application returned HTTP 200")
        print("PASS: controlled candidate failed with exit code 42")
        print("PASS: exact known-good image rollback returned HTTP 200")
        print(
            "Measured recovery time: "
            f"{measured_rto_seconds:.3f} seconds"
        )
        print(
            "Measured rollback time: "
            f"{rollback_seconds:.3f} seconds"
        )

        temp_context.cleanup()
    finally:
        if source_env is not None:
            safe_down(
                compose_file,
                source_project,
                source_env,
            )
        if restore_env is not None:
            safe_down(
                compose_file,
                restore_project,
                restore_env,
            )
        run(
            ["docker", "image", "rm", "-f", candidate_image],
            check=False,
            text=True,
        )
        run(
            ["docker", "image", "rm", "-f", known_good_image],
            check=False,
            text=True,
        )


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(
            f"Recovery exercise failed: {error}",
            file=sys.stderr,
        )
        sys.exit(1)
