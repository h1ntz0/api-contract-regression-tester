# API Contract & Regression Tester

```
┌──────────────────────────────────────┐
│  API Contract & Regression Tester    │
│                                      │
│  OpenAPI → Automated API Testing     │
│                                      │
│  [Demo] [Documentation] [PyPI]       │
└──────────────────────────────────────┘
```

[![CI](https://github.com/h1ntz0/api-contract-regression-tester/actions/workflows/api-regression.yml/badge.svg)](https://github.com/h1ntz0/api-contract-regression-tester)
[![Coverage](https://img.shields.io/badge/coverage-86%25-brightgreen)](https://github.com/h1ntz0/api-contract-regression-tester)
[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Release](https://img.shields.io/badge/release-v0.1.0-orange.svg)](https://github.com/h1ntz0/api-contract-regression-tester/releases)

An open-source API contract and regression testing engine that parses OpenAPI 3.x specifications (JSON, YAML, or Remote HTTPS URLs) into deterministic automated test executions with instant visual evidence and zero manual boilerplate.

---

## 🏗 Architecture & Workflow

```text
                 OpenAPI Specification
                  (JSON / YAML / URL)
                          │
                ┌─────────▼─────────┐
                │ Specification     │
                │ Parser & Loader   │
                └─────────┬─────────┘
                          │
                ┌─────────▼─────────┐
                │ Test Generator    │
                │ (Pos / Neg / Mut) │
                └─────────┬─────────┘
                          │
                ┌─────────▼─────────┐
                │ Test Execution    │
                │ Engine (HTTPX)    │
                └─────────┬─────────┘
                          │
                ┌─────────▼─────────┐
                │ Contract          │
                │ Validator         │
                └─────────┬─────────┘
                          │
                    ┌─────┴─────┐
                    │           │
                    ▼           ▼
                 CLI Output   HTML Dashboard
                    │           │
                    └─────┬─────┘
                          ▼
                     CI/CD Gate
```

---

## 🌟 Core Competencies & Highlights

- **OpenAPI is Source of Truth**: Eliminates repetitive test authoring. Automatically extracts paths, methods, request bodies, query/path parameters, and expected response contracts.
- **Autonomous Test Generation**:
  - **Positive Tests**: Valid payload generation respecting types, required properties, formats, and enums.
  - **Negative Tests**: Mutation testing for missing required properties, invalid datatypes, and invalid enum values.
- **Strict Contract Assertions**:
  - HTTP Status Code verification.
  - Required property completeness.
  - JSON Schema validation via Draft 2020-12.
  - Response header presence and datatype validation.
- **Enterprise Security by Design**:
  - Native credentials redaction (`Bearer ********`, `Basic ********`, `X-API-Key`).
  - Strict HTTPS enforcement for remote specifications.
  - Environment variable resolution for all sensitive keys.
- **Actionable Visual Evidence**: Standalone interactive HTML report with failure breakdown, request/response payload inspector, JSON export, and standard JUnit XML for CI/CD pipelines.

---

## 🚀 Quick Start

### 1. Installation

```bash
git clone https://github.com/h1ntz0/api-contract-regression-tester.git
cd api-contract-regression-tester
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### 2. Discover Endpoints
```bash
api-tester discover examples/openapi.yaml
```

### 3. Generate & Inspect Test Plan
```bash
api-tester generate examples/openapi.yaml --suite all
```

### 4. Run Automated Regression Test
```bash
api-tester run examples/openapi.yaml --base-url http://127.0.0.1:8000 --output ./reports
```

Open `./reports/index.html` in any browser to inspect the interactive test dashboard.

---

## ⚙️ Configuration (`config.yaml`)

```yaml
project:
  name: Enterprise API Test Suite

api:
  base_url: https://api.staging.example.com
  headers:
    X-Client-Version: "1.0.0"

execution:
  timeout_connect: 5
  timeout_read: 30
  workers: 4
  delay_ms: 0
  verify_tls: true

auth:
  type: bearer
  token_env: API_TOKEN

report:
  output_dir: ./reports
  generate_html: true
  generate_json: true
  generate_junit: true

testing:
  positive: true
  negative: true
  contract: true
  suites:
    - all
```

---

## 🐳 Docker Support

Run tests in an isolated rootless container:

```bash
docker build -t api-contract-regression-tester .

docker run --rm \
  -v $(pwd):/workspace \
  api-contract-regression-tester \
  run /workspace/examples/openapi.yaml --base-url http://host.docker.internal:8000 --output /workspace/reports
```

---

## 🔄 CI/CD Integration (GitHub Actions)

Add this workflow to `.github/workflows/api-regression.yml`:

```yaml
name: API Regression

on: [push, pull_request]

jobs:
  regression:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -e ".[dev]"
      - run: api-tester run examples/openapi.yaml --base-url https://api.staging.example.com
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: regression-report
          path: reports/
```

---

## 📊 Quality Gates & Test Suite

Run automated unit and integration tests:

```bash
pytest --cov=api_tester
```

- **Unit Tests**: Parser, Schema Validator, Status Validator, Header Validator, Data Generator, Security Redactor.
- **Integration Tests**: End-to-end execution against live mock API server.
- **Code Coverage**: $\ge 86\%$.

---

## 📜 License
Released under the [MIT License](LICENSE).
