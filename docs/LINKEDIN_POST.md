# 🚀 Building an Open-Source API Contract & Regression Testing Engine with Python & OpenAPI

Sebagai Software Engineer / QA Automation Engineer, kita sering menghadapi masalah klasik dalam pengembangan API:
1. **Contract Drift**: Implementasi API diam-diam berubah tanpa sinkronisasi dokumentasi.
2. **Repetitive Test Maintenance**: Menulis puluhan skenario test Postman/script manual satu per satu setiap kali ada endpoint baru.
3. **Negative Test Overlooked**: Validasi missing property, datatype mismatch, atau enum invalid sering terlewat.

Untuk memecahkan masalah ini, saya membangun:
👉 **API Contract & Regression Tester** (Open-Source CLI Tool & Testing Engine).

---

### 💡 Core Philosophy: "OpenAPI is the Single Source of Truth"
Alih-alih mendefinisikan ulang test case secara manual, engine ini membaca OpenAPI Specification (JSON / YAML / URL HTTPS publik) dan otomatis:
- 🔍 **Endpoint & Schema Discovery**: Memetakan path, parameter, dan JSON Schema.
- ⚡ **Autonomous Test Generation**: Memproduksi skenario **Positive (Happy Path)** dan **Negative Mutation** (missing required fields, type mutation, enum boundaries) secara deterministik.
- 🛡 **Strict Contract Assertions**: Memvalidasi status code, response header, required attributes, dan JSON Schema (Draft 2020-12).
- 🔒 **Enterprise Security by Design**: Masking otomatis terhadap Bearer Token, API Key, dan Basic Auth di logs dan report artifacts.
- 📊 **Actionable Visual Evidence**: Menghasilkan standalone interactive HTML dashboard, JSON result, dan JUnit XML untuk integrasi CI/CD quality gate.

---

### 🛠 Tech Stack & Architecture Highlights:
- **Core Engine**: Python 3.12+ (Clean Architecture, SOLID, Type Hinting)
- **HTTP Client & Concurrency**: HTTPX with async/multi-worker thread pool & timeout policies
- **Schema Validation**: JSONSchema Draft 2020-12
- **CLI & UX**: Typer & Rich Console Interface
- **Reporting**: Jinja2 HTML Dashboard & JUnit XML
- **DevOps**: Docker (Rootless non-root container) & GitHub Actions Pipeline
- **Quality Gate**: Unit & Integration test suite with 86% code coverage

---

🔗 **Repository GitHub:** https://github.com/h1ntz0/api-contract-regression-tester

Bagaimana tim Anda mengelola API contract testing dan mencegah breaking changes di pipeline CI/CD? Mari berdiskusi di kolom komentar! 👇

#SoftwareEngineering #QAAutomation #APITesting #OpenAPI #Python #CICD #DevOps #OpenSource #QualityAssurance #CleanArchitecture
