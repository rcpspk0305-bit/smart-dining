from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from app.core.config import settings


class ChatRequest(BaseModel):
    message: str = Field(
        ..., 
        max_length=settings.CHAT_MESSAGE_MAX_LENGTH, 
        examples=["Bestseller paneer items suggest karo!"]
    )


class ChatSuggestion(BaseModel):
    itemId: str = Field(..., examples=["m1"])
    name: str = Field(..., examples=["Paneer Tikka Multani"])
    price: float = Field(..., examples=[320.0])
    reason: str = Field(..., examples=["This is our bestseller tandoori paneer starter!"])


class ChatResponse(BaseModel):
    message: str = Field(..., description="Concise, warm response in the user's language/language-mix")
    suggestions: List[ChatSuggestion] = Field(default_factory=list, description="At most 3 recommended menu items")
    timestamp: datetime = Field(default_factory=datetime.now)

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Arre, paneer lovers ke liye Dahi Ke Sholay aur Paneer Tikka Multani best options hain!",
                "suggestions": [
                    {
                        "itemId": "m1",
                        "name": "Paneer Tikka Multani",
                        "price": 320.0,
                        "reason": "Our highly rated tandoori paneer bestseller."
                    }
                ],
                "timestamp": "2026-05-29T10:05:00Z"
            }
        }
