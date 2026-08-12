# Buddio — Dokumentasi Perencanaan

AI-powered learning companion untuk pelajar SD, SMP, SMA, mahasiswa, dan self learner.

## Keputusan terkunci (v1.1)

| Area | Keputusan |
|------|-----------|
| Monetisasi | **Gratis + quota AI** |
| Jenjang | User **pilih jenjang**; produk fokus ke jenjang itu per akun |
| Bahasa | **Indonesia only** (awal) |
| Stack | **React + Tailwind** · **FastAPI** · **PostgreSQL** · **LangChain / LlamaIndex** |

Detail: [00-keputusan-produk-dan-stack.md](./00-keputusan-produk-dan-stack.md)

## Dokumen

| # | Dokumen | Isi |
|---|---------|-----|
| 0 | [Keputusan produk & stack](./00-keputusan-produk-dan-stack.md) | Locked decisions |
| 1 | [Product Requirement Document](./01-product-requirement-document.md) | PRD v1.1 — quota, jenjang, fitur |
| 2 | [Technical Architecture](./02-technical-architecture.md) | FastAPI, React SPA, AI pipeline |
| 3 | [Development Roadmap](./03-development-roadmap.md) | Fase 0–5 diselaraskan stack |
| 4 | [Tech Stack (locked)](./04-recommended-tech-stack.md) | Implementasi detail |

## Status

Perencanaan v1.1 — **belum ada implementasi kode**.

## Langkah berikutnya (suggested)

1. Tentukan angka quota default (chat / roadmap / quiz per hari)  
2. Spike LangChain streaming + LlamaIndex pgvector  
3. Wireframe onboarding **pilih jenjang** + tampilan sisa quota  
4. Scaffold monorepo (React + FastAPI) setelah spike OK  
