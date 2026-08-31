"""Unified AI entry point for Buddio.

Uses Google Gemini when GEMINI_API_KEY is configured, otherwise falls back to the
rule-based mock generators so the app always works end-to-end.
"""
import json
import logging
from typing import List, Dict, Optional, Tuple

from app.core.config import settings
from app.ai import mock_ai

logger = logging.getLogger("buddio.ai")

# Tutor behavior applied when a chat comes from a lesson context (the materi page).
# It makes the mentor act like a tutor continuing the lesson rather than a generic chatbot.
TUTOR_PROMPT = (
    "\n\nJika pengguna datang dari halaman materi (pesan mengandung konteks seperti "
    "'sedang belajar materi', 'topik', atau meminta dijelaskan/memberi contoh), "
    "berperilakulah seperti TUTOR UNIVERSITAS PERPERSONAL yang melanjutkan pelajaran, bukan chatbot umum.\n\n"
    "Cara mengajar sebagai tutor:\n"
    "1. Gunakan urutan 'Sederhana → Teknis → Praktis': Berikan intuisi dasar dengan bahasa mudah dulu, "
    "   lalu konsep/rumus teknisnya, lalu penerapannya.\n"
    "2. Identifikasi titik kebingungan spesifik yang disebutkan pengguna atau teks yang disorot.\n"
    "3. Bimbing selangkah demi selangkah (step-by-step) dengan contoh konkret yang terhitung/terperinci bila relevan.\n"
    "4. Akhiri dengan 1 pertanyaan pemantik kecil atau latihan singkat untuk memastikan siswa benar-benar paham.\n"
    "5. Jaga kebenaran teknis. Jangan mengarang fakta, rumus, atau istilah."
)

SYSTEM_PROMPT = (
    "Kamu adalah Buddio, mentor belajar AI yang ramah, sabar, cerdas, dan pedagogis seperti tutor universitas terpilih. "
    "Selalu jawab dalam Bahasa Indonesia. Sesuaikan tingkat bahasa dengan jenjang pengguna "
    "(SD, SMP, SMA, mahasiswa, self learner). "
    "Gunakan pendekatan 'Sederhana → Teknis → Praktis': jelaskan intuisi dulu, ikuti dengan mekanisme teknis yang akurat, "
    "dan akhiri dengan penerapan nyata. Bimbing siswa selangkah demi selangkah agar mampu menguasai materi."
)


