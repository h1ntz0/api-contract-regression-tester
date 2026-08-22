# prd project  
  
```
# PRD — API Contract & Regression Tester

## 1. Product Overview

**API Contract & Regression Tester** adalah open-source API testing platform untuk membantu QA Engineer, QA Automation Engineer, Developer, dan DevOps melakukan automated API contract testing dan regression testing berdasarkan OpenAPI/Swagger specification.

User cukup memberikan OpenAPI specification dalam bentuk:

- Local JSON file
- Local YAML file
- Remote OpenAPI URL

Sistem kemudian akan:

```text
OpenAPI Specification
        ↓
Specification Parser
        ↓
Endpoint Discovery
        ↓
Test Case Generator
        ↓
API Test Runner
        ↓
Contract Validator
        ↓
Regression Engine
        ↓
Test Result
        ↓
HTML Report

```
Tujuan utama project adalah membuat API regression testing menjadi mudah, reproducible, automation-friendly, dan dapat digunakan oleh orang lain tanpa konfigurasi yang kompleks.  
   
⸻  
   
## 2. Problem Statement  
API testing sering dilakukan secara manual menggunakan Postman atau tool sejenis.  
Masalah yang sering muncul:  
1. Test case harus dibuat satu per satu.  
2. Regression testing membutuhkan maintenance.  
3. Perubahan API contract dapat menyebabkan regression yang tidak terdeteksi.  
4. Response schema tidak selalu divalidasi.  
5. Negative testing sering terlewat.  
6. Test evidence tidak selalu terdokumentasi dengan baik.  
7. API automation membutuhkan coding effort.  
8. Automated test belum tentu terintegrasi dengan CI/CD.  
9. Dokumentasi API dan automated test dapat menjadi tidak sinkron.  
Project ini bertujuan mengurangi pekerjaan repetitif tersebut dengan menjadikan OpenAPI specification sebagai sumber utama untuk menghasilkan automated test.  
   
⸻  
   
## 3. Product Goals  
## Primary Goal  
Membangun CLI/API testing engine yang mampu membaca OpenAPI specification dan secara otomatis melakukan:  
* Contract testing  
* Regression testing  
* Positive testing  
* Negative testing  
* Response validation  
* Schema validation  
* Test reporting  
## Secondary Goals  
* Mudah digunakan oleh QA  
* Mudah dijalankan oleh developer  
* Mendukung CI/CD  
* Mendukung Docker  
* Menghasilkan HTML report  
* Reproducible test execution  
* Open-source friendly  
* Mudah dikembangkan oleh contributor  
   
⸻  
   
## 4. Target Users  
## 4.1 QA Engineer  
Untuk menjalankan automated API regression testing tanpa membuat seluruh test secara manual.  
## 4.2 QA Automation Engineer  
Untuk membuat dan maintain API automation framework.  
## 4.3 Backend Developer  
Untuk memastikan implementasi API tetap sesuai dengan OpenAPI contract.  
## 4.4 DevOps Engineer  
Untuk menjalankan API regression testing sebagai bagian dari CI/CD pipeline.  
## 4.5 Open Source Contributor  
Untuk mempelajari API automation, contract testing, software architecture, dan testing framework development.  
   
⸻  
   
## 5. Product Scope  
## 5.1 MVP Scope  
MVP wajib mendukung:  
* OpenAPI 3.x  
* JSON specification  
* YAML specification  
* Local specification file  
* Remote specification URL  
* Endpoint discovery  
* HTTP request execution  
* Automatic test generation  
* Positive testing  
* Basic negative testing  
* HTTP status validation  
* Response schema validation  
* Required field validation  
* Data type validation  
* Enum validation  
* Request validation  
* Response header validation  
* Authentication configuration  
* HTML report  
* CLI interface  
* Exit code untuk CI/CD  
* Docker  
* GitHub Actions example  
   
⸻  
   
## 6. Out of Scope — MVP  
Fitur berikut tidak termasuk MVP:  
* AI-generated test cases  
* GUI test recorder  
* Load testing  
* Stress testing  
* Distributed testing  
* API mocking  
* Full Postman replacement  
* Multi-user account  
* SaaS platform  
* Cloud test execution  
* Complex custom scripting language  
* Test marketplace  
Fitur tersebut hanya dapat dipertimbangkan setelah core testing engine stabil.  
   
⸻  
   
## 7. Product Philosophy  
Project harus mengikuti:  
* Clean Architecture  
* SOLID  
* DRY  
* KISS  
* YAGNI  
* Separation of Concerns  
* Dependency Inversion  
* Reusable Components  
* Configuration over Hardcoding  
* Fail Fast  
* Deterministic Testing  
* Security by Design  
Project tidak boleh dibuat hanya untuk terlihat kompleks.  
Prioritas utama:  
```
Correctness
    ↓
