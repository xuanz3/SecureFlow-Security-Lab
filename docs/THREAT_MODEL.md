# STRIDE Threat Model

## Method

This initial threat model applies STRIDE to the local-first ticket application, CI pipeline, container artefacts and security evidence. Risk ratings are provisional until implementation and testing provide evidence.

| ID | STRIDE | Threat | Affected asset | Initial risk | Planned controls | Validation |
|---|---|---|---|---|---|---|
| T01 | Spoofing | Credential guessing or session theft | User account | High | Password policy, secure cookie, rate limiting | Authentication tests and manual testing |
| T02 | Tampering | User modifies another user's ticket identifier | Ticket data | High | Server-side object authorisation | Negative integration test and Burp retest |
| T03 | Repudiation | Privileged action has no reliable audit trail | Audit evidence | Medium | Structured audit events and correlation IDs | Log review and incident timeline |
| T04 | Information disclosure | Error response exposes stack or database detail | Application internals | Medium | Central exception handling and generic errors | ZAP/manual error testing |
| T05 | Denial of service | Repeated login or expensive requests consume resources | Application availability | Medium | Rate limiting, request limits and bounded uploads | Controlled local tests only |
| T06 | Elevation of privilege | Standard user reaches administrator endpoint | Administrative functions | High | Role policy enforced in backend | Automated negative test |
| T07 | Tampering | Malicious or oversized attachment bypasses checks | File storage | High | Extension, MIME, size and path validation | Upload security tests |
| T08 | Information disclosure | Repository or workflow leaks a secret | CI/CD credentials | High | Gitleaks, secret hygiene and least privilege | Controlled fake-secret fixture |
| T09 | Tampering | Compromised dependency or image enters release | Software supply chain | High | SCA, SBOM, Trivy and versioned images | CI gate evidence |
| T10 | Elevation of privilege | Container runs as root with excess capability | Runtime | Medium | Non-root image and minimal exposure | Docker/Trivy validation |
| T11 | Information disclosure | PostgreSQL is exposed outside required network | Database | High | Internal Docker network only | Nmap and Compose review |
| T12 | Tampering | Insecure Terraform example allows public access | Cloud reference architecture | Medium | Checkov and secure reference module | Static IaC scan |

## Assumptions

- All identities and records are synthetic.
- The application is not publicly hosted during the six-phase project.
- Availability tests must remain low-volume and non-destructive.
- KQL content will be documented as portable examples unless validated in Sentinel.

## Review points

Update this model after application implementation, the first security assessment and final remediation.
