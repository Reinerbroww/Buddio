"""Rule-based AI fallback used when no Gemini API key is configured or the API call fails.

These generators produce plausible, topic-aware content so the full MVP remains testable
without any external AI dependency. The API responses include `mode: "mock"` so the UI
can clearly label generated content.
"""

ROADMAP_TEMPLATES = [
    (
        "Pengenalan {t}",
        "• Apa yang dipelajari: Konsep dasar, istilah penting, dan gambaran umum tentang {t}.\n"
        "• Mengapa penting: Membangun fondasi yang kuat sebelum melangkah ke konsep yang lebih dalam.\n"
        "• Aktivitas belajar: Membaca materi pengantar dan membuat rangkuman kecil istilah penting."
    ),
    (
        "Konsep Inti {t}",
        "• Apa yang dipelajari: Prinsip dan ide utama yang menjadi fondasi {t}.\n"
        "• Mengapa penting: Memahami logika dan alasan di balik konsep ini agar tidak bingung.\n"
        "• Aktivitas belajar: Menggambar peta konsep/mindmap yang menghubungkan topik utama."
    ),
    (
        "Latihan Terpandu",
        "• Apa yang dipelajari: Cara menyelesaikan persoalan terkait {t} dari tingkat mudah ke sulit secara bertahap.\n"
        "• Mengapa penting: Mengasah keterampilan praktis dan membiasakan diri memecahkan masalah.\n"
        "• Aktivitas belajar: Mengerjakan 3 soal latihan dasar dengan panduan atau tips dari mentor."
    ),
    (
        "Studi Kasus & Penerapan",
        "• Apa yang dipelajari: Penerapan {t} pada contoh nyata dan skenario dunia nyata.\n"
        "• Mengapa penting: Membantu melihat manfaat nyata dari ilmu yang sedang dipelajari.\n"
        "• Aktivitas belajar: Menganalisis satu studi kasus praktis dan menjelaskan bagaimana {t} mengatasinya."
    ),
    (
        "Evaluasi & Penguatan",
        "• Apa yang dipelajari: Menguji pemahaman menyeluruh tentang {t} dan mengulang bagian yang masih kurang.\n"
        "• Mengapa penting: Mengetahui batas pemahamanmu agar bisa diperbaiki secara mandiri.\n"
        "• Aktivitas belajar: Mengerjakan kuis evaluasi 5 soal pilihan ganda di Buddio."
    ),
]

QUIZ_TEMPLATES = [
    {
        "question": "Apa langkah pertama yang tepat saat mempelajari {t}?",
        "options": ["Memahami konsep dasar dan istilah penting", "Langsung mengerjakan soal sulit", "Menghafal semua rumus tanpa konteks", "Melompat ke materi lanjutan"],
        "answer_index": 0,
        "explanation": "Memahami konsep dasar dulu membangun fondasi yang kuat sebelum masuk ke bagian yang lebih dalam.",
    },
    {
        "question": "Apa manfaat utama membuat roadmap belajar untuk {t}?",
        "options": ["Belajar lebih terarah dan terukur", "Menghilangkan kebutuhan latihan", "Menghindari praktik sama sekali", "Menghafal tanpa memahami"],
        "answer_index": 0,
        "explanation": "Roadmap memberi jalur yang jelas sehingga progres belajarmu terarah dan mudah diukur.",
    },
    {
        "question": "Metode terbaik untuk menguatkan pemahaman {t} adalah…",
        "options": ["Latihan soal secara bertahap", "Membaca sekali lalu menyerah", "Menunda sampai ujian", "Hanya menonton video"],
        "answer_index": 0,
        "explanation": "Latihan bertahap adalah cara paling efektif untuk memperkuat pemahaman konsep.",
    },
    {
        "question": "Bagaimana cara mengecek pemahaman kamu setelah belajar {t}?",
        "options": ["Mengerjakan kuis dan meninjau kesalahan", "Tidak perlu mengecek", "Mengulang soal yang sama tanpa umpan balik", "Menghafal jawaban orang lain"],
        "answer_index": 0,
        "explanation": "Kuis dengan umpan balik membantu menemukan topik yang masih lemah untuk diulang.",
    },
    {
        "question": "Apa yang harus dilakukan jika ada konsep {t} yang belum dipahami?",
        "options": ["Tanya ke mentor AI dan minta penjelasan ulang", "Mengabaikannya", "Pindah topik tanpa memahami", "Berhenti belajar"],
        "answer_index": 0,
        "explanation": "Mentor AI siap membantu menjelaskan ulang konsep yang sulit dengan bahasa yang sesuai jenjangmu.",
    },
]

