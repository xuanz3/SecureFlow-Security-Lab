# Phase 5 Authorisation Retest

## Conclusion

**PASS** — the existing server-side owner and administrator boundaries correctly deny unauthorised access.

Phase 4 reported final HTTP 200 responses because its browser-style client
followed the cookie-authentication redirect to the access-denied page.
The protected resource itself was not returned. This retest records both
the raw denial response and the final denial page.

## Results

| Test | Area | Raw result | Denial page verified | Result |
|---|---|---|---|---|
| P5-AUTH-01 | Owner access | HTTP 200 | Yes | PASS |
| P5-AUTH-02 | Object-level authorisation | HTTP 302 -> http://localhost:8080/Account/AccessDenied?ReturnUrl=%2FTickets%2FDetails%2F630a267f-f27a-4954-ab89-4bb6c87566a2 | Yes | PASS |
| P5-AUTH-03 | Administrator authorisation | HTTP 302 -> http://localhost:8080/Account/AccessDenied?ReturnUrl=%2FAdmin | Yes | PASS |
| P5-AUTH-04 | Administrator access | HTTP 200 | Yes | PASS |

## Regression coverage

- non-owner read denial
- non-owner modify denial
- owner access
- administrator override
- authenticated Tickets controller boundary
- Admin-role controller boundary

## Classification

- No object-level authorisation bypass was reproduced.
- No administrator-role bypass was reproduced.
- Phase 4 A02/A03 were test-methodology false positives caused by redirect following.
- No Phase 4 Finding Issue is closed by this retest because A02/A03 were not
  among Findings PH4-F01–PH4-F08.

## Safety

Testing used only local project-owned containers and fictional accounts.
No password, cookie or local secret is written to this report.