Reliability
    ↓
Maintainability
    ↓
Developer Experience
    ↓
Performance
    ↓
Additional Features

```
   
⸻  
   
## 8. Recommended Technology Stack  
## Core Language  
**Python 3.12+**  
Alasan:  
* kuat untuk automation  
* ecosystem testing sangat matang  
* mudah dikontribusikan  
* cocok untuk CLI  
* mudah digunakan QA Engineer  
* cocok untuk API testing  
## HTTP Client  
Recommended:  
```
httpx

```
## Schema Validation  
Recommended:  
```
jsonschema

```
## OpenAPI Parser  
Recommended:  
```
prance

```
atau library OpenAPI parser yang stabil dan aktif.  
Pemilihan final harus dilakukan pada tahap technical spike.  
## CLI  
Recommended:  
```
Typer

```
## Test Engine  
Recommended:  
```
pytest

```
## HTML Reporting  
Bisa menggunakan:  
```
Jinja2

```
untuk custom report.  
Alternatif:  
```
pytest-html

```
Technical decision harus dilakukan sebelum implementation.  
## Configuration  
Recommended:  
```
YAML

```
atau:  
```
TOML

```
   
⸻  
   
## 9. High-Level Architecture  
```
┌───────────────────────────────┐
│             CLI               │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│       Configuration Layer      │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│      Specification Loader      │
│                               │
│ JSON / YAML / Remote URL      │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│       OpenAPI Parser           │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│      Internal API Model        │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│       Test Generator           │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│        Test Runner             │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│      Contract Validator        │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│       Result Aggregator        │
└───────────────┬───────────────┘
                │
          ┌─────┴─────┐
          ▼           ▼
      CLI Output   HTML Report

```
   
⸻  
   
## 10. Project Structure  
Recommended initial structure:  
```
api-contract-regression-tester/
│
├── src/
│   └── api_tester/
│       │
│       ├── cli/
│       │   ├── commands.py
│       │   └── output.py
│       │
│       ├── config/
│       │   ├── models.py
│       │   └── loader.py
│       │
│       ├── specification/
│       │   ├── loader.py
│       │   ├── parser.py
│       │   └── models.py
│       │
│       ├── generator/
│       │   ├── generator.py
│       │   ├── positive.py
│       │   └── negative.py
│       │
│       ├── execution/
│       │   ├── client.py
│       │   ├── runner.py
│       │   └── request_builder.py
│       │
│       ├── validation/
│       │   ├── status_code.py
│       │   ├── schema.py
│       │   ├── headers.py
│       │   └── response.py
│       │
│       ├── reporting/
│       │   ├── models.py
│       │   ├── aggregator.py
│       │   └── html.py
│       │
│       └── core/
│           ├── exceptions.py
│           └── constants.py
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
│
├── examples/
│   ├── openapi.yaml
│   └── config.yaml
│
├── templates/
│   └── report.html
│
├── docs/
│   ├── architecture.md
│   ├── configuration.md
│   └── testing.md
│
├── .github/
│   └── workflows/
│       └── api-regression.yml
│
├── Dockerfile
├── pyproject.toml
├── README.md
├── LICENSE
└── .gitignore

```
   
⸻  
   
## 11. Core Components  
## 11.1 CLI  
CLI merupakan entry point utama.  
Contoh:  
```
api-tester --help

```
Commands:  
```
api-tester validate
api-tester discover
api-tester generate
api-tester run
api-tester report

```
   
⸻  
   
## 12. CLI — Validate  
Command:  
```
api-tester validate openapi.yaml

```
Tujuan:  
Memastikan specification valid sebelum test dijalankan.  
Output:  
```
OpenAPI Validation

✓ Specification loaded
✓ OpenAPI version detected
✓ Paths detected
✓ Schemas detected

Specification is valid.

```
Jika invalid:  
```
Specification validation failed.

Error:
Missing required field: info.title

```
Exit code:  
```
1

```
   
⸻  
   
## 13. CLI — Discover  
Command:  
```
api-tester discover openapi.yaml

```
Output:  
```
API Endpoints

GET     /users
POST    /users
GET     /users/{id}
PUT     /users/{id}
DELETE  /users/{id}

Total endpoints: 5

```
Filter:  
```
api-tester discover openapi.yaml --method GET

```
   
⸻  
   
## 14. CLI — Generate  
Command:  
```
api-tester generate openapi.yaml

```
System menghasilkan test plan.  
Contoh:  
```
Generated Test Cases

GET /users
 ├── Valid Request
 └── Invalid Query Parameter

