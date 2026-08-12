from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.topic import Topic
from app.models.quiz import Quiz, QuizQuestion, QuizAttempt
from app.ai import buddio_ai
from app.services.usage_service import UsageService


class AssessmentService:
    def __init__(self, db: Session):
        self.db = db

    def _get_owned_topic(self, user: User, topic_id: int) -> Topic:
        topic = self.db.query(Topic).filter(Topic.id == topic_id, Topic.user_id == user.id).first()
        if not topic:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topik tidak ditemukan.")
        return topic

    def _get_owned_quiz(self, user: User, quiz_id: int) -> Quiz:
        quiz = (
            self.db.query(Quiz)
            .join(Topic, Quiz.topic_id == Topic.id)
            .filter(Quiz.id == quiz_id, Topic.user_id == user.id)
            .first()
        )
        if not quiz:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kuis tidak ditemukan.")
        return quiz

    def generate(self, user: User, topic_id: int, count: int = 5) -> dict:
        topic = self._get_owned_topic(user, topic_id)
        UsageService(self.db).check_and_decrement(user, "quiz")

        data, mode = buddio_ai.generate_quiz(topic.title, user.grade_level or "sma", count)

        quiz = Quiz(topic_id=topic.id, title=data.get("title", f"Kuis {topic.title}"), generated_by_ai=True)
        self.db.add(quiz)
        self.db.flush()

        for q in data.get("questions", []):
            question = QuizQuestion(
                quiz_id=quiz.id,
                question=q.get("question", ""),
                options=q.get("options"),
                answer_index=q.get("answer_index"),
                answer_key=q.get("answer_key"),
                explanation=q.get("explanation"),
            )
            self.db.add(question)

        self.db.commit()
        self.db.refresh(quiz)
        return self.serialize(quiz, mode=mode)

    def list_for_topic(self, user: User, topic_id: int) -> list:
        self._get_owned_topic(user, topic_id)
        quizzes = (
            self.db.query(Quiz)
            .filter(Quiz.topic_id == topic_id)
            .order_by(Quiz.created_at.desc())
            .all()
        )
        return [self.serialize(q, mode="cached", include_answers=False) for q in quizzes]

    def get(self, user: User, quiz_id: int) -> dict:
        quiz = self._get_owned_quiz(user, quiz_id)
        return self.serialize(quiz, mode="cached", include_answers=False)

    def submit(self, user: User, quiz_id: int, answers: dict) -> dict:
        quiz = self._get_owned_quiz(user, quiz_id)
        questions = quiz.questions
        total = len(questions)
        score = 0
        details = []

        for q in questions:
            selected = answers.get(str(q.id), answers.get(q.id))
            correct = (q.answer_index is not None and selected == q.answer_index)
            if correct:
                score += 1
            details.append(
                {
                    "question_id": q.id,
                    "question": q.question,
                    "your_answer": selected,
                    "correct": correct,
                    "correct_answer": q.answer_index,
                    "explanation": q.explanation,
                }
            )

        pct = round((score / total) * 100) if total else 0
        feedback = (
            f"Skor kamu {score}/{total} ({pct}%). "
            + ("Kerja bagus! Konsep ini sudah cukup kuat." if pct >= 80 else "Jangan menyerah! Ulangi bagian yang salah lalu coba lagi.")
        )

        attempt = QuizAttempt(
            quiz_id=quiz.id,
            user_id=user.id,
            score=score,
            total=total,
            feedback=feedback,
            answers=answers,
        )
        self.db.add(attempt)
        self.db.commit()
        self.db.refresh(attempt)

        return {
            "id": attempt.id,
            "quiz_id": attempt.quiz_id,
            "score": attempt.score,
            "total": attempt.total,
            "feedback": attempt.feedback,
            "created_at": attempt.created_at,
            "details": details,
        }

    def get_attempt(self, user: User, attempt_id: int) -> dict:
        attempt = (
            self.db.query(QuizAttempt)
            .filter(QuizAttempt.id == attempt_id, QuizAttempt.user_id == user.id)
            .first()
        )
        if not attempt:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Percobaan kuis tidak ditemukan.")
        return {
            "id": attempt.id,
            "quiz_id": attempt.quiz_id,
            "score": attempt.score,
            "total": attempt.total,
            "feedback": attempt.feedback,
            "created_at": attempt.created_at,
        }

    def serialize(self, quiz: Quiz, mode: str = "cached", include_answers: bool = True) -> dict:
        questions = []
        for q in quiz.questions:
            item = {
                "id": q.id,
                "question": q.question,
                "options": q.options,
                "explanation": q.explanation,
            }
            if include_answers:
                item["answer_index"] = q.answer_index
            questions.append(item)
        return {
            "id": quiz.id,
            "topic_id": quiz.topic_id,
            "title": quiz.title,
            "generated_by_ai": quiz.generated_by_ai,
            "mode": mode,
            "created_at": quiz.created_at,
            "questions": questions,
        }
