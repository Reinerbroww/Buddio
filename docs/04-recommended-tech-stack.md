# Buddio — Tech Stack (Locked)

**Versi:** 2.0  
**Tanggal:** 27 Juli 2026  
**Status:** **Locked** — acuan implementasi  
**Referensi keputusan:** [00-keputusan-produk-dan-stack.md](./00-keputusan-produk-dan-stack.md)

---

## 1. Stack inti (yang dipakai)

| Layer | Teknologi | Catatan |
|-------|-----------|---------|
| **Frontend** | **React** + **Tailwind CSS** | SPA; disarankan **Vite** + **TypeScript** |
| **Backend** | **FastAPI** | REST API, OpenAPI otomatis, SSE streaming chat |
| **Database** | **PostgreSQL** | Satu sumber kebenaran relasional |
| **AI** | **LangChain** + **LlamaIndex** | Chains, tools, RAG; bagi peran di bawah |

## Alasan Pemilihan Stack

React dipilih karena memiliki ekosistem yang matang untuk membangun antarmuka modern dan responsif.

FastAPI dipilih karena memiliki performa tinggi, dokumentasi otomatis, serta sangat cocok untuk integrasi AI menggunakan Python.

PostgreSQL dipilih sebagai database utama karena stabil, scalable, dan mendukung pgvector untuk penyimpanan embedding AI.

LangChain dan LlamaIndex digunakan untuk membangun pipeline AI, Retrieval Augmented Generation (RAG), serta integrasi berbagai model bahasa.

---

## 2. Diagram deploy (target MVP)

```
┌──────────────────────────────────────┐
│  React SPA (Vite) + Tailwind         │
│  - TanStack Query (server state)     │
│  - React Router                      │
│  - Fetch / EventSource (SSE chat)    │
└─────────────────┬────────────────────┘
                  │ HTTPS / REST + SSE
                  ▼
┌──────────────────────────────────────┐
│  FastAPI                             │
│  - Routers per domain                │
│  - JWT auth                          │
│  - Quota middleware (AI endpoints)   │
│  - services/ → business logic        │
└───────┬──────────────┬───────────────┘
        │              │
        ▼              ▼
  PostgreSQL         Redis
  (+ pgvector)       (cache, Celery broker)
        │
        ▼
  Celery workers
  - thread summary
  - roadmap generation (async)
  - LlamaIndex ingest / reindex
        │
        ▼
  LangChain + LlamaIndex
  → LLM API (OpenAI / compatible)
  → embeddings → pgvector
```

---

## 3. Pembagian LangChain vs LlamaIndex

| Use case | Tool utama | Alasan |
|----------|------------|--------|
| **Chat mentor** (streaming, tools, memory) | **LangChain** | Chains, chat history, tool calling `get_roadmap`, `get_mastery` |
| **RAG materi** (template kurikulum, FAQ Buddio) | **LlamaIndex** | Indexing, retrieval, metadata filter jenjang & mapel |
| **Generate roadmap / quiz** (structured JSON) | **LangChain** | Output parser Pydantic, retry, prompt templates per jenjang |
| **Grading jawaban terbuka** | **LangChain** | Rubric chain + skor + confidence |

Keduanya bisa hidup berdampingan: LlamaIndex untuk retrieval; LangChain mengonsumsi chunks sebagai context ke LLM.

---

## 4. Komponen pendukung (rekomendasi implementasi)

| Area | Pilihan | Alternatif |
|------|---------|------------|
| **ORM** | SQLAlchemy 2.0 + Alembic | — |
| **Validasi API** | Pydantic v2 | — |
| **Auth** | JWT (access + refresh), password bcrypt | OAuth Google (Phase 1+) |
| **Job queue** | Celery + Redis | ARQ (lebih ringan, jika tim kecil) |
| **Vector store** | **pgvector** (extension PostgreSQL) | Qdrant (jika RAG sangat besar) |
| **LLM** | OpenAI-compatible API | Azure OpenAI, Gemini via adapter |
| **Embeddings** | Model dari provider yang sama dengan LLM | — |
| **File storage** | S3-compatible (R2, MinIO dev) | Local dev only MVP awal |
| **Frontend UI kit** | shadcn/ui (Tailwind) atau Headless UI | DaisyUI |
| **Form** | React Hook Form + Zod | — |
| **Test backend** | pytest + httpx | — |
| **Test frontend** | Vitest + Playwright (smoke E2E) | — |
| **Lint** | Ruff (Python), ESLint (TS) | — |
| **Observability** | Sentry + structured logging (JSON) | OpenTelemetry later |
| **Analytics** | PostHog | — |
| **Email** | Resend / SMTP | — |
| **Container** | Docker Compose (local: api + db + redis + worker) | — |
| **Hosting** | Railway / Fly.io / AWS ECS + static CDN untuk SPA | — |

---

## 5. Struktur repo (disarankan)

Monorepo atau dua repo; default **monorepo** untuk tim kecil:

```
buddio/
├── apps/
│   └── web/                 # React + Vite + Tailwind
├── services/
│   └── api/                 # FastAPI
│       ├── app/
│       │   ├── routers/
│       │   ├── models/      # SQLAlchemy
│       │   ├── schemas/     # Pydantic
│       │   ├── services/
│       │   └── ai/
│       │       ├── chains/      # LangChain
│       │       └── indexing/    # LlamaIndex
│       └── alembic/
├── packages/                # optional: shared types OpenAPI → TS client
└── docker-compose.yml
```

---

## 6. Konvensi AI per jenjang (backend config)

File konfigurasi (YAML/DB) `grade_level_profiles`:

- `sd`, `smp`, `sma`, `mahasiswa`, `self_learner`
- Fields: `tone`, `max_answer_paragraphs`, `safety_strictness`, `example_style`

Prompt template LangChain memuat `{grade_level}` dari profil user — **bukan** hardcode satu jenjang di produk.

---

## 7. Quota & biaya LLM

- Enforce di FastAPI dependency sebelum memanggil chain LlamaIndex/LangChain.
- Log token usage per `user_id` + `action_type` ke PostgreSQL untuk analisis margin.
- Cache retrieval RAG untuk FAQ statis; summarization thread async via Celery.

Estimasi biaya infra early beta (order of magnitude): PostgreSQL + Redis $25–100/bulan; LLM **$500–3.000+** tergantung MAU & quota — spike wajib di Phase 0.

---

## 8. Yang sengaja tidak dipakai (v1)

| Tidak dipakai | Alasan |
|---------------|--------|
| Next.js full-stack | Keputusan: React SPA + FastAPI terpisah |
| Node BullMQ | Stack Python unified dengan Celery |
| Drizzle/Prisma | Backend Python → SQLAlchemy |
| Multi-bahasa i18n framework | ID only; tambah `next-intl`/i18next later |
| Subscription payment | Setelah model quota stabil |

---

## 9. Checklist sebelum coding Phase 1

- [ ] Docker Compose: Postgres (+ pgvector), Redis, API, worker  
- [ ] `.env.example` (LLM keys, DATABASE_URL, REDIS_URL)  
- [ ] OpenAPI spec v0 + generate TypeScript client untuk React (optional)  
- [ ] Spike: 1 chain LangChain streaming + 1 LlamaIndex query on pgvector  
- [ ] Nilai quota default per action (chat, roadmap, quiz)  

---

*Stack v2.0 menggantikan rekomendasi Next.js monolith di dokumen v1.0.*
