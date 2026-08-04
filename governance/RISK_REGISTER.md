# SecureFlow Risk Register

## Scope and method

This is a project-level project risk self-assessment. It is not an
enterprise risk assessment, certification, regulatory compliance statement
or substitute for production threat, business-impact and legal analysis.

Likelihood and impact use a 1–5 scale. Score equals likelihood multiplied by
impact. Bands are Low 1–4, Moderate 5–9, High 10–14 and Extreme 15–25.

| ID | Risk | Inherent | Residual | Status | Treatment |
|---|---|---:|---:|---|---|
| R-01 | Credential guessing or account compromise | 16 | 8 | Mitigated with residual risk | Add MFA or federated identity before production deployment. |
| R-02 | Broken object or administrator authorisation | 20 | 5 | Mitigated | Retain negative tests and review new object routes during pull requests. |
| R-03 | Malicious or misclassified file upload | 16 | 8 | Mitigated with residual risk | Use a managed antivirus or sandbox service before production use. |
| R-04 | Software supply-chain compromise | 15 | 5 | Mitigated | Continue reviewed dependency and digest updates through pull requests. |
| R-05 | Container privilege escalation or runtime configuration drift | 15 | 5 | Mitigated | Revalidate runtime policy after Compose or hosting changes. |
| R-06 | Credential or secret exposure in source control | 15 | 5 | Mitigated | Use a managed secret store for any deployed environment. |
| R-07 | Security events are not detected or correlated | 16 | 8 | Mitigated with residual risk | Forward events to a real SIEM and tune thresholds before production use. |
| R-08 | Database loss or unusable backup | 15 | 5 | Mitigated with residual risk | Retain scheduled restore testing and add encrypted off-site retention before production. |
| R-09 | Application rollback fails during an incident or bad release | 12 | 4 | Mitigated | Retain immutable known-good image references and rehearse rollback after material deployment changes. |
| R-10 | Governance or compliance capability is overstated | 8 | 4 | Mitigated | Retain limitations in final management and technical reports. |

## Evidence and control detail

### R-01 — Credential guessing or account compromise

- Asset: Local application identities and protected tickets
- Threat: Repeated password attempts against a fictional or future deployed account
- Controls:
  - Password policy and account lockout
  - Source-partitioned login throttling
  - Structured login audit events
  - Sigma and KQL detections
- Evidence:
  - [`security-assessment/results/phase5/UPLOAD_AUTH_RETEST.md`](../security-assessment/results/phase5/UPLOAD_AUTH_RETEST.md)
  - [`detections/README.md`](../detections/README.md)
  - [`incident-response/IR-P5-001-CONTROLLED-SUSPICIOUS-SEQUENCE.md`](../incident-response/IR-P5-001-CONTROLLED-SUSPICIOUS-SEQUENCE.md)
- Owner: Project owner
- Residual treatment decision: Add MFA or federated identity before production deployment.

### R-02 — Broken object or administrator authorisation

- Asset: Tickets, attachments and administrator functions
- Threat: An authenticated user attempts to access another user's object or an administrator route
- Controls:
  - Server-side owner checks
  - Role-based Admin controller boundary
  - Negative regression tests
  - Runtime denial retest
- Evidence:
  - [`security-assessment/results/phase5/AUTHORIZATION_RETEST.md`](../security-assessment/results/phase5/AUTHORIZATION_RETEST.md)
  - [`tests/SecureFlow.Tests/Security/AuthorizationBoundaryTests.cs`](../tests/SecureFlow.Tests/Security/AuthorizationBoundaryTests.cs)
- Owner: Project owner
- Residual treatment decision: Retain negative tests and review new object routes during pull requests.

### R-03 — Malicious or misclassified file upload

- Asset: Application storage, users and downstream file consumers
- Threat: An attacker uploads content whose extension or declared MIME type hides its actual type
- Controls:
  - Extension, MIME, size and signature checks
  - Quarantine-before-release workflow
  - Deterministic local security scanner
  - Upload rejection audit events
- Evidence:
  - [`security-assessment/results/phase5/UPLOAD_AUTH_RETEST.md`](../security-assessment/results/phase5/UPLOAD_AUTH_RETEST.md)
  - [`tests/SecureFlow.Tests/Security/FileSecurityScannerTests.cs`](../tests/SecureFlow.Tests/Security/FileSecurityScannerTests.cs)
- Owner: Project owner
- Residual treatment decision: Use a managed antivirus or sandbox service before production use.

### R-04 — Software supply-chain compromise

- Asset: Application dependencies, container image and release artefacts
- Threat: A vulnerable dependency, mutable build input or compromised automation component enters a release
- Controls:
  - Locked dependency restore
  - Dependency Review and vulnerability audit
  - Action references pinned to commit SHAs
  - Container scanning, SBOM and provenance
  - Digest-pinned .NET base images
- Evidence:
  - [`.github/workflows/dependency-review.yml`](../.github/workflows/dependency-review.yml)
  - [`.github/workflows/container-security.yml`](../.github/workflows/container-security.yml)
  - [`.github/workflows/workflow-policy.yml`](../.github/workflows/workflow-policy.yml)
  - [`security-assessment/results/phase5/CONTAINER_WORKFLOW_RETEST.md`](../security-assessment/results/phase5/CONTAINER_WORKFLOW_RETEST.md)