POST /users
 ├── Valid Request
 ├── Missing Required Field
 ├── Invalid Data Type
 └── Invalid Enum

Total:
18 test cases

```
MVP tidak wajib menghasilkan source code test.  
Test case dapat disimpan sebagai internal execution plan.  
   
⸻  
   
## 15. CLI — Run  
Command utama:  
```
api-tester run openapi.yaml

```
Contoh output:  
```
API Contract & Regression Tester

Specification : openapi.yaml
Base URL      : https://api.example.com

Running tests...

✓ GET    /users
✓ GET    /users/{id}
✓ POST   /users
✓ PUT    /users/{id}
✗ DELETE /users/{id}

──────────────────────────────

Total   : 42
Passed  : 39
Failed  : 3
Skipped : 0

Pass Rate: 92.85%

Report:
reports/index.html

```
   
⸻  
   
## 16. FR-001 — Specification Input  
System harus menerima:  
```
Local JSON
Local YAML
Remote JSON URL
Remote YAML URL

```
Contoh:  
```
api-tester run ./openapi.yaml

```
atau:  
```
api-tester run https://example.com/openapi.json

```
Security requirement:  
Remote URL harus menggunakan:  
```
HTTPS

```
secara default.  
HTTP hanya dapat digunakan dengan explicit configuration.  
   
⸻  
   
## 17. FR-002 — Specification Parser  
Parser harus membaca:  
```
OpenAPI version
API metadata
servers
paths
methods
parameters
requestBody
responses
schemas
required
enum
format
security
tags

```
Internal representation:  
```
ApiSpecification
    ├── metadata
    ├── servers
    └── endpoints

Endpoint
    ├── method
    ├── path
    ├── parameters
    ├── request_schema
    ├── response_schema
    ├── expected_status
    └── security

```
   
⸻  
   
## 18. FR-003 — Endpoint Discovery  
System harus menemukan semua endpoint.  
Contoh:  
```
GET     /users
POST    /users
GET     /users/{id}
PUT     /users/{id}
DELETE  /users/{id}

```
Endpoint harus memiliki unique identifier.  
Contoh:  
```
GET:/users
POST:/users
GET:/users/{id}

```
   
⸻  
   
## 19. FR-004 — Automatic Test Generation  
Test generator harus membuat test berdasarkan:  
* HTTP method  
* parameters  
* request schema  
* response schema  
* required fields  
* enum  
* expected status code  
Contoh:  
```
POST /users

```
Generated:  
```
POST /users — Valid Request

POST /users — Missing Required Field

POST /users — Invalid Data Type

POST /users — Invalid Enum

```
   
⸻  
   
## 20. FR-005 — Test Data Generation  
System harus mampu menghasilkan basic test data berdasarkan OpenAPI schema.  
Contoh:  
```
username:
  type: string

age:
  type: integer

active:
  type: boolean

```
Generated:  
```
{
  "username": "test-user",
  "age": 25,
  "active": true
}

```
Untuk:  
```
role:
  type: string
  enum:
    - admin
    - user

```
System harus menggunakan salah satu valid enum value.  
   
⸻  
   
## 21. FR-006 — Positive Testing  
Positive test harus menggunakan data yang memenuhi contract.  
Validasi:  
```
Status Code
Response Schema
Required Fields
Data Types
Enum
Headers

```
   
⸻  
   
## 22. FR-007 — Negative Testing  
Negative testing menggunakan input invalid.  
Contoh:  
```
Missing required parameter
Invalid data type
Invalid enum
Invalid format
Empty value
Malformed request

```
Expected behavior biasanya berupa:  
```
400
401
403
404
422

```
Namun expected status harus mengikuti specification apabila contract mendefinisikannya.  
System tidak boleh mengasumsikan semua API menggunakan status code yang sama.  
   
⸻  
   
## 23. FR-008 — Status Code Validation  
Expected:  
```
200

```
Actual:  
```
500

```
Result:  
```
FAIL

Expected Status: 200
Actual Status:   500

```
   
⸻  
   
## 24. FR-009 — Schema Validation  
System harus memvalidasi response terhadap schema.  
Contoh:  
```
{
  "id": 1,
  "name": "John"
}

```
Contract:  
```
id:
  type: integer

name:
  type: string

```
Jika response:  
```
{
  "id": "abc",
  "name": "John"
}

```
Result:  
```
FAIL

Field: id
Expected: integer
Actual: string

```
   
⸻  
   
## 25. FR-010 — Required Field Validation  
Jika contract mendefinisikan:  
```
required:
  - id
  - name

```
Response:  
```
{
  "id": 1
}

```
Result:  
```
FAIL

Missing required field:
name

```
   
⸻  
   
## 26. FR-011 — Enum Validation  
Contract:  
```
status:
  type: string
  enum:
    - active
    - inactive

