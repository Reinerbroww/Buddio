# Buddio — Product Requirement Document (PRD)

**Versi:** 1.1  
**Tanggal:** 27 Juli 2026  
**Status:** Perencanaan (keputusan produk & stack terkunci)  
**Produk:** Buddio — AI-powered learning companion  

**Keputusan kunci:** gratis + quota AI · jenjang dipilih user (tanpa fokus produk ke satu jenjang) · Bahasa Indonesia only · stack React + Tailwind, FastAPI, PostgreSQL, LangChain/LlamaIndex — lihat [00-keputusan-produk-dan-stack.md](./00-keputusan-produk-dan-stack.md).

---

## 1. Ringkasan eksekutif

Buddio adalah pendamping belajar berbasis AI yang membantu pelajar di semua jenjang (SD, SMP, SMA, mahasiswa, dan self learner) belajar secara personal: mentor AI, roadmap belajar, evaluasi pemahaman, analisis kelemahan, dan rekomendasi materi.

Produk ini **bukan** pengganti guru atau kurikulum resmi, melainkan **layer personalisasi** di atas tujuan belajar pengguna (sekolah, ujian, atau minat mandiri).

---

## 2. Visi, misi, dan tujuan

| Aspek | Deskripsi |
|--------|-----------|
| **Visi** | Setiap pelajar punya mentor digital yang memahami level, gaya belajar, dan tujuan mereka. |
| **Misi** | Menyederhanakan perjalanan belajar dengan AI yang aman, adaptif, dan terukur. |
| **Tujuan produk** | Meningkatkan retensi, pemahaman konsep, dan kepercayaan diri belajar melalui feedback loop: belajar → uji → analisis → rekomendasi → belajar lagi. |

---

## 3. Masalah yang diselesaikan

1. **Konten berlebihan, arah kurang** — Banyak materi online tanpa jalur belajar yang jelas untuk level dan tujuan spesifik.
2. **Feedback terlambat atau generik** — Latihan tanpa diagnosa kelemahan konsep.
3. **Satu ukuran untuk semua** — Platform edukasi sering tidak menyesuaikan pace dan gaya belajar.
4. **Fragmentasi alat** — Chat AI, catatan, quiz, dan progress tracking terpisah.

---

## 4. Persona & segmen pengguna

### 4.1 Persona utama

| Persona | Kebutuhan | Pain point |
|---------|-----------|------------|
| **Pelajar SD/SMP (dengan orang tua)** | Bimbingan sederhana, aman, sesuai kurikulum | Butuh supervisi; bahasa harus ramah anak |
| **Pelajar SMA** | Persiapan ujian, ringkasan, latihan | Waktu terbatas; butuh fokus topik lemah |
| **Mahasiswa** | Deep dive, proyek, referensi | Butuh sumber terpercaya dan struktur modul |
| **Self learner** | Roadmap fleksibel, skill karier | Tidak tahu mulai dari mana |
| **Orang tua / wali** (sekunder) | Insight progress anak, kontrol privasi | Khawatir konten & screen time |

### 4.2 Jenjang: pilihan user, bukan fokus produk

Buddio **mendukung semua jenjang** (SD, SMP, SMA, mahasiswa, self learner) tanpa membangun produk terpisah per segmen. Saat onboarding, **user memilih jenjangnya**; setelah itu seluruh pengalaman difokuskan pada jenjang tersebut:

- **Roadmap & template tujuan** disesuaikan jenjang + mata pelajaran/minat.
- **AI mentor** memakai prompt profile jenjang (kompleksitas bahasa, contoh analogi, panjang jawaban).
- **Assessment & rekomendasi** memakai bank topik/threshold yang relevan jenjang itu.
- **Guardrails** (khusus SD/SMP: konten aman, hindari topik dewasa).

User dapat **mengubah jenjang** di profil (dengan konfirmasi karena mempengaruhi roadmap & riwayat mastery).

Opsional per user: referensi kurikulum (mis. Kurikulum Merdeka, persiapan SNBT) — bukan wajib MVP.

---

## 4.3 Monetisasi & quota AI (v1)

| Aspek | Kebijakan |
|--------|-----------|
| **Model awal** | **Gratis** dengan **quota** pemakaian fitur AI |
| **Yang di-quota** | Pesan chat mentor, generate/regenerate roadmap, generate quiz/soal |
| **Transparansi** | Indikator sisa quota di UI; penjelasan singkat saat limit tercapai |
| **Paid tier** | **Bukan MVP** — ditambah setelah validasi engagement & biaya inferensi |

Quota mencegah abuse, mengontrol biaya LLM, dan menjadi hook upgrade di fase later (lebih banyak chat, roadmap unlimited, dll.).

---

## 5. Proposisi nilai (value proposition)

- **Personal AI mentor** — Dialog kontekstual berdasarkan materi, progress, dan kesalahan terakhir.
- **Roadmap belajar** — Jalur terstruktur dari tujuan (mis. “lulus SNBT Matematika”) ke milestone mingguan.
- **Evaluasi pemahaman** — Quiz, soal terbuka, dan check-in singkat pasca-sesi.
- **Analisis kelemahan** — Peta kompetensi per topik/subtopik.
- **Rekomendasi materi** — Ringkasan, latihan, dan sumber lanjutan yang disesuaikan.

