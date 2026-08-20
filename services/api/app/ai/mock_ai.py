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
