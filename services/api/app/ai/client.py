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

SYSTEM_PROMPT = (
    "Kamu adalah Buddio, mentor belajar AI yang ramah, sabar, dan pedagogis. "
    "Selalu jawab dalam Bahasa Indonesia. Sesuaikan tingkat bahasa dengan jenjang pengguna "
    "(SD, SMP, SMA, mahasiswa, self learner). "
    "Beri penjelasan bertahap, gunakan analogi sederhana, dan jangan langsung memberi jawaban "
    "final untuk soal latihan ujian — bimbing pengguna untuk sampai ke jawaban sendiri."
)


def _is_gemini_available() -> bool:
    return bool(settings.GEMINI_API_KEY) and not settings.FORCE_MOCK_AI


_gemini_client_instance = None


def _gemini_client():
    global _gemini_client_instance
    if _gemini_client_instance is None:
        from google import genai
        _gemini_client_instance = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _gemini_client_instance


def _generate_json(prompt: str, max_tokens: int = 2048, temperature: float = 0.6) -> dict:
    """Call Gemini and parse a JSON object from the response."""
    client = _gemini_client()
    from google.genai import types
    resp = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
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

        try:
            from google.genai import types
            resp = _gemini_client().models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT, max_output_tokens=2048, temperature=0.6
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
            f"Buatkan roadmap belajar untuk topik '{topic_title}' untuk jenjang {grade_level or 'umum'}."
            + (f" Tujuan: {goal}." if goal else "")
            + " Kembalikan JSON dengan format: "
            + '{"title": "...", "difficulty": "Mudah|Menengah|Sulit", "estimated_hours": <angka>, '
            + '"steps": [{"order_number": 1, "title": "...", "description": "..."}]}. '
            + "Buat 5-7 langkah yang berurutan, deskripsi dalam Bahasa Indonesia."
        )
        try:
            data = _generate_json(prompt, max_tokens=4096)
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


buddio_ai = BuddioAI()
