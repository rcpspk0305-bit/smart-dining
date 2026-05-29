import uuid
from datetime import datetime, timezone
from fastapi import APIRouter
from app.schemas.chat import ChatMessage, ChatMessageCreate
from app.services.ai import AIService

router = APIRouter()

# In-memory mock chat db
MOCK_CHAT_DB = {}

@router.post("/message", response_model=ChatMessage)
def send_chat_message(payload: ChatMessageCreate) -> ChatMessage:
    """
    Send a message to the AI dining guide and receive a custom recommendation or response.
    """
    session_id = payload.session_id
    if session_id not in MOCK_CHAT_DB:
        MOCK_CHAT_DB[session_id] = []

    # Save User message
    user_msg_id = f"msg_{uuid.uuid4().hex[:8]}"
    user_msg = ChatMessage(
        id=user_msg_id,
        sender="user",
        content=payload.content,
        timestamp=datetime.now(timezone.utc)
    )
    MOCK_CHAT_DB[session_id].append(user_msg)

    # Process via AI Service
    ai_text = AIService.generate_response(payload.content, session_id)

    # Save and return Assistant reply
    ai_msg_id = f"msg_{uuid.uuid4().hex[:8]}"
    ai_msg = ChatMessage(
        id=ai_msg_id,
        sender="assistant",
        content=ai_text,
        timestamp=datetime.now(timezone.utc)
    )
    MOCK_CHAT_DB[session_id].append(ai_msg)

    return ai_msg