```
Response:  
```
{
  "status": "deleted"
}

```
Result:  
```
FAIL

Invalid enum value:
deleted

Allowed:
active
inactive

```
   
⸻  
   
## 27. FR-012 — Authentication  
MVP harus memiliki configurable authentication.  
Minimal:  
```
Bearer Token
API Key
Basic Authentication

```
Configuration example:  
```
auth:
  type: bearer
  token_env: API_TOKEN

```
Token harus diambil dari environment variable.  
Tidak boleh menyimpan secret langsung di repository.  
   
⸻  
   
## 28. FR-013 — Environment Configuration  
System harus mendukung environment.  
Contoh:  
```
config/
 ├── dev.yaml
 ├── staging.yaml
 └── production.yaml

```
Example:  
```
base_url: https://api.example.com

timeout:
  connect: 5
  read: 30

```
CLI:  
```
api-tester run openapi.yaml --config config/staging.yaml

```
   
⸻  
   
## 29. FR-014 — Request Timeout  
Setiap request wajib memiliki timeout.  
Default:  
```
Connect timeout: 5 seconds
Read timeout: 30 seconds

```
Timeout harus configurable.  
System tidak boleh memiliki HTTP request tanpa timeout.  
   
⸻  
   
## 30. FR-015 — Retry Policy  
MVP default:  
```
Retry: disabled

```
Retry hanya dapat diaktifkan secara explicit.  
Alasan:  
Regression test tidak boleh menyembunyikan intermittent failure.  
Jika retry digunakan:  
```
retry:
  enabled: true
  max_attempts: 2

```
Report harus tetap menunjukkan bahwa retry terjadi.  
   
⸻  
   
## 31. FR-016 — Test Result  
Setiap test harus memiliki:  
```
Test ID
Endpoint
HTTP Method
Request
Expected Result
Actual Result
Duration
Status
Failure Reason

```
Status:  
```
PASSED
FAILED
SKIPPED
ERROR

```
   
⸻  
   
## 32. FR-017 — HTML Report  
Report harus menyediakan:  
```
Test Summary
Pass Rate
Failed Tests
Skipped Tests
Endpoint Breakdown
HTTP Method Breakdown
Response Time
Contract Violations
Failure Details

```
Contoh:  
```
API Regression Report

Total Tests      120
Passed           112
Failed             6
Skipped            2

Pass Rate       93.33%
Duration        24.7 seconds

```
   
⸻  
   
## 33. Report — Test Detail  
Contoh:  
```
TC-042

POST /users

Status:
FAILED

Expected:
201

Actual:
500

Duration:
842 ms

Contract:
PASS

Response:
{
  "error": "Internal Server Error"
}

```
   
⸻  
   
## 34. Report — Contract Violation  
Contoh:  
```
Contract Violation

Endpoint:
GET /users/{id}

Field:
id

Expected:
integer

Actual:
string

Severity:
HIGH

```
   
⸻  
   
## 35. Regression Test Classification  
Setiap test dapat memiliki:  
```
Smoke
Regression
Contract
Negative

```
Contoh:  
```
api-tester run openapi.yaml --suite smoke

```
atau:  
```
api-tester run openapi.yaml --suite regression

```
MVP dapat memulai dengan:  
```
all

```
Kemudian suite system ditambahkan secara bertahap.  
   
⸻  
   
## 36. Exit Code  
CLI harus memiliki deterministic exit code.  
```
0 = All tests passed

1 = One or more tests failed

2 = Configuration error

3 = Specification error

4 = Execution error

```
Hal ini penting untuk CI/CD.  
   
⸻  
   
## 37. CI/CD Integration  
Project harus menyediakan contoh GitHub Actions.  
Flow:  
```
Push
 ↓
GitHub Actions
 ↓
Install
 ↓
Load OpenAPI
 ↓
Run Regression
 ↓
Generate Report
 ↓
Upload Artifact
 ↓
Pass / Fail

```
Example:  
```
name: API Regression

on:
  push:
  pull_request:

jobs:
  api-test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Install API Tester
        run: pip install api-contract-regression-tester

      - name: Run API Regression
        run: api-tester run examples/openapi.yaml

      - name: Upload Report
        uses: actions/upload-artifact@v4
        with:
          name: api-test-report
          path: reports/

```
Versi final workflow harus mengikuti package name dan CLI final implementation.  
   
⸻  
   
## 38. Docker Support  
Project harus menyediakan Docker image.  
Example:  
```
docker run \
  -v $(pwd):/workspace \
  api-contract-regression-tester \
  run /workspace/openapi.yaml

