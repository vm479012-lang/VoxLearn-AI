"""
Pydantic Schemas for VoxLearn AI
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict

# User & Onboarding
class UserBase(BaseModel):
    name: str = "Aarav Sharma"
    target_board: str = "CBSE Class 10"
    target_exam: str = "Class 10 Board & NTSE"
    learning_pace: str = "adaptive"
    voice_enabled: bool = True

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    streak_days: int
    total_study_minutes: int
    points: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class OnboardingRequest(BaseModel):
    name: str
    target_board: str
    target_exam: str
    learning_pace: str
    voice_enabled: bool
    diagnostic_answers: Optional[List[Dict[str, Any]]] = []

# Concept & Knowledge Graph
class ConceptSummary(BaseModel):
    id: str
    topic: str
    unit_code: str
    name: str
    description: str
    bloom_level: str
    prerequisites: List[str]
    formulas: List[str]
    real_world_analogy: str
    order_index: int
    mastery_percentage: float = 25.0
    status: str = "not_started"

    model_config = ConfigDict(from_attributes=True)

class LearnerMasteryDetail(BaseModel):
    concept_id: str
    concept_name: str
    topic: str
    p_l: float
    mastery_percentage: float
    status: str
    total_attempts: int
    correct_attempts: int
    confidence_avg: float
    last_practiced: datetime

# Quiz & Questions
class OptionSchema(BaseModel):
    text: str
    is_correct: Optional[bool] = None
    misconception_id: Optional[str] = None
    explanation: Optional[str] = None

class OptionClientSchema(BaseModel):
    text: str

class QuestionClientSchema(BaseModel):
    id: str
    concept_id: str
    topic: str
    question_text: str
    options: List[str]
    difficulty: int
    bloom_level: str
    formula_hint: Optional[str] = ""

class QuestionSubmitRequest(BaseModel):
    user_id: int = 1
    quiz_session_id: Optional[str] = None
    question_id: str
    selected_option_index: int
    confidence_level: int = 3  # 1 (Guess) to 5 (Certain)
    time_taken_seconds: int = 20

class QuestionEvaluationResponse(BaseModel):
    question_id: str
    is_correct: bool
    correct_option_index: int
    selected_option_index: int
    explanation: str
    formula_hint: Optional[str] = ""
    # Misconception analysis
    misconception_found: bool = False
    misconception_title: Optional[str] = None
    misconception_category: Optional[str] = None
    why_it_happens: Optional[str] = None
    physical_reality: Optional[str] = None
    remedy_tip: Optional[str] = None
    # Learner Model BKT Update
    concept_id: str
    previous_p_l: float
    updated_p_l: float
    mastery_percentage: float
    mastery_delta: float
    new_status: str

class QuizStartRequest(BaseModel):
    user_id: int = 1
    quiz_type: str = "adaptive"  # adaptive, diagnostic, weak_practice, unit_test
    topic: Optional[str] = None
    concept_id: Optional[str] = None
    num_questions: int = 5

class QuizSessionResponse(BaseModel):
    session_id: str
    user_id: int
    quiz_type: str
    topic: str
    total_questions: int
    questions: List[QuestionClientSchema]

# AI Tutor
class TutorMessageRequest(BaseModel):
    user_id: int = 1
    conversation_id: Optional[str] = None
    message: str
    voice_transcribed: bool = False

class TutorMessageResponse(BaseModel):
    conversation_id: str
    sender: str
    content: str
    topic: str
    socratic_stage: str
    suggested_formulas: List[str] = []
    created_at: datetime

# Dashboard
class DashboardSummaryResponse(BaseModel):
    user: UserResponse
    overall_mastery_percentage: float
    mastered_count: int
    in_progress_count: int
    needs_review_count: int
    total_concepts: int
    estimated_exam_readiness: float
    topic_breakdown: List[Dict[str, Any]]
    weak_concepts: List[Dict[str, Any]]
    recent_activities: List[Dict[str, Any]]
    daily_recommendation: Dict[str, Any]