def get_system_prompt(grade_level: str = "sma") -> str:
    level = (grade_level or "sma").lower().strip()
    
    base_instruction = (
        "Kamu adalah Buddio, mentor belajar AI yang sangat ramah, sabar, dan interaktif. "
        "Selalu jawab dalam Bahasa Indonesia. Tulis penjelasan secara bersih, terstruktur, tidak bertele-tele, "
        "dan hindari dinding teks yang membosankan. Gunakan markdown dengan baik (bullet points, kata kunci penting ditebalkan) "
        "serta jaga agar format jawaban terlihat rapi dan memiliki spasi antar paragraf yang cukup.\n\n"
    )
    
    if level == "sd":
        specific = (
            "GAYA BAHASA & TONE (Jenjang SD - Sekolah Dasar):\n"
            "- Bertindaklah sebagai 'Kak Buddio', kakak mentor yang super ceria, hangat, penuh semangat, dan sabar.\n"
            "- Gunakan kalimat-kalimat pendek, ramah, dan sangat mudah dipahami anak kecil. Panggil pengguna dengan 'Adik' atau 'Kamu'.\n"
            "- Sering gunakan emoji yang lucu dan berwarna (seperti 🌟, 🚀, 🎉, 🎈, 🧸) untuk menyemangati, tapi pastikan tulisan tetap rapi.\n"
            "- Berikan penjelasan yang bersih, visual, dan gunakan analogi dunia anak-anak (misal: membagi kue, petualangan di luar angkasa, mainan).\n"
            "- Jangan pernah memberikan jawaban langsung untuk tugas sekolah. Bimbing mereka selangkah demi selangkah dengan pertanyaan kecil pemantik agar mereka bangga menemukan jawabannya sendiri.\n"
            "- Jika mereka menjawab benar, berikan pujian yang sangat positif dan meriah!"
        )
    elif level == "smp":
        specific = (
            "GAYA BAHASA & TONE (Jenjang SMP - Sekolah Menengah Pertama):\n"
            "- Bertindaklah sebagai mentor belajar yang seru, keren, bersahabat, dan gaul tapi tetap sopan.\n"
            "- Gunakan bahasa yang komunikatif dan santai (misalnya menggunakan 'kamu', kata-kata yang interaktif, tanpa terlalu formal).\n"
            "- Gunakan analogi yang relevan dengan kehidupan remaja masa kini (seperti game, hobi, teknologi, olahraga, atau media sosial).\n"
            "- Gunakan emoji yang aktif dan memotivasi (seperti 💡, 🔥, 👍, 🧠) untuk membuat obrolan terasa dinamis dan tidak kaku.\n"
            "- Penjelasan harus bersih dan terstruktur: tebalkan istilah penting dan batasi paragraf maksimal 3 kalimat.\n"
            "- Dorong rasa ingin tahu mereka. Bantu mereka menyelesaikan soal dengan memberikan petunjuk/hint logis dan membiarkan mereka menyelesaikannya sendiri."
        )
    elif level == "sma":
        specific = (
            "GAYA BAHASA & TONE (Jenjang SMA - Sekolah Menengah Atas):\n"
            "- Bertindaklah sebagai mentor belajar yang cerdas, inspiratif, suportif, dan profesional.\n"
            "- Gunakan gaya bahasa semi-formal yang ramah dan hangat. Gunakan sapaan yang sopan dan mendukung.\n"
            "- Gunakan analogi konseptual yang menghubungkan teori dengan penerapan nyata di dunia sains, teknologi, atau kehidupan sehari-hari.\n"
            "- Struktur tulisan harus sangat bersih dan rapi: gunakan heading jika penjelasan panjang, gunakan poin-poin teratur, dan pisahkan antar ide dengan baris baru.\n"
            "- Berikan pemahaman konsep yang kokoh (mengapa rumus/konsep ini ada, bukan sekadar menghafalnya). Tuntun logika berpikir mereka ketika mendiskusikan soal latihan."
        )
    elif level in ("mahasiswa", "self_learner"):
        specific = (
            "GAYA BAHASA & TONE (Jenjang Perguruan Tinggi / Pembelajar Mandiri):\n"
            "- Bertindaklah sebagai partner diskusi akademis dan profesional yang berwawasan luas, analitis, mendalam, namun tetap ramah.\n"
            "- Gunakan bahasa Indonesia ilmiah yang baik dan benar (semi-formal/formal), dengan istilah-istilah teknis atau akademis yang tepat sesuai bidang studi.\n"
            "- Sajikan penjelasan yang komprehensif, logis, dan mendalam. Fokus pada konseptualisasi, metodologi, dan studi kasus/aplikasi praktis di dunia nyata atau industri.\n"
            "- Penulisan harus sangat bersih, profesional, dan efisien. Gunakan heading, blok kode (code blocks) jika relevan, tabel, atau diagram berbasis teks (markdown), serta spasi yang baik.\n"
            "- Berikan saran metode belajar mandiri atau referensi literatur jika relevan. Hormati kemandirian berpikir mereka dan ajak berdiskusi secara mendalam."
        )
    else:
        specific = (
            "GAYA BAHASA & TONE (Umum):\n"
            "- Jadilah mentor belajar yang ramah, komunikatif, dan sabar.\n"
            "- Gunakan bahasa yang mudah dipahami, bersih, terstruktur dengan markdown, dan gunakan emoji secara proporsional.\n"
            "- Jelaskan secara bertahap dengan analogi sederhana dan tuntun pengguna ke pemecahan masalah."
        )
        
    return base_instruction + specific


def _is_gemini_available() -> bool:
    return bool(settings.GEMINI_API_KEY) and not settings.FORCE_MOCK_AI


_gemini_client_instance = None


