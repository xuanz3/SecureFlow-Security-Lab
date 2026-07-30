# Secret Scanning

Gitleaks scans the complete Git history on pull requests, pushes to `main` and a
weekly schedule.

The workflow does not trust an unverified installer:

1. Downloads a fixed Gitleaks release.
2. Downloads the release checksum manifest.
3. Verifies the Linux archive with SHA-256.
4. Scans with redaction enabled.
5. Uploads a JSON result as workflow evidence.

Local `.env` files and .NET user-secrets remain outside Git. A clean scanner result
does not replace credential rotation after a confirmed exposure.
