"""
AI Tutor Engine for VoxLearn AI
Provides Socratic dialogue, pedagogical scaffolding, voice-friendly cadences,
and physics domain intelligence for Class 10 Physics.
Supports offline intelligent Socratic heuristics and optional LLM expansion.
"""

import re
from typing import Dict, Any, List

# Core domain knowledge base for Class 10 Physics Socratic responses
PHYSICS_TOPIC_KNOWLEDGE: Dict[str, Dict[str, Any]] = {
    "electricity": {
        "keywords": ["current", "voltage", "potential", "ohm", "resistance", "resistivity", "series", "parallel", "joule", "power", "fuse"],
        "core_formulas": [
            "I = Q / t  (Current in Amperes, Charge in Coulombs, Time in Seconds)",
            "V = W / Q  (Potential Difference = Work done per unit charge)",
            "V = I * R  (Ohm's Law: Voltage equals Current times Resistance)",
            "R = rho * (L / A)  (Resistance from resistivity, length, and area)",
            "Series: R_total = R1 + R2 + R3",
            "Parallel: 1/R_total = 1/R1 + 1/R2 + 1/R3",
            "H = I^2 * R * t  (Joule's Heating Law)",
            "P = V * I = I^2 * R = V^2 / R  (Electric Power in Watts)"
        ],
        "analogies": {
            "ohm": "Imagine water flowing through a garden pipe. Voltage is the water pressure pushing the liquid, Current is how many liters pass per second, and Resistance is pebbles or narrow constrictions slowing down the flow.",
            "series": "Think of a single narrow doorway everyone must pass through in single file. Everyone experiences the same flow (current), but each doorway causes its own slowdown (voltage drop).",
            "parallel": "Think of multiple checkout lanes in a supermarket. The total voltage difference is identical across all lanes, but shoppers branch off, so the current splits among the paths."
        },
        "socratic_probes": [
            "What happens to the total resistance when you connect two identical resistors in parallel vs in series?",
            "If a wire is stretched to double its original length, does its volume stay constant? How does its cross-sectional area change?",
            "Why is domestic wiring connected in parallel rather than series?"
        ]
    },
    "light": {
        "keywords": ["reflection", "refraction", "mirror", "lens", "focal", "magnification", "snell", "convex", "concave", "optical"],
        "core_formulas": [
            "Mirror Formula: 1/f = 1/v + 1/u",
            "Lens Formula: 1/f = 1/v - 1/u",
            "Magnification (Mirror): m = -v/u = h_i / h_o",
            "Magnification (Lens): m = +v/u = h_i / h_o",
            "Snell's Law: n = sin(i) / sin(r) = c / v",
            "Lens Power: P = 1 / f(in meters)  (Units: Dioptres D)"
        ],
        "analogies": {
            "refraction": "Picture a marching band marching across smooth pavement that suddenly steps at an angle into thick mud. The soldiers who hit the mud first slow down, causing the entire row to pivot and change direction!",
            "concave_mirror": "A concave mirror curves inward like a cave or a satellite dish, gathering rays together to a sharp focal point.",
            "lens_power": "Power is how strongly a lens can bend light. A thick lens with a short focal length bends light fiercely, having high optical power."
        },
        "socratic_probes": [
            "According to the Cartesian sign convention, why is the object distance 'u' always assigned a negative sign?",
            "If a ray of light enters from water (n=1.33) into glass (n=1.5), does it bend towards or away from the normal?",
            "What kind of lens is used to correct myopia (nearsightedness), and why?"
        ]
    },
    "magnetism": {
        "keywords": ["magnetic", "field", "solenoid", "fleming", "left hand", "right hand", "induction", "motor", "generator", "compass"],
        "core_formulas": [
            "Force on current conductor: F = B * I * L * sin(theta)",
            "Fleming's Left-Hand Rule: Thumb (Motion/Force), Forefinger (Field B), Middle (Current I)",
            "Right-Hand Thumb Rule: Curl fingers around wire, Thumb points in direction of current",
            "Inside a solenoid: Magnetic field lines are uniform, parallel, and straight."
        ],
        "analogies": {
            "solenoid": "A solenoid acts just like an artificial bar magnet whose strength can be turned on and off with an electric switch.",
            "fleming": "Remember the FBI mnemonic for Fleming's Left Hand Rule: F (Thumb) for Force, B (Index) for Magnetic Field, I (Middle) for Current."
        },
        "socratic_probes": [
            "What determines the direction of the magnetic field around a straight current-carrying wire?",
            "Why do magnetic field lines never cross or intersect one another?",
            "What is the safety purpose of the green earthing wire in our home electrical circuits?"
        ]
    },
    "eye": {
        "keywords": ["eye", "cornea", "retina", "ciliary", "accommodation", "myopia", "hypermetropia", "presbyopia", "prism", "dispersion", "scattering", "tyndall"],
        "core_formulas": [
            "Angle of Deviation: delta = (i + e) - A",
            "Rayleigh Scattering: Intensity I is proportional to 1 / (lambda^4)",
            "Near point of normal eye: 25 cm, Far point: Infinity"
        ],
        "analogies": {
            "scattering": "Fine dust particles in the air are tiny, so they preferentially scatter tiny blue wavelengths, painting the daytime sky blue, while large red wavelengths pass right through.",
            "ciliary": "The ciliary muscles are like elastic tensioners on a camera lens, flexing the crystalline lens thick for close reading and flattening it thin for distant horizons."
        },
        "socratic_probes": [
            "Why does the sky appear dark to an astronaut in outer space instead of blue?",
            "Why do stars twinkle while planets in our solar system do not?",
            "In hypermetropia (farsightedness), where is the image formed relative to the retina?"
        ]
    },
    "energy": {
        "keywords": ["energy", "fossil", "solar", "wind", "hydro", "nuclear", "biomass", "geothermal", "non-conventional", "turbine"],
        "core_formulas": [
            "Efficiency = (Useful Energy Output / Total Energy Input) * 100%",
            "Nuclear Fission: E = Delta m * c^2"
        ],
        "analogies": {
            "greenhouse": "Glass panes in a solar cooker trap infrared heat just like Earth's atmosphere traps thermal radiation, cooking the food inside cleanly."
        },
        "socratic_probes": [
            "What are the major environmental drawbacks of building large hydroelectric dams across river valleys?",
            "Why can't solar cells replace all conventional power plants today despite the abundant sunlight?"
        ]
    }
}


