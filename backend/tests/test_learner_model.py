"""
Unit tests for Learner Model (BKT and IRT) and Misconception Diagnostics
"""

import pytest
from app.learner_model import BayesianKnowledgeTracer, ItemResponseTheory
from app.misconception_engine import MisconceptionEngine

def test_bkt_correct_increases_mastery():
    initial_p_l = 0.30
    result = BayesianKnowledgeTracer.update_mastery(
        p_l=initial_p_l,
        is_correct=True,
        confidence_level=4
    )
    assert result["updated_p_l"] > initial_p_l
    assert result["delta"] > 0
    assert result["mastery_percentage"] == round(result["updated_p_l"] * 100, 1)

def test_bkt_incorrect_decreases_mastery():
    initial_p_l = 0.75
    result = BayesianKnowledgeTracer.update_mastery(
        p_l=initial_p_l,
        is_correct=False,
        confidence_level=4
    )
    assert result["updated_p_l"] < initial_p_l
    assert result["delta"] < 0

def test_irt_ability_estimation():
    low_masteries = [0.2, 0.25, 0.3]
    high_masteries = [0.85, 0.9, 0.95]

    theta_low = ItemResponseTheory.estimate_ability(low_masteries)
    theta_high = ItemResponseTheory.estimate_ability(high_masteries)

    assert theta_high > theta_low
    assert theta_high > 0
    assert theta_low < 0

def test_misconception_diagnosis_wire_stretch():
    q_data = {
        "options": [
            {"text": "2R", "is_correct": False, "misconception_id": "MISC_WIRE_STRETCH_RESISTANCE", "explanation": "Forgot area halving"},
            {"text": "4R", "is_correct": True, "misconception_id": None, "explanation": "Correct"}
        ],
        "explanation": "Resistance becomes 4R because volume is invariant.",
        "formula_hint": "R = rho * L / A",
        "bloom_level": "Analyze"
    }

    # Selected wrong answer (2R)
    diag = MisconceptionEngine.diagnose_response(q_data, 0)
    assert diag["is_correct"] is False
    assert diag["misconception_found"] is True
    assert diag["misconception_id"] == "MISC_WIRE_STRETCH_RESISTANCE"
    assert diag["category"] == "formula_application"

    # Selected correct answer (4R)
    diag_correct = MisconceptionEngine.diagnose_response(q_data, 1)
    assert diag_correct["is_correct"] is True
    assert diag_correct["misconception_found"] is False
