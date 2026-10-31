# VoxLearn AI 🎙️🧠
### AI-Powered Adaptive Learning Web Application with a Learner Model
**Hackathon Problem Statement 2: AI Prep Tutor with a Learner Model**

---

## 🌟 Executive Overview
**VoxLearn AI** is a modern, responsive, voice-first adaptive learning platform engineered specifically for secondary STEM education (Class 10 Physics). Built on cognitive science principles and psychometric modeling, VoxLearn AI transitions beyond standard test engines by maintaining a persistent **Learner Model** that tracks student mastery using **Bayesian Knowledge Tracing (BKT)**, dynamically matches difficulty using **Item Response Theory (IRT)**, and deeply diagnoses cognitive errors through **Wrong-Answer Reasoning Analysis**.

VoxLearn AI features a **voice-first architecture compatible with Wispr Flow**, enabling students to speak naturally, formulate physics queries hands-free, and experience speech-synthesized Socratic tutoring with sub-second feedback.

---

## 🚀 Key Features

### 1. 📊 Adaptive Learner Model Engine (BKT & IRT)
- **Bayesian Knowledge Tracing (BKT):** Tracks latent mastery probability $P(L_t)$ for each concept node in the knowledge graph. Incorporates student metacognitive confidence (1 = Guess to 5 = Certain) to dynamically moderate slip $P(S)$ and guess $P(G)$ probabilities.
- **Item Response Theory (IRT):** Calculates student latent ability $\theta \in [-2.5, +2.5]$ from aggregate concept masteries and adaptively picks questions in the student's **Zone of Proximal Development (ZPD)** where success probability is calibrated to $\approx 68\%-72\%$.
- **Prerequisite Propagation:** Knowledge graph nodes verify prerequisite readiness before recommending advanced topics.

### 2. 🔍 Wrong-Answer Reasoning Analysis
- Traditional test platforms only report *that* an answer is wrong. VoxLearn AI diagnoses **why** reasoning failed.
- Cognitive Error Taxonomy:
  1. **Conceptual Misunderstandings:** e.g., Current Consumed Fallacy, Mass vs Optical Density confusion.
  2. **Formula & Application Flaws:** e.g., Wire Stretching Volume Neglect ($R \to 4R$), Cartesian Sign Convention inversion in optics.
  3. **Unit & Calculation Slips:** e.g., failing to convert $mA \to A$ or $cm \to m$ in Lens Power ($P = 1/f$).
  4. **Misreading Traps:** e.g., Overlooking negative qualifiers ("NOT true", "EXCEPT").
- Every misconception response includes:
  - *Why this trap occurs*
  - *The physical reality*
  - *Actionable micro-remedy & mental model analogy*

### 3. 🎙️ Voice-First Interaction & Wispr Flow Compatibility
- **Zero-Dependency Voice Input:** Native Web Speech API integration (`SpeechRecognition`) for instant speech-to-text directly in the browser.
- **Wispr Flow Bridge:** Dedicated Wispr Flow mode and global shortcut guide (Right Option / Alt) for 3x faster STEM dictation.
- **Natural Speech Synthesis (TTS):** Socratic tutor responses can be read aloud with pitch, rate, and mute controls.
- **Dynamic Waveform Visualizer:** Visual audio pulse indicators corresponding to mic input and AI vocal cadences.

### 4. 🧭 Class 10 Physics Curriculum & Knowledge Graph
Richly seeded with 17 foundational concepts, formulas, mental model analogies, and calibrated question banks spanning:
1. **Electricity:** Electric Current, Potential Difference, Ohm's Law, Resistivity & Dimensions, Series & Parallel Combinations, Joule's Heating & Power.
2. **Light — Reflection and Refraction:** Spherical Mirrors, Cartesian Sign Conventions, Snell's Law & Refractive Index, Lenses & Dioptre Power.
3. **Magnetic Effects of Electric Current:** Field Lines, Solenoids & Electromagnets, Fleming's Left-Hand Rule, Domestic Safety & Earthing.
4. **The Human Eye and Colourful World:** Accommodation, Defects of Vision (Myopia/Hypermetropia), Prism Dispersion, Atmospheric Refraction, Rayleigh Scattering ($I \propto 1/\lambda^4$).
5. **Sources of Energy:** Renewable vs Non-Renewable, Solar PV, Hydro & Nuclear Trade-offs.

### 5. 🎯 Personalized Practice & Progress Analytics
- **Weak-Node Workout:** Automatically identifies concepts with $P(L) < 0.65$ and generates customized drills with guided formula scaffolding and analogies.
- **Empirical IRT Curves:** Plots actual student accuracy across difficulty levels 1 through 5.
- **Bloom's Taxonomy Spectrum:** Visualizes cognitive progression from Remember and Understand through Apply, Analyze, and Evaluate.

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React 18, Vite, Tailwind CSS, Lucide Icons, Canvas-Confetti |
| **Backend** | Python 3.14+, FastAPI, SQLAlchemy, SQLite, Pydantic v2, Uvicorn |
| **Algorithms** | Bayesian Knowledge Tracing (BKT), 2-PL Item Response Theory (IRT) |
| **Voice / Speech** | Web Speech API (`SpeechRecognition`, `SpeechSynthesis`), Wispr Flow Dictation Protocol |
| **Testing** | Pytest, FastAPI TestClient, Vite Build Verification |

---

