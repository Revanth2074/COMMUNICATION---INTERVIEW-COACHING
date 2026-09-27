"""
AI-Powered Communication & Interview Coaching System
FastAPI Backend Server

Routes:
  - /api/models          → List available OmniRoute models
  - /api/questions       → Get/generate interview questions
  - /api/evaluate        → Quick single-agent evaluation
  - /api/coach           → Full multi-agent coaching evaluation
  - /api/follow-up       → Generate follow-up questions
  - /api/progress        → Get progress report
  - /api/sessions        → Session management
  - /api/roles           → Available roles
  - /api/speech-to-text  → Convert voice to text
"""
import uuid
import json
from datetime import datetime
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config import settings
from llm_client import llm_client
from models import (
    CandidateProfile, InterviewQuestion, CandidateResponse,
    EvaluationResult, CoachingFeedback, PracticeSession, ProgressReport,
    QuestionRequest,
)
from agents import coach_agent, question_agent
from question_bank import get_questions, get_random_question, generate_question_with_ai


# ──────────────────────────────────────────────────────────────
# In-memory session store (for demo; replace with DB in production)
# ──────────────────────────────────────────────────────────────
sessions_store: dict[str, list[dict]] = {}
profiles_store: dict[str, CandidateProfile] = {}


# ──────────────────────────────────────────────────────────────
# App Lifecycle
# ──────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: discover OmniRoute models."""
    print("[START] Starting Interview Coaching Backend...")
    print(f"[OmniRoute] Base URL: {settings.OMNIROUTE_BASE_URL}")
    models = await llm_client.discover_models()
    print(f"[READY] Ready with {len(models)} model(s) available")
    yield
    print("[STOP] Shutting down Interview Coaching Backend...")


app = FastAPI(
    title="AI Interview Coaching API",
    description="Multi-agent interview coaching system powered by OmniRoute",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ──────────────────────────────────────────────────────────────
# Request Models
# ──────────────────────────────────────────────────────────────
class EvaluateRequest(BaseModel):
    question: str
    response: str
    question_id: str = ""
    expected_competencies: list[str] = []
    candidate_profile: Optional[CandidateProfile] = None
    session_id: str = ""
    reference_answer: Optional[str] = ""


class FollowUpRequest(BaseModel):
    question: str
    response: str
    candidate_profile: Optional[CandidateProfile] = None


class ProgressRequest(BaseModel):
    session_id: str


# ──────────────────────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────────────────────

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "models": llm_client.available_models}


@app.get("/api/models")
async def get_models():
    """List available OmniRoute models."""
    return {
        "models": llm_client.available_models,
        "default_model": llm_client.default_model,
    }


@app.get("/api/roles")
async def get_roles():
    """Get available interview roles."""
    return {
        "roles": settings.ROLES,
        "question_types": settings.QUESTION_TYPES,
        "difficulty_levels": settings.DIFFICULTY_LEVELS,
    }


@app.post("/api/questions")
async def get_question(request: QuestionRequest):
    """Get an interview question (from CSV bank or AI-generated based on role)."""
    try:
        question = await generate_question_with_ai(
            role=request.role,
            competency=request.competency,
            difficulty=request.difficulty,
            candidate_profile=request.candidate_profile,
            source_preference=request.source_preference or "auto",
        )
        return {"question": question.model_dump(), "source": question.source}
    except Exception as e:
        print(f"Question fetch failed, using fallback: {e}")
        question = get_random_question(
            role=request.role,
            difficulty=request.difficulty,
            candidate_profile=request.candidate_profile,
        )
        return {"question": question.model_dump(), "source": "question_bank"}


@app.get("/api/questions/bank")
async def get_question_bank(
    role: str = "",
    competency: str = "",
    difficulty: str = "",
    question_type: str = "",
):
    """Browse the question bank with filters."""
    questions = get_questions(
        role=role or None,
        competency=competency or None,
        difficulty=difficulty or None,
        question_type=question_type or None,
    )
    return {"questions": [q.model_dump() for q in questions], "total": len(questions)}


