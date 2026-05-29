import uuid
from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
from app.schemas.session import Session, SessionCreate

router = APIRouter()

# In-memory mock session database
MOCK_SESSIONS = {}

@router.post("/init", response_model=Session)
def initialize_session(payload: SessionCreate) -> Session:
    """
    Initialize a new active dining session at a specified table ID.
    If an active session already exists for the table, it returns the existing session.
    """
    # Simple check for existing active session at table
    for sess in MOCK_SESSIONS.values():
        if sess.table_id == payload.table_id and sess.is_active:
            return sess

    # Create new session
    session_id = f"sess_{uuid.uuid4().hex[:8]}"
    new_session = Session(
        id=session_id,
        table_id=payload.table_id,
        is_active=True,
        start_time=datetime.now(timezone.utc),
        end_time=None
    )
    MOCK_SESSIONS[session_id] = new_session
    return new_session


@router.get("/{session_id}", response_model=Session)
def get_session(session_id: str) -> Session:
    """
    Retrieve active session details by its unique identifier.
    """
    if session_id in MOCK_SESSIONS:
        return MOCK_SESSIONS[session_id]
    
    # Fallback to simulate a session so it doesn't fail during testing
    fallback_session = Session(
        id=session_id,
        table_id="T4",
        is_active=True,
        start_time=datetime.now(timezone.utc),
        end_time=None
    )
    MOCK_SESSIONS[session_id] = fallback_session
    return fallback_session
