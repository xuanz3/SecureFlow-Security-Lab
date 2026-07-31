# Phase 4 Application Security Assessment

- Run: `20260731T150928Z`
- Started: 2026-07-31 15:09:28 UTC
- Target: `http://localhost:8080`
- Safety boundary: project-owned localhost containers and fictional accounts
- Test results: 9 PASS, 1 FINDING, 2 FAIL
- Validated findings: 8

## Test matrix results

| Test | Area | Expected | Actual | Status |
|---|---|---|---|---|
| A02 | Object-level authorisation | Alice receives HTTP 403 for Bob's ticket | HTTP 200 | FAIL |
| A03 | Role authorisation | Normal user receives HTTP 403 for the administrator route | HTTP 200 | FAIL |
| A03-ADMIN | Role authorisation | Administrator can access the administrator route | HTTP 200 | PASS |
| A05-CSRF | Request integrity | POST without anti-forgery token is rejected | HTTP 400 | PASS |
| A05-404 | Error handling | Unknown ticket identifier returns HTTP 404 without a stack trace | HTTP 404 | PASS |
| A04-EXT | File upload | Executable extension is rejected | Rejected | PASS |
| A04-MIME | File upload | Declared MIME mismatch is rejected | Rejected | PASS |
| A04-SIZE | File upload | File larger than 2 MB is rejected | Rejected | PASS |
| A04-NAME | File upload | Path components are removed from the original filename | Sanitised to report.pdf | PASS |
| A04-SIGNATURE | File upload | File content is verified against the declared type | Non-PDF content accepted as invoice.pdf | FINDING |
| A06 | Security headers | Required browser security headers are present | All required headers present | PASS |
| A01 | Authentication rate limiting | Repeated login attempts eventually receive HTTP 429 | Statuses: 200, 200, 429 | PASS |

## Validated findings

| ID | Severity | Finding | Status |
|---|---|---|---|
| PH4-F01 | Medium | Upload validation trusts the declared file type | Open |
| PH4-F02 | Medium | Uploaded files are not quarantined or malware-scanned | Open |
| PH4-F03 | Medium | Login rate limiting uses a shared global bucket | Open |
| PH4-F04 | Low | Content Security Policy permits inline styles | Open |
| PH4-F05 | Low | Application container root filesystem is writable | Open |
| PH4-F06 | Medium | Container runtime privileges are not explicitly reduced | Open |
| PH4-F07 | Medium | Container base images are referenced by mutable tags | Open |
| PH4-F08 | Medium | Upload request size is not limited before model binding | Open |

## Limitations

- The assessment did not target public systems or third-party services.
- Authentication accounts and ticket records are fictional.
- The passive ZAP baseline from Phase 3 remains separate from these manual/API checks.
- Finding severity is a portfolio risk estimate and should be recalibrated for a real production deployment.
