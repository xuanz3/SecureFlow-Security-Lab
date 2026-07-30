# DAST Host Filtering Remediation

## Failure

The first OWASP ZAP baseline run reached the isolated Docker environment, but the
application returned HTTP 400 for requests using the Docker service hostname
`app`.

ZAP therefore scanned the framework-generated 400 response rather than the
SecureFlow application page. Because that response was created before the
application security-header middleware ran, ZAP reported the Content Security
Policy header as missing.

## Root cause

ASP.NET Core host filtering used the repository setting:

```json
"AllowedHosts": "localhost"
```

The ZAP container correctly targeted `http://app:8080` over the dedicated Compose
network. The internal hostname `app` was not in the allowlist.

## Remediation

The Docker Compose application environment now permits only the names required by
the project-owned local environment:

- `localhost`
- `127.0.0.1`
- `app`

The setting remains an explicit allowlist. It is not changed to the unrestricted
wildcard `*`.

## Validation

The remediation is accepted only when:

1. A request with `Host: app` returns HTTP 200.
2. The response contains the configured Content Security Policy.
3. The ZAP baseline job completes successfully.
4. All other pull-request security gates remain successful.
