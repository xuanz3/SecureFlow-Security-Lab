# IR-P5-001 — Controlled Suspicious Access Sequence

- Classification: **Controlled security exercise**
- Severity: **Medium (simulated)**
- Environment: **Project-owned localhost Docker containers**
- Accounts: **Fictional local identities only**
- Impact: **No unauthorised access and no released malicious content**

## Executive summary

A controlled sequence reproduced credential guessing, account lockout, cross-user ticket access and a spoofed PDF upload. SecureFlow denied each protected action and recorded structured audit evidence. All five Phase 5 detections triggered against the sanitised event set.

## Timeline

| UTC | Event type | Outcome | User | Object type | Object ID |
|---|---|---|---|---|---|
| 2026-08-01T14:42:21.726067+00:00 | Login | Success | fictional-bob | — | — |
| 2026-08-01T14:42:21.862595+00:00 | TicketCreated | Success | fictional-bob | Ticket | 04a0198e-b088-4935-b06f-99f74d39ae52 |
| 2026-08-01T14:42:21.968314+00:00 | Login | Success | fictional-alice | — | — |
| 2026-08-01T14:42:21.982762+00:00 | TicketCreated | Success | fictional-alice | Ticket | 7195256c-9910-449d-a5f3-74c665e41072 |
| 2026-08-01T14:42:21.993025+00:00 | TicketAccess | Denied | fictional-alice | Ticket | 04a0198e-b088-4935-b06f-99f74d39ae52 |
| 2026-08-01T14:42:22.022275+00:00 | AttachmentScan | Rejected | fictional-alice | Ticket | 7195256c-9910-449d-a5f3-74c665e41072 |
| 2026-08-01T14:42:22.114002+00:00 | Login | Failure | fictional-alice | — | — |
| 2026-08-01T14:42:22.187+00:00 | Login | Failure | fictional-alice | — | — |
| 2026-08-01T14:42:22.266291+00:00 | Login | Failure | fictional-alice | — | — |
| 2026-08-01T14:42:24.96719+00:00 | Login | Failure | fictional-alice | — | — |
| 2026-08-01T14:42:25.092013+00:00 | Login | LockedOut | fictional-alice | — | — |

## Detection results

| Detection | Result | Matched event IDs |
|---|---|---|
| D1 | Triggered | 53, 54, 55, 56 |
| D2 | Triggered | 57 |
| D3 | Triggered | 51 |
| D4 | Triggered | 52 |
| D5 | Triggered | 51, 52, 53, 54, 55, 56, 57 |

## Investigation

- The ticket ownership boundary denied access before protected content.
- The quarantine scanner rejected the spoofed PDF before release.
- Identity lockout activated after the configured threshold.
- The application remained healthy throughout the exercise.
- No credentials, cookies or raw source addresses were committed.

## Containment and recovery

No production containment was necessary. The script reset the fictional Alice lockout state after evidence extraction.

## Disposition

The events were deliberately generated to validate monitoring coverage. Security controls operated as designed, and the exercise is closed with no residual incident impact.

## Evidence integrity

- Sanitised audit events: **11**
- Source addresses: replaced with `local-test-source`
- Identity IDs: mapped to fictional labels
- Credentials and cookies: never written
