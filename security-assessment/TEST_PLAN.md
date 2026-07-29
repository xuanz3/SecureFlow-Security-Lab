# Security Assessment Test Plan

## Test objectives

1. Validate authentication and session controls.
2. Validate role and object-level authorisation.
3. Validate file-upload protections.
4. Inspect error handling and security headers.
5. Inspect Docker network and runtime privileges.
6. Validate CI/CD and dependency security controls.
7. Review Terraform reference configuration.
8. Produce findings that can be remediated and retested.

## Test matrix

| Test ID | Area | Method | Expected evidence |
|---|---|---|---|
| A01 | Authentication | Manual and integration test | Rate limit and generic failure response |
| A02 | Object authorisation | Identifier substitution | Denial plus audit event |
| A03 | Role authorisation | Standard user requests admin route | 403/denial plus regression test |
| A04 | Upload | Invalid type, large size, crafted name | Rejection and safe storage behaviour |
| A05 | Error handling | Invalid identifiers and malformed input | No stack or database disclosure |
| A06 | Security headers | ZAP/manual response review | Documented header baseline |
| A07 | Container | Trivy and Dockerfile review | Non-root and reduced findings |
| A08 | Network | Nmap and Compose inspection | Only required app port externally bound |
| A09 | Secrets | Gitleaks controlled fixture | Pipeline failure then clean retest |
| A10 | IaC | Checkov against secure/insecure examples | Failing fixture and passing reference |

## Finding quality standard

Every accepted finding must include affected asset, evidence, reproduction, technical cause, business impact, CWE/OWASP mapping, severity rationale, recommendation, linked Issue, linked remediation PR and retest status.
