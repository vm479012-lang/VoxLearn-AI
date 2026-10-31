"""
Integration tests for FastAPI endpoints
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.data.seed import seed_database

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    seed_database()

client = TestClient(app)

def test_root_and_health():
    res_root = client.get("/")
    assert res_root.status_code == 200
    assert res_root.json()["app"] == "VoxLearn AI"

    res_health = client.get("/health")
    assert res_health.status_code == 200
    assert res_health.json()["status"] == "healthy"

def test_user_profile():
    res = client.get("/api/user/profile?user_id=1")
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == 1
    assert "name" in data

def test_dashboard_summary():
    res = client.get("/api/dashboard/summary?user_id=1")
    assert res.status_code == 200
    data = res.json()
    assert "overall_mastery_percentage" in data
    assert "topic_breakdown" in data
    assert len(data["topic_breakdown"]) > 0
    assert "estimated_exam_readiness" in data
    assert "daily_recommendation" in data

def test_tutor_message():
    res = client.post("/api/tutor/message", json={
        "user_id": 1,
        "message": "Can you explain why a wire's resistance quadruples when stretched to double length?",
        "voice_transcribed": True
    })
    assert res.status_code == 200
    data = res.json()
    assert "content" in data
    assert data["sender"] == "assistant"
    assert "topic" in data

def test_quiz_flow():
    # 1. Start quiz
    start_res = client.post("/api/quiz/start", json={
        "user_id": 1,
        "quiz_type": "adaptive",
        "num_questions": 3
    })
    assert start_res.status_code == 200
    start_data = start_res.json()
    session_id = start_data["session_id"]
    questions = start_data["questions"]
    assert len(questions) > 0

    first_q = questions[0]

    # 2. Submit answer
    submit_res = client.post("/api/quiz/submit_answer", json={
        "user_id": 1,
        "quiz_session_id": session_id,
        "question_id": first_q["id"],
        "selected_option_index": 0,
        "confidence_level": 4,
        "time_taken_seconds": 15
    })
    assert submit_res.status_code == 200
    eval_data = submit_res.json()
    assert "is_correct" in eval_data
    assert "updated_p_l" in eval_data
    assert "mastery_percentage" in eval_data

    # 3. Complete session
    complete_res = client.post(f"/api/quiz/complete/{session_id}")
    assert complete_res.status_code == 200
    comp_data = complete_res.json()
    assert "accuracy_percentage" in comp_data

def test_mastery_and_graph():
    res_overview = client.get("/api/mastery/overview?user_id=1")
    assert res_overview.status_code == 200
    overview_data = res_overview.json()
    assert len(overview_data) >= 10

    res_graph = client.get("/api/mastery/graph?user_id=1")
    assert res_graph.status_code == 200
    graph_data = res_graph.json()
    assert "nodes" in graph_data
    assert "edges" in graph_data

def test_practice_and_analytics():
    res_misc = client.get("/api/practice/misconceptions?user_id=1")
    assert res_misc.status_code == 200
    misc_data = res_misc.json()
    assert len(misc_data) >= 5

    res_workout = client.get("/api/practice/weak_workout?user_id=1")
    assert res_workout.status_code == 200
    workout_data = res_workout.json()
    assert "questions" in workout_data

    res_analytics = client.get("/api/practice/analytics?user_id=1")
    assert res_analytics.status_code == 200
    analytics_data = res_analytics.json()
    assert "accuracy_by_difficulty" in analytics_data
    assert "misconception_distribution" in analytics_data
