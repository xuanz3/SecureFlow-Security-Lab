# Six-Day Delivery Roadmap

| Day | Phase | Primary output |
|---|---|---|
| 1 | Security design | Repository, scope, architecture, threat model, ROE and backlog |
| 2 | Secure application | ASP.NET Core, PostgreSQL, identity, RBAC, tickets, upload and audit |
| 3 | DevSecOps | Tests, CodeQL, Gitleaks, Trivy, SBOM, ZAP and GHCR release |
| 4 | Assessment | Burp/ZAP testing, findings, vulnerability register, IaC and network evidence |
| 5 | Remediation and detection | Fix PRs, retesting, Sigma/KQL and incident investigation |
| 6 | Assurance and release | Risk/control documents, restore, rollback, reports and v1.0 release |

## Scope-control rule

A complete evidence loop is more valuable than a partially implemented tool. Optional tools are removed before core authorisation, testing, findings, remediation and recovery evidence.

## Target GitHub evidence

- 55–75 meaningful commits
- 16–18 pull requests
- 28–36 issues
- 6 milestones
- 6–8 Actions workflows
- 8–10 validated findings
- 5–6 closed remediation loops
- 5 releases
