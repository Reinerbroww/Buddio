# Buddio — Development Roadmap

**Versi:** 1.1  
**Tanggal:** 27 Juli 2026  
**Horizon:** ~12 bulan (dari kickoff)

**Keputusan terkunci:** gratis + quota · jenjang dipilih user · Bahasa Indonesia · React + FastAPI + PostgreSQL + LangChain/LlamaIndex.

---

## 1. Filosofi roadmap

- **Outcome-driven:** Setiap fase menutup loop belajar (mentor → evaluasi → insight → rekomendasi).
- **Ship early, learn fast:** MVP sempit tapi end-to-end, bukan fitur setengah jadi.
- **Parallel tracks:** Product/engineering, pedagogy/content, growth/compliance.

---

## 2. Ringkasan fase

| Fase | Durasi (indikatif) | Fokus | Exit criteria |
|------|-------------------|--------|---------------|
| **Phase 0 — Discovery** | 2–3 minggu | Validasi, desain, spike AI (LangChain/LlamaIndex) | PRD v1.1, spike streaming + RAG, angka quota |
| **Phase 1 — Foundation** | 4–6 minggu | Auth, profil + **pilih jenjang**, quota dasar, infra | Staging: React + FastAPI + Postgres |
| **Phase 2 — MVP Core** | 8–10 minggu | Mentor, roadmap, assessment dasar | Closed beta 50–100 user, loop belajar utuh |
| **Phase 3 — Beta** | 6–8 minggu | Insights, rekomendasi, polish, safety | Open beta 1K user, KPI activation terukur |
| **Phase 4 — GA v1** | 4–6 minggu | Scale, **tuning quota**, compliance | Launch publik, monitoring SLO |
| **Phase 5 — Growth** | Ongoing | Mobile, RAG materi, parent mode, partnerships | Retention & monetization experiments |

---

## 3. Phase 0 — Discovery (minggu 1–3)

### Deliverables

- [ ] Validasi 8–12 wawancara pengguna (SMA, mahasiswa, self learner)
- [ ] Competitive scan (Duolingo Max, Khanmigo, ChatGPT Edu, Ruangguru, dll.)
- [ ] User flow & wireframe high-fidelity (5 layar utama)
- [ ] Spike: LangChain SSE chat + LlamaIndex pgvector retrieval (latency & biaya 100 sesi)
- [ ] Tentukan angka default quota (chat / roadmap / quiz)
- [ ] Finalisasi PRD v1.1 & backlog MVP

### Tim

Product + Design + Tech lead (part-time engineer untuk spike)

---

## 4. Phase 1 — Foundation (minggu 4–9)

### Engineering

- [ ] Monorepo: `apps/web` (React + Vite + Tailwind), `services/api` (FastAPI)
- [ ] Docker Compose: PostgreSQL (+ pgvector), Redis, API, Celery worker
- [ ] CI/CD: Ruff/pytest + ESLint/Vitest; deploy staging
- [ ] PostgreSQL schema v1: user, profile (**grade_level**), quota ledger
- [ ] Auth JWT: register/login (Bahasa Indonesia error messages)
- [ ] OpenAPI + Swagger; CORS untuk SPA
- [ ] UI shell: routing, layout, onboarding **pilih jenjang**
- [ ] Widget **sisa quota** (placeholder data)

### Product / Design

- [ ] Copy onboarding **Bahasa Indonesia** (semua jenjang setara, bukan satu segmen)
- [ ] Template tujuan belajar per jenjang (3–5 per kategori: ujian, ulangan, skill mandiri)

**Milestone:** *Foundation Complete* — internal dogfood login & profil.

---

## 5. Phase 2 — MVP Core (minggu 10–19)

### Sprint breakdown (contoh 2 minggu/sprint)

#### Sprint A — Roadmap

- Generate roadmap dari template + tujuan (LangChain structured JSON; **consume quota**)
- UI timeline milestone, mark complete
- Persist & edit manual milestone

#### Sprint B — AI Mentor v1

- Chat UI streaming (SSE)
- Context: profil **jenjang** + milestone aktif + 10 pesan terakhir + optional RAG LlamaIndex
- Safety pre/post filter basic
- Thread list & history

#### Sprint C — Assessment v1

