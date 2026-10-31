"""
Curriculum and Knowledge Graph for Class 10 Physics:
1. Electricity
2. Light - Reflection and Refraction
3. Magnetic Effects of Electric Current
4. The Human Eye and the Colourful World
5. Sources of Energy
"""

CONCEPTS = [
    # Unit 1: Electricity
    {
        "id": "elec_current_charge",
        "topic": "Electricity",
        "unit_code": "unit_1",
        "name": "Electric Current and Charge",
        "description": "Flow of electric charges through a conductor per unit time; measured in Amperes using an ammeter.",
        "bloom_level": "Remember",
        "prerequisites": [],
        "formulas": ["I = Q / t", "Q = n * e (where e = 1.6 * 10^-19 C)"],
        "real_world_analogy": "Flow rate of water in a river (liters of water passing per second).",
        "order_index": 1
    },
    {
        "id": "elec_potential_difference",
        "topic": "Electricity",
        "unit_code": "unit_1",
        "name": "Electric Potential & Potential Difference",
        "description": "Work done in moving a unit positive charge from one point to another; measured in Volts by a voltmeter connected in parallel.",
        "bloom_level": "Understand",
        "prerequisites": ["elec_current_charge"],
        "formulas": ["V = W / Q (1 Volt = 1 Joule / 1 Coulomb)"],
        "real_world_analogy": "Water pressure difference created by an elevated water tank that causes water to flow downhill.",
        "order_index": 2
    },
    {
        "id": "elec_ohms_law",
        "topic": "Electricity",
        "unit_code": "unit_1",
        "name": "Ohm's Law & Resistance",
        "description": "Potential difference across a metallic conductor is directly proportional to current flowing through it at constant temperature.",
        "bloom_level": "Apply",
        "prerequisites": ["elec_potential_difference", "elec_current_charge"],
        "formulas": ["V = I * R", "R = V / I (Unit: Ohm Omega)"],
        "real_world_analogy": "Rocks and constrictions in a pipe that resist the flow of water despite pump pressure.",
        "order_index": 3
    },
    {
        "id": "elec_resistivity_factors",
        "topic": "Electricity",
        "unit_code": "unit_1",
        "name": "Factors Affecting Resistance & Resistivity",
        "description": "Resistance depends directly on length (L), inversely on cross-sectional area (A), and the inherent material resistivity (rho).",
        "bloom_level": "Analyze",
        "prerequisites": ["elec_ohms_law"],
        "formulas": ["R = rho * (L / A)", "rho = R * A / L (Unit: Ohm*meter)"],
        "real_world_analogy": "A longer, narrower hallway creates more traffic resistance than a short, wide foyer.",
        "order_index": 4
    },
    {
        "id": "elec_resistors_combination",
        "topic": "Electricity",
        "unit_code": "unit_1",
        "name": "Series and Parallel Combinations",
        "description": "Series circuits maintain equal current with additive resistances; parallel circuits maintain equal voltage with reciprocal reciprocal conductance.",
        "bloom_level": "Apply",
        "prerequisites": ["elec_ohms_law"],
        "formulas": [
            "Series: R_s = R1 + R2 + ... + Rn",
            "Parallel: 1/R_p = 1/R1 + 1/R2 + ... + 1/Rn"
        ],
        "real_world_analogy": "Series is single-file security checkpoints; Parallel is multiple open airport security lanes.",
        "order_index": 5
    },
    {
        "id": "elec_joules_heating",
        "topic": "Electricity",
        "unit_code": "unit_1",
        "name": "Joule's Law of Heating & Electric Power",
        "description": "Heat produced in a resistor is proportional to square of current, resistance, and time. Electric power is rate of energy dissipation.",
        "bloom_level": "Evaluate",
        "prerequisites": ["elec_ohms_law"],
        "formulas": [
            "H = I^2 * R * t",
            "P = V * I = I^2 * R = V^2 / R",
            "Commercial unit: 1 kWh = 3.6 * 10^6 J"
        ],
        "real_world_analogy": "Friction generating heat when tires skid on pavement; fast electrons colliding with conductor lattice ions.",
        "order_index": 6
    },

    # Unit 2: Light - Reflection and Refraction
    {
        "id": "opt_reflection_spherical_mirrors",
        "topic": "Light: Reflection & Refraction",
        "unit_code": "unit_2",
        "name": "Reflection & Spherical Mirrors",
        "description": "Laws of reflection, focal length f = R/2, image formation by concave and convex mirrors.",
        "bloom_level": "Understand",
        "prerequisites": [],
        "formulas": ["f = R / 2"],
        "real_world_analogy": "Shining sides of a stainless steel soup spoon: inside is concave, back is convex.",
        "order_index": 7
    },
    {
        "id": "opt_mirror_formula_magnification",
        "topic": "Light: Reflection & Refraction",
        "unit_code": "unit_2",
        "name": "Mirror Formula and Cartesian Sign Convention",
        "description": "Relationship between focal length, object distance, and image distance with Cartesian sign conventions.",
        "bloom_level": "Apply",
        "prerequisites": ["opt_reflection_spherical_mirrors"],
        "formulas": [
            "Mirror Formula: 1/f = 1/v + 1/u",
            "Magnification: m = -v / u = h_i / h_o"
        ],
        "real_world_analogy": "Standard coordinate graph where left of the origin (pole) is negative x, right is positive x.",
        "order_index": 8
    },
    {
        "id": "opt_refraction_snells_law",
        "topic": "Light: Reflection & Refraction",
        "unit_code": "unit_2",
        "name": "Refraction of Light and Snell's Law",
        "description": "Bending of light across optical boundaries due to velocity variation; refractive index ratio.",
        "bloom_level": "Understand",
        "prerequisites": [],
        "formulas": [
            "n = sin(i) / sin(r)",
            "n_21 = v1 / v2 = n2 / n1",
            "Absolute index n = c / v"
        ],
        "real_world_analogy": "Marching band stepping diagonally into thick mud: wheels slowing down cause steering angle shift.",
        "order_index": 9
    },
    {
        "id": "opt_lenses_and_power",
        "topic": "Light: Reflection & Refraction",
        "unit_code": "unit_2",
        "name": "Spherical Lenses, Lens Formula & Power",
        "description": "Convex (converging) and concave (diverging) lens imagery, thin lens equation, and optical power in Dioptres.",
        "bloom_level": "Apply",
        "prerequisites": ["opt_refraction_snells_law"],
        "formulas": [
            "Lens Formula: 1/f = 1/v - 1/u",
            "Magnification: m = +v / u = h_i / h_o",
            "Power: P = 1 / f (f in meters, P in Dioptres D)"
        ],
        "real_world_analogy": "Magnifying glass focusing bright sun rays onto a pinpoint dry leaf.",
        "order_index": 10
    },

    # Unit 3: Magnetic Effects of Electric Current
    {
        "id": "mag_field_lines_patterns",
        "topic": "Magnetic Effects of Electric Current",
        "unit_code": "unit_3",
        "name": "Magnetic Field Lines & Current Conductor",
        "description": "Field lines form closed concentric loops around a straight current conductor; Right-Hand Thumb Rule.",
        "bloom_level": "Understand",
        "prerequisites": ["elec_current_charge"],
        "formulas": ["B proportional to I / r (straight wire)", "B proportional to n * I (solenoid)"],
        "real_world_analogy": "Concentric ripples expanding outwards when a stone drops into still water.",
        "order_index": 11
    },
    {
        "id": "mag_solenoid_electromagnet",
        "topic": "Magnetic Effects of Electric Current",
        "unit_code": "unit_3",
        "name": "Magnetic Field in a Solenoid & Electromagnet",
        "description": "Uniform parallel internal magnetic field inside a helical coil; soft iron core enhances field strength.",
        "bloom_level": "Apply",
        "prerequisites": ["mag_field_lines_patterns"],
        "formulas": ["B = mu_0 * n * I"],
        "real_world_analogy": "A switchable bar magnet used in crane scrapyards to lift and release heavy cars.",
        "order_index": 12
    },
    {
        "id": "mag_flemings_left_hand_motor",
        "topic": "Magnetic Effects of Electric Current",
        "unit_code": "unit_3",
        "name": "Force on Conductor & Fleming's Left-Hand Rule",
        "description": "Conductor carrying current perpendicular to magnetic field experiences Lorentz mechanical force.",
        "bloom_level": "Apply",
        "prerequisites": ["mag_field_lines_patterns"],
        "formulas": ["F = B * I * L * sin(theta)"],
        "real_world_analogy": "Electric fan or mixer motor converting electrical current in magnetic fields to rotational motion.",
        "order_index": 13
    },
    {
        "id": "mag_domestic_circuits_safety",
        "topic": "Magnetic Effects of Electric Current",
        "unit_code": "unit_3",
        "name": "Domestic Electric Circuits & Safety Earthing",
        "description": "Live (220V), neutral, and earth wires; safety fuses and grounding to prevent electric shocks.",
        "bloom_level": "Evaluate",
        "prerequisites": ["elec_resistors_combination", "elec_joules_heating"],
        "formulas": ["I_rated = Power / Voltage (Fuse rating check)"],
        "real_world_analogy": "A safety escape valve on a steam cooker preventing overpressure explosions.",
        "order_index": 14
    },

    # Unit 4: The Human Eye and Colourful World
    {
        "id": "eye_structure_defects",
        "topic": "The Human Eye and Colourful World",
        "unit_code": "unit_4",
        "name": "Human Eye Accommodation & Defects of Vision",
        "description": "Ciliary muscle focusing; Myopia corrected by concave lens, Hypermetropia corrected by convex lens.",
        "bloom_level": "Understand",
        "prerequisites": ["opt_lenses_and_power"],
        "formulas": ["1/f = 1/v - 1/u (Corrective lens power)"],
        "real_world_analogy": "Auto-focus lens mechanism in digital cameras adapting between macro and landscape shots.",
        "order_index": 15
    },
    {
        "id": "eye_dispersion_scattering",
        "topic": "The Human Eye and Colourful World",
        "unit_code": "unit_4",
        "name": "Prism Dispersion, Atmospheric Refraction & Scattering",
        "description": "Splitting of white light (VIBGYOR), atmospheric twinkling of stars, and Rayleigh scattering making sky blue.",
        "bloom_level": "Understand",
        "prerequisites": ["opt_refraction_snells_law"],
        "formulas": ["Rayleigh scattering: I proportional to 1 / lambda^4"],
        "real_world_analogy": "Rainbow after rain; microscopic atmospheric sieves scattering small blue waves while letting large red waves pass.",
        "order_index": 16
    },

    # Unit 5: Sources of Energy
    {
        "id": "energy_conventional_renewable",
        "topic": "Sources of Energy",
        "unit_code": "unit_5",
        "name": "Renewable vs Non-renewable Energy Sources",
        "description": "Fossil fuels, thermal, hydro, biomass, wind, solar, and nuclear power generation with environmental trade-offs.",
        "bloom_level": "Evaluate",
        "prerequisites": [],
        "formulas": ["Efficiency = (Useful output / Total input) * 100%"],
        "real_world_analogy": "Spending an inheritance from a savings account (fossil fuel) vs earning recurring solar salary (sunlight).",
        "order_index": 17
    }
]

