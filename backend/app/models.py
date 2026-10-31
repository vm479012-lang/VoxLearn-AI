import json
import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), default="Aarav Sharma")
    target_board = Column(String(50), default="CBSE Class 10")
    target_exam = Column(String(100), default="Class 10 Board & NTSE")
    learning_pace = Column(String(50), default="adaptive")  # fast, moderate, deep
    voice_enabled = Column(Boolean, default=True)
    streak_days = Column(Integer, default=5)
    total_study_minutes = Column(Integer, default=185)
    points = Column(Integer, default=640)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    masteries = relationship("LearnerMastery", back_populates="user", cascade="all, delete-orphan")
    quiz_sessions = relationship("QuizSession", back_populates="user", cascade="all, delete-orphan")
    conversations = relationship("TutorConversation", back_populates="user", cascade="all, delete-orphan")
    activities = relationship("StudyActivity", back_populates="user", cascade="all, delete-orphan")


class Concept(Base):
    __tablename__ = "concepts"

    id = Column(String(80), primary_key=True, index=True)  # e.g. "elec_ohms_law"
    topic = Column(String(100), index=True)  # e.g. "Electricity"
    unit_code = Column(String(50), default="unit_1")
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    bloom_level = Column(String(50), default="Understand")  # Remember, Understand, Apply, Analyze, Evaluate
    prerequisites_json = Column(Text, default="[]")  # List of concept IDs
    formulas_json = Column(Text, default="[]")  # List of LaTeX / text formulas
    real_world_analogy = Column(Text, default="")
    order_index = Column(Integer, default=0)

    questions = relationship("Question", back_populates="concept", cascade="all, delete-orphan")
    misconceptions = relationship("Misconception", back_populates="concept", cascade="all, delete-orphan")
    masteries = relationship("LearnerMastery", back_populates="concept", cascade="all, delete-orphan")

    @property
    def prerequisites(self):
        return json.loads(self.prerequisites_json or "[]")

    @prerequisites.setter
    def prerequisites(self, val):
        self.prerequisites_json = json.dumps(val)

    @property
    def formulas(self):
        return json.loads(self.formulas_json or "[]")

    @formulas.setter
    def formulas(self, val):
        self.formulas_json = json.dumps(val)


class LearnerMastery(Base):
    __tablename__ = "learner_masteries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    concept_id = Column(String(80), ForeignKey("concepts.id"), index=True)
    
    # Bayesian Knowledge Tracing (BKT) Parameters
    # P(L_t) = Probability of knowing the concept at current state (0.0 to 1.0)
    p_l = Column(Float, default=0.25)
    # P(T) = Probability of transitioning from not known to known after an opportunity
    p_transit = Column(Float, default=0.18)
    # P(S) = Probability of slip (knowing but answering wrong, e.g. calculation slip)
    p_slip = Column(Float, default=0.10)
    # P(G) = Probability of guess (not knowing but guessing right)
    p_guess = Column(Float, default=0.20)

    total_attempts = Column(Integer, default=0)
    correct_attempts = Column(Integer, default=0)
    consecutive_correct = Column(Integer, default=0)
    confidence_avg = Column(Float, default=3.0)  # scale 1-5
    last_practiced = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String(50), default="in_progress")  # not_started, needs_review, in_progress, mastered

    user = relationship("User", back_populates="masteries")
    concept = relationship("Concept", back_populates="masteries")


class Misconception(Base):
    __tablename__ = "misconceptions"

    id = Column(String(80), primary_key=True, index=True)  # e.g. "MISC_ELEC_CURRENT_CONSUMED"
    concept_id = Column(String(80), ForeignKey("concepts.id"), index=True)
    category = Column(String(50), default="conceptual")  # conceptual, formula_application, calculation_unit, misreading
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    why_it_happens = Column(Text, nullable=False)
    remedy_tip = Column(Text, nullable=False)

    concept = relationship("Concept", back_populates="misconceptions")


class Question(Base):
    __tablename__ = "questions"

    id = Column(String(80), primary_key=True, index=True)
    concept_id = Column(String(80), ForeignKey("concepts.id"), index=True)
    topic = Column(String(100), index=True)
    question_text = Column(Text, nullable=False)
    options_json = Column(Text, nullable=False)  # JSON list of dicts: [{text, is_correct, misconception_id, explanation}]
    difficulty = Column(Integer, default=2)  # 1 to 5 (IRT difficulty mapping)
    bloom_level = Column(String(50), default="Understand")
    formula_hint = Column(Text, default="")
    explanation = Column(Text, nullable=False)

    concept = relationship("Concept", back_populates="questions")
    responses = relationship("QuestionResponse", back_populates="question")

    @property
    def options(self):
        return json.loads(self.options_json or "[]")

    @options.setter
    def options(self, val):
        self.options_json = json.dumps(val)


class QuizSession(Base):
    __tablename__ = "quiz_sessions"

    id = Column(String(80), primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    quiz_type = Column(String(50), default="adaptive")  # adaptive, diagnostic, weak_practice, unit_test
    topic = Column(String(100), default="Class 10 Physics")
    score = Column(Integer, default=0)
    total_questions = Column(Integer, default=0)
    accuracy_percentage = Column(Float, default=0.0)
    difficulty_average = Column(Float, default=2.5)
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="quiz_sessions")
    responses = relationship("QuestionResponse", back_populates="quiz_session", cascade="all, delete-orphan")


class QuestionResponse(Base):
    __tablename__ = "question_responses"

    id = Column(Integer, primary_key=True, index=True)
    quiz_session_id = Column(String(80), ForeignKey("quiz_sessions.id"), index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    question_id = Column(String(80), ForeignKey("questions.id"), index=True)
    selected_option_index = Column(Integer, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    confidence_level = Column(Integer, default=3)  # 1 (Guess) to 5 (Certain)
    time_taken_seconds = Column(Integer, default=25)
    misconception_id = Column(String(80), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    quiz_session = relationship("QuizSession", back_populates="responses")
    question = relationship("Question", back_populates="responses")


class TutorConversation(Base):
    __tablename__ = "tutor_conversations"

    id = Column(String(80), primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    title = Column(String(150), default="Physics Socratic Tutoring")
    topic = Column(String(100), default="Electricity")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="conversations")
    messages = relationship("TutorMessage", back_populates="conversation", cascade="all, delete-orphan")


class TutorMessage(Base):
    __tablename__ = "tutor_messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String(80), ForeignKey("tutor_conversations.id"), index=True)
    sender = Column(String(20), default="assistant")  # 'user', 'assistant'
    content = Column(Text, nullable=False)
    voice_transcribed = Column(Boolean, default=False)
    socratic_stage = Column(String(50), default="guidance")  # elicit, challenge, analogize, consolidate
    formulas_json = Column(Text, default="[]")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    conversation = relationship("TutorConversation", back_populates="messages")

    @property
    def formulas(self):
        return json.loads(self.formulas_json or "[]")

    @formulas.setter
    def formulas(self, val):
        self.formulas_json = json.dumps(val)


class StudyActivity(Base):
    __tablename__ = "study_activities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    activity_type = Column(String(50), default="quiz")  # quiz, tutor, diagnostic, practice
    title = Column(String(150), nullable=False)
    description = Column(String(255), nullable=False)
    points = Column(Integer, default=20)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="activities")