- MCQ per topik (generated + seeded bank kecil)
- Attempt flow, skor, simpan riwayat
- Trigger update mastery score sederhana (rata-rata terbobot)

#### Sprint D — Integrasi loop

- Dari chat: ajak “quiz cepat” topik terkait
- Dari roadmap: CTA “mulai belajar” → mentor dengan konteks milestone
- Home dashboard: lanjutkan + progress bar roadmap

**Milestone:** *MVP Core* — closed beta, NPS internal, bug bash.

---

## 6. Phase 3 — Beta (minggu 20–27)

### Fitur

- [ ] **Insights dashboard:** heatmap topik, trend skor 4 minggu
- [ ] **Rekomendasi rule-based** (3–5 kartu di home)
- [ ] **Regenerasi sebagian roadmap** setelah assessment buruk
- [ ] **Feedback thumbs** pada jawaban AI
- [ ] **Admin minimal:** prompt version, user support lookup (internal)
- [ ] **Email:** reminder belajar (opt-in)
- [ ] **Aksesibilitas pass 1:** keyboard, contrast, labels

### Non-fungsional

- Load test 500 concurrent chat sessions (simulated)
- LLM budget alerts & fallback provider
- Privacy policy, terms, consent onboarding

**Milestone:** *Open Beta* — landing page, waitlist atau open sign-up terbatas.

---

## 7. Phase 4 — GA v1 (minggu 28–33)

### Fitur

- [ ] **Quota tuning** di admin + pesan UX saat limit (Bahasa Indonesia)
- [ ] Hapus akun & export data
- [ ] Monitoring SLO dashboard & on-call runbook
- [ ] Performance: P95 chat latency tuning
- [ ] SEO landing & blog 3 artikel edukasi

### Compliance

- [ ] Review UU PDP checklist
- [ ] Age gate jenjang SD/SMP + copy orang tua

**Milestone:** *GA v1 Launch* — press kit internal, support channel (email/chat).

---

## 8. Phase 5 — Growth (bulan 9–12+)

Prioritas bergantung data beta; urutan default:

1. **Upload PDF / materi sekolah** → RAG personal
2. **Mode orang tua** (progress summary)
3. **PWA / mobile polish**
4. **Gamifikasi ringan** (streak, badge milestone)
5. **API partnership** sekolah / B2B pilot
6. **Bahasa Inggris** UI + mentor (setelah ID stabil)

---

## 9. Backlog prioritas (MoSCoW setelah MVP)

| Must (Beta) | Should (GA+) | Could | Won't (v1) |
|-------------|--------------|-------|------------|
| Insights & rekomendasi | Paid top-up quota | Study groups | Full LMS |
| Safety & feedback AI | Parent mode | Native iOS/Android | Live video class |
| Email reminder | RAG upload user | Offline mode | Multi-bahasa EN |

---

## 10. Tim & kapasitas (estimasi)

| Role | Phase 1–2 | Phase 3–4 |
|------|-----------|-----------|
| Product Manager | 1 | 1 |
| Designer | 0.5–1 | 1 |
| Full-stack engineer | 2 | 3 |
| Backend / AI (FastAPI, LangChain, LlamaIndex) | 1 | 1 |
| QA | 0 | 0.5–1 |
| Pedagogy advisor | 0.25 | 0.25 |

---

## 11. Risiko timeline & mitigasi

| Risiko | Dampak | Mitigasi |
|--------|--------|----------|
| Scope creep fitur AI | +4–6 minggu | Lock MVP scope; parking lot v2 |
| Regulasi / konten anak | Launch delay | Legal review Phase 3 |
| LLM price spike | Margin | Model routing, quota, caching |
| Low activation | Pivot fitur | Onboarding A/B sebelum GA |

---

## 12. Definition of Done (global)

- Unit + integration test untuk path kritis
- Review keamanan untuk endpoint auth & chat
- Dokumentasi API updated
- Feature flag atau kill switch untuk AI
- Metrik event tracking untuk funnel utama

---

## 13. Kalender visual (high level)

```
Q3 2026          Q4 2026              Q1 2027
|----|----|----|----|----|----|----|----|
 P0   P1      P2 MVP Core      P3 Beta   P4 GA
      Foundation                              P5 Growth →
```

---

*Roadmap ini fleksibel; review bi-weekly dengan metrik beta untuk reprioritisasi.*