```
Docker image harus:  
* lightweight  
* non-root  
* deterministic  
* configurable  
* memiliki health/basic execution check jika diperlukan  
   
⸻  
   
## 39. Security Requirements  
Security harus menjadi bagian dari design.  
## Secrets  
Tidak boleh:  
```
token: my-secret-token

```
Recommended:  
```
token_env: API_TOKEN

```
Kemudian:  
```
export API_TOKEN="..."

```
## Logging  
Token/password/API key tidak boleh muncul dalam log.  
Contoh:  
```
Authorization: Bearer ********

```
bukan:  
```
Authorization: Bearer eyJhbGci...

```
## Remote Specification  
Remote URL harus divalidasi.  
System harus mempertimbangkan SSRF protection terutama jika tool nantinya digunakan sebagai service.  
## TLS  
TLS certificate verification aktif secara default.  
Disable verification hanya melalui explicit configuration.  
   
⸻  
   
## 40. Performance Requirements  
MVP harus mampu menjalankan minimal:  
```
100 endpoints

```
dengan reasonable execution time.  
System harus mendukung controlled concurrency.  
Example:  
```
execution:
  workers: 5

```
Default:  
```
workers: 1

```
Concurrency tidak boleh menyebabkan server overload secara tidak sengaja.  
   
⸻  
   
## 41. Observability  
CLI harus memberikan informasi execution yang cukup:  
```
Current endpoint
Test progress
Passed
Failed
Skipped
Duration

```
Contoh:  
```
Running API Tests...

[████████████████░░░░] 80%

96 / 120 tests

Passed : 91
Failed : 4
Skipped: 1

```
   
⸻  
   
## 42. Error Handling  
Error harus dikategorikan.  
## Specification Error  
```
Invalid OpenAPI document

```
## Configuration Error  
```
Missing base_url

```
## Network Error  
```
Connection refused

```
## Timeout  
```
Request timeout after 30 seconds

```
## Contract Error  
```
Response schema mismatch

```
## Assertion Failure  
```
Expected status 200 but received 500

```
Error harus actionable.  
Jangan hanya:  
```
Something went wrong.

```
   
⸻  
   
## 43. Database Impact  
## MVP  
Tidak menggunakan database.  
Semua execution result dapat disimpan sebagai:  
```
JSON
HTML
JUnit XML

```
Contoh:  
```
reports/
├── index.html
├── results.json
└── junit.xml

```
Database baru dipertimbangkan jika project berubah menjadi centralized dashboard.  
   
⸻  
   
## 44. API Design  
MVP tidak membutuhkan backend API.  
Architecture:  
```
CLI
 ↓
Application Core
 ↓
HTTP Client

```
Jika future version membutuhkan web dashboard:  
```
Frontend
    ↓
Backend API
    ↓
Testing Engine
    ↓
Storage

```
Tetapi backend tidak boleh dibuat sebelum memang dibutuhkan.  
   
⸻  
   
## 45. Configuration Example  
```
project:
  name: Example API

api:
  base_url: https://api.example.com

execution:
  timeout: 30
  workers: 1

auth:
  type: bearer
  token_env: API_TOKEN

report:
  output: ./reports

testing:
  positive: true
  negative: true
  contract: true

```
   
⸻  
   
## 46. Test Case Strategy  
## Specification Tests  
Test parser:  
```
Valid OpenAPI
Invalid OpenAPI
Missing paths
Invalid schema
Unsupported version

```
## Generator Tests  
```
GET generation
POST generation
PUT generation
DELETE generation
Parameter generation
Schema generation
Negative test generation

```
## HTTP Client Tests  
```
200
400
401
403
404
500
Timeout
Connection error

```
## Validator Tests  
```
Valid schema
Invalid schema
Missing required field
Invalid type
Invalid enum
Invalid format

```
## Report Tests  
```
All passed
Some failed
Skipped
Empty test result
Contract violation

```
   
⸻  
   
## 47. Example Test Scenario  
Given:  
```
/users/{id}:
  get:
    parameters:
      - name: id
        in: path
        required: true
        schema:
          type: integer
    responses:
      '200':
        description: Success

```
System menghasilkan:  
```
TC-001
GET /users/{id}
Valid integer ID

TC-002
GET /users/{id}
Invalid ID type

TC-003
GET /users/{id}
Missing ID

```
   
⸻  
   
## 48. Example Full Execution  
Input:  
```
api-tester run openapi.yaml

```
Process:  
```
1. Load specification
2. Validate specification
3. Discover endpoints
4. Build test plan
5. Generate test data
6. Execute request
7. Validate status code
8. Validate headers
9. Validate response schema
10. Store result
11. Generate report
12. Return exit code

