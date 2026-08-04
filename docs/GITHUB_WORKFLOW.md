# GitHub Delivery Workflow

SecureFlow uses an issue-driven workflow so that design, implementation, assessment and remediation remain traceable.

## Work sequence

1. Define an Issue with objective, acceptance criteria and evidence requirements.
2. Create a focused branch from `main`.
3. Make small commits using conventional prefixes such as `feat`, `test`, `security`, `fix`, `ci`, `docs` and `chore`.
4. Open a Pull Request that explains the change, risk, tests and remaining limitations.
5. Confirm automated checks and manual evidence before merging.
6. Close the linked Issue and update the relevant finding or report.
7. Create a release at major project milestones.

## Branch naming

- `feature/<capability>`
- `test/<control>`
- `security/<assessment>`
- `fix/<finding>`
- `ci/<workflow>`
- `docs/<artefact>`

## Pull Request minimum content

- Purpose and scope
- Security impact
- Files and behaviours changed
- Automated validation
- Manual validation
- Evidence location
- Remaining risk or limitation
- Linked Issue using `Closes #<number>`

Direct feature development on `main` is avoided. Controlled insecure fixtures remain isolated and are never merged into the normal runtime path.
