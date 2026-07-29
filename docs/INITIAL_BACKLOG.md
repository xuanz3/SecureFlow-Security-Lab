# Initial GitHub Backlog

This backlog is designed for six milestones. Issue bodies should reference the relevant security requirement, required evidence and acceptance test.

## M1 — Security Design

1. Finalise project scope and safety boundary
2. Review local-first architecture and trust boundaries
3. Complete initial STRIDE threat model
4. Define security requirements and acceptance criteria
5. Approve Rules of Engagement and assessment plan

## M2 — Secure Application

6. Create ASP.NET Core solution and project structure
7. Add PostgreSQL, migrations and synthetic seed data
8. Implement authentication and secure session configuration
9. Implement administrator and standard-user roles
10. Implement ticket creation and ownership model
11. Enforce object-level ticket authorisation
12. Implement secure file-upload validation
13. Add structured security audit logging
14. Add health check and generic error handling
15. Add minimum authorisation and upload negative tests

## M3 — DevSecOps Pipeline

16. Add build and automated test workflow
17. Add CodeQL analysis
18. Add Gitleaks secret scanning
19. Add dependency vulnerability review and Dependabot
20. Add Trivy filesystem and container scanning
21. Generate SBOM for release artefacts
22. Add OWASP ZAP baseline workflow
23. Publish versioned container image to GHCR

## M4 — Security Assessment

24. Execute authorised Web and API manual test matrix
25. Create formal vulnerability register
26. Review Docker network exposure with Nmap
27. Add secure Azure Terraform reference configuration
28. Add controlled insecure IaC fixture and Checkov evidence

## M5 — Remediation and Detection

29. Remediate and retest object-level authorisation finding
30. Remediate and retest upload and authentication findings
31. Add five Sigma rules and five documented KQL examples
32. Complete one application security incident investigation

## M6 — Assurance and Release

33. Create asset, data-classification and risk registers
34. Complete NIST CSF 2.0 current/target profile
35. Complete scoped Essential Eight gap assessment and POA&M
36. Perform PostgreSQL backup and clean restore exercise
37. Validate application image rollback
38. Publish executive and technical security reports
39. Curate selected evidence and final README
40. Create v1.0 portfolio release and retrospective
