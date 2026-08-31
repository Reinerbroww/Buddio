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
            f"Dalam dunia **{topic_title}**, data mentah di dunia nyata hampir tidak pernah langsung siap pakai. "
            f"Proses **{step_title}** merupakan jembatan krusial antara data mentah kasar dan model berkualitas tinggi.\n\n"
            "Berikut adalah gambaran peta mental alur lengkapnya:\n\n"
            "```text\n"
            "Raw Data Mentah (Lengkap dengan missing values, outliers, & format acak)\n"
            "        ↓\n"
            "1. Pembersihan Data (Data Cleaning: Imputasi nilai hilang & hapus duplikat)\n"
            "        ↓\n"
            "2. Transformasi & Scaling (Min-Max Scaling / Z-score Standardization)\n"
            "        ↓\n"
            "3. Categorical Encoding (Label Encoding vs One-Hot Encoding)\n"
            "        ↓\n"
            "4. Feature Engineering (Membuat fitur baru, binning, & fitur interaksi)\n"
            "        ↓\n"
            "5. Dimensionality Reduction (PCA / Reduksi Dimensi)\n"
            "        ↓\n"
            "Model / Pemrosesan Akhir\n"
            "```\n\n"
            "---\n\n"

            "> [!tujuan]\n"
            "> **Tujuan Pembelajaran:**\n"
            "> Setelah mempelajari materi ini, kamu akan bisa:\n"
            "> - [ ] **Menjelaskan** tahapan utama dalam alur pemrosesan data mentah hingga fitur siap pakai.\n"
            "> - [ ] **Menghitung** hasil Min-Max Scaling secara mandiri selangkah demi selangkah hingga angka akhir.\n"
            "> - [ ] **Memilih** antara Label Encoding dan One-Hot Encoding berdasarkan jenis variabel kategorikal.\n"
            "> - [ ] **Mengidentifikasi** dan mencegah *data leakage* dengan menerapkan pemisahan data train/test yang benar.\n"
            "> - [ ] **Menjelaskan** tujuan utama Principal Component Analysis (PCA) dalam reduksi dimensi.\n\n"

            "---\n\n"

            "### 1. Pembersihan Data (Data Cleaning)\n\n"
            "**Intuisi:** Bayangkan kamu membeli buah segar dari pasar. Sebelum dimasak, kamu harus membuang bagian yang busuk dan mencucinya terlebih dahulu.\n\n"
            "**Komponen Utama Pembersihan:**\n"
            "- **Nilai Hilang (Missing Values):** Diatasi dengan *Imputation* (mengisi dengan Mean/Median untuk data numerik, atau Mode untuk kategorikal) atau menghapus baris jika data hilang sangat sedikit.\n"
            "- **Data Duplikat:** Menghapus baris yang identik agar tidak memberikan bobot ganda pada sampel tertentu.\n"
            "- **Outliers (Pencilan):** Nilai ekstrem (seperti umur `250` tahun) yang perlu diidentifikasi dan ditangani agar tidak merusak perhitungan statistik.\n\n"

            "---\n\n"

            "### 2. Feature Scaling & Transformasi Data\n\n"
            "**Masalah:** Komputer hanya melihat angka murni. Jika fitur *Umur* berkisar `18–60` dan *Gaji* berkisar `3.000.000–500.000.000`, algoritma berbasis jarak akan menganggap *Gaji* $1.000.000\\times$ lebih penting daripada *Umur*!\n\n"
            "**Solusi (Min-Max Scaling):** Memetakan seluruh angka ke dalam rentang **[0, 1]**.\n\n"
            "$$X_{scaled} = \\frac{X - X_{min}}{X_{max} - X_{min}}$$\n\n"

            "> [!contoh]\n"
            "> **Worked Example: Perhitungan Min-Max Scaling Tuntas**\n"
            ">\n"
            "> **Diketahui:** Dataset $X = [20, 30, 50]$\n"
            "> - Nilai minimum ($X_{min}$) = $20$\n"
            "> - Nilai maksimum ($X_{max}$) = $50$\n"
            "> - Rentang ($X_{max} - X_{min}$) = $50 - 20 = 30$\n"
            ">\n"
            "> **Hitungan Langkah demi Langkah:**\n"
            "> 1. Untuk data $X = 20$:\n"
            ">    $$X_{scaled} = \\frac{20 - 20}{50 - 20} = \\frac{0}{30} = 0$$\n"
            "> 2. Untuk data $X = 30$:\n"
            ">    $$X_{scaled} = \\frac{30 - 20}{50 - 20} = \\frac{10}{30} = \\frac{1}{3} \\approx 0.33$$\n"
            "> 3. Untuk data $X = 50$:\n"
            ">    $$X_{scaled} = \\frac{50 - 20}{50 - 20} = \\frac{30}{30} = 1$$\n"
            ">\n"
            "> **Hasil Akhir:** Matrix ter-scale = `[0, 0.33, 1]`.\n"
            "> *Penjelasan:* Nilai minimum menjadi 0, nilai maksimum menjadi 1, dan nilai tengah dipetakan secara proporsional.\n\n"

            "---\n\n"

            "### 3. Encoding Data Kategorikal\n\n"
            "Komputer membutuhkan data berupa angka. Data teks seperti jenis kelamin atau kota harus diubah menjadi format numerik:\n\n"
            "1. **Label / Ordinal Encoding:** Digunakan untuk kategori yang memiliki tingkatan/urutan (misal: *SD=1, SMP=2, SMA=3*).\n"
            "2. **One-Hot Encoding:** Digunakan untuk kategori nominal tanpa tingkatan (misal: *Merah, Hijau, Biru*). Setiap kategori diubah menjadi kolom biner (`0` atau `1`) baru untuk menghindari komputer menganggap 'Biru > Merah'.\n\n"

            "---\n\n"

            "### 4. Feature Engineering & Reduksi Dimensi (PCA)\n\n"
            "- **Feature Engineering:** Proses membuat fitur baru yang lebih informatif dari fitur yang ada. Contoh: Dari kolom `Tanggal_Lahir`, kita buat fitur baru `Umur`.\n"
            "- **Principal Component Analysis (PCA):** Teknik reduksi dimensi unsupervised yang mengubah banyak fitur yang saling berkorelasi menjadi sedikit komponen utama (*principal components*) tanpa kehilangan banyak variasi informasi.\n\n"

            "---\n\n"

            "### 5. Coba Sendiri (Praktis & Solusi Lengkap)\n\n"
            "> [!coba]\n"
            "> **Soal Latihan:**\n"
            "> Sebuah dataset memiliki nilai minimum $X_{min} = 10$ dan maksimum $X_{max} = 40$. Berapakah hasil Min-Max Scaling untuk nilai $X = 25$?\n"
            ">\n"
            "> ---\n"
            "> **Pembahasan & Jawaban Langkah demi Langkah:**\n"
            "> 1. **Identifikasi rumus:** $X_{scaled} = \\frac{X - X_{min}}{X_{max} - X_{min}}$\n"
            "> 2. **Substitusi nilai:** $X_{scaled} = \\frac{25 - 10}{40 - 10}$\n"
            "> 3. **Hitung pembilang dan penyebut:** \\frac{15}{30}\n"
            "> 4. **Hasil Akhir:** $0.5$\n"
            "> *Kesimpulan:* Karena 25 berada tepat di tengah-tengah antara 10 dan 40, hasil scaling-nya adalah **0.5**.\n\n"

            "---\n\n"

            "### 6. Kesalahan Umum: Data Leakage\n\n"
            "> [!perhatian]\n"
            "> ❌ **Workflow Buruk (Data Leakage!):**\n"
            "> `Seluruh Dataset → Fit Scaler (hitung Xmin & Xmax seluruh data) → Split Train/Test`\n"
            "> *Bahaya:* Scaler mengintip data Test sebelum model dilatih, membuat evaluasi akurasi terlalu optimistis secara palsu.\n"
            ">\n"
            "> ✅ **Workflow Benar:**\n"
            "> `Seluruh Dataset → Split Train/Test → Fit Scaler HANYA pada Train → Transform Train & Test`\n"
            "> *Alasan:* Menjamin bahwa informasi dari data Test tetap murni tidak terlihat selama proses pelatihan model.\n\n"

            "---\n\n"

            "> [!ingat]\n"
            "> **Ringkasan & Poin Kunci:**\n"
            "> - **Data Cleaning** menyelesaikan missing values, duplikat, dan outliers sebelum transformasi.\n"
            "> - **Min-Max Scaling** memetakan nilai numerik ke rentang `[0, 1]`, sedangkan **Standardization (Z-score)** mengubah distribusi menjadi mean 0 dan varians 1.\n"
            "> - **One-Hot Encoding** mencegah model membuat asumsi urutan palsu pada data kategorikal nominal.\n"
            "> - **PCA** mengurangi jumlah fitur berdimensi tinggi sambil mempertahankan variansi informasi terbanyak.\n"
            "> - **Data Leakage** harus dicegah dengan selalu melakukan *fit* transformer hanya pada dataset *training*.\n\n"

            "---\n\n"

            "### Uji Pemahaman Self-Check\n\n"
            "> [!quiz]\n"
            "> **Soal 1 (Pemahaman Encoding):**\n"
            "> Mengapa kita sebaiknya tidak menggunakan Label Encoding untuk kolom 'Kota Asal' (Jakarta, Bandung, Surabaya)?\n"
            ">\n"
            "> **Soal 2 (Penalaran Scaling):**\n"
            "> Apa dampak yang terjadi jika kita tidak melakukan feature scaling pada algoritma K-Means Clustering?\n"
            ">\n"
            "> ---\n"
            "> **Jawaban & Pembahasan:**\n"
            "> 1. Karena 'Kota Asal' bersifat nominal tanpa tingkatan urutan. Jika diberi angka 1, 2, 3, model matematika akan salah menganggap Surabaya (3) lebih berbobot daripada Jakarta (1).\n"
            "> 2. K-Means menghitung jarak Euclidean antar poin. Fitur berukuran skala besar akan mendominasi perhitungan jarak, sehingga fitur bernilai kecil diabaikan.\n"
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
