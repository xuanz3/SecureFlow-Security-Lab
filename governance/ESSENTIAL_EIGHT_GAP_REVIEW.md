# Essential Eight Applicability and Gap Review

## Assessment boundary

This is an applicability and evidence review for a local Linux containerised web
application portfolio. It is not an ASD Essential Eight assessment, and no
Maturity Level One, Two or Three claim is made.

The official assessment process evaluates the implementation and effectiveness
of controls across an organisation. SecureFlow does not include a managed
Windows endpoint fleet, Microsoft Office environment, enterprise identity
provider or production operations team. Those boundaries materially limit what
can be assessed.

## Strategy review

| Essential Eight strategy | Applicability to SecureFlow | Evidence status | Gap or limitation | Action |
|---|---|---|---|---|
| Application control | Limited | Not assessed | Container allow-listing and endpoint application control are not implemented or claimed. | Evaluate image admission/signing policy in a real deployment. |
| Patch applications | Relevant | Partial | Dependabot-style updates, locked restore and dependency review demonstrate software maintenance, but no enterprise patch SLA or fleet coverage exists. | Define update SLA and evidence ageing in the final operating model. |
| Configure Microsoft Office macro settings | Outside runtime scope | Not applicable to this lab | The project has no Microsoft Office deployment or managed user endpoints. | Assess separately for any organisation using Office. |
| User application hardening | Partly relevant | Partial | CSP, security headers and upload controls harden the web application, but browser/Office endpoint configuration is not managed. | Add endpoint baseline evidence only in an enterprise implementation. |
| Restrict administrative privileges | Relevant | Partial | Admin RBAC, non-root containers, dropped capabilities and explicit workflow permissions are evidenced. PAM, JIT elevation and periodic access review are not. | Add federated identity, access review and privileged workflow controls before production. |
| Patch operating systems | Relevant | Partial | Digest-pinned .NET base images and Trivy scanning are evidenced. Host and endpoint OS patch operations are outside the project. | Define reviewed base-image refresh and host patch processes. |
| Multi-factor authentication | Relevant | Not implemented | Local ASP.NET Core Identity uses passwords and lockout only. | Add MFA or federation before production deployment. |
| Regular backups | Relevant | Demonstrated for the local exercise | Backup integrity, clean restore and measured recovery were verified locally; enterprise scheduling, encryption, off-site retention and organisational coverage remain outside scope. | Retain scheduled restore testing and add production retention controls before deployment. |

## Interpretation

The project provides useful evidence adjacent to several Essential Eight
strategies, especially restricted privileges, application patching and backup
planning. It does not establish organisational implementation effectiveness or
an Essential Eight maturity level.

## Version note

This review references the published Essential Eight Maturity Model dated
November 2023 and the associated ASD assessment guidance available on
2 August 2026. ASD announced consultation on the evolution of the Essential
Eight in June 2026; this review must be revisited after a replacement model is
published.
