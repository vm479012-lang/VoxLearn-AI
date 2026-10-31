"""
AI Tutor router with Socratic guidance, voice-first interaction, and Wispr Flow support.
"""

import uuid
import datetime
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, TutorConversation, TutorMessage, StudyActivity
from ..schemas import TutorMessageRequest, TutorMessageResponse
from ..tutor_engine import TutorEngine

router = APIRouter(prefix="/tutor", tags=["AI Tutor"])

@router.post("/message", response_model=TutorMessageResponse)
def send_tutor_message(req: TutorMessageRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == req.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get or create conversation
    conv_id = req.conversation_id
    conversation = None
    if conv_id:
        conversation = db.query(TutorConversation).filter(TutorConversation.id == conv_id).first()

    if not conversation:
        conv_id = f"conv_{uuid.uuid4().hex[:10]}"
        topic_detected = TutorEngine.detect_topic(req.message)
        conversation = TutorConversation(
            id=conv_id,
            user_id=user.id,
            title=f"Socratic Session: {topic_detected.capitalize()}",
            topic=topic_detected.capitalize()
        )
        db.add(conversation)
        db.commit()

    # Save User message
    user_msg = TutorMessage(
        conversation_id=conv_id,
        sender="user",
        content=req.message,
        voice_transcribed=req.voice_transcribed,
        socratic_stage="user_query"
    )
    db.add(user_msg)

    # Generate Socratic AI response
    socratic_result = TutorEngine.generate_socratic_response(
        user_message=req.message,
        user_mastery_context={"user_name": user.name}
    )

    # Save Assistant response
    assistant_msg = TutorMessage(
        conversation_id=conv_id,
        sender="assistant",
        content=socratic_result["response_text"],
        voice_transcribed=False,
        socratic_stage=socratic_result["socratic_stage"],
        formulas_json=str(socratic_result.get("suggested_formulas", []))
    )
    assistant_msg.formulas = socratic_result.get("suggested_formulas", [])
    db.add(assistant_msg)

    # Add points and activity
    user.points += 15
    user.total_study_minutes += 3
    conversation.updated_at = datetime.datetime.utcnow()

    activity = StudyActivity(
        user_id=user.id,
        activity_type="tutor",
        title=f"AI Tutor: {socratic_result['topic']}",
        description=f"Engaged in voice-enabled Socratic dialogue on {socratic_result['topic']}",
        points=15
    )
    db.add(activity)
    db.commit()
    db.refresh(assistant_msg)

    return TutorMessageResponse(
        conversation_id=conv_id,
        sender="assistant",
        content=assistant_msg.content,
        topic=socratic_result["topic"],
        socratic_stage=assistant_msg.socratic_stage,
        suggested_formulas=assistant_msg.formulas,
        created_at=assistant_msg.created_at
    )

@router.get("/conversations")
def list_conversations(user_id: int = 1, db: Session = Depends(get_db)):
    convs = (
        db.query(TutorConversation)
        .filter(TutorConversation.user_id == user_id)
        .order_by(TutorConversation.updated_at.desc())
        .limit(10)
        .all()
    )
    return [
        {
            "id": c.id,
            "title": c.title,
            "topic": c.topic,
            "updated_at": c.updated_at.strftime("%b %d, %H:%M"),
            "message_count": len(c.messages)
        }
        for c in convs
    ]

@router.get("/conversation/{conv_id}")
def get_conversation_history(conv_id: str, db: Session = Depends(get_db)):
    conv = db.query(TutorConversation).filter(TutorConversation.id == conv_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")

    messages = (
        db.query(TutorMessage)
        .filter(TutorMessage.conversation_id == conv_id)
        .order_by(TutorMessage.created_at.asc())
        .all()
    )

    return {
        "id": conv.id,
        "title": conv.title,
        "topic": conv.topic,
        "messages": [
            {
                "id": m.id,
                "sender": m.sender,
                "content": m.content,
                "voice_transcribed": m.voice_transcribed,
                "socratic_stage": m.socratic_stage,
                "formulas": m.formulas,
                "created_at": m.created_at.strftime("%H:%M")
            }
            for m in messages
        ]
    }
