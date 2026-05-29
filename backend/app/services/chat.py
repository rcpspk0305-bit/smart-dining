from app.schemas.chat import ChatResponse
from app.services.ai_orchestrator import AIOrchestrator


class ChatService:
    @staticmethod
    def generate_chat_reply(message: str, session_id: str) -> ChatResponse:
        """
        Delegates message parsing, dialect translation, and tandoori upselling 
        to the AIOrchestrator core engine.
        """
        return AIOrchestrator.process_chat(message, session_id)
