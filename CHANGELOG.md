# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-08-22

### Added
- **OpenAPI 3.x Parser**: JSON, YAML, and HTTPS URL loaders with recursive internal `$ref` pointer resolution.
- **Automated Test Generator**: Positive (happy path) & negative test generator (missing required fields, type mutation, enum boundaries).
- **Execution Engine**: Configurable HTTP client powered by `httpx` with timeout management, retry policy, concurrency support, and credential redaction.
- **Contract & Schema Validator**: JSON Schema Draft 2020-12 validation, response header verification, and status code assertions.
- **Multi-format Reporting**: Interactive standalone HTML report dashboard (Jinja2), JUnit XML (`junit.xml`), and raw JSON (`results.json`).
- **CLI Commands**: Rich terminal user interface for `validate`, `discover`, `generate`, and `run` commands.
- **CI/CD & Container**: GitHub Actions workflow template and rootless Docker container.