@app.post("/api/evaluate")
async def evaluate_response(request: EvaluateRequest):
    """Quick single-agent evaluation."""
    try:
        result = await coach_agent.quick_evaluate(
            question=request.question,
            response=request.response,
            reference_answer=request.reference_answer,
        )

        # Store session data
        if request.session_id:
            if request.session_id not in sessions_store:
                sessions_store[request.session_id] = []
            sessions_store[request.session_id].append({
                "timestamp": datetime.now().isoformat(),
                "question": request.question,
                "response": request.response,
                "score": result.overall_score,
                "strengths": result.strengths,
                "improvements": result.areas_for_improvement,
                "type": "quick_eval",
            })

        return {"evaluation": result.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/coach")
async def coach_response(request: EvaluateRequest):
    """Full multi-agent coaching evaluation."""
    try:
        # Gather session history for recurring gap detection
        session_history = None
        if request.session_id and request.session_id in sessions_store:
            session_history = sessions_store[request.session_id]

        feedback = await coach_agent.evaluate_response(
            question=request.question,
            response=request.response,
            expected_competencies=request.expected_competencies,
            candidate_profile=request.candidate_profile,
            session_history=session_history,
            reference_answer=request.reference_answer,
        )

        # Store session data
        if request.session_id:
            if request.session_id not in sessions_store:
                sessions_store[request.session_id] = []
            sessions_store[request.session_id].append({
                "timestamp": datetime.now().isoformat(),
                "question": request.question,
                "response": request.response,
                "score": feedback.overall_score,
                "strengths": feedback.consolidated_strengths,
                "improvements": feedback.consolidated_improvements,
                "type": "full_coaching",
            })

        return {"coaching": feedback.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/follow-up")
async def get_follow_up_questions(request: FollowUpRequest):
    """Generate follow-up questions based on the candidate's response."""
    try:
        follow_ups = await question_agent.generate_follow_up(
            original_question=request.question,
            candidate_response=request.response,
            profile=request.candidate_profile,
        )
        return {"follow_up_questions": follow_ups}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/sessions/create")
async def create_session(profile: Optional[CandidateProfile] = None):
    """Create a new practice session."""
    session_id = str(uuid.uuid4())[:12]
    sessions_store[session_id] = []
    if profile:
        profiles_store[session_id] = profile
    return {"session_id": session_id, "created_at": datetime.now().isoformat()}


@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str):
    """Get session history."""
    if session_id not in sessions_store:
        raise HTTPException(status_code=404, detail="Session not found")
    return {
        "session_id": session_id,
        "history": sessions_store[session_id],
        "total_practices": len(sessions_store[session_id]),
    }


@app.get("/api/progress/{session_id}")
async def get_progress(session_id: str):
    """Get progress report for a session."""
    if session_id not in sessions_store or not sessions_store[session_id]:
        raise HTTPException(status_code=404, detail="Session not found or no practice data")

    history = sessions_store[session_id]
    scores = [h["score"] for h in history]
    all_strengths = []
    all_improvements = []
    for h in history:
        all_strengths.extend(h.get("strengths", []))
        all_improvements.extend(h.get("improvements", []))

    # Find recurring items
    from collections import Counter
    strength_counts = Counter(all_strengths)
    improvement_counts = Counter(all_improvements)

    top_strengths = [s for s, c in strength_counts.most_common(5)]
    persistent_gaps = [g for g, c in improvement_counts.most_common(5) if c >= 1]

    avg_score = sum(scores) / len(scores) if scores else 0

    # Generate AI recommendations based on progress
    recommendations = []
    if avg_score < 5:
        recommendations.append("Focus on fundamentals: structure your answers using the STAR method")
    if avg_score >= 5 and avg_score < 7:
        recommendations.append("Good progress! Work on adding specific examples and metrics to your answers")
    if avg_score >= 7:
        recommendations.append("Excellent performance! Practice with more difficult questions to keep improving")

    return {
        "progress": ProgressReport(
            total_sessions=len(history),
            average_score=round(avg_score, 1),
            score_trend=scores,
            top_strengths=top_strengths,
            persistent_gaps=persistent_gaps,
            improvement_areas=dict(improvement_counts.most_common(10)),
            recommendations=recommendations,
        ).model_dump()
    }


@app.post("/api/speech-to-text")
async def speech_to_text(audio: UploadFile = File(...)):
    """Convert uploaded audio to text using SpeechRecognition."""
    try:
        import speech_recognition as sr
        import tempfile
        import os

        # Save uploaded file temporarily
        temp_path = os.path.join(tempfile.gettempdir(), f"audio_{uuid.uuid4()}.wav")
        content = await audio.read()
        with open(temp_path, "wb") as f:
            f.write(content)

        # Recognize speech
        recognizer = sr.Recognizer()
        with sr.AudioFile(temp_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)

        # Clean up
        os.unlink(temp_path)

        return {"text": text, "success": True}
    except Exception as e:
        return {"text": "", "success": False, "error": str(e)}


# ──────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
    )
