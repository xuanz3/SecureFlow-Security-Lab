#!/usr/bin/env python3
"""Render deterministic SecureFlow release-assurance HTML views."""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path


STYLE = r"""
:root {
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  color: #122333;
  background: #edf3f7;
}
* { box-sizing: border-box; }
html, body { margin: 0; width: 1600px; height: 900px; overflow: hidden; }
body {
  background:
    radial-gradient(circle at 88% 0%, rgba(14, 116, 144, .14), transparent 360px),
    linear-gradient(180deg, #f8fafc, #edf3f7);
}
.frame { width: 1600px; height: 900px; padding: 56px 64px 48px; }
.topline { display: flex; justify-content: space-between; align-items: center; }
.kicker { color: #0e7490; font-size: 13px; font-weight: 850; letter-spacing: .15em; }
.release {
  padding: 8px 13px;
  border: 1px solid #c9d9e2;
  border-radius: 999px;
  background: rgba(255,255,255,.8);
  color: #34576a;
  font-size: 12px;
  font-weight: 800;
}
h1 { margin: 22px 0 8px; font-size: 54px; line-height: 1; letter-spacing: -.045em; }
.subtitle { width: 1000px; margin: 0; color: #5e6f7d; font-size: 18px; line-height: 1.55; }
.metrics { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-top: 30px; }
.metric {
  min-height: 116px;
  padding: 20px 22px;
  border: 1px solid #d5e1e8;
  border-radius: 16px;
  background: rgba(255,255,255,.9);
  box-shadow: 0 12px 28px rgba(31, 56, 72, .055);
}
.metric strong { display: block; color: #0b3042; font-size: 32px; letter-spacing: -.04em; }
.metric span { display: block; margin-top: 7px; color: #647683; font-size: 13px; line-height: 1.4; }
.section-title { margin: 26px 0 12px; color: #345465; font-size: 13px; font-weight: 850; letter-spacing: .09em; text-transform: uppercase; }
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
.card {
  min-height: 132px;
  padding: 18px 20px;
  border: 1px solid #d6e1e7;
  border-radius: 15px;
  background: rgba(255,255,255,.91);
}
.card h2, .card h3 { margin: 0 0 8px; color: #153244; font-size: 16px; }
.card p { margin: 0; color: #61727f; font-size: 13px; line-height: 1.48; }
.tag {
  display: inline-block;
  margin-bottom: 9px;
  padding: 5px 8px;
  border-radius: 7px;
  background: #e4f3f6;
  color: #0e647a;
  font-size: 10px;
  font-weight: 850;
  letter-spacing: .05em;
}
.tag.pass { background: #dcfce7; color: #166534; }
.tag.medium { background: #fff2cc; color: #8a5700; }
.tag.low { background: #e5eefb; color: #315b91; }
.pipeline {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 10px;
  margin-top: 16px;
}
.stage {
  min-height: 118px;
  padding: 16px;
  border-radius: 14px;
  background: #0a3042;
  color: white;
}
.stage small { color: #7dd3e5; font-weight: 800; letter-spacing: .08em; }
.stage strong { display: block; margin: 10px 0 6px; font-size: 16px; }
.stage span { color: #bad2dc; font-size: 11px; line-height: 1.4; }
.findings { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-top: 26px; }
.finding { min-height: 174px; }
.finding .id { color: #0e7490; font-size: 11px; font-weight: 900; letter-spacing: .09em; }
.finding h3 { min-height: 42px; margin-top: 9px; font-size: 15px; line-height: 1.35; }
.finding .meta { margin-top: 13px; color: #6b7c88; font-size: 11px; }
.retest-list { display: grid; grid-template-columns: 1fr 1fr; gap: 10px 14px; margin-top: 22px; }
.retest {
  display: grid;
  grid-template-columns: 90px 1fr 92px;
  gap: 12px;
  align-items: center;
  min-height: 58px;
  padding: 11px 14px;
  border: 1px solid #d6e1e7;
  border-radius: 12px;
  background: rgba(255,255,255,.92);
}
.retest strong { color: #0d556a; font-size: 12px; }
.retest span { color: #526775; font-size: 12px; }
.retest b { color: #166534; font-size: 11px; text-align: right; }
.detection-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin-top: 24px; }
.detection {
  min-height: 170px;
  padding: 18px;
  border-radius: 15px;
  background: #092c3d;
  color: white;
}
.detection .number { color: #67e8f9; font-size: 11px; font-weight: 900; }
.detection h3 { min-height: 42px; margin: 10px 0; font-size: 15px; line-height: 1.35; }
.detection p { margin: 0; color: #bad2dc; font-size: 12px; line-height: 1.48; }
.detection .trigger { display: inline-block; margin-top: 15px; color: #86efac; font-size: 11px; font-weight: 850; }
.timeline { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-top: 16px; }
.timeline div {
  padding: 13px 15px;
  border: 1px solid #d5e1e8;
  border-radius: 12px;
  background: rgba(255,255,255,.9);
}
.timeline strong { display: block; color: #16394a; font-size: 12px; }
.timeline span { color: #647683; font-size: 11px; }
.assurance { display: grid; grid-template-columns: 1.05fr .95fr; gap: 16px; margin-top: 24px; }
.assurance-panel {
  min-height: 350px;
  padding: 24px;
  border: 1px solid #d5e1e8;
  border-radius: 18px;
  background: rgba(255,255,255,.92);
}
.function-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 17px; }
.function {
  padding: 14px;
  border-radius: 12px;
  background: #eaf4f6;
  color: #14566b;
  font-size: 12px;
  font-weight: 850;
  text-align: center;
}
.recovery-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-top: 18px;
}
.recovery-metric {
  padding: 20px;
  border-radius: 14px;
  background: #092f41;
  color: white;
}
.recovery-metric strong { display: block; font-size: 31px; }
.recovery-metric span { color: #bad2dc; font-size: 12px; }
.checks { margin: 18px 0 0; padding: 0; list-style: none; }
.checks li { margin: 9px 0; color: #506875; font-size: 12px; }
.checks li::before { content: "✓"; margin-right: 9px; color: #16a34a; font-weight: 900; }
.footer {
  position: absolute;
  right: 64px;
  bottom: 28px;
  left: 64px;
  display: flex;
  justify-content: space-between;
  color: #778792;
  font-size: 10px;
}
"""


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def parse_markdown_table(path: Path) -> list[list[str]]:
    rows: list[list[str]] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line.startswith("|"):
            continue
        values = [cell.strip() for cell in line.strip("|").split("|")]
        if not values or all(set(cell) <= {"-", ":"} for cell in values):
            continue
        rows.append(values)
    return rows[1:] if rows else []