MISCONCEPTIONS = [
    {
        "id": "MISC_CURRENT_CONSUMED",
        "concept_id": "elec_current_charge",
        "category": "conceptual",
        "title": "Current Consumed Fallacy",
        "description": "Believing electric current gets 'used up' by lamps or appliances in a circuit.",
        "why_it_happens": "Equating electric current with battery chemical fuel rather than rate of charge circulation.",
        "remedy_tip": "Charges are conserved: rate of electrons entering any component exactly equals rate exiting."
    },
    {
        "id": "MISC_WIRE_STRETCH_RESISTANCE",
        "concept_id": "elec_resistivity_factors",
        "category": "formula_application",
        "title": "Wire Stretching Volume Neglect",
        "description": "Thinking stretching a wire to 2x length only doubles resistance.",
        "why_it_happens": "Ignoring that stretching pulls the wire thinner, halving cross-sectional area A.",
        "remedy_tip": "Since volume V = A*L is invariant, R is proportional to L^2. 2x length -> 4x resistance!"
    },
    {
        "id": "MISC_SERIES_PARALLEL_VOLTAGE",
        "concept_id": "elec_resistors_combination",
        "category": "conceptual",
        "title": "Series/Parallel Parameter Inversion",
        "description": "Confusing current vs voltage conservation across series and parallel networks.",
        "why_it_happens": "Memorizing formulas without physical intuition of path branching vs single conduit.",
        "remedy_tip": "One path = Same Current (Series). Shared nodes = Same Potential Difference (Parallel)."
    },
    {
        "id": "MISC_OPTICS_SIGN_CONVENTION",
        "concept_id": "opt_mirror_formula_magnification",
        "category": "formula_application",
        "title": "Cartesian Sign Convention Reversal",
        "description": "Using positive object distance u or wrong sign for focal length.",
        "why_it_happens": "Forgetting real objects lie on negative x-axis relative to pole.",
        "remedy_tip": "Real object u is ALWAYS negative (-). Concave mirror f is negative (-), convex is positive (+)."
    },
    {
        "id": "MISC_REFRACTION_DENSITY_SPEED",
        "concept_id": "opt_refraction_snells_law",
        "category": "conceptual",
        "title": "Optical vs Mass Density Confusion",
        "description": "Believing mass density determines optical bending speed.",
        "why_it_happens": "Assuming lighter fluids must be optically rarer.",
        "remedy_tip": "Kerosene floats on water (lower mass density) but has higher refractive index (optically denser)!"
    },
    {
        "id": "MISC_MAGNETIC_FORCE_DIRECTION",
        "concept_id": "mag_flemings_left_hand_motor",
        "category": "formula_application",
        "title": "Fleming's Left Hand vs Right Hand Reversal",
        "description": "Using right hand for motor mechanical force direction.",
        "why_it_happens": "Confusing motor rule (Left Hand) with generator induction rule (Right Hand).",
        "remedy_tip": "Left Hand = Force/Motion (Motor). Right Hand = Induced Current (Generator). FBI fingers!"
    },
    {
        "id": "MISC_SCATTERING_WAVELENGTH_INVERSE",
        "concept_id": "eye_dispersion_scattering",
        "category": "conceptual",
        "title": "Rayleigh Scattering Inversion",
        "description": "Believing red light scatters more because it travels further.",
        "why_it_happens": "Confusing transmission through fog with lateral scattering.",
        "remedy_tip": "Scattering intensity is proportional to 1 / lambda^4. Red has longest wavelength, so it scatters LEAST."
    },
    {
        "id": "MISC_UNIT_PREFIX_SLIP",
        "concept_id": "opt_lenses_and_power",
        "category": "calculation_unit",
        "title": "Power Calculation Unit Prefix Slip",
        "description": "Calculating Lens Power P = 1 / f with focal length left in centimeters.",
        "why_it_happens": "Directly computing 1 / 20 cm = 0.05 D instead of converting 20 cm = 0.2 m -> P = 5 D.",
        "remedy_tip": "Dioptre requires focal length strictly in METERS (P = 100 / f_in_cm)!"
    },
    {
        "id": "MISC_NEGATIVE_NOT_MISREAD",
        "concept_id": "mag_domestic_circuits_safety",
        "category": "misreading",
        "title": "Negative Question Stem Misread",
        "description": "Choosing a true statement when asked for the INCORRECT safety feature.",
        "why_it_happens": "Skimming past the capitalized NOT or INCORRECT word.",
        "remedy_tip": "Actively highlight words like NOT or FALSE before evaluating choices."
    }
]

