# Final Portfolio Evidence

The six final images are generated once from the completed and validated v1.0
project. They replace phase-by-phase screenshots and are the only images shown
on the root README.

| Image | Purpose | Source |
|---|---|---|
| `01-application-overview.png` | Final product and capability overview | Hardened local Docker application |
| `02-security-pipeline.png` | DevSecOps control coverage | Workflow files and final technical report |
| `03-assessment-findings.png` | Eight validated findings | Phase 4 vulnerability register |
| `04-remediation-retest.png` | Eight successful remediation retests | Phase 5 remediation matrix and test evidence |
| `05-detection-investigation.png` | Sigma, KQL and controlled incident | Detection evaluation JSON |
| `06-governance-recovery.png` | Risk, framework and recovery results | Phase 6 validation JSON |

## Reproduction

The final-release automation starts the hardened application in isolated Docker
containers and runs:

```bash
evidence/final/tools/capture_final_evidence.sh http://127.0.0.1:<dynamic-port>
```

The capture process uses:

- Playwright `1.55.0`
- an installed Google Chrome browser verified and controlled by that Playwright version
- fixed `1600 × 900` viewport
- fixed filenames and selectors
- repository-local evidence data
- PNG dimension, file-count and SHA-256 validation

## Evidence policy

- no GitHub webpage screenshots;
- no terminal screenshots;
- no local usernames, paths, credentials or private addresses;
- no raw database backup;
- exactly six final PNG files;
- root README links only to these final images.

`manifest.json` records image dimensions, sizes, SHA-256 values and source
categories. `SHA256SUMS.txt` provides independent checksum verification.
