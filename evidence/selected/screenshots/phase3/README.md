# Phase 3 DevSecOps Evidence Index

| ID | Evidence | Demonstrated capability |
|---|---|---|
| P3-01 | `P3-01_pr48-merged-phase3.png` | Merged Phase 3 pull request closing Issues #14–#17 |
| P3-02 | `P3-02_codeql-pass.png` | Successful CodeQL C# static analysis |
| P3-03 | `P3-03_gitleaks-pass.png` | Successful full-history Gitleaks secret scan |
| P3-04 | `P3-04_trivy-sbom-security-gate.png` | Trivy scanning, SARIF upload, CycloneDX SBOM and critical gate |
| P3-05 | `P3-05_zap-baseline-pass.png` | Successful isolated OWASP ZAP baseline DAST |
| P3-06 | `P3-06_ghcr-versioned-container.png` | Versioned public GHCR image |

## Archived workflow artifacts

The publication script downloads and preserves:

- `container-security-evidence.zip`
- `zap-baseline-report.zip`

No passwords, `.env` values or tokens are visible in the screenshots.
