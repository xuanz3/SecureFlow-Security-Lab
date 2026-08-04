# GitHub Repository Setup

## Repository

- Name: `SecureFlow-Security-Lab`
- Visibility: Public
- Description: `Local-first AppSec, DevSecOps, vulnerability management, detection, GRC and recovery project lab.`
- Do not initialise the remote with a README, licence or `.gitignore`; these already exist locally.

## Milestones

Create six milestones:

1. M1 — Security Design
2. M2 — Secure Application
3. M3 — DevSecOps Pipeline
4. M4 — Security Assessment
5. M5 — Remediation and Detection
6. M6 — Assurance and Release

## Project board columns

- Backlog
- Ready
- In Progress
- Review
- Done

## Recommended repository settings

After the first branch and workflow exist:

- Require a pull request before merging to `main`.
- Require status checks once the build workflow is stable.
- Disable force pushes and branch deletion for `main`.
- Enable Dependabot alerts and dependency graph.
- Enable private vulnerability reporting if available.
- Keep GitHub Actions workflow permissions read-only by default.

## Merge strategy

Use regular merge commits for milestone PRs so the visible commit history remains intact. Do not squash the whole phase into one commit.
