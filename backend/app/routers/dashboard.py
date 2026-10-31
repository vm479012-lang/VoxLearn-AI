"""
Dashboard API router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Concept, LearnerMastery, StudyActivity, QuizSession
from ..schemas import DashboardSummaryResponse

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary", response_model=DashboardSummaryResponse)
def get_dashboard_summary(user_id: int = 1, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    concepts = db.query(Concept).all()
    masteries = db.query(LearnerMastery).filter(LearnerMastery.user_id == user_id).all()
    mastery_map = {m.concept_id: m for m in masteries}

    total_concepts = len(concepts) if concepts else 1
    mastered_count = 0
    in_progress_count = 0
    needs_review_count = 0
    sum_mastery = 0.0

    topic_stats = {}
    weak_concept_list = []

    for c in concepts:
        m = mastery_map.get(c.id)
        p_l = m.p_l if m else 0.25
        sum_mastery += p_l

        topic_name = c.topic
        if topic_name not in topic_stats:
            topic_stats[topic_name] = {"total": 0, "sum_p_l": 0.0, "concepts": []}
        topic_stats[topic_name]["total"] += 1
        topic_stats[topic_name]["sum_p_l"] += p_l
        topic_stats[topic_name]["concepts"].append({"id": c.id, "name": c.name, "mastery": round(p_l * 100, 1)})

        if p_l >= 0.80:
            mastered_count += 1
        elif p_l >= 0.50:
            in_progress_count += 1
        else:
            needs_review_count += 1
            weak_concept_list.append({
                "concept_id": c.id,
                "name": c.name,
                "topic": c.topic,
                "mastery_percentage": round(p_l * 100, 1),
                "remedy_focus": c.real_world_analogy or "Review foundational formula"
            })

    overall_mastery = round((sum_mastery / total_concepts) * 100, 1)

    # Sort weak concepts by lowest mastery first
    weak_concept_list.sort(key=lambda x: x["mastery_percentage"])

    # Build topic breakdown
    topic_breakdown = []
    for topic_name, data in topic_stats.items():
        avg = round((data["sum_p_l"] / data["total"]) * 100, 1) if data["total"] else 0.0
        status = "Strong" if avg >= 75 else ("Fair" if avg >= 50 else "Attention Needed")
        topic_breakdown.append({
            "topic": topic_name,
            "mastery_percentage": avg,
            "total_concepts": data["total"],
            "status": status,
            "concepts": data["concepts"]
        })

    # Recent activities
    activities = (
        db.query(StudyActivity)
        .filter(StudyActivity.user_id == user_id)
        .order_by(StudyActivity.created_at.desc())
        .limit(6)
        .all()
    )
    recent_activities = [
        {
            "id": act.id,
            "type": act.activity_type,
            "title": act.title,
            "description": act.description,
            "points": act.points,
            "created_at": act.created_at.strftime("%b %d, %H:%M")
        }
        for act in activities
    ]

    # Dynamic recommendation
    if weak_concept_list:
        target = weak_concept_list[0]
        daily_rec = {
            "title": f"Targeted Sprint: {target['name']}",
            "description": f"Your mastery is {target['mastery_percentage']}%. Strengthen this concept with a 3-minute Socratic practice session to boost overall exam score.",
            "action_type": "practice",
            "concept_id": target["concept_id"],
            "estimated_minutes": 5,
            "target_topic": target["topic"]
        }
    else:
        daily_rec = {
            "title": "Mastery Challenge: Comprehensive Class 10 Simulation",
            "description": "All core concepts are in strong standing! Take a full-length adaptive simulation quiz to solidify top percentile rank.",
            "action_type": "adaptive_quiz",
            "concept_id": None,
            "estimated_minutes": 10,
            "target_topic": "All Physics"
        }

    # Exam readiness heuristic: combines mastery %, consistency, and depth
    exam_readiness = round(min(98.5, max(30.0, overall_mastery * 0.9 + user.streak_days * 1.5)), 1)

    return {
        "user": user,
        "overall_mastery_percentage": overall_mastery,
        "mastered_count": mastered_count,
        "in_progress_count": in_progress_count,
        "needs_review_count": needs_review_count,
        "total_concepts": total_concepts,
        "estimated_exam_readiness": exam_readiness,
        "topic_breakdown": topic_breakdown,
        "weak_concepts": weak_concept_list[:4],
        "recent_activities": recent_activities,
        "daily_recommendation": daily_rec
    }