class TutorEngine:
    """
    Socratic pedagogical tutor capable of conversational voice interaction.
    """

    @staticmethod
    def detect_topic(message: str) -> str:
        msg = message.lower()
        scores = {}
        for topic, data in PHYSICS_TOPIC_KNOWLEDGE.items():
            score = sum(1 for kw in data["keywords"] if kw in msg)
            scores[topic] = score

        best_topic = max(scores, key=scores.get)
        if scores[best_topic] > 0:
            return best_topic
        return "electricity"

    @staticmethod
    def generate_socratic_response(
        user_message: str,
        conversation_history: List[Dict[str, str]] = None,
        user_mastery_context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Generates a structured Socratic response designed for voice read-aloud and deep learning.
        """
        clean_msg = user_message.strip()
        topic_key = TutorEngine.detect_topic(clean_msg)
        topic_data = PHYSICS_TOPIC_KNOWLEDGE[topic_key]

        lower_msg = clean_msg.lower()

        # Step 1: Detect specific intent
        is_greeting = any(w in lower_msg for w in ["hello", "hi", "hey", "start", "namaste"])
        is_asking_formula = any(w in lower_msg for w in ["formula", "equation", "calculate", "how to find", "derive"])
        is_asking_analogy = any(w in lower_msg for w in ["analogy", "real life", "intuition", "simple words", "explain like"])
        is_asking_why = any(w in lower_msg for w in ["why", "how come", "reason", "misconception", "confused"])
        is_quiz_hint = any(w in lower_msg for w in ["hint", "stuck", "clue", "help me solve"])

        suggested_formulas = []
        voice_cadence_text = ""
        socratic_stage = "guidance"

        if is_greeting and len(clean_msg.split()) < 5:
            voice_cadence_text = (
                f"Hello! I am your VoxLearn AI Physics tutor. We can explore Electricity, Light, "
                f"Magnetism, or the Human Eye. You can speak naturally or use Wispr Flow. "
                f"What concept or problem shall we tackle together today?"
            )
            socratic_stage = "welcome"

        elif is_asking_formula:
            formulas = topic_data.get("core_formulas", [])
            suggested_formulas = formulas[:4]
            voice_cadence_text = (
                f"Here are the foundational formulas for {topic_key.capitalize()}.\n\n"
                + "\n".join([f"• {f}" for f in formulas[:4]])
                + "\n\nLet's apply one of these to a real question: which quantity do you know first?"
            )
            socratic_stage = "elicit"

        elif is_asking_analogy:
            analogies = topic_data.get("analogies", {})
            chosen_analogy = next(iter(analogies.values()), "Let's connect this to everyday experience.")
            voice_cadence_text = (
                f"Here is an intuitive way to visualize this:\n\n{chosen_analogy}\n\n"
                f"Can you tell me how that compares to the flow of charges in a circuit?"
            )
            socratic_stage = "analogize"

        elif is_quiz_hint:
            voice_cadence_text = (
                "Let's break the problem down step by step. First, identify what is given in the problem: "
                "are you working with series or parallel, reflection or refraction? "
                "Tell me the known variables and what we are trying to solve for!"
            )
            socratic_stage = "challenge"

        else:
            # Socratic pedagogical conversation: validate, scaffold, probe
            analogies = topic_data.get("analogies", {})
            sample_analogy = next(iter(analogies.values()), "")
            probes = topic_data.get("socratic_probes", [])
            selected_probe = probes[0] if probes else "What does your intuition say?"

            voice_cadence_text = (
                f"That is an insightful question about {topic_key.capitalize()}. "
                f"Before jumping straight to numbers, let's look at the underlying physics.\n\n"
                f"Key Intuition: {sample_analogy}\n\n"
                f"Now consider this guiding question: {selected_probe}"
            )
            suggested_formulas = topic_data.get("core_formulas", [])[:2]
            socratic_stage = "probe"

        return {
            "response_text": voice_cadence_text,
            "topic": topic_key.capitalize(),
            "socratic_stage": socratic_stage,
            "suggested_formulas": suggested_formulas,
            "voice_enabled": True
        }
