# Rules of Engagement

## Authorisation

The repository owner authorises testing only against local SecureFlow containers, generated test accounts and deliberately created insecure fixtures.

## Permitted targets

- `localhost` and loopback-bound SecureFlow services
- Docker Compose services created by this repository
- Generated application data and test accounts
- Terraform files stored in this repository
- Container images built from this repository

## Permitted activities

- Manual Web and API testing with Burp Suite Community
- OWASP ZAP baseline scanning
- Low-volume Nmap service discovery against local targets
- Trivy and Checkov static scanning
- Authentication, authorisation, upload and error-handling tests
- Controlled use of fake secrets and insecure fixtures in isolated branches

## Prohibited activities

- Testing public IP addresses, unrelated domains or third-party services
- Credential stuffing with real credentials
- Destructive deletion outside resettable test data
- Persistence, malware, ransomware or evasion payloads
- High-volume denial-of-service testing
- Collection or publication of personal data or real secrets

## Stop conditions

Testing stops immediately if:

- the target is not clearly project-owned;
- a test reaches a non-local service unexpectedly;
- real credentials or personal information appear;
- the workstation becomes unstable;
- the test cannot be safely reversed.

## Evidence handling

- Redact credentials, tokens and sensitive local paths.
- Store selected screenshots separately from the full archive.
- Hash final evidence files where practical.
- Record tool, version, time, target and limitations.
