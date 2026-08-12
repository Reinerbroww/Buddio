# Buddio — Keputusan Produk & Stack (Locked)

**Versi:** 1.0  
**Tanggal:** 27 Juli 2026  
**Status:** Disetujui untuk perencanaan & implementasi awal

---

## Keputusan produk

| Topik | Keputusan |
|--------|-----------|
| **Monetisasi awal** | **Gratis + quota AI** (batas pesan/token/hari atau bulan per user). Paid tier opsional setelah PMF. |
| **Jenjang** | **Tidak ada fokus produk ke satu jenjang.** User memilih jenjang saat onboarding; seluruh pengalaman (bahasa AI, roadmap, assessment, guardrails) **mengikuti jenjang yang dipilih**. |
| **Bahasa** | **Bahasa Indonesia only** untuk UI, copy, prompt sistem, dan output mentor default. |

### Jenjang yang didukung (user choice)

- SD  
- SMP  
- SMA  
- Mahasiswa  
- Self learner  

Per jenjang: parameter pedagogis (kompleksitas bahasa, panjang jawaban, guardrails usia) di **konfigurasi backend**, bukan build produk terpisah per segmen.

### Quota AI (konsep MVP)

| Dimensi | Contoh kebijakan awal (disesuaikan saat spike) |
|---------|--------------------------------------------------|
| Chat mentor | N pesan / hari (mis. 30) |
| Generate roadmap | M kali / minggu (mis. 3) |
| Generate quiz | K kali / hari (mis. 5) |
| Reset | Harian UTC+7 / rolling 24 jam |

UI wajib menampilkan **sisa quota** dan pesan ramah saat habis (CTA: kembali besok / upgrade later).

---

## Keputusan teknologi (stack locked)

| Layer | Pilihan |
|-------|---------|
| **Frontend** | **React** + **Tailwind CSS** |
| **Backend** | **FastAPI** (Python) |
| **Database** | **PostgreSQL** |
| **AI orchestration** | **LangChain** dan/atau **LlamaIndex** (RAG, chains, agents) |

### Implikasi arsitektur

- **Frontend terpisah** (SPA, disarankan Vite + React + TypeScript) ↔ REST API + SSE streaming dari FastAPI.  
- **ORM:** SQLAlchemy 2.0 + Alembic migrations.  
- **Async jobs:** Celery + Redis (roadmap batch, summarization, indexing RAG).  
- **Vector/RAG MVP:** pgvector di PostgreSQL via LlamaIndex (atau LangChain vector store adapter).  
- **Auth:** JWT (access + refresh) dari FastAPI; OAuth Google opsional fase Foundation.

---

## Out of scope sementara

- Multi-bahasa (EN)  
- Subscription berbayar (sampai quota model stabil)  
- Native mobile (web responsive / PWA later)

---

## Prinsip Pengalaman Pengguna (UX Principles)

Buddio bukan chatbot AI, melainkan platform pembelajaran yang menggunakan AI sebagai mentor.

Seluruh alur aplikasi harus berpusat pada perjalanan belajar pengguna (learning journey), bukan percakapan dengan AI.

Urutan pengalaman pengguna:

1. Menentukan tujuan belajar
2. Memilih atau membuat mata pelajaran
3. Mengikuti roadmap pembelajaran
4. Belajar materi
5. Berdiskusi dengan AI Mentor
6. Mengikuti evaluasi pemahaman
7. Mendapatkan analisis kelemahan
8. Melanjutkan pembelajaran berdasarkan rekomendasi AI

AI hanya muncul sebagai pendamping selama proses tersebut, bukan sebagai halaman utama aplikasi.

## Dokumen terkait

- [PRD v1.1](./01-product-requirement-document.md)  
- [Technical Architecture v1.1](./02-technical-architecture.md)  
- [Development Roadmap v1.1](./03-development-roadmap.md)  
- [Tech Stack (locked)](./04-recommended-tech-stack.md)
- [Design Language (locked)](./05-design-language.md)
- [User Flow (locked)](./06-user-flow.md)
- [UI Wireframe (locked)](./07-ui-wireframe.md)