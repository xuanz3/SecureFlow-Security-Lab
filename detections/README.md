# SecureFlow Detection Content

This directory contains portable detection content mapped to the structured
`SecurityAuditEvent` schema.

## Field mapping

| SecureFlow field | Microsoft Sentinel custom-log field |
|---|---|
| `EventType` | `EventType_s` |
| `Outcome` | `Outcome_s` |
| `UserId` | `UserId_s` |
| `ObjectType` | `ObjectType_s` |
| `ObjectId` | `ObjectId_s` |
| `CorrelationId` | `CorrelationId_s` |
| `SourceAddress` | `SourceAddress_s` |
| `OccurredAtUtc` | `OccurredAtUtc_t` |

The KQL examples use `SecureFlowAuditEvents_CL` as the illustrative custom-log
table. A production workspace may use a different table name.

## Detection set

| ID | Sigma | KQL | Purpose |
|---|---|---|---|
| D1 | `login_failure_burst.yml` | `login_failure_burst.kql` | Repeated login failures |
| D2 | `account_lockout.yml` | `account_lockout.kql` | Account lockout |
| D3 | `ticket_access_denied.yml` | `ticket_access_denied.kql` | Object-level denial |
| D4 | `upload_security_rejection.yml` | `upload_security_rejection.kql` | Upload/quarantine rejection |
| D5 | `multi_control_denial_sequence.yml` | `multi_control_denial_sequence.kql` | Multi-control suspicious sequence |

## Validation

`security-assessment/tools/validate_detection_content.py` verifies the content
count, required Sigma metadata, unique rule identifiers, KQL structure and the
controlled incident fixture.

The controlled incident report is stored at
`incident-response/IR-P5-001-CONTROLLED-SUSPICIOUS-SEQUENCE.md`.
