# Immutable Workflow Dependencies

All third-party GitHub Actions are pinned to complete commit SHAs.

| Dependency | Release | Commit / digest |
|---|---|---|
| actions/checkout | v6.0.2 | `de0fac2e4500dabe0009e67214ff5f5447ce83dd` |
| actions/setup-dotnet | v6.0.0 | `a98b56852c35b8e3190ac28c8c2271da59106c68` |
| actions/upload-artifact | v7.0.1 | `043fb46d1a93c77aae656e7c1c64a875d1fc6a0a` |
| actions/dependency-review-action | v5.0.0 | `a1d282b36b6f3519aa1f3fc636f609c47dddb294` |
| github/codeql-action | codeql-bundle-v2.26.2 | `18420e3271f74589575af831a523c833acda327f` |
| docker/setup-buildx-action | v4.2.0 | `bb05f3f5519dd87d3ba754cc423b652a5edd6d2c` |
| docker/build-push-action | v7.3.0 | `53b7df96c91f9c12dcc8a07bcb9ccacbed38856a` |
| docker/login-action | v4.6.0 | `dbcb813823bdd20940b903addbd779551569679f` |
| docker/metadata-action | v6.2.0 | `dc802804100637a589fabce1cb79ff13a1411302` |
| actions/attest | v4.2.1 | `508db95dd578ae2727ebd6217d5ba78e4fbda05d` |
| anchore/sbom-action | v0.24.0 | `e22c389904149dbc22b58101806040fa8d37a610` |
| aquasecurity/trivy-action | v0.36.0 | `ed142fd0673e97e23eac54620cfb913e5ce36c25` |
| ZAP stable image | registry digest | `ghcr.io/zaproxy/zaproxy@sha256:8d387b1a63e3425beef4846e39719f5af2a787753af2d8b6558c6257d7a577a2` |
| Gitleaks CLI | v8.30.1 | Release archive verified against official SHA-256 manifest |

## Trivy incident response

The workflow uses a post-incident, v-prefixed Trivy Action release and pins its
complete commit SHA. This avoids mutable tags and records the exact implementation
reviewed for this pipeline.

## Maintenance

Dependabot proposes Action updates. Each proposed SHA change must be reviewed and
pass the complete pipeline before merge.
