# Phase 5 Remediation and Detection Plan

## Objective

Convert the Phase 4 assessment into traceable remediation, regression testing,
retesting, detection engineering and incident-investigation evidence.

## Delivery sequence

### PR 1 — Authorisation remediation

Scope:

- Issue #26: object-level authorisation
- Issue #27: administrator authorisation
- Retest the Phase 4 A02 and A03 failures

Required evidence:

- failing regression tests before the fix
- server-side owner and role enforcement
- passing negative tests after the fix
- retest record with HTTP result and correlation identifier

### PR 2 — Upload and authentication hardening

Scope:

- Finding #52 / PH4-F01: server-side file-signature validation
- Finding #53 / PH4-F02: quarantine and deterministic local scanning interface
- Finding #54 / PH4-F03: partitioned login throttling with a global backstop
- Finding #55 / PH4-F04: remove CSP `unsafe-inline`
- Finding #59 / PH4-F08: multipart and endpoint request-size limits
- Issue #28

The local scanner must use harmless test signatures only. Live malware is out
of scope.

### PR 3 — Container and workflow hardening

Scope:

- Finding #56 / PH4-F05: read-only application root filesystem
- Finding #57 / PH4-F06: drop Linux capabilities and prevent privilege gain
- Finding #58 / PH4-F07: pin application base images by verified digest
- Issue #29

The upload volume and required temporary paths remain explicitly writable.

### PR 4 — Detection engineering and investigation

Scope:

- five Sigma rules
- five equivalent KQL examples
- controlled suspicious access sequence
- one evidence-based incident report
- Issue #30

Detection themes:

1. repeated authentication failure or throttling
2. object-level authorisation denial
3. administrator-route denial
4. rejected or quarantined upload
5. suspicious sequence sharing a correlation or source context

### Final Phase 5 retest

Every Finding Issue must contain:

- remediation PR
- automated regression-test result
- manual or scripted retest result
- residual-risk statement
- closure reason

## Screenshot rule

Phase 5 does not add screenshots to the root README. Final project screenshots
are selected only after Phase 6 using the isolated Playwright evidence workflow.