## ⚡ Exact Startup Commands

### Prerequisites
- Python 3.10+ (tested with Python 3.14)
- Node.js 18+ and npm

---

### Step 1: Start the Backend (FastAPI)

In your terminal / PowerShell:
```powershell
# Navigate to the backend directory
cd backend

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Run the backend server (automatically initializes & seeds database on startup)
python run.py
```
> The backend will start on **`http://localhost:8000`**.  
> Interactive OpenAPI documentation is accessible at **`http://localhost:8000/docs`**.

---

### Step 2: Start the Frontend (React + Vite)

In a separate terminal window:
```powershell
# Navigate to the frontend directory
cd frontend

# Install dependencies (if not already installed)
npm install

# Start the Vite development server
npm run dev
```
> The frontend will launch at **`http://localhost:5173`**.

---

## 🧪 Running Tests

To verify both learner model algorithms (BKT, IRT, Misconception Diagnostics) and all API endpoints:
```powershell
cd backend
python -m pytest tests
```
*Output: 11 passed tests verifying math correctness, difficulty adaptation, and endpoint stability.*

To verify frontend production bundle:
```powershell
cd frontend
npm run build
```

---

## 📂 Project Architecture

```
VoxLearn-AI/
├── backend/
│   ├── app/
│   │   ├── config.py                 # App settings & CORS
│   │   ├── database.py               # SQLite & SQLAlchemy engine
│   │   ├── models.py                 # User, Concept, Mastery, Question, Misconception
│   │   ├── schemas.py                # Pydantic validation schemas
│   │   ├── learner_model.py          # BKT & IRT psychometric engine
│   │   ├── tutor_engine.py           # Socratic voice dialogue engine
│   │   ├── misconception_engine.py   # Diagnostic classification & remedies
│   │   ├── data/
│   │   │   ├── physics_curriculum.py # Class 10 Knowledge Graph & Questions
│   │   │   └── seed.py               # Database seeder
│   │   ├── routers/
│   │   │   ├── auth_user.py          # Profile & Onboarding
│   │   │   ├── dashboard.py          # Learner Model metrics & recommendations
│   │   │   ├── tutor.py              # Socratic conversational tutor
│   │   │   ├── quiz.py               # Adaptive quiz & BKT updates
│   │   │   ├── mastery.py            # Concept graph & prerequisite checks
│   │   │   └── practice.py           # Weak workout & IRT analytics
│   │   └── main.py                   # FastAPI application root & lifespan
│   ├── run.py                        # Uvicorn entry script
│   ├── requirements.txt
│   └── tests/
│       ├── test_learner_model.py     # BKT and IRT unit tests
│       └── test_api_endpoints.py     # Full integration tests
├── frontend/
│   ├── package.json
│   ├── vite.config.js                # Vite config with API proxy
│   ├── tailwind.config.js            # Custom color palette and animations
│   ├── src/
│   │   ├── context/
│   │   │   ├── LearnerContext.jsx    # User & dashboard state
│   │   │   └── VoiceContext.jsx      # Speech recognition & Wispr Flow bridge
│   │   ├── services/
│   │   │   ├── api.js                # HTTP client
│   │   │   └── voiceService.js       # Voice recognition & TTS wrapper
│   │   ├── components/
│   │   │   ├── Navbar.jsx            # Live stats, streak, Wispr pill
│   │   │   ├── Sidebar.jsx           # Module navigation
│   │   │   ├── AudioVisualizer.jsx   # Waveform pulse
│   │   │   └── WisprFlowModal.jsx    # Wispr Flow setup & test injection
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx         # Executive learner overview
│   │   │   ├── Onboarding.jsx        # Profile & diagnostic calibration
│   │   │   ├── AITutor.jsx           # Voice-first Socratic tutor
│   │   │   ├── AdaptiveQuiz.jsx      # IRT adaptive quiz & BKT updates
│   │   │   ├── MasteryView.jsx       # Knowledge graph & prerequisite checks
│   │   │   ├── MisconceptionAnalysis.jsx # Wrong-answer reasoning catalog
│   │   │   ├── PersonalizedPractice.jsx  # Weak concept workout
│   │   │   └── Analytics.jsx         # IRT curves & Bloom's taxonomy
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
└── README.md
```

---

## 🏆 Hackathon Alignment Summary (Problem 2)

| Problem Statement Requirement | VoxLearn AI Implementation |
|---|---|
| **Learner Model** | Implemented Bayesian Knowledge Tracing with confidence weighting ($P(L_t) \to P(L_{t+1})$) and 2-PL Item Response Theory ($\theta$ ability matching). |
| **Adaptive Quizzes** | Dynamically adapts difficulty toward the student's Zone of Proximal Development ($\approx 70\%$ success probability). |
| **Wrong-Answer Reasoning** | Identifies specific misconception categories (Conceptual, Formula, Unit slip, Misreading) and provides actionable physical mental models. |
| **Voice-First / Wispr Flow** | Real-time speech recognition, SpeechSynthesis TTS read-aloud, audio visualizer, and Wispr Flow global shortcut compatibility. |
| **Class 10 Physics Data** | 17 verified concepts, 9 misconception taxonomies, and 17+ calibrated board-level questions with Bloom's taxonomy tags. |
| **Persistence & Usability** | Full SQLite persistence, seed data for immediate demonstration, responsive mobile navigation, zero broken buttons. |
