# Evidence Standard

## Principles

- Configuration, code, tests and written analysis are primary evidence.
- Screenshots support reproducible artefacts; they do not replace them.
- Evidence must show both successful controls and meaningful failure/remediation cases.
- No metric is reported without its test environment, sample, tool and limitation.

## Selected evidence naming

```text
E01_architecture_overview.png
E02_authorisation_negative_test.png
E03_security_pipeline_failure.png
E04_security_pipeline_pass.png
E05_manual_finding_evidence.png
E06_remediation_retest.png
E07_detection_and_timeline.png
E08_database_restore_validation.png
```

## Finding evidence chain

1. Finding ID and report entry
2. GitHub Issue
3. Reproduction or failing test
4. Remediation commits and pull request
5. CI result
6. Manual retest
7. Closed finding status

## Screenshot hygiene

- Capture only the relevant region.
- Hide tokens, cookies, local usernames and unnecessary browser tabs.
- Include a short caption and source path in `evidence/selected/README.md`.
- Keep troubleshooting screenshots in `evidence/archive/`.
