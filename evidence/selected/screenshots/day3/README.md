# Day 3 DevSecOps Evidence Index

| ID | Evidence | Demonstrated capability |
|---|---|---|
| D3-01 | `D3-01_pr48-merged-phase2.png` | Merged Phase 2 pull request closing Issues #14–#17 |
| D3-02 | `D3-02_codeql-pass.png` | Successful CodeQL C# static analysis |
| D3-03 | `D3-03_gitleaks-pass.png` | Successful full-history Gitleaks secret scan |
| D3-04 | `D3-04_trivy-sbom-security-gate.png` | Trivy scanning, SARIF upload, CycloneDX SBOM and critical gate |
| D3-05 | `D3-05_zap-baseline-pass.png` | Successful isolated OWASP ZAP baseline DAST |
| D3-06 | `D3-06_ghcr-versioned-container.png` | Versioned public GHCR image |

## Archived workflow artifacts

The publication script downloads and preserves:

- `container-security-evidence.zip`
- `zap-baseline-report.zip`

No passwords, `.env` values or tokens are visible in the screenshots.
