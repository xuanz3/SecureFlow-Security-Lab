# Project Scope

## Purpose

SecureFlow is a self-directed enterprise security engineering and assurance lab. It is designed to demonstrate a complete security lifecycle around a deliberately small business application rather than maximise infrastructure size or tool count.

## Business scenario

The reference application models a small internal ticket-management service. Standard users create and view their own tickets. Administrators review all tickets, manage selected security-sensitive actions and inspect audit records.

## In scope

- Local ASP.NET Core application and PostgreSQL database
- Authentication, role-based access control and object-level authorisation
- File upload, audit logging, validation, security headers and rate limiting
- Docker packaging and local network exposure
- GitHub Actions build, test and security gates
- SAST, dependency, secret, container, IaC and DAST scanning
- Authorised Web/API assessment using local project targets
- Vulnerability triage, remediation, regression testing and retesting
- Application security logging, Sigma rules and KQL examples
- Risk register, control mapping and recovery exercises

## Out of scope

- Testing public or third-party targets
- Real customer, employer or university data
- Production credentials, payment information or personal records
- Destructive exploitation, persistence or denial-of-service testing
- Production Azure deployment
- Commercial scanners, SIEM, EDR or identity platforms
- Claims of formal compliance or certification

## Constraints

- No additional Azure virtual machines
- Local-first execution on a personal Mac
- Free and open-source tools wherever possible
- One six-day implementation cycle
- Documentation and evidence must be reproducible and safe to publish

## Success definition

The project is complete when a reviewer can trace selected security issues through:

**Finding → GitHub Issue → failing test or evidence → remediation PR → automated validation → manual retest → closure**
