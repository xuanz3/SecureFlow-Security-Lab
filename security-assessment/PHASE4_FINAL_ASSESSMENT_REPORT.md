# Phase 4 Final Security Assessment Report

## Executive summary

SecureFlow was assessed inside the authorised project-owned local Docker
environment. The assessment combined manual/API security tests, targeted
source and configuration review, Checkov IaC analysis, Nmap exposure checks
and a controlled packet capture.

- Application tests: 9 PASS, 1 FINDING, 2 FAIL
- Validated findings: 8
- Medium: 6
- Low: 2
- High/Critical: 0

No public, third-party or production system was tested.

## Scope

- Local ASP.NET Core SecureFlow application
- Local PostgreSQL container
- Fictional Admin, Alice and Bob accounts
- Dockerfile and Docker Compose configuration
- Non-deployed Azure Terraform reference and insecure fixture
- Loopback and the Mac's active LAN address on TCP 5432/8080 only

## Validated controls

- **A03-ADMIN — Role authorisation:** HTTP 200
- **A05-CSRF — Request integrity:** HTTP 400
- **A05-404 — Error handling:** HTTP 404
- **A04-EXT — File upload:** Rejected
- **A04-MIME — File upload:** Rejected
- **A04-SIZE — File upload:** Rejected
- **A04-NAME — File upload:** Sanitised to report.pdf
- **A06 — Security headers:** All required headers present
- **A01 — Authentication rate limiting:** Statuses: 200, 200, 429

## Test deviations and findings

| Test | Area | Expected | Actual | Result |
|---|---|---|---|---|
| A02 | Object-level authorisation | Alice receives HTTP 403 for Bob's ticket | HTTP 200 | FAIL |
| A03 | Role authorisation | Normal user receives HTTP 403 for the administrator route | HTTP 200 | FAIL |
| A04-SIGNATURE | File upload | File content is verified against the declared type | Non-PDF content accepted as invoice.pdf | FINDING |

## Findings

| ID | Severity | Finding | GitHub issue |
|---|---|---|---|
| PH4-F01 | Medium | Upload validation trusts the declared file type | [#52](https://github.com/xuanz3/SecureFlow-Security-Lab/issues/52) |
| PH4-F02 | Medium | Uploaded files are not quarantined or malware-scanned | [#53](https://github.com/xuanz3/SecureFlow-Security-Lab/issues/53) |
| PH4-F03 | Medium | Login rate limiting uses a shared global bucket | [#54](https://github.com/xuanz3/SecureFlow-Security-Lab/issues/54) |
| PH4-F04 | Low | Content Security Policy permits inline styles | [#55](https://github.com/xuanz3/SecureFlow-Security-Lab/issues/55) |
| PH4-F05 | Low | Application container root filesystem is writable | [#56](https://github.com/xuanz3/SecureFlow-Security-Lab/issues/56) |
| PH4-F06 | Medium | Container runtime privileges are not explicitly reduced | [#57](https://github.com/xuanz3/SecureFlow-Security-Lab/issues/57) |
| PH4-F07 | Medium | Container base images are referenced by mutable tags | [#58](https://github.com/xuanz3/SecureFlow-Security-Lab/issues/58) |
| PH4-F08 | Medium | Upload request size is not limited before model binding | [#59](https://github.com/xuanz3/SecureFlow-Security-Lab/issues/59) |

## Evidence

- [Application assessment](results/phase4/APPLICATION_ASSESSMENT.md)
- [Vulnerability register](results/phase4/VULNERABILITY_REGISTER.md)
- [Checkov summary](results/phase4/CHECKOV_ASSESSMENT.md)
- [Network exposure summary](results/phase4/NETWORK_ASSESSMENT.md)
- Raw artifacts: `evidence/archive/artifacts/phase4/`

## Limitations

- The environment uses local HTTP and fictional data.
- The assessment does not claim production penetration-test coverage.
- Checkov reference results are manually triaged and no Azure resources were deployed.
- Malware-scanner integration was assessed by design/code review, not by introducing live malware.
- Finding severity is an estimate for this project environment.

## Next phase

Phase 5 will remediate selected findings through separate pull requests,
add regression tests and detection content, and record retest outcomes.