---

## 6. Ruang lingkup fitur

### 6.1 Fitur inti (Core)

| ID | Fitur | Deskripsi | Prioritas MVP |
|----|--------|-----------|---------------|
| F1 | **Autentikasi & profil** | Email/OAuth, **pilih jenjang**, mata pelajaran/minat, tujuan belajar | P0 |
| F1b | **Quota AI** | Tracking & enforce limit; tampilan sisa quota | P0 |
| F2 | **AI Mentor (chat)** | Sesi tanya jawab dengan konteks profil + materi aktif; mode “jelaskan”, “contoh”, “quiz cepat” | P0 |
| F3 | **Roadmap belajar** | Generate & edit roadmap dari tujuan; milestone, estimasi waktu, status | P0 |
| F4 | **Evaluasi pemahaman** | Assessment per topik (MCQ, short answer); skor & riwayat | P0 |
| F5 | **Analisis kelemahan** | Dashboard kompetensi: kuat/lemah per topik, trend | P1 |
| F6 | **Rekomendasi materi** | Daftar aksi: ulang topik, latihan, baca ringkas, sesi mentor | P1 |
| F7 | **Progress & streak** | Aktivitas harian, completion roadmap | P1 |
| F8 | **Riwayat sesi** | Chat & assessment tersimpan untuk kontinuitas | P0 |

### 6.2 Fitur pendukung (Post-MVP)

| ID | Fitur | Prioritas |
|----|--------|-----------|
| F9 | Mode orang tua / akun keluarga | P2 |
| F10 | Integrasi kalender & reminder | P2 |
| F11 | Upload materi (PDF/slide) untuk konteks AI | P2 |
| F12 | Komunitas / study group | P3 |
| F13 | Gamifikasi (badge, level) | P2 |
| F14 | Offline ringkas (cache roadmap & materi) | P3 |
| F15 | Multi-bahasa (EN, dll.) | P3 (post–Bahasa Indonesia stabil) |

### 6.3 Non-goals (v1)

- Sertifikasi resmi atau akreditasi institusi.
- Pengganti LMS sekolah penuh (gradebook, absensi).
- Generasi jawaban ujian tanpa proses belajar (anti-cheating sebagai prinsip produk).

---

## 7. User stories (contoh prioritas tinggi)

1. **Sebagai pelajar (jenjang apa pun)**, saya ingin memilih jenjang saya saat daftar agar mentor dan roadmap sesuai level saya.
2. **Sebagai pelajar**, saya ingin memasukkan tujuan belajar (mis. “SNBT Matematika 8 minggu” atau “master dasar Python”) agar Buddio membuat roadmap.
3. **Sebagai pelajar**, saya ingin bertanya konsep sulit kepada mentor AI yang mengingat kesalahan quiz terakhir saya.
4. **Sebagai pelajar**, setelah menyelesaikan modul, saya ingin quiz singkat dan melihat topik mana yang perlu diulang.
5. **Sebagai pelajar**, saya ingin tahu sisa quota chat hari ini agar bisa atur sesi belajar.
6. **Sebagai self learner**, saya ingin rekomendasi materi berikutnya berdasarkan analisis kelemahan, bukan daftar generik.
7. **Sebagai orang tua**, saya ingin melihat ringkasan progress tanpa akses penuh ke chat pribadi anak (fase later).

---

## 8. Alur pengguna (user journeys)

## User Journey

Landing Page

↓

Login / Register

↓

Onboarding (Pilih Jenjang)

↓

Dashboard

↓

Tambah Mata Pelajaran

↓

Halaman Mata Pelajaran

↓

Roadmap Belajar

↓

Belajar Materi

↓

Chat Mentor AI

↓

Quiz

↓

Check Understanding

↓

Weakness Analysis

↓

Rekomendasi Pembelajaran Selanjutnya

### 8.1 Onboarding

```
Daftar → Pilih jenjang (wajib) → Tujuan belajar (bebas / template sesuai jenjang) →
Mata pelajaran/minat → Generate roadmap awal (pakai quota) → Sesi mentor perkenalan (Bahasa Indonesia)
```

### 8.2 Loop belajar harian

```
Buka dashboard → Lanjutkan roadmap / rekomendasi →
Belajar (chat + materi) → Evaluasi singkat →
Update peta kompetensi → Rekomendasi besok
```

### 8.3 Evaluasi & perbaikan

```
Selesai milestone → Assessment topik → Skor & breakdown →
Analisis kelemahan → Roadmap disesuaikan (review manual user) →
Materi & sesi fokus topik lemah
```

---

## 9. Persyaratan fungsional

Dashboard tidak menjadi tempat utama berinteraksi dengan AI.

Dashboard berfungsi sebagai pusat aktivitas belajar pengguna yang menampilkan:

