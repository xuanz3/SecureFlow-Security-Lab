# NIST Cybersecurity Framework 2.0 Project Profile

## Purpose

This is a selected, function-level Current/Target Profile for the SecureFlow
portfolio project. It uses NIST CSF 2.0 as a communication structure for
project evidence. It is not a complete Core outcome assessment, CSF Tier
determination, certification or organisational compliance statement.

NIST CSF 2.0 describes six concurrent and continuous Functions: Govern,
Identify, Protect, Detect, Respond and Recover.

## Current and target profile

| Function | Current project outcome | Current status | Evidence | Target outcome |
|---|---|---|---|---|
| Govern | Scope, safety boundaries, evidence rules, risk ownership and workflow policy are documented. | Partial | `governance/RISK_REGISTER.md`; `.github/workflows/workflow-policy.yml` | Complete Issue #31 governance review and retain evidence-linked claims in the final reports. |
| Identify | Application assets, identities, data flows, threats, findings and residual risks are identified. | Established for the lab | `security-assessment/PHASE4_FINAL_ASSESSMENT_REPORT.md`; `governance/RISK_REGISTER.md` | Reassess assets and risks after recovery exercises and any deployment change. |
| Protect | Identity, authorisation, upload, dependency, secret, container and browser protections are implemented and retested. | Established with stated limitations | `security-assessment/PHASE5_REMEDIATION_DETECTION_REPORT.md`; `security-assessment/results/phase5/CONTAINER_WORKFLOW_RETEST.md` | Add MFA/federation, managed malware scanning and production secret management before deployment. |
| Detect | Structured audit events, five Sigma rules, five KQL examples and automated content validation exist. | Established for local evidence | `detections/README.md`; `incident-response/IR-P5-001-CONTROLLED-SUSPICIOUS-SEQUENCE.md` | Forward events to a real SIEM, define alert ownership and tune against operational baselines. |
| Respond | A controlled suspicious sequence was analysed, contained and documented. | Partial | `incident-response/IR-P5-001-CONTROLLED-SUSPICIOUS-SEQUENCE.md` | Add organisational communication, escalation, legal/privacy and external-notification procedures where applicable. |
| Recover | A PostgreSQL backup was validated and restored into a clean volume, and a controlled failing candidate image was rolled back to an exact known-good image. | Established for the local exercise | `recovery/PHASE6_RECOVERY_EXERCISE_REPORT.md`; `docs/PHASE6_RECOVERY_VALIDATION.md` | Add encrypted off-site retention, scheduled exercises and organisation-approved RPO/RTO before production. |

## Priority gaps

1. Recovery capability is not yet exercised; Issue #32 is the highest-priority
   target because database loss and rollback remain High/Extreme residual risks.
2. The local identity implementation does not provide MFA or federation.
3. Detection content is validated against local evidence, not a live SIEM.
4. Managed malware scanning, managed secrets and operational access reviews are
   outside the current lab.

## Framework reference

- NIST CSF 2.0, NIST CSWP 29, published 26 February 2024.
- The framework is outcome-based and does not prescribe one implementation.
- This profile was prepared on 2 August 2026 and should be reviewed when the
  project scope or framework changes.
