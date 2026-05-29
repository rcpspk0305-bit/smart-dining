from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class SessionBase(BaseModel):
    table_id: str = Field(..., examples=["T4"])


class SessionCreate(SessionBase):
    pass


class Session(SessionBase):
    id: str
    is_active: bool = True
    created_at: datetime
    expires_at: datetime
    ttl_seconds_remaining: float

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "sess_abc123",
                "table_id": "T4",
                "is_active": True,
                "created_at": "2026-05-29T10:00:00Z",
                "expires_at": "2026-05-29T12:00:00Z",
                "ttl_seconds_remaining": 7200.0
            }
        }