```
   
⸻  
   
## 49. UX Principle  
Walaupun MVP berupa CLI, UX harus tetap diperhatikan.  
Command harus predictable.  
Good:  
```
api-tester validate openapi.yaml
api-tester discover openapi.yaml
api-tester generate openapi.yaml
api-tester run openapi.yaml

```
Bad:  
```
api-tester x --do-test --spec-file ...

```
CLI harus memiliki:  
```
api-tester --help

```
dan setiap command:  
```
api-tester run --help

```
   
⸻  
   
## 50. README Requirements  
README harus menjadi bagian penting dari project.  
README minimal memiliki:  
```
Project Overview
Features
Architecture
Installation
Quick Start
Configuration
CLI Commands
Authentication
Test Generation
Report
Docker
CI/CD
Examples
Troubleshooting
Development
Testing
Contributing
License

```
Quick Start harus dapat dilakukan dalam kurang dari 5 menit.  
   
⸻  
   
## 51. Demo Project  
Repository harus menyediakan sample API.  
Contoh:  
```
examples/
├── openapi.yaml
├── config.yaml
└── README.md

```
User harus dapat menjalankan:  
```
api-tester run examples/openapi.yaml

```
tanpa harus membuat specification sendiri.  
   
⸻  
   
## 52. Demo API  
Sebaiknya project menyediakan API demo sendiri untuk testing.  
Contoh domain:  
```
Users
Products
Orders
Authentication

```
API demo sengaja memiliki beberapa predictable behavior untuk memastikan testing engine dapat didemonstrasikan.  
Contoh:  
```
GET /users
GET /users/{id}
POST /users
PUT /users/{id}
DELETE /users/{id}

```
   
⸻  
   
## 53. Quality Gates  
Project tidak dianggap selesai hanya karena CLI dapat berjalan.  
Minimal quality gate:  
```
Unit Test       ≥ 80%
Integration     Required
Lint            Pass
Type Check      Pass
Security Scan   Pass
Build           Pass
Docker Build    Pass
CI Pipeline     Pass

```
Coverage bukan satu-satunya indikator kualitas.  
   
⸻  
   
## 54. Testing Pyramid  
Project harus menggunakan:  
```
             E2E
            /   \
       Integration
          /     \
        Unit Tests

```
Mayoritas test berada pada unit test.  
Integration test digunakan untuk:  
* HTTP client  
* OpenAPI parser  
* schema validation  
* report generation  
E2E digunakan untuk memastikan CLI bekerja end-to-end.  
   
⸻  
   
## 55. Logging  
Logging level:  
```
ERROR
WARN
INFO
DEBUG

```
Default:  
```
INFO

```
Debug:  
```
api-tester run openapi.yaml --log-level DEBUG

```
Sensitive data harus selalu di-redact.  
   
⸻  
   
## 56. Configuration Validation  
Invalid configuration harus ditolak sebelum test berjalan.  
Contoh:  
```
workers: -1

```
Result:  
```
Configuration Error

workers must be greater than 0.

```
   
⸻  
   
## 57. Dependency Management  
Dependency harus seminimal mungkin.  
Setiap dependency harus memiliki alasan yang jelas.  
Tidak boleh menambahkan library hanya karena:  
```
"lebih gampang"

```
Dependency harus dievaluasi berdasarkan:  
* maintenance  
* security  
* license  
* community  
* performance  
* compatibility  
   
⸻  
   
## 58. Development Principles  
Developer harus:  
* tidak melakukan premature abstraction  
* tidak membuat framework di atas framework  
* tidak membuat generic system yang belum dibutuhkan  
* tidak menambahkan AI hanya agar terlihat modern  
* tidak membuat microservices untuk MVP  
* tidak membuat database tanpa requirement  
* tidak membuat frontend sebelum core engine stabil  
   
⸻  
   
## 59. Project Milestones  
## Milestone 0 — Technical Spike  
Tujuan:  
Memvalidasi library dan architecture.  
Tasks:  
```
- Evaluate OpenAPI parser
- Evaluate schema validator
- Evaluate HTTP client
- Evaluate CLI framework
- Evaluate report approach
- Define internal models

```
Output:  
```
Architecture Decision Record

```
   
⸻  
   
## 60. Milestone 1 — Project Foundation  
Tasks:  
```
- Repository setup
- Python project setup
- Dependency management
- CLI skeleton
- Configuration model
- Error handling foundation
- Logging foundation
- Unit test setup
- CI setup

```
Acceptance:  
```
api-tester --help

```
berhasil.  
   
⸻  
   
## 61. Milestone 2 — OpenAPI Parser  
Tasks:  
```
- Load JSON
- Load YAML
- Load URL
- Validate specification
- Parse metadata
- Parse servers
- Parse paths
- Parse methods
- Parse parameters
- Parse schemas
- Parse responses

