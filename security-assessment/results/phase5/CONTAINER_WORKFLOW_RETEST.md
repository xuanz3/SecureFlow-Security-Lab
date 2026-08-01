# Phase 5 Container and Workflow Retest

## Result

**PASS** — container runtime and workflow permissions were hardened and
validated against the Phase 4 findings.

## Container controls

| Control | Result |
|---|---|
| Non-root configured user | `appuser` |
| Read-only root filesystem | `True` |
| Dropped capabilities | `['ALL']` |
| Security options | `['no-new-privileges:true']` |
| Writable temporary mount | `['/tmp']` |
| Base images | Both .NET stages pinned to verified SHA-256 digests |

Only `/tmp`, uploads, quarantine and Data Protection keys remain writable.

## Workflow controls

- Workflows validated: **9**
- Policy result: **PASS**
- Every workflow declares top-level permissions.
- `write-all` and `read-all` are forbidden.
- Third-party Actions require full 40-character commit SHAs.
- Checkout credentials must not persist.

A dedicated `Workflow Policy` GitHub Action now enforces these conditions
for future pull requests.

## Runtime tests

```text
PASS: application process uses non-root UID 100
PASS: application root filesystem is read-only
PASS: all Linux capabilities are dropped
PASS: no-new-privileges is enabled
PASS: write to the application root was denied
PASS: required writable path works: /tmp/.phase5-write-test
PASS: required writable path works: /app/App_Data/uploads/.phase5-write-test
PASS: required writable path works: /app/App_Data/quarantine/.phase5-write-test
PASS: required writable path works: /home/appuser/.aspnet/DataProtection-Keys/.phase5-write-test
PASS: readiness endpoint remained HTTP 200
```

## Remediated findings

- PH4-F05 / #56 — application root filesystem is read-only.
- PH4-F06 / #57 — all capabilities are dropped and privilege gain is disabled.
- PH4-F07 / #58 — .NET SDK and runtime images are digest-pinned.
- Parent Issue #29 — runtime and workflow least-privilege policy is enforced.

## Residual risk

The local PostgreSQL development image remains version-tagged because the
validated finding concerned the application build stages. Production
deployment should also pin database images through a reviewed update process.

No environment variables or credentials are present in the committed Docker
runtime evidence.
