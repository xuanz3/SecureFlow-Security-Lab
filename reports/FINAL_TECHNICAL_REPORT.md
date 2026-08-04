# SecureFlow v1.0.1 Technical Report

## 1. System overview

SecureFlow is an ASP.NET Core 10 MVC application backed by PostgreSQL 17 and
Entity Framework Core. It uses ASP.NET Core Identity, role-based administrator
boundaries, object-level ticket ownership checks, protected attachment storage,
structured audit events, health checks and a reproducible Docker environment.

The completed implementation covers six delivery phases:

| Phase | Technical focus | Primary evidence |
|---|---|---|
| 1 | Security design and repository governance | `docs/`, GitHub Issues and pull requests |
| 2 | Secure application foundation | `src/`, `tests/`, Docker Compose |
| 3 | DevSecOps and supply-chain assurance | `.github/workflows/`, SBOM and scan evidence |
| 4 | Authorised application, container, IaC and network assessment | `security-assessment/results/phase4/` |
| 5 | Remediation, detection engineering and incident investigation | `security-assessment/results/phase5/`, `detections/`, `incident-response/` |
| 6 | Governance, clean restore, rollback and final reporting | `governance/`, `recovery/`, `reports/`, `evidence/final/` |

## 2. Security architecture

### Identity and authorisation

- ASP.NET Core Identity with fictional local accounts
- `Admin` and `User` role separation
- server-side ticket ownership enforcement
- negative authorisation regression tests
- password policy, lockout and source-partitioned login limiting
- secure cookie settings and anti-forgery validation

### Upload security

- request-size controls before model binding
- extension, declared type and file-signature validation
- quarantine-before-release processing
- deterministic local scanner abstraction
- server-detected content type
- structured scan and rejection audit events

### Container and browser posture

- non-root application user
- read-only application root filesystem
- all Linux capabilities dropped
- `no-new-privileges`
- explicit writable mounts only
- digest-pinned .NET SDK and runtime images
- Content Security Policy without `unsafe-inline`
- security headers, liveness and database readiness endpoints

## 3. DevSecOps pipeline

Pull requests validate locked restore, Release build, 34 automated tests,
Docker build, Dependency Review, CodeQL, Gitleaks, Trivy, Checkov, an isolated
OWASP ZAP baseline, Sigma/KQL content, workflow permissions, governance
evidence and recovery evidence.

GitHub Actions use explicit top-level permissions, immutable action commit
references and checkout with persisted credentials disabled. Release workflows
publish versioned container images, SBOM evidence and provenance.

## 4. Findings-to-remediation traceability

| Finding | Original weakness | Remediation | Retest result |
|---|---|---|---|
| PH4-F01 | Declared file type trusted | File-signature and content verification | PASS |
| PH4-F02 | No quarantine or scanning gate | Quarantine, scanner abstraction and release state | PASS |
| PH4-F03 | Shared login limiter bucket | Source-partitioned login limiter | PASS |
| PH4-F04 | CSP permitted inline styles | CSP policy and stylesheet refactor | PASS |
| PH4-F05 | Writable application root | Read-only root filesystem | PASS |
| PH4-F06 | Excess runtime privilege | Drop all capabilities and prevent privilege gain | PASS |
| PH4-F07 | Mutable .NET image tags | Digest-pinned SDK and runtime images | PASS |
| PH4-F08 | Late upload-size enforcement | Multipart and endpoint request-size limits | PASS |

Finding closure requires a merged remediation pull request and committed retest
evidence. The authoritative matrix is
`security-assessment/results/phase5/FINDING_REMEDIATION_MATRIX.md`.

## 5. Detection and incident evidence

Five Sigma rules and five Microsoft Sentinel KQL examples cover repeated login
failures, account lockout, cross-user ticket denial, upload security rejection
and a multi-control suspicious sequence.

A controlled local scenario produced 11 sanitised audit events. All five
detections triggered. Internal identity identifiers were mapped to fictional
labels, source addresses were replaced, and no credentials or cookies were
committed.

## 6. Governance

The project risk register contains 10 evidence-linked risks. The NIST CSF 2.0
profile represents Govern, Identify, Protect, Detect, Respond and Recover.
The Essential Eight review covers all eight strategies while clearly stating
scope limitations and making no maturity-level claim.

After the recovery exercise, the governance validator reports zero open Phase 6
risk treatments.

## 7. Backup, restore and rollback

The recovery exercise:

1. built a known-good image from the tested commit;
2. started an isolated source database and application;
3. created and SHA-256 validated a PostgreSQL custom-format archive;
4. verified a second target database was empty;
5. restored the archive with `pg_restore --exit-on-error`;
6. compared all 11 public tables, every row count and the schema fingerprint;
7. verified a deterministic recovery marker exactly once;
8. confirmed the restored application returned HTTP 200;
9. deployed a controlled candidate that exited with code 42;
10. restored the exact known-good image identity;
11. confirmed HTTP 200 and unchanged database integrity.

Observed local recovery time was 5.007 seconds and rollback time was 1.473
seconds. These are exercise measurements, not production commitments.

## 8. Release evidence and reproducibility

Six final images are generated from a clean isolated clone. The application
overview is captured from a hardened Docker runtime. The remaining evidence
views are rendered directly from committed Markdown and JSON records.

Capture uses a fixed Playwright version, verified installed Chrome, fixed 1600×900 viewport, deterministic
routes, content assertions, exact filenames, PNG dimension validation, SHA-256
checksums and a machine-readable manifest.

## 9. Known limitations

- local Identity does not provide MFA or federation;
- the deterministic scanner is not a production antivirus service;
- the KQL content is not connected to a live Microsoft Sentinel workspace;
- the project does not claim production cloud deployment;
- the governance material is not certification or organisational compliance;
- recovery measurements are limited to the controlled local dataset.

## 10. Evidence navigation

- `README.md`
- `reports/FINAL_MANAGEMENT_REPORT.md`
- `docs/FINAL_VALIDATION.md`
- `evidence/final/README.md`
- `security-assessment/PHASE4_FINAL_ASSESSMENT_REPORT.md`
- `security-assessment/PHASE5_REMEDIATION_DETECTION_REPORT.md`
- `incident-response/IR-P5-001-CONTROLLED-SUSPICIOUS-SEQUENCE.md`
- `governance/RISK_REGISTER.md`
- `recovery/PHASE6_RECOVERY_EXERCISE_REPORT.md`