```
Acceptance:  
```
api-tester discover openapi.yaml

```
menampilkan endpoint dengan benar.  
   
⸻  
   
## 62. Milestone 3 — Test Generator  
Tasks:  
```
- Endpoint test model
- Positive test generator
- Request data generator
- Parameter generator
- Negative test generator
- Test classification

```
Acceptance:  
Specification dapat menghasilkan deterministic test plan.  
   
⸻  
   
## 63. Milestone 4 — HTTP Execution Engine  
Tasks:  
```
- HTTP client
- Request builder
- Headers
- Query parameters
- Path parameters
- Request body
- Authentication
- Timeout
- Error handling

```
Acceptance:  
Test plan dapat dieksekusi terhadap API.  
   
⸻  
   
## 64. Milestone 5 — Contract Validator  
Tasks:  
```
- Status validation
- Header validation
- Schema validation
- Required field validation
- Type validation
- Enum validation
- Error reporting

```
Acceptance:  
Contract violation dapat dideteksi dengan jelas.  
   
⸻  
   
## 65. Milestone 6 — Reporting  
Tasks:  
```
- Result model
- Result aggregation
- CLI summary
- JSON report
- JUnit XML
- HTML report

```
Acceptance:  
User mendapatkan report lengkap setelah test selesai.  
   
⸻  
   
## 66. Milestone 7 — CI/CD & Docker  
Tasks:  
```
- Dockerfile
- Docker execution
- GitHub Actions
- Exit codes
- Artifact upload
- Example CI pipeline

```
Acceptance:  
Project dapat dijalankan di clean GitHub Actions runner.  
   
⸻  
   
## 67. Milestone 8 — Documentation  
Tasks:  
```
- README
- Installation guide
- Quick start
- Configuration guide
- CLI documentation
- Authentication guide
- CI/CD guide
- Architecture documentation
- Troubleshooting
- Contribution guide

```
Acceptance:  
Fresh user dapat menjalankan project tanpa bantuan developer.  
   
⸻  
   
## 68. Future Roadmap  
Setelah MVP stabil:  
## V1  
* Custom test assertions  
* Custom test data  
* Test tagging  
* Test filtering  
* Parallel execution  
* Environment management  
* Better report  
## V2  
* Breaking change detection  
* OpenAPI diff  
* Contract drift detection  
* Historical result  
* Flaky test detection  
* Test trend analysis  
## V3  
Optional web dashboard:  
```
CLI
 ↓
API Testing Engine
 ↓
Backend
 ↓
Database
 ↓
Web Dashboard

```
   
⸻  
   
## 69. Breaking Change Detection  
Future feature.  
System membandingkan:  
```
openapi-v1.yaml
        ↓
        compare
        ↓
openapi-v2.yaml

```
Kemudian menghasilkan:  
```
Breaking Changes

✗ Removed endpoint:
GET /users

✗ Required field added:
POST /users.email

⚠ Response schema changed:
GET /users/{id}

```
Ini dapat menjadi salah satu fitur paling valuable pada versi berikutnya.  
   
⸻  
   
## 70. Contract Drift Detection  
Future feature:  
```
OpenAPI Contract
       ↓
Expected API
       ↓
Actual API
       ↓
Compare

```
Contoh:  
```
Contract:
id = integer

Actual:
id = string

DRIFT DETECTED

```
   
⸻  
   
## 71. Risk Analysis  
## Risk 1 — OpenAPI Complexity  
OpenAPI memiliki banyak fitur.  
Mitigation:  
MVP hanya mendukung subset OpenAPI yang jelas dan documented.  
   
⸻  
   
## Risk 2 — False Positive  
Negative testing tidak selalu memiliki expected status yang sama.  
Mitigation:  
Expected result harus berasal dari contract apabila tersedia.  
   
⸻  
   
## Risk 3 — API Side Effects  
POST/PUT/DELETE dapat mengubah data.  
Mitigation:  
Dokumentasikan bahwa test environment harus disposable atau isolated.  
Future:  
Support cleanup strategy.  
   
⸻  
   
## Risk 4 — Rate Limiting  
Automation dapat terkena rate limit.  
Mitigation:  
Controlled concurrency dan configurable delay.  
   
⸻  
   
## Risk 5 — Sensitive Data  
Token dapat masuk ke logs.  
Mitigation:  
Automatic secret redaction.  
   
⸻  
   
## Risk 6 — Flaky Network  
Network failure dapat terlihat seperti application failure.  
Mitigation:  
Bedakan:  
```
ASSERTION_FAILURE
NETWORK_ERROR
TIMEOUT
CONNECTION_ERROR