- Progress belajar
- Mata pelajaran aktif
- Statistik belajar
- Streak belajar
- Sisa quota AI
- Target belajar

Interaksi AI dimulai ketika pengguna masuk ke halaman mata pelajaran.

### 9.1 AI Mentor

- **Bahasa:** UI dan respons mentor default **Bahasa Indonesia** (istilah asing boleh jika relevan mata pelajaran).
- Mempertahankan konteks sesi dan profil (within session + persistent summary).
- Menyesuaikan tingkat bahasa berdasarkan **jenjang yang dipilih user** (bukan setting global produk).
- Mode pedagogis: hint bertahap, bukan langsung jawaban final untuk latihan ujian (configurable).
- Sitasi/internal reference ke materi roadmap jika tersedia.

### 9.2 Roadmap

- CRUD milestone; status: belum / sedang / selesai.
- Regenerasi sebagian (satu modul) tanpa menghapus progress selesai.
- Template roadmap per jenjang/tujuan.

### 9.3 Evaluasi

- Bank soal generated + fixed template per topik.
- Penilaian otomatis untuk MCQ; rubric + LLM assist untuk jawaban terbuka (dengan human-review flag jika confidence rendah).
- Attempt history dan retake policy.

### 9.4 Analisis & rekomendasi

- Skor agregat per topik (rolling window).
- Rule + model: jika skor < threshold → rekomendasi ulang + latihan.
- Explainability singkat: “Karena kesalahan di …”

### 9.5 Quota AI

- Setiap aksi AI (chat, generate roadmap, generate quiz) mem decrement quota yang sesuai.
- Response API jelas saat `429` / quota habis; frontend tampilkan waktu reset jika ada.
- Admin/internal: override atau top-up quota (fase beta).

---

## 10. Persyaratan non-fungsional

| Kategori | Target awal |
|----------|-------------|
| **Ketersediaan** | 99.5% (MVP); path ke 99.9% |
| **Latency chat** | First token < 3s (P95) di kondisi normal |
| **Skalabilitas** | 10K MAU MVP; desain horizontal |
| **Keamanan** | OAuth2, encryption at rest/transit, RBAC dasar |
| **Privasi** | Consent jelas; data minimization; hapus akun |
| **Compliance** | Kesiapan UU PDP Indonesia; COPPA-like guardrails untuk anak |
| **Aksesibilitas** | WCAG 2.1 AA (target fase Beta) |
| **Observability** | Logging terstruktur, tracing request AI, alerting error rate |

---

## 11. Kebijakan AI & kepercayaan

- **Safety:** Filter topik tidak pantas; eskalasi untuk krisis kesehatan mental (resource links).
- **Akurasi:** Disclaimer edukatif; dorong verifikasi sumber untuk fakta kritis.
- **Anti-plagiarism / academic integrity:** Mode “bimbingan” default untuk pekerjaan rumah.
- **Transparansi:** Label konten dihasilkan AI; opsi feedback “salah / tidak jelas”.

---

## 12. Metrik kesuksesan (KPI)

| Metrik | Definisi | Target MVP (indikatif) |
|--------|----------|-------------------------|
| Activation | User selesai onboarding + 1 sesi mentor | ≥ 60% |
| Engagement | DAU/MAU | ≥ 25% |
| Learning loop | User menyelesai ≥1 evaluasi/minggu | ≥ 40% MAU |
| Retention D30 | Kembali setelah 30 hari | ≥ 20% |
| NPS | Survey in-app | ≥ 30 |
| Quality AI | Thumbs down rate | < 8% |

---

## 13. Ketergantungan & asumsi

- Akses API model LLM stabil (primary + fallback provider).
- Tim awal: product, 2–3 engineer full-stack, 1 designer, opsi pedagogy advisor.
- Konten kurikulum awal: template + generative; partnership sekolah optional later.

---

## 14. Risiko produk

| Risiko | Mitigasi |
|--------|----------|
| Halusinasi AI | RAG terbatas, confidence threshold, feedback loop |
| Biaya inferensi tinggi | Caching, model routing (kecil vs besar), quota tier |
| Anak di bawah umur | Age gate, parental flow, moderated prompts |
| Churn pasca hype | Roadmap & streak + outcome metrics yang terlihat |

---

## 15. Glosarium

- **Milestone** — Unit roadmap (modul/minggu).
- **Kompetensi** — Topik/subtopik dengan skor mastery.
- **Sesi mentor** — Thread chat pedagogis dengan konteks belajar.

---

## 16. Lampiran: wireframe konseptual (teks)

- **Home:** Progress hari ini, lanjutkan roadmap, rekomendasi 3 kartu.
- **Mentor:** Chat + chip aksi (jelaskan, contoh, quiz).
- **Roadmap:** Timeline vertikal dengan milestone.
- **Insights:** Heatmap topik, trend 4 minggu.
- **Profil:** Jenjang, tujuan, preferensi belajar.

---

*Dokumen ini menjadi acuan untuk arsitektur teknis dan roadmap pengembangan Buddio.*
