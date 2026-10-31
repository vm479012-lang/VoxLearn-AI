"""
Adaptive Quiz Router with IRT question selection, BKT knowledge updates, and misconception analysis.
"""

import uuid
import datetime
import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Question, QuizSession, QuestionResponse, LearnerMastery, StudyActivity, Concept
from ..schemas import QuizStartRequest, QuizSessionResponse, QuestionSubmitRequest, QuestionEvaluationResponse
from ..learner_model import BayesianKnowledgeTracer, ItemResponseTheory
from ..misconception_engine import MisconceptionEngine

router = APIRouter(prefix="/quiz", tags=["Adaptive Quiz"])

@router.post("/start", response_model=QuizSessionResponse)
def start_quiz(req: QuizStartRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == req.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    session_id = f"quiz_{uuid.uuid4().hex[:10]}"

    # Query candidate questions
    q_query = db.query(Question)
    if req.topic:
        q_query = q_query.filter(Question.topic == req.topic)
    if req.concept_id:
        q_query = q_query.filter(Question.concept_id == req.concept_id)

    candidates = q_query.all()
    if not candidates:
        # Fallback to all questions
        candidates = db.query(Question).all()

    # Calculate user ability theta using IRT from current masteries
    masteries = db.query(LearnerMastery).filter(LearnerMastery.user_id == user.id).all()
    mastery_vals = [m.p_l for m in masteries] if masteries else [0.5]
    theta = ItemResponseTheory.estimate_ability(mastery_vals)

    # Convert candidates to dict format for IRT selection
    q_dicts = [
        {
            "id": q.id,
            "concept_id": q.concept_id,
            "topic": q.topic,
            "question_text": q.question_text,
            "options": [opt["text"] for opt in q.options],
            "difficulty": q.difficulty,
            "bloom_level": q.bloom_level,
            "formula_hint": q.formula_hint or ""
        }
        for q in candidates
    ]

    selected_questions = []
    num_to_pick = min(req.num_questions, len(q_dicts))

    # Adaptive selection: pick first question near ZPD, then mix adjacent difficulties
    if req.quiz_type == "adaptive":
        # Sort questions by distance to target difficulty for user's ability
        q_dicts_sorted = sorted(
            q_dicts,
            key=lambda q: abs(ItemResponseTheory.probability_correct(theta, q["difficulty"]) - 0.70)
        )
        selected_questions = q_dicts_sorted[:num_to_pick]
        random.shuffle(selected_questions)
    elif req.quiz_type == "weak_practice":
        # Sort by lowest concept mastery
        weak_c_ids = {m.concept_id for m in masteries if m.p_l < 0.60}
        weak_qs = [q for q in q_dicts if q["concept_id"] in weak_c_ids]
        selected_questions = (weak_qs + [q for q in q_dicts if q not in weak_qs])[:num_to_pick]
    else:
        # Diagnostic / standard
        selected_questions = random.sample(q_dicts, num_to_pick)

    # Create session record
    session = QuizSession(
        id=session_id,
        user_id=user.id,
        quiz_type=req.quiz_type,
        topic=req.topic or "Class 10 Physics Adaptive",
        score=0,
        total_questions=len(selected_questions),
        difficulty_average=round(sum(q["difficulty"] for q in selected_questions) / max(1, len(selected_questions)), 1)
    )
    db.add(session)
    db.commit()

    return QuizSessionResponse(
        session_id=session_id,
        user_id=user.id,
        quiz_type=req.quiz_type,
        topic=session.topic,
        total_questions=len(selected_questions),
        questions=selected_questions
    )

@router.post("/submit_answer", response_model=QuestionEvaluationResponse)
def submit_question_answer(req: QuestionSubmitRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == req.user_id).first()
    question = db.query(Question).filter(Question.id == req.question_id).first()

    if not user or not question:
        raise HTTPException(status_code=404, detail="User or Question not found")

    options = question.options
    if req.selected_option_index < 0 or req.selected_option_index >= len(options):
        raise HTTPException(status_code=400, detail="Invalid option index")

    selected_opt = options[req.selected_option_index]
    is_correct = selected_opt.get("is_correct", False)
    misc_id = selected_opt.get("misconception_id")

    # Find correct option index
    correct_idx = next((i for i, opt in enumerate(options) if opt.get("is_correct")), 0)

    # Run Misconception Diagnostics
    q_dict = {
        "options": options,
        "explanation": question.explanation,
        "formula_hint": question.formula_hint,
        "bloom_level": question.bloom_level
    }
    diag = MisconceptionEngine.diagnose_response(q_dict, req.selected_option_index)

    # Retrieve or initialize LearnerMastery for this concept
    mastery = db.query(LearnerMastery).filter(
        LearnerMastery.user_id == user.id,
        LearnerMastery.concept_id == question.concept_id
    ).first()

    if not mastery:
        mastery = LearnerMastery(
            user_id=user.id,
            concept_id=question.concept_id,
            p_l=0.30,
            p_transit=0.18,
            p_slip=0.10,
            p_guess=0.20
        )
        db.add(mastery)

    prev_p_l = mastery.p_l

    # Apply Bayesian Knowledge Tracing (BKT) update with student confidence
    bkt_update = BayesianKnowledgeTracer.update_mastery(
        p_l=prev_p_l,
        is_correct=is_correct,
        p_transit=mastery.p_transit,
        p_slip=mastery.p_slip,
        p_guess=mastery.p_guess,
        confidence_level=req.confidence_level
    )

    # Persist updated parameters
    mastery.p_l = bkt_update["updated_p_l"]
    mastery.status = bkt_update["status"]
    mastery.total_attempts += 1
    if is_correct:
        mastery.correct_attempts += 1
        mastery.consecutive_correct += 1
    else:
        mastery.consecutive_correct = 0

    mastery.confidence_avg = round((mastery.confidence_avg * 0.7) + (req.confidence_level * 0.3), 2)
    mastery.last_practiced = datetime.datetime.utcnow()

    # Log question response
    resp = QuestionResponse(
        quiz_session_id=req.quiz_session_id or f"direct_{uuid.uuid4().hex[:8]}",
        user_id=user.id,
        question_id=question.id,
        selected_option_index=req.selected_option_index,
        is_correct=is_correct,
        confidence_level=req.confidence_level,
        time_taken_seconds=req.time_taken_seconds,
        misconception_id=misc_id
    )
    db.add(resp)

    # Update session score if session exists
    if req.quiz_session_id:
        session = db.query(QuizSession).filter(QuizSession.id == req.quiz_session_id).first()
        if session and is_correct:
            session.score += 1

    db.commit()

    return QuestionEvaluationResponse(
        question_id=question.id,
        is_correct=is_correct,
        correct_option_index=correct_idx,
        selected_option_index=req.selected_option_index,
        explanation=question.explanation,
        formula_hint=question.formula_hint or "",
        misconception_found=diag.get("misconception_found", False),
        misconception_title=diag.get("title"),
        misconception_category=diag.get("category"),
        why_it_happens=diag.get("why_it_happens"),
        physical_reality=diag.get("physical_reality"),
        remedy_tip=diag.get("remedy_tip"),
        concept_id=question.concept_id,
        previous_p_l=round(prev_p_l, 4),
        updated_p_l=round(bkt_update["updated_p_l"], 4),
        mastery_percentage=bkt_update["mastery_percentage"],
        mastery_delta=bkt_update["delta"],
        new_status=bkt_update["status"]
    )

@router.post("/complete/{session_id}")
def complete_quiz_session(session_id: str, db: Session = Depends(get_db)):
    session = db.query(QuizSession).filter(QuizSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    session.completed_at = datetime.datetime.utcnow()
    total = max(1, session.total_questions)
    accuracy = round((session.score / total) * 100, 1)
    session.accuracy_percentage = accuracy

    user = db.query(User).filter(User.id == session.user_id).first()
    points_earned = (session.score * 20) + 10
    if user:
        user.points += points_earned
        user.total_study_minutes += 5

        activity = StudyActivity(
            user_id=user.id,
            activity_type="quiz",
            title=f"Completed {session.topic}",
            description=f"Scored {session.score}/{session.total_questions} ({accuracy}% accuracy)",
            points=points_earned
        )
        db.add(activity)

    db.commit()

    return {
        "session_id": session.id,
        "score": session.score,
        "total_questions": session.total_questions,
        "accuracy_percentage": accuracy,
        "points_earned": points_earned,
        "completed_at": session.completed_at.strftime("%b %d, %H:%M")
    }
