"""
Learner Model Engine for VoxLearn AI
Implements:
1. Bayesian Knowledge Tracing (BKT) with confidence-weighted updates
2. Item Response Theory (IRT) difficulty calibration and adaptive question selection
3. Knowledge State Graph evaluation (prerequisite mastery propagation)
"""

import math
from typing import Dict, Any, List, Optional


class BayesianKnowledgeTracer:
    """
    Standard Bayesian Knowledge Tracing (Corbett & Anderson) with confidence moderation.
    Tracks latent mastery probability P(L) for individual concept nodes.
    """

    @staticmethod
    def update_mastery(
        p_l: float,
        is_correct: bool,
        p_transit: float = 0.18,
        p_slip: float = 0.10,
        p_guess: float = 0.20,
        confidence_level: int = 3  # 1 (Guess) to 5 (Certain)
    ) -> Dict[str, float]:
        """
        Calculates posterior P(L_{t+1}) given observation and student metacognitive confidence.
        """
        # Clamp inputs safely
        p_l = max(0.01, min(0.99, p_l))
        p_transit = max(0.01, min(0.50, p_transit))

        # Adjust guess and slip parameters based on reported metacognitive confidence (1 to 5)
        # If user was certain (5) and wrong -> it was likely a genuine misconception, not a slip.
        # If user guessed (1) and correct -> it was likely a guess.
        adjusted_guess = p_guess
        adjusted_slip = p_slip

        if confidence_level == 1:
            adjusted_guess = min(0.50, p_guess * 1.8)
        elif confidence_level == 2:
            adjusted_guess = min(0.35, p_guess * 1.3)
        elif confidence_level == 4:
            adjusted_slip = max(0.04, p_slip * 0.7)
            adjusted_guess = max(0.08, p_guess * 0.7)
        elif confidence_level == 5:
            adjusted_slip = max(0.02, p_slip * 0.4)
            adjusted_guess = max(0.04, p_guess * 0.4)

        if is_correct:
            # Bayes formula for P(L_t | Correct)
            numerator = p_l * (1.0 - adjusted_slip)
            denominator = numerator + (1.0 - p_l) * adjusted_guess
            posterior = numerator / max(1e-6, denominator)
        else:
            # Bayes formula for P(L_t | Incorrect)
            numerator = p_l * adjusted_slip
            denominator = numerator + (1.0 - p_l) * (1.0 - adjusted_guess)
            posterior = numerator / max(1e-6, denominator)

        # Transition model: P(L_{t+1}) = posterior + (1 - posterior) * P(T)
        next_p_l = posterior + (1.0 - posterior) * p_transit
        next_p_l = round(max(0.02, min(0.98, next_p_l)), 4)

        status = "mastered" if next_p_l >= 0.80 else ("in_progress" if next_p_l >= 0.45 else "needs_review")

        return {
            "previous_p_l": round(p_l, 4),
            "posterior_before_transit": round(posterior, 4),
            "updated_p_l": next_p_l,
            "mastery_percentage": round(next_p_l * 100, 1),
            "status": status,
            "delta": round(next_p_l - p_l, 4)
        }


class ItemResponseTheory:
    """
    2-Parameter Logistic (2-PL) IRT for dynamic adaptive question selection.
    """

    @staticmethod
    def estimate_ability(mastery_values: List[float]) -> float:
        """
        Maps average concept mastery (0.0 to 1.0) to latent student ability theta in [-2.5, +2.5].
        """
        if not mastery_values:
            return 0.0
        avg_mastery = sum(mastery_values) / len(mastery_values)
        # Logit-like mapping
        # 0.5 -> 0.0, 0.9 -> ~1.8, 0.1 -> ~-1.8
        clamped = max(0.05, min(0.95, avg_mastery))
        theta = math.log(clamped / (1.0 - clamped))
        return round(max(-2.5, min(2.5, theta)), 2)

    @staticmethod
    def probability_correct(theta: float, difficulty: int, discrimination: float = 1.2) -> float:
        """
        Maps question difficulty (1-5) to IRT parameter b in [-2.0, 2.0].
        Calculates P(correct | theta, b, a).
        """
        # Map 1..5 to -1.8, -0.9, 0.0, +0.9, +1.8
        b = (difficulty - 3) * 0.9
        exponent = -discrimination * (theta - b)
        # Avoid overflow
        exponent = max(-15.0, min(15.0, exponent))
        prob = 1.0 / (1.0 + math.exp(exponent))
        return prob

    @staticmethod
    def select_next_question(
        available_questions: List[Dict[str, Any]],
        theta: float,
        target_success_prob: float = 0.68  # Target Zone of Proximal Development
    ) -> Optional[Dict[str, Any]]:
        """
        Finds the question that places the student closest to the Zone of Proximal Development (ZPD).
        """
        if not available_questions:
            return None

        best_q = None
        min_distance = float('inf')

        for q in available_questions:
            diff = q.get("difficulty", 3)
            prob = ItemResponseTheory.probability_correct(theta, diff)
            distance = abs(prob - target_success_prob)
            if distance < min_distance:
                min_distance = distance
                best_q = q

        return best_q


def propagate_prerequisite_knowledge(
    concept_id: str,
    concept_map: Dict[str, Dict[str, Any]],
    mastery_map: Dict[str, float]
) -> Dict[str, Any]:
    """
    Checks if a concept's prerequisites are met.
    If prerequisites have low mastery, recommends reviewing them first.
    """
    concept = concept_map.get(concept_id, {})
    prereqs = concept.get("prerequisites", [])

    weak_prereqs = []
    for p_id in prereqs:
        p_mastery = mastery_map.get(p_id, 0.25)
        if p_mastery < 0.60:
            p_data = concept_map.get(p_id, {})
            weak_prereqs.append({
                "concept_id": p_id,
                "name": p_data.get("name", p_id),
                "mastery": round(p_mastery * 100, 1)
            })

    ready = len(weak_prereqs) == 0
    return {
        "is_ready": ready,
        "weak_prerequisites": weak_prereqs,
        "recommendation": "Ready to tackle!" if ready else f"Recommendation: Strengthen {weak_prereqs[0]['name']} first."
    }