def _gemini_client():
    global _gemini_client_instance
    if _gemini_client_instance is None:
        from google import genai
        _gemini_client_instance = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _gemini_client_instance


def _generate_json(prompt: str, max_tokens: int = 2048, temperature: float = 0.6, system_instruction: Optional[str] = None) -> dict:
    """Call Gemini and parse a JSON object from the response."""
    client = _gemini_client()
    from google.genai import types
    resp = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction or SYSTEM_PROMPT,
            response_mime_type="application/json",
            max_output_tokens=max_tokens,
            temperature=temperature,
        ),
    )
    text = (resp.text or "").strip()
    # Some models wrap JSON in markdown fences.
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text)


def _sanitize_and_validate_lesson_content(content: str, step_title: str, topic_title: str) -> str:
    """Ensure generated lesson markdown contains no empty callouts or dangling empty section headers."""
    if not content:
        return content

    # 1. Fix empty [!tujuan] callout if no bullet points exist inside it
    if "> [!tujuan]" in content:
        tujuan_idx = content.find("> [!tujuan]")
        next_section = content.find("---", tujuan_idx)
        tujuan_block = content[tujuan_idx:next_section] if next_section != -1 else content[tujuan_idx:]
        if "- [" not in tujuan_block and "- " not in tujuan_block:
            default_tujuan = (
                "> [!tujuan]\n"
                "> **Tujuan Pembelajaran:**\n"
                "> Setelah mempelajari materi ini, kamu akan bisa:\n"
                f"> - [ ] **Menjelaskan** konsep inti dan peran penting {step_title} dalam {topic_title}.\n"
                f"> - [ ] **Mengidentifikasi** tahapan utama dan mekanisme kerja {step_title}.\n"
                f"> - [ ] **Menghitung/Menerapkan** teknik {step_title} pada skenario nyata selangkah demi selangkah.\n"
                f"> - [ ] **Menganalisis** kesalahan umum dan batasan penerapan {step_title}.\n"
            )
            content = content[:tujuan_idx] + default_tujuan + "\n" + content[tujuan_idx + len(tujuan_block):]

    # 2. Fix empty [!ingat] callout if no bullet points exist inside it
    if "> [!ingat]" in content:
        ingat_idx = content.find("> [!ingat]")
        next_section = content.find("---", ingat_idx)
        ingat_block = content[ingat_idx:next_section] if next_section != -1 else content[ingat_idx:]
        if "- " not in ingat_block and "* " not in ingat_block:
            default_ingat = (
                "> [!ingat]\n"
                "> **Ringkasan & Poin Kunci:**\n"
                f"> - **Fondasi:** {step_title} merupakan tahapan krusial dalam pemrosesan {topic_title}.\n"
                "> - **Pendekatan Bertahap:** Pahami intuisi dan masalah sebelum menerapkan rumus atau fungsi teknis.\n"
                "> - **Validasi Data:** Selalu pisahkan dataset training dan test sebelum melakukan fitting parameter.\n"
            )
            content = content[:ingat_idx] + default_ingat + "\n" + content[ingat_idx + len(ingat_block):]

    # 3. Clean up dangling empty section headers like "Pembahasan & Jawaban:\n\n---"
    dangling_replacements = [
        (
            "Pembahasan & Jawaban:\n\n---",
            "Pembahasan & Jawaban:\n> Lakukan perhitungan sesuai rumus di atas untuk mendapatkan nilai akhir ter-scale.\n\n---",
        ),
        (
            "Langkah Perhitungan:\n\n---",
            "Langkah Perhitungan:\n> 1. Tentukan nilai minimum dan maksimum data.\n> 2. Hitung substitusi variabel ke dalam rumus.\n\n---",
        ),
    ]
    for old_pat, new_pat in dangling_replacements:
        if old_pat in content:
            content = content.replace(old_pat, new_pat)

    return content


