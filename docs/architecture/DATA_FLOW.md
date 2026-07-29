# Data Flow

## Primary user flow

```mermaid
sequenceDiagram
    participant U as User
    participant A as ASP.NET Core App
    participant D as PostgreSQL
    participant L as Audit Log

    U->>A: Submit login credentials
    A->>D: Validate account and retrieve roles
    D-->>A: Identity and role data
    A-->>U: Authenticated session cookie
    U->>A: Request ticket resource
    A->>A: Verify role and ticket ownership
    A->>D: Query authorised ticket
    D-->>A: Ticket data
    A->>L: Record access event and outcome
    A-->>U: Authorised response or denial
```

## Sensitive data classes

| Data | Classification | Required handling |
|---|---|---|
| Password hash | Restricted | Never logged or exported |
| Authentication cookie | Restricted | HttpOnly, Secure assumption, SameSite |
| Ticket content | Internal | Object-level authorisation |
| Uploaded file | Internal | Type, size and storage validation |
| Audit record | Internal security | Integrity, timestamp and correlation ID |
| Test accounts | Synthetic | Clearly identified as non-production |

## Logging rules

Security logs may record user identifiers, action names, resource identifiers, outcome, source address and correlation ID. They must not record passwords, raw session cookies, access tokens or full uploaded-file contents.