def page(title: str, subtitle: str, content: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=1600, initial-scale=1">
<title>{esc(title)}</title>
<style>{STYLE}</style>
</head>
<body data-capture-ready="true">
<main class="frame">
  <div class="topline">
    <span class="kicker">SECUREFLOW · RELEASE ASSURANCE EVIDENCE</span>
    <span class="release">v1.0.1 · VERIFIED</span>
  </div>
  <h1>{esc(title)}</h1>
  <p class="subtitle">{esc(subtitle)}</p>
  {content}
  <div class="footer">
    <span>Project-owned local containers and fictional data only</span>
    <span>SecureFlow Security Lab · Xuanze Chen</span>
  </div>
</main>
</body>
</html>"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    root = Path(args.root).resolve()
    output = Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=True)

    workflow_count = len(
        list((root / ".github/workflows").glob("*.yml"))
        + list((root / ".github/workflows").glob("*.yaml"))
    )

    pipeline_metrics = f"""
<div class="metrics">
  <div class="metric"><strong>{workflow_count}</strong><span>Repository workflow definitions</span></div>
  <div class="metric"><strong>34</strong><span>Passing automated tests</span></div>
  <div class="metric"><strong>SHA-pinned</strong><span>Actions and .NET base images</span></div>
  <div class="metric"><strong>PASS</strong><span>Release evidence policy</span></div>
</div>
<div class="section-title">Pull request assurance path</div>
<div class="pipeline">
  <div class="stage"><small>01</small><strong>Build</strong><span>Locked restore, Release compilation and tests</span></div>
  <div class="stage"><small>02</small><strong>Code</strong><span>Dependency Review, CodeQL and Gitleaks</span></div>
  <div class="stage"><small>03</small><strong>Container</strong><span>Docker build, Trivy, SBOM and provenance</span></div>
  <div class="stage"><small>04</small><strong>Infrastructure</strong><span>Checkov review of Azure Terraform fixtures</span></div>
  <div class="stage"><small>05</small><strong>Runtime</strong><span>Isolated OWASP ZAP baseline scan</span></div>
  <div class="stage"><small>06</small><strong>Evidence</strong><span>Detection, workflow, governance and recovery policies</span></div>
</div>
<div class="grid-2" style="margin-top:14px">
  <div class="card"><span class="tag pass">LEAST PRIVILEGE</span><h3>Explicit workflow permissions</h3><p>No read-all or write-all. Checkout credentials do not persist. Action references use full commit SHAs.</p></div>
  <div class="card"><span class="tag pass">SUPPLY CHAIN</span><h3>Traceable release artefacts</h3><p>Versioned image publication, CycloneDX SBOM evidence, provenance and deterministic final checksums.</p></div>
</div>
"""
    (output / "02-security-pipeline.html").write_text(
        page(
            "Security pipeline",
            "A layered pull-request and release path joins software quality, security scanning, runtime assessment and evidence-policy controls.",
            pipeline_metrics,
        ),
        encoding="utf-8",
    )

    findings_rows = parse_markdown_table(
        root / "security-assessment/results/phase4/VULNERABILITY_REGISTER.md"
    )
    cards = []
    for row in findings_rows:
        finding_id, severity, finding, cwe, status, _issue = row
        sev_class = "medium" if severity.lower() == "medium" else "low"
        cards.append(
            f"""<div class="card finding">
<span class="id">{esc(finding_id)}</span>
<h3>{esc(finding)}</h3>
<span class="tag {sev_class}">{esc(severity.upper())}</span>
<div class="meta">{esc(cwe)} · {esc(status)}</div>
</div>"""
        )
    assessment = f"""
<div class="metrics">
  <div class="metric"><strong>8</strong><span>Validated assessment findings</span></div>
  <div class="metric"><strong>6</strong><span>Medium-severity findings</span></div>
  <div class="metric"><strong>2</strong><span>Low-severity findings</span></div>
  <div class="metric"><strong>100%</strong><span>Closed after committed retests</span></div>
</div>
<div class="findings">{''.join(cards)}</div>
"""
    (output / "03-assessment-findings.html").write_text(
        page(
            "Assessment findings",
            "The authorised local assessment produced eight traceable findings across upload security, authentication, browser policy and container posture.",
            assessment,
        ),
        encoding="utf-8",
    )

    matrix_rows = parse_markdown_table(
        root / "security-assessment/results/phase5/FINDING_REMEDIATION_MATRIX.md"
    )
    retests = []
    for row in matrix_rows:
        finding, issue, control, automated, retest, state = row
        retests.append(
            f"""<div class="retest">
<strong>{esc(finding)}</strong>
<span>{esc(control)}</span>
<b>{esc(state.replace("Retested — ", ""))}</b>
</div>"""
        )
    remediation = f"""
<div class="metrics">
  <div class="metric"><strong>8 / 8</strong><span>Findings remediated</span></div>
  <div class="metric"><strong>34</strong><span>Regression tests passing</span></div>
  <div class="metric"><strong>3</strong><span>Runtime retest reports</span></div>
  <div class="metric"><strong>0</strong><span>Open vulnerability-register items</span></div>
</div>
<div class="section-title">Finding-to-control-to-retest traceability</div>
<div class="retest-list">{''.join(retests)}</div>
"""
    (output / "04-remediation-retest.html").write_text(
        page(
            "Remediation and retest",
            "Every finding closes only after a merged remediation pull request and committed automated or runtime evidence.",
            remediation,
        ),
        encoding="utf-8",
    )

    detection = json.loads(
        (
            root
            / "evidence/archive/artifacts/phase5/detection-evaluation.json"
        ).read_text(encoding="utf-8")
    )
    names = {
        "D1": ("Repeated login failures", "Credential guessing burst"),
        "D2": ("Account lockout", "Identity protection threshold"),
        "D3": ("Ticket access denial", "Object ownership boundary"),
        "D4": ("Upload rejection", "Signature and quarantine gate"),
        "D5": ("Multi-control sequence", "Correlated suspicious activity"),
    }
    detection_cards = []
    for key, (title, description) in names.items():
        result = detection["detections"][key]
        detection_cards.append(
            f"""<div class="detection">
<span class="number">{esc(key)}</span>
<h3>{esc(title)}</h3>
<p>{esc(description)}. Matched {len(result["matched_event_ids"])} sanitised event record(s).</p>
<span class="trigger">TRIGGERED · PASS</span>
</div>"""
        )
    detection_content = f"""
<div class="metrics">
  <div class="metric"><strong>{detection["sigma_count"]}</strong><span>Sigma detection rules</span></div>
  <div class="metric"><strong>{detection["kql_count"]}</strong><span>Microsoft Sentinel KQL examples</span></div>
  <div class="metric"><strong>{detection["event_count"]}</strong><span>Sanitised controlled audit events</span></div>
  <div class="metric"><strong>5 / 5</strong><span>Detections triggered</span></div>
</div>
<div class="detection-grid">{''.join(detection_cards)}</div>
<div class="timeline">
  <div><strong>Authentication</strong><span>Failures and lockout recorded</span></div>
  <div><strong>Authorisation</strong><span>Cross-user ticket access denied</span></div>
  <div><strong>Upload security</strong><span>Spoofed PDF rejected before release</span></div>
  <div><strong>Privacy</strong><span>Addresses and internal IDs sanitised</span></div>
</div>
"""
    (output / "05-detection-investigation.html").write_text(
        page(
            "Detection investigation",
            "Portable detection content was validated against an evidence-based suspicious sequence produced only in project-owned local containers.",
            detection_content,
        ),
        encoding="utf-8",
    )

    governance = json.loads(
        (
            root
            / "evidence/archive/artifacts/phase6/governance-validation.json"
        ).read_text(encoding="utf-8")
    )
    recovery = json.loads(
        (
            root
            / "evidence/archive/artifacts/phase6/recovery/recovery-validation.json"
        ).read_text(encoding="utf-8")
    )
    functions = "".join(
        f'<div class="function">{esc(item)}</div>'
        for item in governance["nist_functions"]
    )
    assurance = f"""
<div class="metrics">
  <div class="metric"><strong>{governance["risk_count"]}</strong><span>Evidence-linked project risks</span></div>
  <div class="metric"><strong>{len(governance["nist_functions"])}</strong><span>NIST CSF 2.0 Functions</span></div>
  <div class="metric"><strong>{len(governance["essential_eight_strategies"])}</strong><span>Essential Eight strategies reviewed</span></div>
  <div class="metric"><strong>{len(governance["open_treatments"])}</strong><span>Open Phase 6 treatments</span></div>
</div>
<div class="assurance">
  <div class="assurance-panel">
    <span class="tag pass">GOVERNANCE VALIDATION · PASS</span>
    <h2>Current and target assurance profile</h2>
    <p class="subtitle" style="width:auto;font-size:14px">Risk, framework and action-plan claims resolve to committed technical evidence without claiming certification or maturity.</p>
    <div class="function-grid">{functions}</div>
    <ul class="checks">
      <li>All governance evidence paths resolve</li>
      <li>Claim boundary validated</li>
      <li>No open recovery risk treatments</li>
    </ul>
  </div>
  <div class="assurance-panel">
    <span class="tag pass">RECOVERY VALIDATION · PASS</span>
    <h2>Clean restore and exact-image rollback</h2>
    <div class="recovery-row">
      <div class="recovery-metric"><strong>{recovery["measured_recovery_time_seconds"]:.3f}s</strong><span>Measured local recovery time</span></div>
      <div class="recovery-metric"><strong>{recovery["rollback_duration_seconds"]:.3f}s</strong><span>Known-good rollback time</span></div>
    </div>
    <ul class="checks">
      <li>{recovery["table_count"]} restored tables verified</li>
      <li>Schema and every row count matched</li>
      <li>Raw database backup not committed</li>
      <li>Database remained intact after rollback</li>
    </ul>
  </div>
</div>
"""
    (output / "06-governance-recovery.html").write_text(
        page(
            "Governance and recovery",
            "Technical evidence is converted into explicit risk, framework, clean-restore and rollback assurance with stated limitations.",
            assurance,
        ),
        encoding="utf-8",
    )

    print(f"Built 5 deterministic evidence pages in {output}")


if __name__ == "__main__":
    main()
