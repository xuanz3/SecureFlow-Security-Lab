# DevSecOps Pipeline

## Pull-request gates

| Gate | Purpose | Failure policy |
|---|---|---|
| Build and test | Locked restore, Release build and automated tests | Any restore, build or test failure |
| Docker build | Reproducible container build | Any image build failure |
| Dependency review | Newly introduced vulnerable dependencies | High or critical severity |
| CodeQL | C# static analysis using `security-extended` queries | Workflow or analysis failure |
| Gitleaks | Full-history secret detection | Any detected secret |
| Trivy | Container vulnerabilities and configuration review | Fixed critical container vulnerability |
| ZAP baseline | Passive DAST against an isolated local stack | Selected security-header rules at FAIL |

## Supply-chain outputs

- NuGet lock files
- Trivy SARIF for the GitHub code-scanning interface
- CycloneDX container SBOM
- ZAP HTML, Markdown and JSON reports
- Versioned GHCR images
- Build provenance and SBOM attestations

## Token and workflow design

- Workflow permissions are declared per workflow.
- Checkout credentials are not persisted.
- Pull-request jobs use read-only repository access except where SARIF upload is
  explicitly required.
- Container publication runs only for a published Release or manual dispatch.
- Third-party Actions are pinned to full commit SHAs.
- The ZAP image is pinned to a registry digest.

## Security boundary

DAST starts a dedicated Docker Compose project using randomly generated,
workflow-only passwords. The scan targets only that project-owned runner network.
No external target is permitted.