# Question bank with Bloom's Taxonomy, IRT difficulties (1-5), and misconception links
QUESTIONS = [
    # 1. Electricity - Current & Charge
    {
        "id": "q_elec_01",
        "concept_id": "elec_current_charge",
        "topic": "Electricity",
        "question_text": "A current of 0.5 A is drawn by a filament of an electric bulb for 10 minutes. How much electric charge flows through the circuit?",
        "difficulty": 2,
        "bloom_level": "Apply",
        "formula_hint": "I = Q / t  =>  Q = I * t  (Ensure time is converted to SI seconds!)",
        "explanation": "Given I = 0.5 A and t = 10 minutes = 10 * 60 s = 600 s. The total charge Q = I * t = 0.5 A * 600 s = 300 C.",
        "options": [
            {"text": "5 C", "is_correct": False, "misconception_id": "MISC_UNIT_PREFIX_SLIP", "explanation": "Did not convert minutes to seconds (0.5 * 10). Time must be in seconds!"},
            {"text": "50 C", "is_correct": False, "misconception_id": "MISC_UNIT_PREFIX_SLIP", "explanation": "Arithmetic unit error in time scaling."},
            {"text": "300 C", "is_correct": True, "misconception_id": None, "explanation": "Correct! Q = 0.5 A * 600 s = 300 Coulombs."},
            {"text": "600 C", "is_correct": False, "misconception_id": "MISC_WIRE_STRETCH_RESISTANCE", "explanation": "Forgot to multiply by current (0.5 A)."}
        ]
    },
    # 2. Electricity - Current Consumed Misconception
    {
        "id": "q_elec_02",
        "concept_id": "elec_current_charge",
        "topic": "Electricity",
        "question_text": "An ammeter placed before a glowing electric lamp in a series circuit reads 2.0 A. What will an ammeter placed immediately AFTER the lamp read?",
        "difficulty": 1,
        "bloom_level": "Understand",
        "formula_hint": "Think about conservation of electric charge in a single closed circuit loop.",
        "explanation": "Due to conservation of electric charge, the rate of charge entering any component equals the rate of charge leaving. The current remains 2.0 A.",
        "options": [
            {"text": "Less than 2.0 A, because some current is consumed to produce light", "is_correct": False, "misconception_id": "MISC_CURRENT_CONSUMED", "explanation": "Current is not consumed! Energy is transferred, but charge flow rate is conserved."},
            {"text": "Exactly 2.0 A", "is_correct": True, "misconception_id": None, "explanation": "Correct! Charge cannot accumulate or disappear in a closed series loop."},
            {"text": "0 A, because the lamp absorbs all electrical current", "is_correct": False, "misconception_id": "MISC_CURRENT_CONSUMED", "explanation": "A lamp is not an electron sponge; charges flow continuously through it."},
            {"text": "More than 2.0 A due to electrical acceleration inside the filament", "is_correct": False, "misconception_id": "MISC_SERIES_PARALLEL_VOLTAGE", "explanation": "Conductor drift velocity does not magnify current post-filament."}
        ]
    },
    # 3. Electricity - Ohm's Law
    {
        "id": "q_elec_03",
        "concept_id": "elec_ohms_law",
        "topic": "Electricity",
        "question_text": "A potential difference of 12 V across a resistor causes a steady current of 2.4 A to flow. If the potential difference is doubled to 24 V, what will the new current be (assuming temperature is constant)?",
        "difficulty": 2,
        "bloom_level": "Understand",
        "formula_hint": "V = I * R  =>  Current I is directly proportional to Voltage V when R is constant.",
        "explanation": "According to Ohm's Law, I is directly proportional to V when R and temperature remain constant. Doubling V from 12 V to 24 V doubles the current from 2.4 A to 4.8 A.",
        "options": [
            {"text": "1.2 A", "is_correct": False, "misconception_id": "MISC_SERIES_PARALLEL_VOLTAGE", "explanation": "Inverted proportionality; voltage increase increases current, not halves it."},
            {"text": "2.4 A", "is_correct": False, "misconception_id": "MISC_CURRENT_CONSUMED", "explanation": "Current does not stay fixed when voltage changes across a linear resistor."},
            {"text": "4.8 A", "is_correct": True, "misconception_id": None, "explanation": "Correct! I = V / R; doubling V doubles I."},
            {"text": "9.6 A", "is_correct": False, "misconception_id": "MISC_WIRE_STRETCH_RESISTANCE", "explanation": "Quadrupled current inappropriately."}
        ]
    },
    # 4. Electricity - Wire Stretching Resistance
    {
        "id": "q_elec_04",
        "concept_id": "elec_resistivity_factors",
        "topic": "Electricity",
        "question_text": "A cylindrical copper wire having initial resistance R is uniformly stretched until its length is doubled. What is the new resistance of the wire?",
        "difficulty": 4,
        "bloom_level": "Analyze",
        "formula_hint": "R = rho * L / A. When stretched, volume V = A * L remains constant!",
        "explanation": "When stretched to 2L, cross-sectional area becomes A/2 so volume remains invariant. New resistance R' = rho * (2L) / (A/2) = 4 * (rho * L / A) = 4R.",
        "options": [
            {"text": "2R", "is_correct": False, "misconception_id": "MISC_WIRE_STRETCH_RESISTANCE", "explanation": "Classic trap! Forgot that stretching also halves cross-sectional area A, making it 4R."},
            {"text": "4R", "is_correct": True, "misconception_id": None, "explanation": "Spot on! L doubles and A halves, producing a 4-fold increase in resistance."},
            {"text": "R / 2", "is_correct": False, "misconception_id": "MISC_WIRE_STRETCH_RESISTANCE", "explanation": "Longer wires have higher resistance, not lower."},
            {"text": "R (Resistance is an invariant material property)", "is_correct": False, "misconception_id": "MISC_CURRENT_CONSUMED", "explanation": "Resistivity rho is invariant, but geometric resistance R depends on dimensions."}
        ]
    },
    # 5. Electricity - Parallel Combinations
    {
        "id": "q_elec_05",
        "concept_id": "elec_resistors_combination",
        "topic": "Electricity",
        "question_text": "Two resistors of 6 Omega and 3 Omega are connected in parallel across a 6 V battery. What is the equivalent resistance and the total current drawn from the battery?",
        "difficulty": 3,
        "bloom_level": "Apply",
        "formula_hint": "1/R_p = 1/R1 + 1/R2  =>  R_p = (R1 * R2)/(R1 + R2), then I = V / R_p",
        "explanation": "R_p = (6 * 3) / (6 + 3) = 18 / 9 = 2 Omega. Total current I = V / R_p = 6 V / 2 Omega = 3 A.",
        "options": [
            {"text": "R_eq = 9 Omega, Total Current = 0.67 A", "is_correct": False, "misconception_id": "MISC_SERIES_PARALLEL_VOLTAGE", "explanation": "You added them in series (6 + 3 = 9 Omega)! In parallel, equivalent resistance is lower than each branch."},
            {"text": "R_eq = 2 Omega, Total Current = 3 A", "is_correct": True, "misconception_id": None, "explanation": "Correct! 1/6 + 1/3 = 3/6 => R_eq = 2 Omega, and I = 6/2 = 3 A."},
            {"text": "R_eq = 2 Omega, Total Current = 12 A", "is_correct": False, "misconception_id": "MISC_UNIT_PREFIX_SLIP", "explanation": "Multiplied V * R instead of dividing V / R."},
            {"text": "R_eq = 4.5 Omega, Total Current = 1.33 A", "is_correct": False, "misconception_id": "MISC_SERIES_PARALLEL_VOLTAGE", "explanation": "Averaged the resistances instead of taking the reciprocal sum."}
        ]
    },
    # 6. Electricity - Joule's Heating
    {
        "id": "q_elec_06",
        "concept_id": "elec_joules_heating",
        "topic": "Electricity",
        "question_text": "An electric iron of resistance 20 Omega takes a current of 5 A. Calculate the heat developed in 30 seconds.",
        "difficulty": 3,
        "bloom_level": "Apply",
        "formula_hint": "H = I^2 * R * t",
        "explanation": "H = (5 A)^2 * 20 Omega * 30 s = 25 * 20 * 30 = 15,000 Joules = 1.5 * 10^4 J.",
        "options": [
            {"text": "3,000 J", "is_correct": False, "misconception_id": "MISC_WIRE_STRETCH_RESISTANCE", "explanation": "Used H = I * R * t without squaring current I (5 * 20 * 30 = 3000). Joule's heating is I^2 * R * t!"},
            {"text": "15,000 J", "is_correct": True, "misconception_id": None, "explanation": "Correct! H = (5^2) * 20 * 30 = 25 * 600 = 15,000 Joules."},
            {"text": "7,500 J", "is_correct": False, "misconception_id": "MISC_UNIT_PREFIX_SLIP", "explanation": "Arithmetic slip by halving value."},
            {"text": "30,000 J", "is_correct": False, "misconception_id": "MISC_CURRENT_CONSUMED", "explanation": "Incorrect factor of 2 multiplication."}
        ]
    },
    # 7. Light - Concave Mirror Image Formation
    {
        "id": "q_opt_01",
        "concept_id": "opt_reflection_spherical_mirrors",
        "topic": "Light: Reflection & Refraction",
        "question_text": "Where should an object be placed in front of a concave mirror to obtain an image of the SAME size as the object?",
        "difficulty": 1,
        "bloom_level": "Remember",
        "formula_hint": "Think of the point where object distance u equals radius of curvature R = 2f.",
        "explanation": "When an object is placed at the Centre of Curvature (C) of a concave mirror, a real, inverted image of exactly the same size is formed at C.",
        "options": [
            {"text": "Between Focus and Pole", "is_correct": False, "misconception_id": "MISC_OPTICS_SIGN_CONVENTION", "explanation": "Produces an enlarged, virtual, and erect image behind the mirror."},
            {"text": "At the Principal Focus (F)", "is_correct": False, "misconception_id": "MISC_OPTICS_SIGN_CONVENTION", "explanation": "Produces an infinitely large image at infinity."},
            {"text": "At the Centre of Curvature (C)", "is_correct": True, "misconception_id": None, "explanation": "Correct! At C, image distance equals object distance and magnification m = -1."},
            {"text": "Beyond the Centre of Curvature", "is_correct": False, "misconception_id": "MISC_OPTICS_SIGN_CONVENTION", "explanation": "Produces a diminished image between C and F."}
        ]
    },
    # 8. Light - Mirror Formula and Sign Convention
    {
        "id": "q_opt_02",
        "concept_id": "opt_mirror_formula_magnification",
        "topic": "Light: Reflection & Refraction",
        "question_text": "A concave mirror produces three times magnified real image of an object placed at 10 cm in front of it. Where is the image located?",
        "difficulty": 3,
        "bloom_level": "Apply",
        "formula_hint": "m = -v / u. Since it's a real image, magnification is negative: m = -3.",
        "explanation": "Object distance u = -10 cm. For a real image in a mirror, m = -3. Since m = -v / u, -3 = -v / (-10) => v = -30 cm (30 cm in front of the mirror).",
        "options": [
            {"text": "+30 cm (30 cm behind the mirror)", "is_correct": False, "misconception_id": "MISC_OPTICS_SIGN_CONVENTION", "explanation": "Real images in mirrors are formed in FRONT of the mirror, with v negative (-30 cm). Behind the mirror would be virtual!"},
            {"text": "-30 cm (30 cm in front of the mirror)", "is_correct": True, "misconception_id": None, "explanation": "Correct! m = -v/u => -3 = -v/(-10) => v = -30 cm."},
            {"text": "-3.33 cm", "is_correct": False, "misconception_id": "MISC_OPTICS_SIGN_CONVENTION", "explanation": "Divided u by m instead of multiplying."},
            {"text": "-15 cm", "is_correct": False, "misconception_id": "MISC_UNIT_PREFIX_SLIP", "explanation": "Arithmetic computation error."}
        ]
    },
    # 9. Light - Snell's Law and Optical Density
    {
        "id": "q_opt_03",
        "concept_id": "opt_refraction_snells_law",
        "topic": "Light: Reflection & Refraction",
        "question_text": "Kerosene (n = 1.44) floats on top of water (n = 1.33). When a ray of light passes from water into kerosene, how does it behave?",
        "difficulty": 3,
        "bloom_level": "Understand",
        "formula_hint": "Light bends TOWARD the normal when entering an optically DENSER medium (higher n).",
        "explanation": "Kerosene has higher refractive index (1.44 > 1.33), so it is optically denser than water despite having a lower mass density. Light slows down and bends towards the normal.",
        "options": [
            {"text": "Bends away from normal because kerosene is less dense and floats", "is_correct": False, "misconception_id": "MISC_REFRACTION_DENSITY_SPEED", "explanation": "Optical density is NOT mass density! Kerosene has higher refractive index (1.44 vs 1.33), so light slows down."},
            {"text": "Bends towards the normal because kerosene has higher refractive index", "is_correct": True, "misconception_id": None, "explanation": "Correct! Optical density depends on speed of light (refractive index), not mass flotation."},
            {"text": "Passes undeviated because both are liquids", "is_correct": False, "misconception_id": "MISC_REFRACTION_DENSITY_SPEED", "explanation": "Different refractive indices always cause bending at oblique incidence."},
            {"text": "Undergoes total internal reflection automatically", "is_correct": False, "misconception_id": "MISC_OPTICS_SIGN_CONVENTION", "explanation": "Total internal reflection only occurs from denser to rarer medium."}
        ]
    },
    # 10. Light - Lens Power in Dioptres
    {
        "id": "q_opt_04",
        "concept_id": "opt_lenses_and_power",
        "topic": "Light: Reflection & Refraction",
        "question_text": "A doctor prescribes a corrective convex lens of focal length +20 cm. What is the power of this lens?",
        "difficulty": 2,
        "bloom_level": "Apply",
        "formula_hint": "P = 1 / f(in meters). Convert cm to meters first: 20 cm = 0.20 m.",
        "explanation": "f = +20 cm = +0.2 m. Power P = 1 / f = 1 / (+0.2) = +5.0 Dioptres (D). Convex lens has positive power.",
        "options": [
            {"text": "+0.05 D", "is_correct": False, "misconception_id": "MISC_UNIT_PREFIX_SLIP", "explanation": "Forgot to convert 20 cm into meters (P = 1/20)! Lens power requires meters: 1/0.2 = +5 D."},
            {"text": "+5.0 D", "is_correct": True, "misconception_id": None, "explanation": "Correct! P = 1 / (0.2 m) = +5.0 Dioptres."},
            {"text": "-5.0 D", "is_correct": False, "misconception_id": "MISC_OPTICS_SIGN_CONVENTION", "explanation": "A convex lens is converging and always has positive focal length and power."},
            {"text": "+20 D", "is_correct": False, "misconception_id": "MISC_UNIT_PREFIX_SLIP", "explanation": "Assumed power equals focal length value directly."}
        ]
    },
    # 11. Magnetism - Field Lines Never Intersect
    {
        "id": "q_mag_01",
        "concept_id": "mag_field_lines_patterns",
        "topic": "Magnetic Effects of Electric Current",
        "question_text": "Why can two magnetic field lines NEVER intersect each other?",
        "difficulty": 2,
        "bloom_level": "Understand",
        "formula_hint": "What would a magnetic compass needle do if placed at an intersection point?",
        "explanation": "If two field lines intersected, a compass placed at the intersection would have to point in two different directions at the same physical point, which is physically impossible.",
        "options": [
            {"text": "Because magnetic field lines repel each other by electrostatic repulsion", "is_correct": False, "misconception_id": "MISC_CURRENT_CONSUMED", "explanation": "Field lines are geometric representations of field vectors, not charged physical wires."},
            {"text": "Because a compass needle would have to point in two different directions simultaneously", "is_correct": True, "misconception_id": None, "explanation": "Correct! At any single point in space, there can only be one net resultant magnetic field vector."},
            {"text": "Because magnetic fields are always strictly parallel", "is_correct": False, "misconception_id": "MISC_MAGNETIC_FORCE_DIRECTION", "explanation": "Field lines curve around magnets; they are only uniform inside a solenoid."},
            {"text": "Because magnetic monopoles always exist at line junctions", "is_correct": False, "misconception_id": "MISC_REFRACTION_DENSITY_SPEED", "explanation": "Isolated magnetic monopoles do not exist in classical electromagnetism."}
        ]
    },
    # 12. Magnetism - Solenoid
    {
        "id": "q_mag_02",
        "concept_id": "mag_solenoid_electromagnet",
        "topic": "Magnetic Effects of Electric Current",
        "question_text": "The pattern of the magnetic field lines inside a long current-carrying solenoid is:",
        "difficulty": 2,
        "bloom_level": "Remember",
        "formula_hint": "Inside a solenoid, the magnetic field is uniform at all points.",
        "explanation": "Inside a long solenoid, the magnetic field lines are in the form of parallel straight lines, indicating that the magnetic field is uniform throughout.",
        "options": [
            {"text": "Concentric circles around the axis", "is_correct": False, "misconception_id": "MISC_MAGNETIC_FORCE_DIRECTION", "explanation": "Concentric circles occur around a straight wire, not inside a solenoid."},
            {"text": "Parallel straight lines indicating a uniform field", "is_correct": True, "misconception_id": None, "explanation": "Correct! Solenoid interior has a strong, uniform magnetic field represented by parallel lines."},
            {"text": "Zero, because opposite turns cancel each other completely", "is_correct": False, "misconception_id": "MISC_CURRENT_CONSUMED", "explanation": "Turns reinforce one another inside the coil."},
            {"text": "Diverging spirals radiating outward", "is_correct": False, "misconception_id": "MISC_MAGNETIC_FORCE_DIRECTION", "explanation": "Field lines are parallel and closed."}
        ]
    },
    # 13. Magnetism - Fleming's Left Hand Rule
    {
        "id": "q_mag_03",
        "concept_id": "mag_flemings_left_hand_motor",
        "topic": "Magnetic Effects of Electric Current",
        "question_text": "In Fleming's Left-Hand Rule, what do the thumb, forefinger, and middle finger represent respectively?",
        "difficulty": 2,
        "bloom_level": "Remember",
        "formula_hint": "Remember the mnemonic 'FBI': Force (Thumb), B-Field (Forefinger), Current I (Middle).",
        "explanation": "In Fleming's Left-Hand Rule, the Thumb represents Force (Motion), the Forefinger represents Magnetic Field, and the Middle finger represents Current.",
        "options": [
            {"text": "Thumb: Current, Forefinger: Field, Middle: Force", "is_correct": False, "misconception_id": "MISC_MAGNETIC_FORCE_DIRECTION", "explanation": "Reversed thumb and middle finger. Thumb is Force (Motion)."},
            {"text": "Thumb: Force (Motion), Forefinger: Magnetic Field, Middle: Electric Current", "is_correct": True, "misconception_id": None, "explanation": "Correct! Thumb = Force, Forefinger = Field B, Middle = Current I (FBI)."},
            {"text": "Thumb: Voltage, Forefinger: Resistance, Middle: Current", "is_correct": False, "misconception_id": "MISC_SERIES_PARALLEL_VOLTAGE", "explanation": "Ohm's law variables do not map to Fleming's spatial vectors."},
            {"text": "Thumb: Induced Current, Forefinger: Motion, Middle: Field", "is_correct": False, "misconception_id": "MISC_MAGNETIC_FORCE_DIRECTION", "explanation": "Confused with generator induction rule."}
        ]
    },
    # 14. Magnetism - Domestic Safety & Earthing
    {
        "id": "q_mag_04",
        "concept_id": "mag_domestic_circuits_safety",
        "topic": "Magnetic Effects of Electric Current",
        "question_text": "Which of the following statements about domestic electric wiring safety is INCORRECT?",
        "difficulty": 3,
        "bloom_level": "Evaluate",
        "formula_hint": "Pay close attention to where the safety fuse must be connected (live wire vs neutral).",
        "explanation": "The safety fuse must ALWAYS be connected in series with the LIVE wire, never the neutral wire. If connected to neutral, a blown fuse leaves the appliance at 220V potential!",
        "options": [
            {"text": "The earth wire with green insulation provides a low-resistance path to ground for leakage currents", "is_correct": False, "misconception_id": "MISC_NEGATIVE_NOT_MISREAD", "explanation": "This statement is correct and is a vital safety measure."},
            {"text": "An electric fuse should be connected in the NEUTRAL wire rather than the live wire", "is_correct": True, "misconception_id": None, "explanation": "Correct choice! This statement is FALSE/INCORRECT. The fuse must strictly be in the LIVE wire."},
            {"text": "All domestic appliances are connected in parallel to ensure independent operation and 220 V voltage", "is_correct": False, "misconception_id": "MISC_NEGATIVE_NOT_MISREAD", "explanation": "This statement is true; parallel connection maintains full voltage."},
            {"text": "Short-circuit occurs when live and neutral wires come in direct contact, drastically reducing resistance", "is_correct": False, "misconception_id": "MISC_NEGATIVE_NOT_MISREAD", "explanation": "This statement is true; short circuits cause surge current."}
        ]
    },
    # 15. Human Eye - Myopia Correction
    {
        "id": "q_eye_01",
        "concept_id": "eye_structure_defects",
        "topic": "The Human Eye and Colourful World",
        "question_text": "A student cannot see distant blackboard letters clearly but can read their textbook comfortably. Which defect of vision do they have, and which corrective lens is required?",
        "difficulty": 2,
        "bloom_level": "Understand",
        "formula_hint": "Cannot see far away = Nearsightedness (Myopia). Image forms in FRONT of retina.",
        "explanation": "The student has Myopia (nearsightedness), where distant images converge in front of the retina. A diverging (concave) lens of suitable power diverges rays back onto the retina.",
        "options": [
            {"text": "Hypermetropia, corrected by a convex lens", "is_correct": False, "misconception_id": "MISC_OPTICS_SIGN_CONVENTION", "explanation": "Hypermetropia is farsightedness (difficulty seeing nearby text). The student sees nearby text fine!"},
            {"text": "Myopia, corrected by a concave lens", "is_correct": True, "misconception_id": None, "explanation": "Correct! Myopia requires a diverging concave lens to shift the focal plane onto the retina."},
            {"text": "Presbyopia, corrected by a bifocal lens", "is_correct": False, "misconception_id": "MISC_OPTICS_SIGN_CONVENTION", "explanation": "Presbyopia is age-related loss of accommodation for near vision."},
            {"text": "Astigmatism, corrected by a cylindrical lens", "is_correct": False, "misconception_id": "MISC_REFRACTION_DENSITY_SPEED", "explanation": "Astigmatism is due to irregular cornea curvature in perpendicular planes."}
        ]
    },
    # 16. Human Eye - Rayleigh Scattering & Red Sky
    {
        "id": "q_eye_02",
        "concept_id": "eye_dispersion_scattering",
        "topic": "The Human Eye and Colourful World",
        "question_text": "At sunrise and sunset, the Sun appears reddish because:",
        "difficulty": 3,
        "bloom_level": "Understand",
        "formula_hint": "Scattering intensity is inversely proportional to lambda^4. Red has the longest visible wavelength.",
        "explanation": "Light from the Sun near the horizon travels through a thicker layer of atmosphere. Shorter wavelengths (blue/violet) are scattered away strongly, so mostly longer red wavelengths reach our eyes.",
        "options": [
            {"text": "Red light is scattered the most by atmospheric particles", "is_correct": False, "misconception_id": "MISC_SCATTERING_WAVELENGTH_INVERSE", "explanation": "Red scatters the LEAST because it has the longest wavelength (I ~ 1/lambda^4)!"},
            {"text": "Blue light of shorter wavelength is scattered away, leaving mostly red light to reach our eyes", "is_correct": True, "misconception_id": None, "explanation": "Correct! Blue scatters out sideways; red survives the long atmospheric path to reach our eyes."},
            {"text": "The Sun actually cools down at sunrise and sunset, shifting emission to red", "is_correct": False, "misconception_id": "MISC_CURRENT_CONSUMED", "explanation": "Sun temperature remains constant; this is an optical atmospheric effect."},
            {"text": "Atmospheric refraction absorbs all visible light except infrared and red", "is_correct": False, "misconception_id": "MISC_REFRACTION_DENSITY_SPEED", "explanation": "The mechanism is Rayleigh scattering, not selective bulk absorption."}
        ]
    },
    # 17. Sources of Energy - Non-conventional
    {
        "id": "q_energy_01",
        "concept_id": "energy_conventional_renewable",
        "topic": "Sources of Energy",
        "question_text": "Which of the following is a major environmental advantage of utilizing a Solar Photovoltaic Cell compared to a Coal Thermal Power Plant?",
        "difficulty": 1,
        "bloom_level": "Understand",
        "formula_hint": "Consider greenhouse emissions and operational waste.",
        "explanation": "Solar cells produce clean electricity directly from solar photons without releasing greenhouse gases (CO2) or sulfur dioxide during operational generation.",
        "options": [
            {"text": "Solar cells work at peak 100% capacity during stormy nights", "is_correct": False, "misconception_id": "MISC_CURRENT_CONSUMED", "explanation": "Solar PV requires sunlight and produces no power at night without batteries."},
            {"text": "Zero greenhouse emissions or acid-rain gases during operational electricity generation", "is_correct": True, "misconception_id": None, "explanation": "Correct! Solar PV generates electricity without burning carbon or emitting SO2/NOx."},
            {"text": "Solar cells require no silicon or manufacturing resources", "is_correct": False, "misconception_id": "MISC_NEGATIVE_NOT_MISREAD", "explanation": "Solar cells require refined silicon and manufacturing energy."},
            {"text": "Solar power cannot be converted into alternating current", "is_correct": False, "misconception_id": "MISC_SERIES_PARALLEL_VOLTAGE", "explanation": "Inverters easily convert DC solar power to 220V AC."}
        ]
    }
]
