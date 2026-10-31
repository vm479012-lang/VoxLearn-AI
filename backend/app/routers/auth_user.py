"""
User and Onboarding router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, LearnerMastery, Concept, StudyActivity
from ..schemas import UserResponse, OnboardingRequest
from ..learner_model import BayesianKnowledgeTracer

router = APIRouter(prefix="/user", tags=["User & Onboarding"])

@router.get("/profile", response_model=UserResponse)
def get_user_profile(user_id: int = 1, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/onboarding")
def complete_onboarding(data: OnboardingRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == 1).first()
    if not user:
        user = User(id=1)
        db.add(user)

    user.name = data.name
    user.target_board = data.target_board
    user.target_exam = data.target_exam
    user.learning_pace = data.learning_pace
    user.voice_enabled = data.voice_enabled

    # Process diagnostic answers if submitted
    if data.diagnostic_answers:
        for ans in data.diagnostic_answers:
            concept_id = ans.get("concept_id")
            is_correct = ans.get("is_correct", False)
            conf = ans.get("confidence_level", 3)

            mastery = db.query(LearnerMastery).filter(
                LearnerMastery.user_id == user.id,
                LearnerMastery.concept_id == concept_id
            ).first()

            if not mastery:
                mastery = LearnerMastery(
                    user_id=user.id,
                    concept_id=concept_id,
                    p_l=0.30 if is_correct else 0.15
                )
                db.add(mastery)
            else:
                update_res = BayesianKnowledgeTracer.update_mastery(
                    p_l=mastery.p_l,
                    is_correct=is_correct,
                    confidence_level=conf
                )
                mastery.p_l = update_res["updated_p_l"]
                mastery.status = update_res["status"]

    activity = StudyActivity(
        user_id=user.id,
        activity_type="onboarding",
        title="Completed Baseline Onboarding & Calibration",
        description=f"Calibrated learner model for {data.target_exam}",
        points=100
    )
    db.add(activity)
    db.commit()
    db.refresh(user)

    return {
        "success": True,
        "message": "Learner model successfully initialized and calibrated!",
        "user": {
            "id": user.id,
            "name": user.name,
            "target_board": user.target_board,
            "target_exam": user.target_exam,
            "learning_pace": user.learning_pace,
            "voice_enabled": user.voice_enabled
        }
    }