class BuddioAI:
    """Facade over Gemini with graceful mock fallback."""

    @property
    def mode(self) -> str:
        return "gemini" if _is_gemini_available() else "mock"

    def chat(
        self,
        message: str,
        history: Optional[List[Dict]] = None,
        grade_level: str = "sma",
        topic_title: str = "",
    ) -> Tuple[str, int, str]:
        """Returns (answer, token_usage, mode)."""
        if not _is_gemini_available():
            return mock_ai.mock_chat(message, topic_title), 0, "mock"

        parts = []
        parts.append(
            "Berikut riwayat percakapan sebelumnya (jika ada). Gunakan untuk menjaga konteks.\n"
            + json.dumps(history[-10:] if history else [], ensure_ascii=False)
        )
        parts.append(
            f"Jenjang pengguna: {grade_level or 'umum'}. Topik aktif: {topic_title or '-'}.\n"
            f"Pertanyaan user: {message}"
        )
        prompt = "\n".join(parts)

        sys_prompt = get_system_prompt(grade_level)
        # If the message carries lesson context, add tutor behavior so the mentor continues
        # the lesson instead of acting like a generic chatbot.
        lesson_context_markers = (
            "sedang belajar materi",
            "bagian ini",
            "tolong jelaskan",
            "tolong berikan contoh",
            "materi ini",
        )
        if any(m in message.lower() for m in lesson_context_markers):
            sys_prompt = sys_prompt + TUTOR_PROMPT
        try:
            from google.genai import types
            resp = _gemini_client().models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=sys_prompt, max_output_tokens=2048, temperature=0.6
                ),
            )
            answer = (resp.text or "").strip()
            usage = getattr(resp, "usage_metadata", None)
            token_usage = int(getattr(usage, "total_token_count", 0)) if usage else 0
            if not answer:
                raise ValueError("Empty Gemini response")
            return answer, token_usage, "gemini"
        except Exception as exc:  # noqa: BLE001
            logger.warning("Gemini chat failed, falling back to mock: %s", exc)
            return mock_ai.mock_chat(message, topic_title), 0, "mock"

    def generate_roadmap(self, topic_title: str, grade_level: str = "sma", goal: str = "") -> Tuple[dict, str]:
        """Returns (roadmap_dict, mode)."""
        if not _is_gemini_available():
            return mock_ai.mock_roadmap(topic_title, goal), "mock"

        prompt = (
            f"Buatkan roadmap belajar untuk topik '{topic_title}' untuk jenjang {grade_level or 'sma'}. "
            + (f"Tujuan akhir belajar pengguna: {goal}. " if goal else "")
            + "Kembalikan JSON dengan format: "
            + '{"title": "...", "difficulty": "Mudah|Menengah|Sulit", "estimated_hours": <angka>, '
            + '"steps": [{"order_number": 1, "title": "...", "description": "..."}]}. '
            + "Buat 5-7 langkah yang berurutan, ditulis dalam Bahasa Indonesia.\n\n"
            + "PENTING UNTUK DESKRIPSI TIAP LANGKAH (description):\n"
            + "Tulis deskripsi secara mendetail, bersih, terstruktur, dan tidak membosankan. "
            + "Gunakan pemformatan teks yang rapi dengan baris baru (newline) dan poin-poin agar mudah dibaca.\n"
            + "Di dalam tiap deskripsi langkah, cantumkan:\n"
            + "1. Apa yang dipelajari: penjelasan konsep inti secara sederhana.\n"
            + "2. Mengapa ini penting: manfaat konsep ini.\n"
            + "3. Aktivitas belajar: cara praktis mempelajarinya.\n\n"
            + f"Sesuaikan tingkat kesulitan, analogi, dan kedetailan penjelasan dengan jenjang pendidikan pengguna: {grade_level or 'sma'}.\n"
            + "- Jenjang SD: penjelasan super sederhana, ramah, penuh semangat, gunakan analogi menyenangkan, tanpa rumus rumit.\n"
            + "- Jenjang SMP: komunikatif, seru, tantang rasa ingin tahu, hubungkan dengan hal terdekat di sekitarnya.\n"
            + "- Jenjang SMA: penjelasan konseptual yang jelas, seimbangkan teori dan praktek.\n"
            + "- Jenjang Mahasiswa/Self Learner: mendalam, logis, terperinci, gunakan istilah standar industri/akademik."
        )
        
        roadmap_sys_prompt = (
            "Kamu adalah Buddio, mentor belajar AI yang ahli menyusun kurikulum dan peta belajar (roadmap) yang personal, terstruktur, dan pedagogis. "
            "Tugasmu adalah menyusun langkah belajar yang jelas, berurutan, dan terperinci dalam Bahasa Indonesia."
        )
        
        try:
            data = _generate_json(prompt, max_tokens=4096, system_instruction=roadmap_sys_prompt)
            data.setdefault("steps", [])
            return data, "gemini"
        except Exception as exc:  # noqa: BLE001
            logger.warning("Gemini roadmap failed, falling back to mock: %s", exc)
            return mock_ai.mock_roadmap(topic_title, goal), "mock"

    def generate_quiz(self, topic_title: str, grade_level: str = "sma", count: int = 5) -> Tuple[dict, str]:
        """Returns (quiz_dict, mode)."""
        if not _is_gemini_available():
            return mock_ai.mock_quiz(topic_title, count), "mock"

        prompt = (
            f"Buatkan kuis {count} soal pilihan ganda untuk topik '{topic_title}' jenjang {grade_level or 'umum'}. "
            "Setiap soal harus memiliki 4 pilihan jawaban. Kembalikan JSON dengan format: "
            '{"title": "...", "questions": [{"question": "...", "options": ["a","b","c","d"], '
            '"answer_index": <indeks benar>, "explanation": "..."}]}. '
            "Tulis semua dalam Bahasa Indonesia."
        )
        try:
            data = _generate_json(prompt, max_tokens=4096)
            data.setdefault("questions", [])
            data["questions"] = data["questions"][:count]
            return data, "gemini"
        except Exception as exc:  # noqa: BLE001
            logger.warning("Gemini quiz failed, falling back to mock: %s", exc)
            return mock_ai.mock_quiz(topic_title, count), "mock"

    def generate_lesson(
        self,
        step_title: str,
        topic_title: str,
        grade_level: str = "sma",
        step_description: str = "",
    ) -> Tuple[dict, str]:
        """Generate rich lesson content (materi) with YouTube video suggestions.

        Returns (lesson_dict, mode) where lesson_dict has:
            content: str   -- rich markdown materi
            videos: list   -- [{"title": "...", "url": "...", "description": "..."}]
        """
        if not _is_gemini_available():
            return mock_ai.mock_lesson(step_title, topic_title), "mock"

        prompt = (
            f'Buatkan materi pembelajaran untuk langkah "{step_title}" '
            f'dalam topik "{topic_title}" untuk jenjang {grade_level or "sma"}.\n\n'
            f"Deskripsi langkah: {step_description or '-'}\n\n"
            "Kembalikan JSON dengan format:\n"
            "{\n"
            '  "content": "...",\n'
            '  "videos": [\n'
            '    {"title": "Judul Video", "url": "https://www.youtube.com/watch?v=VIDEO_ID", "description": "Deskripsi singkat"}\n'
            "  ]\n"
            "}\n\n"
            "=================================================================\n"
            " SYARAT UTAMA: INSTRUCTIONAL COMPLETENESS & BREADTH OF TOPIC\n"
            "=================================================================\n\n"
            f"1. CAKUPAN TOPIK LENGKAP ({step_title}):\n"
            "   - Identifikasi SELURUH cakupan topik/langkah ini. Jika judulnya mencakup beberapa subtopik utama "
            "     (misal Data Preprocessing & Feature Engineering mencakup Data Cleaning, Transformation/Scaling, Encoding, Feature Engineering, Feature Selection, Dimensionality Reduction, dan Data Leakage), "
            "     MAKA kamu WAJIB memberikan gambaran dan penjelasan bertahap untuk SELURUH subtopik tersebut!\n"
            "   - DILARANG menghabiskan seluruh materi hanya untuk 1 sub-teknik kecil (misalnya hanya Feature Scaling saja), kecuali jika judul langkah memang sangat spesifik.\n\n"
            "2. ATURAN ANTI-DUMMY / ANTI-PLACEHOLDER (SANGAT KETAT):\n"
            "   - Sebuah bagian TIDAK LENGKAP hanya karena judulnya ada! Setiap bagian yang dibuat HARUS berisi konten nyata yang mengajarkan.\n"
            "   - DILARANG membuat header/callout kosong tanpa isi di bawahnya (misal `>[!tujuan]` tanpa bullet point, "
            "     atau `Langkah Perhitungan:` tanpa deretan hitungan, atau `Pembahasan & Jawaban:` tanpa solusi).\n"
            "   - Jika kamu membuat `Langkah Perhitungan:`, kamu WAJIB menuliskan hitungan matematikanya selangkah demi selangkah sampai hasil akhir!\n"
            "   - Jika kamu membuat `Pembahasan & Jawaban:`, kamu WAJIB menyertakan langkah penyelesaian dan jawaban akhirnya secara tegas!\n"
            "   - Jika kamu membuat `>[!tujuan]`, kamu WAJIB menyertakan minimal 3-5 poin tujuan terukur dengan kata kerja konkret!\n"
            "   - Jika kamu membuat `>[!ingat]`, kamu WAJIB menyertakan minimal 3-5 poin ringkasan pengetahuan substansial!\n\n"
            "3. WORKED EXAMPLE HARUS BENAR-BENAR DIKERJAKAN (FULLY WORKED):\n"
            "   - Tuliskan data awal, rumus/algoritma, substitusi nilai untuk SETIAP elemen data, hitungan langkah demi langkah, dan hasil akhirnya.\n"
            "   - Siswa harus bisa mengulangi perhitungan ini secara mandiri tanpa membutuhkan sumber tambahan.\n\n"
            "4. TRY IT YOURSELF (`>[!coba]`):\n"
            "   - Berikan SOAL latihan yang jelas + PEMBAHASAN LENGKAP (langkah penalaran, hitungan, jawaban akhir, dan alasan kebenarannya) yang dipisahkan garis `---`.\n\n"
            "5. PETA MENTAL (MENTAL MAP FIRST):\n"
            "   - Buka materi dengan diagram alur (ASCII flowchart) yang memetakan bagaimana seluruh subtopik saling terhubung.\n\n"
            "6. VALIDASI VIDEO YOUTUBE:\n"
            "   - Berikan video HANYA jika ID YouTube 11-karakter PASTI VALID dan BENAR-BENAR RELEVAN EDUKATIF. Jika ragu, kembalikan `\"videos\": []`.\n"
        )

        lesson_sys_prompt = (
            "Kamu adalah Buddio, AI Mentor & Tutor Pembelajaran terkemuka yang bertugas MENGAJAR siswa step-by-step.\n\n"
            "Prinsip Inti: Keutamaan Pembelajaran & Kelengkapan Konten (Instructional Completeness).\n"
            "Prioritas: Keakuratan → Pemahaman Bertahap (Sederhana → Teknis → Praktis) → Penerapan → Latihan.\n\n"
            "Aturan Emas:\n"
            "- Petakan seluruh cakupan topik secara seimbang, jangan mempersempit topik luas hanya menjadi satu sub-teknik kecil.\n"
            "- DILARANG menghasilkan header atau callout kosong di bawahnya tanpa isi/perhitungan/jawaban yang lengkap.\n"
            "- Contoh hitungan (worked example) harus dikerjakan tuntas dari awal hingga angka akhir.\n"
            "- Latihan `>[!coba]` harus berisi soal DAN jawaban/pembahasan lengkap."
        )

        try:
            data = _generate_json(prompt, max_tokens=8192, system_instruction=lesson_sys_prompt)
            raw_content = data.get("content", "")
            data["content"] = _sanitize_and_validate_lesson_content(raw_content, step_title, topic_title)
            data.setdefault("videos", [])
            return data, "gemini"
        except Exception as exc:  # noqa: BLE001
            logger.warning("Gemini lesson failed, falling back to mock: %s", exc)
            return mock_ai.mock_lesson(step_title, topic_title), "mock"


buddio_ai = BuddioAI()