MOCK_GREETING = "Halo! Aku Kak Buddio, mentor belajarmu. Aku dalam mode demo (tanpa kunci API AI), jadi jawaban ini adalah contoh. Jika kamu ingin jawaban yang lebih pintar dan personal, tambahkan GEMINI_API_KEY di file .env."


def _expand(template: str, topic: str) -> str:
    return template.replace("{t}", topic)


def mock_roadmap(topic_title: str, goal: str = "") -> dict:
    steps = [
        {"order_number": i + 1, "title": _expand(t[0], topic_title), "description": _expand(t[1], topic_title)}
        for i, t in enumerate(ROADMAP_TEMPLATES)
    ]
    title = f"Roadmap {topic_title}"
    if goal:
        title = f"Roadmap {topic_title} — {goal}"
    return {
        "title": title,
        "difficulty": "Menengah",
        "estimated_hours": len(steps) * 2,
        "steps": steps,
    }


def mock_quiz(topic_title: str, count: int = 5) -> dict:
    questions = []
    templates = (QUIZ_TEMPLATES * ((count // len(QUIZ_TEMPLATES)) + 1))[:count]
    for i, tpl in enumerate(templates, start=1):
        q = dict(tpl)
        q["question"] = _expand(q["question"], topic_title)
        q["explanation"] = _expand(q["explanation"], topic_title)
        questions.append(q)
    return {
        "title": f"Kuis {topic_title}",
        "questions": questions,
    }


def mock_lesson(step_title: str, topic_title: str) -> dict:
    return {
        "content": (
            f"### Peta Besar & Alur Konseptual: {step_title}\n\n"
            f"Sebelum kita mendalami **{step_title}**, mari pahami gambaran besar alur kerja "
            f"dalam **{topic_title}**:\n\n"
            f"```text\n"
            f"Input Mentah (Raw Data)\n"
            f"        ↓\n"
            f"Pembersihan Data (Cleaning)\n"
            f"        ↓\n"
            f"Transformasi & Feature Scaling ({step_title})\n"
            f"        ↓\n"
            f"Feature Engineering & Seleksi\n"
            f"        ↓\n"
            f"Model / Pemrosesan Akhir\n"
            f"```\n\n"
            f"Data mentah sering kali memiliki rentang nilai yang sangat jauh berbeda (misalnya Umur 18–60 "
            f"vs Gaji 3.000.000–500.000.000). Jika langsung dimasukkan ke algoritma, fitur dengan rentang angka besar "
            f"akan mendominasi pemrosesan. Di sinilah **{step_title}** berperan untuk menyelaraskan data.\n\n"
            f"---\n\n"

            f"> [!tujuan]\n"
            f"> **Tujuan Pembelajaran:**\n"
            f"> Setelah mempelajari materi ini, kamu akan bisa:\n"
            f"> - [ ] **Menjelaskan** mengapa data mentah memerlukan pemrosesan dan scaling sebelum digunakan.\n"
            f"> - [ ] **Menghitung** hasil Min-Max Scaling pada dataset sederhana secara mandiri selangkah demi selangkah.\n"
            f"> - [ ] **Mengidentifikasi** potensi *data leakage* dalam workflow pemrosesan data.\n"
            f"> - [ ] **Membandingkan** Min-Max Scaling dengan Standardization (Z-score) untuk memilih teknik yang tepat.\n\n"

            f"---\n\n"

            f"### 1. Intuisi Dasar (Sederhana)\n\n"
            f"Bayangkan kamu membandingkan tinggi badan dalam centimeter (misal 170 cm) dengan berat badan "
            f"dalam kilogram (misal 65 kg). Meskipun angkanya berbeda jauh (170 vs 65), kita tahu keduanya "
            f"adalah ukuran manusia yang wajar.\n\n"
            f"Komputer tidak paham arti 'cm' atau 'kg'. Komputer hanya melihat angka `170` jauh lebih besar dari `65`. "
            f"Scaling bertugas mengonversi skala yang berbeda ini ke dalam rentang pengukuran standar yang seimbang "
            f"(misalnya 0 hingga 1).\n\n"

            f"---\n\n"

            f"### 2. Definisi Formal & Rumus (Teknis)\n\n"
            f"**Min-Max Scaling** adalah teknik transformasi linear yang memetakan nilai fitur numerik "
            f"ke dalam rentang tertentu, secara umum **[0, 1]**.\n\n"
            f"Persamaan matematis Min-Max Scaling adalah:\n\n"
            f"$$X_{{scaled}} = \\frac{{X - X_{{min}}}}{{X_{{max}} - X_{{min}}}}$$\n\n"
            f"**Keterangan Variabel:**\n"
            f"- $X$: Nilai asli data yang ingin di-scale\n"
            f"- $X_{{min}}$: Nilai terkecil dalam kolom/fitur tersebut\n"
            f"- $X_{{max}}$: Nilai terbesar dalam kolom/fitur tersebut\n"
            f"- $X_{{scaled}}$: Nilai hasil transformasi yang berada di rentang [0, 1]\n\n"

            f"---\n\n"

            f"### 3. Worked Example: Perhitungan Langkah demi Langkah\n\n"
            f"> [!contoh]\n"
            f"> **Contoh Terhitung: Mengubah Data `[20, 30, 50]`**\n"
            f">\n"
            f"> **Diketahui:** Dataset $X = [20, 30, 50]$\n"
            f"> - Nilai minimum ($X_{{min}}$) = $20$\n"
            f"> - Nilai maksimum ($X_{{max}}$) = $50$\n"
            f"> - Penyebut rentang ($X_{{max}} - X_{{min}}$) = $50 - 20 = 30$\n"
            f">\n"
            f"> **Langkah Perhitungan:**\n"
            f"> 1. Untuk $X = 20$:\n"
            f">    $$X_{{scaled}} = \\frac{{20 - 20}}{{50 - 20}} = \\frac{{0}}{{30}} = 0$$\n"
            f"> 2. Untuk $X = 30$:\n"
            f">    $$X_{{scaled}} = \\frac{{30 - 20}}{{50 - 20}} = \\frac{{10}}{{30}} = \\frac{{1}}{{3}} \\approx 0.33$$\n"
            f"> 3. Untuk $X = 50$:\n"
            f">    $$X_{{scaled}} = \\frac{{50 - 20}}{{50 - 20}} = \\frac{{30}}{{30}} = 1$$\n"
            f">\n"
            f"> **Hasil Akhir:** Data ter-scale menjadi `[0, 0.33, 1]`.\n"
            f"> *Makna:* Nilai terkecil (20) menjadi 0, nilai terbesar (50) menjadi 1, dan nilai di antaranya (30) "
            f"berada tepat secara proporsional di 0.33.\n\n"

            f"---\n\n"

            f"### 4. Coba Sendiri (Praktis)\n\n"
            f"> [!coba]\n"
            f"> **Tugas Latihan:**\n"
            f"> Diberikan dataset `[10, 20, 40]`. Berapakah nilai ter-scale untuk angka **20** menggunakan Min-Max Scaling?\n"
            f">\n"
            f"> ---\n"
            f"> **Pembahasan & Jawaban:**\n"
            f"> - $X_{{min}} = 10$, $X_{{max}} = 40$\n"
            f"> - Rumus: $X_{{scaled}} = \\frac{{20 - 10}}{{40 - 10}} = \\frac{{10}}{{30}} = \\frac{{1}}{{3}} \\approx 0.33$\n"
            f"> - Jadi nilai 20 ter-scale menjadi **0.33**.\n\n"

            f"---\n\n"

            f"### 5. Kesalahan Umum: Miskonsepsi & Data Leakage\n\n"
            f"Banyak praktisi pemula melakukan kesalahan serius saat memisahkan dataset latihan (train) dan uji (test):\n\n"
            f"> [!perhatian]\n"
            f"> ❌ **Workflow Salah (Data Leakage):**\n"
            f"> `Seluruh Dataset → Fit Scaler (hitung Xmin & Xmax seluruh data) → Split Train/Test`\n"
            f"> *Mengapa Salah?* Scaler mempelajari informasi dari data Test sebelum model dilatih! Ini membuat evaluasi model menjadi bias.\n"
            f">\n"
            f"> ✅ **Workflow Benar:**\n"
            f"> `Seluruh Dataset → Split Train/Test → Fit Scaler HANYA pada Train → Transformasi Train & Test`\n"
            f"> *Mengapa Benar?* Scaler hanya menghitung $X_{{min}}$ dan $X_{{max}}$ dari data Train, lalu menerapkan parameter tersebut ke data Test.\n\n"

            f"---\n\n"

            f"> [!ingat]\n"
            f"> **Ringkasan & Poin Kunci:**\n"
            f"> - **Feature Scaling** mencegah fitur berukuran angka besar mendominasi algoritma pemrosesan.\n"
            f"> - **Min-Max Scaling** memetakan data ke rentang `[0, 1]` menggunakan rumus $\\frac{{X - X_{{min}}}}{{X_{{max}} - X_{{min}}}}$.\n"
            f"> - Hitung statistik ($X_{{min}}, X_{{max}}$) **hanya dari data training** untuk mencegah data leakage.\n"
            f"> - Gunakan Standardization (Z-score) jika data memiliki banyak *outliers* karena Min-Max sensitif terhadap nilai ekstrem.\n\n"

            f"---\n\n"

            f"### Uji Pemahaman Self-Check\n\n"
            f"> [!quiz]\n"
            f"> **Soal 1 (Pemahaman Dasar):**\n"
            f"> Mengapa algoritma berbasis jarak seperti K-Nearest Neighbors (KNN) sangat membutuhkan scaling data?\n"
            f">\n"
            f"> **Soal 2 (Penalaran Workflow):**\n"
            f"> Jika sebuah dataset memiliki nilai minimum 100 dan maksimum 500, ke angka berapakah nilai 100 akan ter-scale?\n"
            f">\n"
            f"> ---\n"
            f"> **Jawaban & Pembahasan:**\n"
            f"> 1. Karena KNN menghitung jarak Euclidean antar poin. Tanpa scaling, fitur berukuran jutaan akan mendominasi jarak dibandingkan fitur berukuran puluhan.\n"
            f"> 2. Nilai 100 adalah $X_{{min}}$, sehingga $\\frac{{100 - 100}}{{500 - 100}} = \\frac{{0}}{{400}} = 0$.\n"
        ),
        "videos": [],
    }


def mock_chat(message: str, topic_title: str) -> str:
    return (
        "Halo Adik hebat! 🌟\n\n"
        "Kak Buddio senang sekali bisa menemani kamu belajar hari ini!\n\n"
        "### 🎒 4 Jurus Rahasia Operasi Hitung Dasar\n\n"
        "1. **🔢 Mengenal Angka & Jumlah**\n"
        "   - Angka adalah simbol untuk menghitung benda.\n"
        "   - Contoh: Angka **3** artinya ada 🍎 🍎 🍎 tiga buah apel.\n"
        "   - Rumus matematika sederhana: $2 \\times 3 = 6$\n\n"
        "2. **➕ Penjumlahan**\n"
        "   - Konsepnya adalah **menggabungkan** benda.\n"
        "   - Persamaan matematika lanjutan:\n"
        "     $$x^2 + y^2 = z^2$$\n\n"
        "---\n\n"
        "### 🧩 Tebak-Tebakan Seru\n\n"
        "Kamu punya **3 robot** 🤖🤖🤖 lalu mendapat **2 robot** lagi.\n\n"
        "Berapa jumlah robotmu?"
    )
