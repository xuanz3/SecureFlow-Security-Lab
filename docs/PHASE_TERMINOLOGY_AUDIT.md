# Phase Terminology Audit

SecureFlow uses sequential delivery phases for every project stage.

## Canonical sequence

| Phase | Scope |
|---|---|
| Phase 1 | Security design and repository governance |
| Phase 2 | Secure application foundation |
| Phase 3 | DevSecOps automation and supply-chain assurance |
| Phase 4 | Authorised security assessment |
| Phase 5 | Remediation and detection engineering |
| Phase 6 | Governance, recovery and final reporting |

## Audited mutable surfaces

- Tracked file and directory names
- README and Markdown documentation
- Evidence directories, indexes and screenshot identifiers
- Issues and issue bodies
- Pull-request titles and descriptions
- Labels and milestones
- Release titles and notes
- Repository description

## Naming standard

- Prose: `Phase N`
- Branches and labels: `phase-N`
- Evidence directories: `phaseN`
- Screenshot evidence: `PN-XX`

Historical commit objects and merged pull-request source refs are immutable audit
records and are not force-rewritten. Current repository content and editable
GitHub metadata use phase terminology only.