```
   
⸻  
   
## 72. Non-Functional Requirements  
## Reliability  
Test result harus deterministic sebisa mungkin.  
## Maintainability  
Core engine harus modular.  
## Portability  
Harus dapat berjalan di:  
```
Windows
Linux
macOS
Docker
GitHub Actions

```
## Performance  
Tidak boleh melakukan request concurrency tanpa batas.  
## Security  
Secret tidak boleh disimpan atau ditampilkan secara plaintext.  
## Usability  
Quick start harus sederhana.  
   
⸻  
   
## 73. Definition of Done  
MVP dianggap selesai apabila:  
```
[ ] OpenAPI JSON supported
[ ] OpenAPI YAML supported
[ ] Remote specification supported
[ ] Specification validation implemented
[ ] Endpoint discovery implemented
[ ] Positive test generation implemented
[ ] Negative test generation implemented
[ ] HTTP execution implemented
[ ] Authentication implemented
[ ] Status validation implemented
[ ] Schema validation implemented
[ ] Required field validation implemented
[ ] Type validation implemented
[ ] Enum validation implemented
[ ] Timeout implemented
[ ] Error handling implemented
[ ] CLI implemented
[ ] JSON report implemented
[ ] HTML report implemented
[ ] Exit codes implemented
[ ] Docker support implemented
[ ] GitHub Actions implemented
[ ] Unit tests implemented
[ ] Integration tests implemented
[ ] E2E tests implemented
[ ] Security checks implemented
[ ] README completed
[ ] Example API/specification available
[ ] Fresh installation tested

```
   
⸻  
   
## 74. Success Metrics  
Project dianggap berhasil apabila:  
**Usability**  
Fresh user dapat menjalankan first test dalam:  
```
≤ 5 minutes

```
**Automation**  
Minimal:  
```
80%+

```
dari test case basic dapat dibuat berdasarkan OpenAPI tanpa manual coding.  
**Reliability**  
Core test suite:  
```
100% deterministic

```
dengan mocked/integration environment yang terkontrol.  
**CI/CD**  
Pipeline dapat menjalankan regression test dan gagal ketika critical test gagal.  
**Open Source**  
Repository memiliki:  
* documentation  
* example  
* contribution guide  
* issue template  
* CI  
* release process  
   
⸻  
   
## 75. GitHub Repository Presentation  
Repository harus terlihat seperti production-grade open-source project.  
Recommended:  
```
README.md
LICENSE
CONTRIBUTING.md
SECURITY.md
CHANGELOG.md
CODE_OF_CONDUCT.md

```
README harus memiliki:  
```
┌──────────────────────────────────────┐
│ API Contract & Regression Tester     │
│                                      │
│ OpenAPI → Automated API Testing      │
│                                      │
│ [Demo] [Documentation] [PyPI]        │
└──────────────────────────────────────┘

```
Badge:  
```
CI
Coverage
Python Version
License
Release

```
Jangan memasukkan badge yang tidak benar-benar digunakan.  
   
⸻  
   
## 76. LinkedIn Portfolio Value  
Project harus dapat menunjukkan beberapa kompetensi sekaligus:  
```
API Testing
     +
Automation
     +
Contract Testing
     +
Python
     +
CLI Development
     +
Schema Validation
     +
CI/CD
     +
Docker
     +
Software Architecture

```
Dengan demikian project tidak terlihat seperti:  
“Saya membuat script API testing.”  
Tetapi:  
“Saya membangun open-source API contract and regression testing tool yang mengubah OpenAPI specification menjadi automated test execution dan actionable test reports.”  
   
⸻  
   
## 77. Final Product Vision  
Final architecture yang diharapkan:  
```
                 OpenAPI
                    │
          ┌─────────▼─────────┐
          │ Specification      │
          │ Parser             │
          └─────────┬─────────┘
                    │
          ┌─────────▼─────────┐
          │ Test Generator     │
          └─────────┬─────────┘
                    │
          ┌─────────▼─────────┐
          │ Test Execution     │
          │ Engine             │
          └─────────┬─────────┘
                    │
          ┌─────────▼─────────┐
          │ Contract Validator │
          └─────────┬─────────┘
                    │
              ┌─────┴─────┐
              │           │
              ▼           ▼
           CLI Output   HTML Report
              │           │
              └─────┬─────┘
                    ▼
                 CI/CD

```
**Prinsip utama project:**  
**OpenAPI is the source of truth.**  
User tidak seharusnya perlu mendefinisikan ulang informasi yang sudah tersedia di OpenAPI specification. Tool membaca contract tersebut, menghasilkan test yang relevan, menjalankannya secara deterministic, lalu memberikan evidence yang jelas ketika API sesuai atau menyimpang dari contract.  
