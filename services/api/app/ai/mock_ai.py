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
            f"### Kenapa {step_title} itu Penting?\n\n"
            f"Coba jawab pertanyaan ini dalam hati: **Kalau kamu belajar {topic_title}, "
            f"bagian mana yang rasanya paling bikin bingung?**\n\n"
            f"Kalau kamu pernah merasa \"kok ini susah banget\" saat belajar {topic_title}, "
            f"kemungkinan besar {step_title} adalah kuncinya. Begitu kamu paham bagian ini, "
            f"semua hal lain di {topic_title} akan terasa lebih ringan.\n\n"
            f"Bayangin seperti belajar naik sepeda — ada satu momen di mana kamu tiba-tiba bisa "
            f"seimbang sendiri. {step_title} adalah momen itu untuk {topic_title}.\n\n"

            f"---\n\n"

            f"> [!tujuan]\n"
            f"> Setelah mempelajari materi ini, kamu akan bisa:\n"
            f"> - [ ] Menjelaskan apa itu {step_title} dengan bahasamu sendiri\n"
            f"> - [ ] Mengenali {step_title} saat menemukannya dalam konteks nyata\n"
            f"> - [ ] Membedakan {step_title} dari konsep lain yang mirip\n"
            f"> - [ ] Menerapkan {step_title} untuk menyelesaikan masalah sederhana\n\n"

            f"---\n\n"

            f"### Memahami {step_title} dari Nol\n\n"
            f"Sebelum kita masuk ke penjelasan teknis, coba pahami analogi ini:\n\n"
            f"**Analogi:** Bayangkan kamu sedang merakit LEGO. {step_title} itu seperti "
            f"potongan kecil yang kelihatannya sederhana, tapi tanpa potongan ini, "
            f"seluruh modelmu nggak akan bisa berdiri dengan benar.\n\n"
            f"Jadi, {step_title} adalah salah satu konsep fundamental dalam **{topic_title}**. "
            f"Konsep ini berfungsi sebagai fondasi — artinya, hampir semua materi lanjutan "
            f"di {topic_title} dibangun di atas pemahamanmu tentang {step_title}.\n\n"

            f"> [!tip]\n"
            f"> **Cara Mengingat:** Saat belajar konsep baru, coba tanyakan pada diri sendiri "
            f"tiga hal: (1) Apa ini? (2) Kenapa penting? (3) Kapan saya pakai? "
            f"Kalau bisa jawab ketiganya, berarti kamu sudah paham!\n\n"

            f"---\n\n"

            f"### Bagaimana {step_title} Bekerja\n\n"
            f"Oke, sekarang kita masuk ke bagian inti. Tapi tenang, kita akan mulai dari "
            f"yang paling sederhana dulu.\n\n"
            f"**Langkah 1: Kenali Istilahnya**\n"
            f"Sebelum bisa benar-benar memahami {step_title}, kamu perlu tahu beberapa "
            f"istilah penting. Jangan khawatir — kita akan jelaskan satu per satu.\n\n"
            f"**Langkah 2: Pahami Logikanya**\n"
            f"{step_title} bekerja dengan prinsip yang cukup intuitif. "
            f"Bayangkan seperti sebuah mesin: ada input (yang masuk), proses (yang terjadi), "
            f"dan output (yang keluar). {step_title} mengikuti pola yang serupa.\n\n"
            f"**Langkah 3: Lihat dalam Konteks**\n"
            f"Sekarang setelah kamu tahu apa itu dan bagaimana cara kerjanya, "
            f"saatnya melihat bagaimana {step_title} muncul dalam situasi nyata.\n\n"

            f"> [!funfact]\n"
            f"> **Fakta Menarik:** Banyak programmer profesional mengakui bahwa mereka "
            f"benar-benar memahami konsep seperti {step_title} setelah menggunakannya "
            f"berulang kali dalam proyek nyata — bukan hanya dari membaca buku. "
            f"Jadi, praktik itu penting!\n\n"

            f"---\n\n"

            f"### Contoh Nyata\n\n"
            f"Teori tanpa contoh itu seperti resep tanpa gambar — susah dibayangkan. "
            f"Jadi kita langsung lihat contohnya, yuk!\n\n"

            f"> [!contoh]\n"
            f"> **Contoh 1 — Yang Paling Sederhana**\n"
            f">\n"
            f"> Bayangkan kamu punya kotak berisi 5 apel. Kamu mau bagi ke 2 teman. "
            f"Berapa masing-masing dapat? Ini adalah contoh paling basic dari {step_title} "
            f"dalam situasi sehari-hari.\n\n"

            f"> [!contoh]\n"
            f"> **Contoh 2 — Lebih Dekat ke Dunia Nyata**\n"
            f">\n"
            f"> Sekarang coba bayangkan situasi yang sedikit lebih kompleks. "
            f"Kamu diminta menjelaskan {step_title} kepada teman yang belum tahu apa-apa. "
            f"Kata-kata apa yang akan kamu gunakan? Kadang, menjelaskan ke orang lain "
            f"adalah cara terbaik untuk menguji pemahaman kita sendiri.\n\n"

            f"> [!contoh]\n"
            f"> **Contoh 3 — Tantangan**\n"
            f">\n"
            f"> Coba hubungkan {step_title} dengan salah satu hobi atau aktivitas yang kamu "
            f"sukai. Misalnya: kalau kamu suka memasak, gaming, atau olahraga — "
            f"di mana kamu bisa menemukan pola yang mirip dengan {step_title}?\n\n"

            f"---\n\n"

            f"### Jangan Sampai Tertipu!\n\n"
            f"Ada beberapa kesalahan umum yang sering dilakukan saat mempelajari {step_title}. "
            f"Kenali supaya kamu bisa menghindarinya.\n\n"

            f"> [!perhatian]\n"
            f"> **Hati-hati!**\n"
            f"> ❌ **Miskonsepsi:** Menganggap {step_title} hanya teori yang nggak penting\n"
            f"> ✅ **Yang Benar:** {step_title} adalah fondasi — tanpa ini, materi lanjutan "
            f"akan jauh lebih sulit\n"
            f">\n"
            f"> ❌ **Miskonsepsi:** Menghafal definisi tanpa memahami maknanya\n"
            f"> ✅ **Yang Benar:** Coba jelaskan dengan bahasamu sendiri. "
            f"Kalau bisa dijelaskan, berarti sudah dipahami\n\n"

            f"---\n\n"

            f"### Ringkasan\n\n"
            f"Oke, kita sudah sampai di penghujung materi ini. Mari kita revisi "
            f"apa saja yang sudah kamu pelajari:\n\n"

            f"> [!ingat]\n"
            f"> **Yang Perlu Kamu Ingat:**\n"
            f"> - {step_title} adalah fondasi dari {topic_title}\n"
            f"> - Pahami KENAPA dan BAGAIMANA, bukan hanya APA\n"
            f"> - Gunakan analogi untuk membantu memahami konsep abstrak\n"
            f"> - Jangan takut salah — kesalahan adalah bagian dari belajar\n\n"

            f"---\n\n"

            f"### Uji Pemahamanmu\n\n"
            f"Sekarang saatnya melihat seberapa dalam pemahamanmu. "
            f"Jawab pertanyaan-pertanyaan ini tanpa melihat materi di atas!\n\n"

            f"> [!quiz]\n"
            f"> **Soal 1 — Pemahaman Dasar:**\n"
            f"> Jelaskan dengan bahasamu sendiri apa itu {step_title} dan "
            f"mengapa penting dalam {topic_title}.\n"
            f">\n"
            f"> **Soal 2 — Penerapan:**\n"
            f"> Berikan satu contoh situasi nyata di mana {step_title} "
            f">bisa digunakan untuk menyelesaikan masalah.\n"
            f">\n"
            f"> **Soal 3 — Analisis:**\n"
            f"> Apa yang terjadi jika seseorang melewati {step_title} "
            f"tanpa benar-benar memahaminya? Jelaskan dampaknya.\n\n"

            f"---\n\n"
            f"**Jawaban:**\n\n"
            f"1. {step_title} adalah konsep fundamental dalam {topic_title} yang berfungsi "
            f"sebagai fondasi. Tanpa pemahaman yang kuat tentang {step_title}, "
            f"materi lanjutan akan terasa jauh lebih sulit.\n\n"
            f"2. [Tulis jawabanmu sendiri berdasarkan contoh yang kamu temukan "
            f"saat mempelajari materi ini. Tidak ada jawaban yang salah selama "
            f"bisa dipertanggungjawabkan logikanya.]\n\n"
            f"3. Jika {step_title} dilewati tanpa pemahaman yang cukup, "
            f"siswa akan kesulitan saat masuk ke materi berikutnya. "
            f"Bayangkan seperti membangun rumah tanpa fondasi — "
            f"lama-kelamaan akan goyang.\n\n"

            f"---\n\n"

            f"**Hebat! Kamu sudah menyelesaikan materi tentang {step_title}.** "
            f"Ingat, memahami sesuatu butuh waktu — jangan buru-buru. "
            f"Yang terpenting adalah kamu sudah melangkah hari ini. "
            f"Setiap ahli pernah jadi pemula! 💪"
        ),
        "videos": [
            {
                "title": f"Penjelasan Dasar {step_title}",
                "url": f"https://www.youtube.com/results?search_query={step_title.replace(' ', '+')}+tutorial+bahasa+indonesia",
                "description": f"Video penjelasan dasar tentang {step_title} untuk pemula."
            },
            {
                "title": f"Pembahasan Mendalam {step_title}",
                "url": f"https://www.youtube.com/results?search_query={step_title.replace(' ', '+')}+lanjutan+{topic_title.replace(' ', '+')}",
                "description": f"Video pembahasan lebih dalam mengenai {step_title}."
            },
            {
                "title": f"Latihan Soal {step_title}",
                "url": f"https://www.youtube.com/results?search_query={step_title.replace(' ', '+')}+latihan+soal",
                "description": f"Video latihan soal tentang {step_title}."
            },
        ],
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