- Owner: Project owner
- Residual treatment decision: Continue reviewed dependency and digest updates through pull requests.

### R-05 — Container privilege escalation or runtime configuration drift

- Asset: Application container and host boundary
- Threat: A compromised process writes to the image, gains capabilities or runs with excess privilege
- Controls:
  - Non-root runtime user
  - Read-only root filesystem
  - All Linux capabilities dropped
  - No-new-privileges
  - Explicit writable volumes only
  - Workflow policy validation
- Evidence:
  - [`infrastructure/docker/Dockerfile`](../infrastructure/docker/Dockerfile)
  - [`infrastructure/docker/compose.yml`](../infrastructure/docker/compose.yml)
  - [`security-assessment/results/phase5/CONTAINER_WORKFLOW_RETEST.md`](../security-assessment/results/phase5/CONTAINER_WORKFLOW_RETEST.md)
- Owner: Project owner
- Residual treatment decision: Revalidate runtime policy after Compose or hosting changes.

### R-06 — Credential or secret exposure in source control

- Asset: Database password, fictional account secrets and CI credentials
- Threat: A local secret is committed or a workflow retains credentials unnecessarily
- Controls:
  - Local-only generated .env file
  - Gitleaks workflow
  - Checkout persist-credentials disabled
  - Explicit workflow permissions
- Evidence:
  - [`.github/workflows/secret-scan.yml`](../.github/workflows/secret-scan.yml)
  - [`.github/workflows/workflow-policy.yml`](../.github/workflows/workflow-policy.yml)
  - [`security-assessment/results/phase5/CONTAINER_WORKFLOW_RETEST.md`](../security-assessment/results/phase5/CONTAINER_WORKFLOW_RETEST.md)
- Owner: Project owner
- Residual treatment decision: Use a managed secret store for any deployed environment.

### R-07 — Security events are not detected or correlated

- Asset: Audit trail and incident response capability
- Threat: Credential, authorisation and upload abuse occurs without an actionable alert
- Controls:
  - Structured audit schema
  - Five Sigma rules
  - Five KQL examples
  - Automated detection-content validation
  - Controlled incident evaluation
- Evidence:
  - [`detections/README.md`](../detections/README.md)
  - [`.github/workflows/detection-content.yml`](../.github/workflows/detection-content.yml)
  - [`incident-response/IR-P5-001-CONTROLLED-SUSPICIOUS-SEQUENCE.md`](../incident-response/IR-P5-001-CONTROLLED-SUSPICIOUS-SEQUENCE.md)
- Owner: Project owner
- Residual treatment decision: Forward events to a real SIEM and tune thresholds before production use.

### R-08 — Database loss or unusable backup

- Asset: PostgreSQL tickets, attachments metadata, identities and audit events
- Threat: Data is deleted or corrupted and the available backup cannot be restored
- Controls:
  - Persistent PostgreSQL volume
  - Custom-format database backup with SHA-256 validation
  - Clean-volume restore with schema and row-count comparison
  - Measured local recovery exercise and failure runbook
- Evidence:
  - [`infrastructure/docker/compose.yml`](../infrastructure/docker/compose.yml)
  - [`recovery/PHASE6_RECOVERY_EXERCISE_REPORT.md`](../recovery/PHASE6_RECOVERY_EXERCISE_REPORT.md)
  - [`docs/PHASE6_RECOVERY_VALIDATION.md`](../docs/PHASE6_RECOVERY_VALIDATION.md)
  - [`recovery/runbooks/DATABASE_BACKUP_RESTORE.md`](../recovery/runbooks/DATABASE_BACKUP_RESTORE.md)
- Owner: Project owner
- Residual treatment decision: Retain scheduled restore testing and add encrypted off-site retention before production.

### R-09 — Application rollback fails during an incident or bad release

- Asset: Service availability and release integrity
- Threat: A faulty application version cannot be replaced by a known-good version within an acceptable time
- Controls:
  - Versioned Git releases
  - Published container images and provenance
  - Exact known-good image identity verification
  - Controlled candidate failure and measured rollback exercise
- Evidence:
  - [`.github/workflows/publish-image.yml`](../.github/workflows/publish-image.yml)
  - [`recovery/PHASE6_RECOVERY_EXERCISE_REPORT.md`](../recovery/PHASE6_RECOVERY_EXERCISE_REPORT.md)
  - [`docs/PHASE6_RECOVERY_VALIDATION.md`](../docs/PHASE6_RECOVERY_VALIDATION.md)
  - [`recovery/runbooks/APPLICATION_ROLLBACK.md`](../recovery/runbooks/APPLICATION_ROLLBACK.md)
- Owner: Project owner
- Residual treatment decision: Retain immutable known-good image references and rehearse rollback after material deployment changes.

### R-10 — Governance or compliance capability is overstated

- Asset: project credibility and stakeholder trust
- Threat: Project evidence is presented as certification, enterprise compliance or a complete organisational assessment
- Controls:
  - Explicit scope and limitations
  - Evidence-linked claims
  - No certification or maturity-level claim
  - Automated governance-content validation
- Evidence:
  - [`README.md`](../README.md)
  - [`security-assessment/PHASE5_REMEDIATION_DETECTION_REPORT.md`](../security-assessment/PHASE5_REMEDIATION_DETECTION_REPORT.md)
- Owner: Project owner
- Residual treatment decision: Retain limitations in final management and technical reports.
