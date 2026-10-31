"""
Misconception Engine for VoxLearn AI
Analyzes incorrect answers, classifies cognitive failure modes,
and generates targeted diagnostic breakdowns with actionable micro-remedies.
"""

from typing import Dict, Any, Optional

MISCONCEPTION_CATALOG: Dict[str, Dict[str, Any]] = {
    "MISC_CURRENT_CONSUMED": {
        "category": "conceptual",
        "title": "Current Consumed Fallacy",
        "description": "Believing that electric current is 'used up' by components (like lamps or resistors) in a circuit.",
        "why_it_happens": "Learners intuitively associate electric current with fuel (like gasoline or battery drain) rather than the rate of charge flow through a closed loop.",
        "physical_reality": "Current is the rate of flow of charge (I = Q/t). Due to conservation of charge, the rate at which charges enter a resistor equals the rate at which they exit.",
        "remedy_tip": "Think of a closed water circuit with a circulating pump: water doesn't disappear at the water wheel; it just transfers kinetic energy!"
    },
    "MISC_SERIES_PARALLEL_VOLTAGE": {
        "category": "conceptual",
        "title": "Voltage-Current Property Inversion",
        "description": "Confusing voltage distribution with current distribution in series vs parallel circuits.",
        "why_it_happens": "Remembering one rule (e.g. 'current is constant') and accidentally applying it across parallel branches instead of series nodes.",
        "physical_reality": "In series, there is only one pathway, so Current is identical everywhere. In parallel, all branches share the same two terminal nodes, so Potential Difference (Voltage) is identical.",
        "remedy_tip": "Series = Single path (Same Current). Parallel = Pairs of terminals (Same Voltage)."
    },
    "MISC_WIRE_STRETCH_RESISTANCE": {
        "category": "formula_application",
        "title": "Volume Invariance Neglect during Wire Stretching",
        "description": "Assuming resistance only doubles when length is doubled by stretching, forgetting area halving.",
        "why_it_happens": "Applying R = rho * L / A while treating A as constant. When a wire is drawn out, its volume (V = A * L) remains invariant.",
        "physical_reality": "If length doubles (L' = 2L), cross-sectional area halves (A' = A/2). Hence R' = rho * (2L) / (A/2) = 4R! Resistance increases 4-fold.",
        "remedy_tip": "Whenever a problem says 'stretched' or 'drawn', volume is constant: R is proportional to L squared!"
    },
    "MISC_OPTICS_SIGN_CONVENTION": {
        "category": "formula_application",
        "title": "Cartesian Sign Convention Flip",
        "description": "Flipping signs for object distance (u) or focal length (f) in mirror/lens formulas.",
        "why_it_happens": "Forgetting that real objects are placed to the left of the optical center / pole, making u always negative in Cartesian convention.",
        "physical_reality": "Object distance 'u' is ALWAYS negative (-). Concave mirror/lens has negative 'f' (-). Convex mirror/lens has positive 'f' (+).",
        "remedy_tip": "Always sketch the optical axis with Cartesian (x, y) coordinates. Left of pole is negative, right is positive."
    },
    "MISC_REFRACTION_DENSITY_SPEED": {
        "category": "conceptual",
        "title": "Optical vs Mass Density Confusion",
        "description": "Assuming optically denser medium must always be mass-denser (e.g., thinking kerosene is optically rarer than water because it floats).",
        "why_it_happens": "Equating optical density (speed of light reduction) with mass density (mass per unit volume).",
        "physical_reality": "Kerosene floats on water (lower mass density), but its refractive index is 1.44 vs water's 1.33. Kerosene is optically DENSER than water!",
        "remedy_tip": "Optical density measures light speed reduction, NOT weight per volume!"
    },
    "MISC_MAGNETIC_FORCE_DIRECTION": {
        "category": "formula_application",
        "title": "Fleming's Left Hand Rule vs Right Hand Confusion",
        "description": "Using Fleming's Right-Hand Rule (generator/induced current) instead of Left-Hand Rule (motor/mechanical force).",
        "why_it_happens": "Both rules use thumb, index, and middle fingers at right angles, leading to accidental hand swaps.",
        "physical_reality": "Left Hand = Force on moving charge/conductor in B-field (Motors). Right Hand = Induced current (Generators). Remember 'FBI': Thumb=Force, Forefinger=B-field, Middle=Current I.",
        "remedy_tip": "Left hand creates Motion (Motors). Right hand is for generator Results (Induced current)."
    },
    "MISC_SCATTERING_WAVELENGTH_INVERSE": {
        "category": "conceptual",
        "title": "Scattering Power vs Wavelength Dependency",
        "description": "Thinking red scatters more because it has higher wavelength or travels farther.",
        "why_it_happens": "Noting that danger signals are red and assuming red scatters strongly.",
        "physical_reality": "Rayleigh scattering intensity is inversely proportional to the 4th power of wavelength: I ~ 1 / lambda^4. Red has longest wavelength, so it scatters LEAST!",
        "remedy_tip": "Red scatters least -> travels through fog and distance without dispersion -> that's why danger signals are red!"
    },
    "MISC_UNIT_PREFIX_SLIP": {
        "category": "calculation_unit",
        "title": "SI Unit / Prefix Scale Slip",
        "description": "Failing to convert milli-amperes (mA) to Amperes (A) or centimeters (cm) to meters (m) in power/energy equations.",
        "why_it_happens": "Plugging raw numbers directly into formulas without inspecting prefix multipliers.",
        "physical_reality": "P = V * I requires I in Amperes (1 mA = 10^-3 A). Lens Power P = 1 / f requires focal length in METERS, not cm.",
        "remedy_tip": "Before plugging numbers into any Physics formula, convert all quantities to standard SI units: m, s, kg, A, V."
    },
    "MISC_NEGATIVE_NOT_MISREAD": {
        "category": "misreading",
        "title": "Negative Constraint Misread",
        "description": "Overlooking negative qualifiers like 'INCORRECT', 'NOT', or 'LEAST' in the question stem.",
        "why_it_happens": "Fast skimming activates recognition of the first factually true statement rather than identifying the false one requested.",
        "physical_reality": "Standardized tests frequently use inverted constraints to evaluate rigorous attention to problem specification.",
        "remedy_tip": "Circle or highlight words like 'NOT', 'INCORRECT', and 'EXCEPT' before reading option choices."
    }
}


