"""
Concept Mastery Tracking and Knowledge Graph router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Concept, LearnerMastery, Misconception
from ..learner_model import propagate_prerequisite_knowledge

router = APIRouter(prefix="/mastery", tags=["Concept Mastery & Knowledge Graph"])

@router.get("/overview")
def get_mastery_overview(user_id: int = 1, db: Session = Depends(get_db)):
    concepts = db.query(Concept).order_by(Concept.order_index.asc()).all()
    masteries = db.query(LearnerMastery).filter(LearnerMastery.user_id == user_id).all()
    mastery_map = {m.concept_id: m for m in masteries}

    result = []
    for c in concepts:
        m = mastery_map.get(c.id)
        p_l = m.p_l if m else 0.25
        status = m.status if m else "not_started"
        result.append({
            "id": c.id,
            "topic": c.topic,
            "unit_code": c.unit_code,
            "name": c.name,
            "description": c.description,
            "bloom_level": c.bloom_level,
            "prerequisites": c.prerequisites,
            "formulas": c.formulas,
            "real_world_analogy": c.real_world_analogy,
            "p_l": round(p_l, 4),
            "mastery_percentage": round(p_l * 100, 1),
            "status": status,
            "total_attempts": m.total_attempts if m else 0,
            "correct_attempts": m.correct_attempts if m else 0,
            "confidence_avg": m.confidence_avg if m else 3.0
        })

    return result

@router.get("/graph")
def get_knowledge_graph(user_id: int = 1, db: Session = Depends(get_db)):
    concepts = db.query(Concept).order_by(Concept.order_index.asc()).all()
    masteries = db.query(LearnerMastery).filter(LearnerMastery.user_id == user_id).all()
    mastery_map = {m.concept_id: m.p_l for m in masteries}

    nodes = []
    edges = []

    for c in concepts:
        p_l = mastery_map.get(c.id, 0.25)
        status = "mastered" if p_l >= 0.80 else ("in_progress" if p_l >= 0.50 else "needs_review")
        nodes.append({
            "id": c.id,
            "label": c.name,
            "topic": c.topic,
            "unit_code": c.unit_code,
            "mastery": round(p_l * 100, 1),
            "status": status,
            "bloom": c.bloom_level
        })

        for p_id in c.prerequisites:
            edges.append({
                "source": p_id,
                "target": c.id,
                "label": "requires"
            })

    return {
        "nodes": nodes,
        "edges": edges,
        "total_nodes": len(nodes),
        "total_edges": len(edges)
    }

@router.get("/concept/{concept_id}")
def get_concept_detail(concept_id: str, user_id: int = 1, db: Session = Depends(get_db)):
    concept = db.query(Concept).filter(Concept.id == concept_id).first()
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")

    mastery = db.query(LearnerMastery).filter(
        LearnerMastery.user_id == user_id,
        LearnerMastery.concept_id == concept_id
    ).first()

    p_l = mastery.p_l if mastery else 0.25

    # Check prerequisites
    all_concepts = db.query(Concept).all()
    c_map = {c.id: {"name": c.name, "prerequisites": c.prerequisites} for c in all_concepts}
    all_masteries = db.query(LearnerMastery).filter(LearnerMastery.user_id == user_id).all()
    m_map = {m.concept_id: m.p_l for m in all_masteries}

    prereq_eval = propagate_prerequisite_knowledge(concept_id, c_map, m_map)

    # Get linked misconceptions
    misconceptions = db.query(Misconception).filter(Misconception.concept_id == concept_id).all()

    return {
        "id": concept.id,
        "topic": concept.topic,
        "name": concept.name,
        "description": concept.description,
        "bloom_level": concept.bloom_level,
        "prerequisites": concept.prerequisites,
        "formulas": concept.formulas,
        "real_world_analogy": concept.real_world_analogy,
        "mastery_percentage": round(p_l * 100, 1),
        "p_l": round(p_l, 4),
        "status": mastery.status if mastery else "not_started",
        "prerequisite_check": prereq_eval,
        "misconceptions": [
            {
                "id": m.id,
                "title": m.title,
                "category": m.category,
                "description": m.description,
                "why_it_happens": m.why_it_happens,
                "remedy_tip": m.remedy_tip
            }
            for m in misconceptions
        ]
    }
