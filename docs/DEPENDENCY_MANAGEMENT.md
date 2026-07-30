# Dependency Management

## Locked restore

NuGet lock files are committed for the application and test projects. CI restores
with `--locked-mode`, so an unexpected transitive dependency change fails before
build or test execution.

## Pull-request controls

The dependency review workflow rejects newly introduced dependencies with known
high or critical vulnerabilities. It complements the repository dependency graph
and the command-line NuGet audit saved as a workflow artifact.

## Automated maintenance

Dependabot checks three ecosystems weekly:

- NuGet packages
- GitHub Actions
- Docker base images

Updates are raised as pull requests and must pass the same security gates as
developer-authored changes.