class MisconceptionEngine:
    @staticmethod
    def diagnose_response(
        question_data: Dict[str, Any],
        selected_option_index: int
    ) -> Dict[str, Any]:
        """
        Diagnoses an incorrect answer option and extracts deep reasoning analysis.
        """
        options = question_data.get("options", [])
        if selected_option_index < 0 or selected_option_index >= len(options):
            return {
                "is_correct": False,
                "misconception_found": False,
                "message": "Invalid option selected."
            }

        selected_opt = options[selected_option_index]
        is_correct = selected_opt.get("is_correct", False)

        if is_correct:
            return {
                "is_correct": True,
                "misconception_found": False,
                "title": "Correct Understanding!",
                "explanation": question_data.get("explanation", "Great job! Your conceptual reasoning is solid.")
            }

        # Find linked misconception
        misc_id = selected_opt.get("misconception_id")
        misc_info = MISCONCEPTION_CATALOG.get(misc_id) if misc_id else None

        if not misc_info:
            # Fallback heuristic categorization
            category = "conceptual"
            title = "Conceptual Divergence"
            why = selected_opt.get("explanation", "The selected option conflicts with fundamental physical laws.")
            physical = question_data.get("explanation", "Review the underlying principle.")
            remedy = "Re-examine the formula and definitions governing this phenomenon."
        else:
            category = misc_info["category"]
            title = misc_info["title"]
            why = misc_info["why_it_happens"]
            physical = misc_info["physical_reality"]
            remedy = misc_info["remedy_tip"]

        return {
            "is_correct": False,
            "misconception_found": True,
            "misconception_id": misc_id,
            "category": category,
            "title": title,
            "selected_text": selected_opt.get("text", ""),
            "option_critique": selected_opt.get("explanation", ""),
            "why_it_happens": why,
            "physical_reality": physical,
            "remedy_tip": remedy,
            "bloom_level": question_data.get("bloom_level", "Understand"),
            "formula_hint": question_data.get("formula_hint", ""),
            "correct_explanation": question_data.get("explanation", "")
        }
