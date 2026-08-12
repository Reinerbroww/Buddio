# Buddio — Web (Frontend)

Teman belajar berbasis AI. Frontend Next.js 16 untuk Buddio.

- **Framework:** Next.js 16 (App Router) + React 19 + TypeScript + Tailwind CSS v4
- **Icons:** Lucide Icons
- **Fonts:** Plus Jakarta Sans (heading) · Inter (body)

## Menjalankan

```bash
npm install
npm run dev
```

Buka **http://localhost:3000**.

## Script

| Command        | Fungsi                        |
|----------------|-------------------------------|
| `npm run dev`  | Development server (Turbopack) |
| `npm run build`| Production build               |
| `npm run start`| Jalankan hasil build           |
| `npm run lint` | ESLint                         |

## Struktur

```
src/
├── app/          # Pages (landing, auth, onboarding, dashboard)
├── components/   # Komponen bersama
├── context/      # AuthContext
├── services/     # API clients
└── lib/          # Types & utilities
```

> Dokumentasi lengkap ada di [README root](../../README.md).
