"""
Database seeding script for VoxLearn AI
Populates Class 10 Physics concepts, misconceptions, questions,
and default student profile with calibrated baseline masteries.
"""

import json
from sqlalchemy.orm import Session
from ..database import engine, Base, SessionLocal
from ..models import User, Concept, Misconception, Question, LearnerMastery, StudyActivity, QuizSession, QuestionResponse
from .physics_curriculum import CONCEPTS, MISCONCEPTIONS, QUESTIONS

def seed_database():
    print("Creating all database tables...")
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        # 1. Seed or update concepts
        print(f"Seeding {len(CONCEPTS)} Class 10 Physics concepts...")
        for c_data in CONCEPTS:
            existing = db.query(Concept).filter(Concept.id == c_data["id"]).first()
            if not existing:
                concept = Concept(
                    id=c_data["id"],
                    topic=c_data["topic"],
                    unit_code=c_data["unit_code"],
                    name=c_data["name"],
                    description=c_data["description"],
                    bloom_level=c_data["bloom_level"],
                    prerequisites_json=json.dumps(c_data["prerequisites"]),
                    formulas_json=json.dumps(c_data["formulas"]),
                    real_world_analogy=c_data["real_world_analogy"],
                    order_index=c_data["order_index"]
                )
                db.add(concept)

        # 2. Seed misconceptions
        print(f"Seeding {len(MISCONCEPTIONS)} misconception diagnostics...")
        for m_data in MISCONCEPTIONS:
            existing_m = db.query(Misconception).filter(Misconception.id == m_data["id"]).first()
            if not existing_m:
                misc = Misconception(
                    id=m_data["id"],
                    concept_id=m_data["concept_id"],
                    category=m_data["category"],
                    title=m_data["title"],
                    description=m_data["description"],
                    why_it_happens=m_data["why_it_happens"],
                    remedy_tip=m_data["remedy_tip"]
                )
                db.add(misc)

        # 3. Seed questions
        print(f"Seeding {len(QUESTIONS)} calibrated questions...")
        for q_data in QUESTIONS:
            existing_q = db.query(Question).filter(Question.id == q_data["id"]).first()
            if not existing_q:
                q = Question(
                    id=q_data["id"],
                    concept_id=q_data["concept_id"],
                    topic=q_data["topic"],
                    question_text=q_data["question_text"],
                    options_json=json.dumps(q_data["options"]),
                    difficulty=q_data["difficulty"],
                    bloom_level=q_data["bloom_level"],
                    formula_hint=q_data.get("formula_hint", ""),
                    explanation=q_data["explanation"]
                )
                db.add(q)

        db.commit()

        # 4. Seed default user if not exists
        user = db.query(User).filter(User.id == 1).first()
        if not user:
            print("Creating default learner profile (Aarav Sharma)...")
            user = User(
                id=1,
                name="Aarav Sharma",
                target_board="CBSE Class 10",
                target_exam="Board Exam & NTSE",
                learning_pace="adaptive",
                voice_enabled=True,
                streak_days=5,
                total_study_minutes=195,
                points=720
            )
            db.add(user)
            db.commit()

            # Seed initial masteries for Aarav
            # Some mastered (P_L > 0.8), some in progress (0.45 - 0.79), some needing review (< 0.45)
            mastery_presets = {
                "elec_current_charge": 0.88,
                "elec_potential_difference": 0.74,
                "elec_ohms_law": 0.82,
                "elec_resistivity_factors": 0.42,  # Weak node (stretching wire trap)
                "elec_resistors_combination": 0.58,
                "elec_joules_heating": 0.65,
                "opt_reflection_spherical_mirrors": 0.85,
                "opt_mirror_formula_magnification": 0.48, # Weak node (sign convention)
                "opt_refraction_snells_law": 0.52,
                "opt_lenses_and_power": 0.78,
                "mag_field_lines_patterns": 0.84,
                "mag_solenoid_electromagnet": 0.76,
                "mag_flemings_left_hand_motor": 0.45,
                "mag_domestic_circuits_safety": 0.70,
                "eye_structure_defects": 0.80,
                "eye_dispersion_scattering": 0.62,
                "energy_conventional_renewable": 0.90
            }

            for c_id, p_l in mastery_presets.items():
                status = "mastered" if p_l >= 0.80 else ("in_progress" if p_l >= 0.50 else "needs_review")
                m = LearnerMastery(
                    user_id=1,
                    concept_id=c_id,
                    p_l=p_l,
                    p_transit=0.18,
                    p_slip=0.10,
                    p_guess=0.20,
                    total_attempts=5 if p_l > 0.7 else 3,
                    correct_attempts=4 if p_l > 0.7 else 1,
                    consecutive_correct=3 if p_l > 0.8 else 1,
                    confidence_avg=4.2 if p_l > 0.8 else 2.8,
                    status=status
                )
                db.add(m)

            # Seed sample recent activities
            activities = [
                StudyActivity(user_id=1, activity_type="quiz", title="Completed Adaptive Electricity Quiz", description="Scored 80% on Ohm's Law and Circuit Analysis", points=50),
                StudyActivity(user_id=1, activity_type="tutor", title="Voice Socratic Session on Snell's Law", description="Discussed optical density vs mass density with AI Tutor", points=30),
                StudyActivity(user_id=1, activity_type="practice", title="Misconception Remedy Workout", description="Targeted wire stretching volume invariance trap", points=40),
            ]
            for act in activities:
                db.add(act)

            db.commit()
            print("Successfully initialized default learner state!")

    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
