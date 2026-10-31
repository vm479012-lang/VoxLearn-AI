"""
Personalized Practice, Misconception Analysis, and Analytics Router
"""

from collections import Counter
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Concept, LearnerMastery, Misconception, QuestionResponse, Question
from ..misconception_engine import MISCONCEPTION_CATALOG

router = APIRouter(prefix="/practice", tags=["Personalized Practice & Misconceptions"])

@router.get("/misconceptions")
def get_all_misconceptions(user_id: int = 1, db: Session = Depends(get_db)):
    # Query all responses to count how often each misconception was triggered
    responses = db.query(QuestionResponse).filter(
        QuestionResponse.user_id == user_id,
        QuestionResponse.is_correct == False,
        QuestionResponse.misconception_id != None
    ).all()

    trigger_counts = Counter([r.misconception_id for r in responses])

    catalog_list = []
    for m_id, data in MISCONCEPTION_CATALOG.items():
        # Find linked concept name if possible
        misc_record = db.query(Misconception).filter(Misconception.id == m_id).first()
        concept_name = "General Physics"
        if misc_record and misc_record.concept:
            concept_name = misc_record.concept.name

        catalog_list.append({
            "id": m_id,
            "category": data["category"],
            "title": data["title"],
            "description": data["description"],
            "why_it_happens": data["why_it_happens"],
            "physical_reality": data["physical_reality"],
            "remedy_tip": data["remedy_tip"],
            "concept_name": concept_name,
            "triggered_count": trigger_counts.get(m_id, 0)
        })

    # Sort by most triggered first
    catalog_list.sort(key=lambda x: x["triggered_count"], reverse=True)
    return catalog_list

@router.get("/weak_workout")
def get_personalized_workout(user_id: int = 1, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Find concepts with p_l < 0.65
    masteries = (
        db.query(LearnerMastery)
        .filter(LearnerMastery.user_id == user_id)
        .order_by(LearnerMastery.p_l.asc())
        .limit(3)
        .all()
    )

    weak_concept_ids = [m.concept_id for m in masteries]

    # Find targeted questions for these weak concepts
    questions = (
        db.query(Question)
        .filter(Question.concept_id.in_(weak_concept_ids))
        .limit(5)
        .all()
    )

    if not questions:
        questions = db.query(Question).limit(5).all()

    cards = []
    for q in questions:
        concept = db.query(Concept).filter(Concept.id == q.concept_id).first()
        cards.append({
            "question_id": q.id,
            "concept_id": q.concept_id,
            "concept_name": concept.name if concept else "Physics Concept",
            "topic": q.topic,
            "question_text": q.question_text,
            "options": [opt["text"] for opt in q.options],
            "difficulty": q.difficulty,
            "bloom_level": q.bloom_level,
            "formula_hint": q.formula_hint,
            "analogy": concept.real_world_analogy if concept else ""
        })

    return {
        "workout_id": f"workout_{user.id}",
        "target_concepts": [
            {
                "id": m.concept_id,
                "mastery_percentage": round(m.p_l * 100, 1),
                "status": m.status
            }
            for m in masteries
        ],
        "question_count": len(cards),
        "questions": cards
    }

@router.get("/analytics")
def get_progress_analytics(user_id: int = 1, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    masteries = db.query(LearnerMastery).filter(LearnerMastery.user_id == user_id).all()
    responses = db.query(QuestionResponse).filter(QuestionResponse.user_id == user_id).all()

    # Accuracy by difficulty
    diff_stats = {1: [0, 0], 2: [0, 0], 3: [0, 0], 4: [0, 0], 5: [0, 0]}
    for r in responses:
        if r.question:
            diff = r.question.difficulty
            diff_stats[diff][1] += 1
            if r.is_correct:
                diff_stats[diff][0] += 1

    accuracy_by_difficulty = [
        {
            "difficulty": f"Level {d}",
            "accuracy": round((diff_stats[d][0] / max(1, diff_stats[d][1])) * 100, 1) if diff_stats[d][1] > 0 else 75.0,
            "attempts": diff_stats[d][1]
        }
        for d in range(1, 6)
    ]

    # Misconception category breakdown
    category_counts = {"conceptual": 0, "formula_application": 0, "calculation_unit": 0, "misreading": 0}
    for r in responses:
        if not r.is_correct and r.misconception_id:
            misc_info = MISCONCEPTION_CATALOG.get(r.misconception_id)
            if misc_info:
                cat = misc_info.get("category", "conceptual")
                category_counts[cat] = category_counts.get(cat, 0) + 1

    misconception_distribution = [
        {"name": "Conceptual", "value": max(2, category_counts["conceptual"]), "color": "#ef4444"},
        {"name": "Formula Application", "value": max(3, category_counts["formula_application"]), "color": "#f59e0b"},
        {"name": "Calculation & Units", "value": max(1, category_counts["calculation_unit"]), "color": "#3b82f6"},
        {"name": "Misreading Traps", "value": max(1, category_counts["misreading"]), "color": "#8b5cf6"}
    ]

    # Bloom's level distribution
    bloom_stats = {}
    for m in masteries:
        if m.concept:
            b = m.concept.bloom_level
            if b not in bloom_stats:
                bloom_stats[b] = []
            bloom_stats[b].append(m.p_l * 100)

    bloom_mastery = [
        {"bloom": b, "average_mastery": round(sum(vals)/len(vals), 1)}
        for b, vals in bloom_stats.items()
    ]

    return {
        "user_id": user.id,
        "total_responses": len(responses),
        "accuracy_by_difficulty": accuracy_by_difficulty,
        "misconception_distribution": misconception_distribution,
        "bloom_mastery": bloom_mastery,
        "streak_days": user.streak_days,
        "total_minutes": user.total_study_minutes,
        "points": user.points
    }
