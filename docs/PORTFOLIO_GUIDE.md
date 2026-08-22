# Panduan Portofolio LinkedIn & GitHub Upload

Dokumen ini berisi panduan lengkap untuk mempublikasikan project **API Contract & Regression Tester** ke GitHub dan LinkedIn.

---

## 1. Persiapan Push ke GitHub

Jalankan perintah berikut di terminal WSL Anda:

```bash
cd "/mnt/d/WSL/Project/API Contract & Regression Tester"

# 1. Inisialisasi Git repository
git init

# 2. Add semua file (sesuai .gitignore yang sudah rapi)
git add .

# 3. Commit pertama
git commit -m "feat: initial release of OpenAPI contract and regression testing engine v0.1.0"

# 4. Ganti ke main branch
git branch -M main

# 5. Hubungkan ke repository GitHub Anda (buat repo baru di github.com lebih dulu)
git remote add origin https://github.com/USERNAME_ANDA/api-contract-regression-tester.git

# 6. Push ke GitHub
git push -u origin main
```

---

## 2. Setting Repository GitHub (Best Practice)

- **Description**: `Automated OpenAPI 3.x contract & regression testing CLI engine in Python with synthetic test generation and interactive HTML reports.`
- **Website / Demo**: Link GitHub Pages atau link video singkat jika ada.
- **Topics / Tags**:
  `api-testing`, `contract-testing`, `openapi`, `swagger`, `qa-automation`, `python`, `cli`, `regression-testing`, `schema-validation`, `ci-cd`, `docker`

---

## 3. Komponen Visual untuk Postingan LinkedIn

Untuk membuat postingan LinkedIn memiliki interaksi tinggi (high reach):
1. **Screenshot 1**: Terminal CLI saat menjalankan `api-tester run examples/openapi.yaml` (menampilkan Rich CLI banner & tabel test case).
2. **Screenshot 2**: Interactive HTML Report (`reports/index.html`) yang menampilkan Pass Rate 90%+, response payload, dan contract violation box.
3. **Diagram Arsitektur**: Ambil diagram ASCII yang ada di `README.md` atau masukkan ke diagram visual (Mermaid / Canva).

---

## 4. Copy-Paste Draft LinkedIn

Gunakan teks yang sudah disiapkan di file:
📂 `docs/LINKEDIN_POST.md`
