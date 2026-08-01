# Phase 5 Finding Remediation Matrix

| Finding | Issue | Planned control | Automated evidence | Retest | Initial state |
|---|---:|---|---|---|---|
| PH4-F01 | #52 | File signature/content verification | upload regression test | controlled mismatched PDF upload | Open |
| PH4-F02 | #53 | Quarantine, scanner abstraction and release state | scanner/quarantine tests | clean and rejected harmless fixtures | Open |
| PH4-F03 | #54 | Partitioned login rate limit plus global backstop | independent-client limiter tests | separate fictional sessions | Open |
| PH4-F04 | #55 | CSP without `unsafe-inline` | header assertion | browser/header request | Open |
| PH4-F05 | #56 | Read-only root filesystem | Compose/runtime assertion | Docker inspect | Open |
| PH4-F06 | #57 | Drop all capabilities and disable privilege gain | Compose/runtime assertion | Docker inspect | Open |
| PH4-F07 | #58 | Digest-pinned .NET base images | Dockerfile policy test | reproducible Docker build | Open |
| PH4-F08 | #59 | Multipart and endpoint request-size limits | oversized-request test | controlled oversized request | Open |

Findings close only after the remediation PR is merged and the corresponding
retest result is committed.
