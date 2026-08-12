<div align="center">

# Buddio

### Belajar Bersama. Bertumbuh Bersama.

Teman belajar berbasis AI yang paham level belajarmu — dari SD hingga profesional.

<br/>

![Next.js](https://img.shields.io/badge/Next.js%2016-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)
![React](https://img.shields.io/badge/React%2019-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS%20v4-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL%2016-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![pgvector](https://img.shields.io/badge/pgvector-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Gemini](https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=googlegemini&logoColor=white)

<br/>

_&ldquo;No one should have to learn alone.&rdquo;_

</div>

---

## ✨ Fitur

| | |
|---|---|
| 🎯 **Onboarding Jenjang** | Pilih jenjang (SD, SMP, SMA, Mahasiswa, Self Learner) — seluruh AI menyesuaikan bahasa & tingkat kesulitan |
| 🗺️ **Peta Belajar AI** | Roadmap personal langkah demi langkah berdasarkan topik dan tujuan belajarmu |
| 💬 **Mentor AI 24/7** | Tanya apa saja, dijawab ramah dengan analogi yang mudah dipahami |
| 📝 **Kuis Adaptif** | Soal dibuat AI sesuai materi, lengkap dengan skor dan pembahasan |
| 📈 **Pelacakan Progres** | Pantau jam belajar, streak, dan persentase penyelesaian tiap topik |
| ⏱️ **Kuota AI Harian** | Pembatasan wajar per hari (chat, roadmap, kuis) agar AI dipakai bijak |
| 🧪 **Mode Demo** | Tanpa kunci API, semua fitur tetap berjalan dengan jawaban contoh |

---

## 🧱 Tech Stack

| Layer | Teknologi |
|-------|-----------|
| **Frontend** | [Next.js 16](https://nextjs.org) (App Router + Turbopack) · React 19 · TypeScript · [Tailwind CSS v4](https://tailwindcss.com) · Lucide Icons |
| **Backend** | [FastAPI](https://fastapi.tiangolo.com) · SQLAlchemy 2 · Pydantic v2 · bcrypt · PyJWT |
| **Database** | PostgreSQL 16 + [pgvector](https://github.com/pgvector/pgvector) (via Docker Compose) |
| **AI Engine** | Google Gemini (`google-genai`) dengan fallback mock generator |
| **Auth** | JWT Bearer Token |

---

## 📁 Struktur Proyek

```
buddio/
├── apps/
│   └── web/                  # Frontend Next.js
│       └── src/
│           ├── app/          # Pages (landing, auth, onboarding, dashboard)
│           ├── components/   # Komponen bersama (logo, dll.)
│           ├── context/      # AuthContext
│           ├── services/     # API clients (auth, topic, roadmap, mentor, quiz)
│           └── lib/          # Types & utilities
│
├── services/
│   └── api/                  # Backend FastAPI
│       └── app/
│           ├── ai/           # Gemini client + mock generators
│           ├── api/          # (alembic - direncanakan)
│           ├── core/         # config, security, database
│           ├── models/       # SQLAlchemy models
│           ├── routers/      # REST endpoints
│           ├── schemas/      # Pydantic schemas
│           └── services/     # Business logic
│
├── docs/                     # PRD, arsitektur, desain sistem, wireframe
└── docker-compose.yml        # PostgreSQL 16 + pgvector
```

---

## 🚀 Quick Start

### Prasyarat

- [Docker](https://www.docker.com/products/docker-desktop) (+ WSL2 di Windows)
- Python 3.11+
- Node.js 18+

### 1. Jalankan Database

```bash
docker compose up -d
```

PostgreSQL 16 + pgvector berjalan di `localhost:5432` (db: `buddio_db`, user: `buddio_user`, password: `buddio_password`).

### 2. Jalankan Backend

```bash
cd services/api
python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt

# Buat tabel database (Alembic migration direncanakan)
python -c "from app.models import Base; from app.core.database import engine; Base.metadata.create_all(bind=engine)"

# Jalankan server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Backend siap di **http://localhost:8000** — dokumentasi Swagger di **http://localhost:8000/docs** dan health check di **`GET /api/health`**.

### 3. Jalankan Frontend

```bash
cd apps/web
npm install
npm run dev
```

Buka **http://localhost:3000**.

---

## ⚙️ Konfigurasi Environment

Salin `.env.example` (di root proyek) menjadi `.env` di root proyek **atau** di `services/api/`:

| Variabel | Default | Keterangan |
|----------|---------|------------|
| `GEMINI_API_KEY` | — | Kunci API Google Gemini (opsional; tanpa ini app jalan di mode demo) |
| `GEMINI_MODEL` | `gemini-flash-latest` | Model Gemini yang dipakai |
| `FORCE_MOCK_AI` | `false` | Paksa mode mock walau ada kunci API |
| `SECRET_KEY` | dev-only | Kunci JWT — **wajib diganti** di produksi |
| `DATABASE_URL` | `postgresql+psycopg://buddio_user:buddio_password@localhost:5432/buddio_db` | Koneksi database |
| `CORS_ORIGINS` | `http://localhost:3000` | Origin frontend yang diizinkan |
| `QUOTA_CHAT_DAILY` | `20` | Kuota chat AI per hari |
| `QUOTA_ROADMAP_DAILY` | `2` | Kuota generate roadmap per hari |
| `QUOTA_QUIZ_DAILY` | `3` | Kuota generate kuis per hari |

---

## 🔌 API Overview

Semua endpoint REST di bawah prefix **`/api`**. Dokumentasi interaktif: **http://localhost:8000/docs**

| Area | Endpoint | Fungsi |
|------|----------|--------|
| Auth | `POST /auth/register` · `POST /auth/login` | Registrasi & login (JWT) |
| Users | `GET/PATCH /users/me` · `PATCH /users/me/password` | Profil & ganti password |
| Onboarding | `POST /onboarding/grade-level` · `/learning-goal` | Set jenjang & tujuan |
| Topics | `GET/POST /topics` · `DELETE /topics/{id}` | Kelola topik belajar |
| Roadmaps | `POST /roadmaps/generate` · `GET /roadmaps/topic/{id}` · `PATCH /roadmaps/steps/{id}` | Roadmap AI + progres |
| Lessons | `GET /lessons/{id}` · `PATCH /lessons/{id}/complete` | Materi per langkah |
| Mentor | `POST /mentor/chat` · `GET /mentor/history/{topicId}` | Chat dengan Kak Buddio |
| Quiz | `POST /quiz/generate` · `POST /quiz/{id}/submit` | Kuis AI + penilaian |
| Progress | `GET /progress/statistics` · `GET /progress/all` | Ringkasan progres |
| Usage | `GET /usage/me` | Sisa kuota AI harian |

---

## 🧪 Kualitas

- ✅ **Smoke test API 41/41** — perjalanan user lengkap (registrasi → onboarding → topik → roadmap → lesson → mentor → kuis → progres → kuota → auth)
- ✅ **Lint bersih** (`npm run lint`)
- ✅ **Production build hijau** (`npm run build` — 13 routes)

---

## 📚 Dokumentasi

| Dokumen | Isi |
|---------|-----|
| [Keputusan Produk & Stack](docs/00-keputusan-produk-dan-stack.md) | Keputusan terkunci (monetisasi, jenjang, bahasa, stack) |
| [PRD](docs/01-product-requirement-document.md) | Product Requirement Document v1.1 |
| [Arsitektur Teknis](docs/02-technical-architecture.md) | FastAPI, React, AI pipeline |
| [Development Roadmap](docs/03-development-roadmap.md) | Fase 0–5 |
| [Design System](docs/05-design-system.md) | Filosofi, warna, tipografi, komponen |
| [Brand Guideline](docs/12-brand-guideline.md) | Identitas & tone of voice Buddio |
| [User Flow](docs/06-user-flow.md) · [IA](docs/07-information-architecture.md) · [Wireframe](docs/08-ui-wireframe.md) | Pengalaman pengguna |

---

## 🗺️ Status Proyek

**MVP** — fitur inti berjalan end-to-end dengan Postgres live, AI Gemini real (atau mode demo), dan 41/41 smoke test lolos.

Rencana berikutnya:

- [ ] Migrasi database dengan Alembic (pengganti `create_all`)
- [ ] Hardening konfigurasi produksi (`SECRET_KEY` via env, CORS ketat)
- [ ] Feedback loop & analytics penggunaan
- [ ] Riwayat attempt kuis yang lebih kaya

---

## 🤝 Kontribusi

Pull request sangat diterima! Untuk perubahan besar, buka isu dulu untuk diskusi.

## 📄 Lisensi

MIT © 2026 Buddio
