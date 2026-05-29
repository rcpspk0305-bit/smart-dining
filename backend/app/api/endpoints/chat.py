from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat import ChatService
from app.services.session import SessionService

router = APIRouter()


@router.post("/session/{sessionId}/ai/chat", response_model=ChatResponse)
def post_ai_chat_message(sessionId: str, payload: ChatRequest) -> ChatResponse:
    """
    POST /api/session/{sessionId}/ai/chat
    Submit a query to the AI dining guide and receive a custom menu recommendation or assistance response.
    """
    # Verify session exists
    session = SessionService.get_session(sessionId)
    if not session:
        raise HTTPException(status_code=404, detail="Active table session not found")

    return ChatService.generate_chat_reply(
        message=payload.message,
        session_id=sessionId
    )
