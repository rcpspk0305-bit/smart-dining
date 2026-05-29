import uuid
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict
from app.schemas.session import Session

# Global in-memory sessions dictionary mapping session_id -> Session
MOCK_SESSIONS_DB: Dict[str, Session] = {}

# Session TTL constant in hours
SESSION_TTL_HOURS = 2


class SessionService:
    @staticmethod
    def get_or_create_table_session(table_id: str) -> Session:
        """
        Check if an active, unexpired session exists for a specific table ID.
        If yes, return it; otherwise create and return a new active session with TTL.
        """
        now = datetime.now(timezone.utc)
        
        # Check for existing active session at table
        for sess in list(MOCK_SESSIONS_DB.values()):
            if sess.table_id == table_id and sess.is_active:
                # Calculate current remaining TTL
                remaining = (sess.expires_at - now).total_seconds()
                if remaining > 0:
                    sess.ttl_seconds_remaining = remaining
                    return sess
                else:
                    # Session expired! Close it.
                    sess.is_active = False
                    sess.ttl_seconds_remaining = 0.0

        # Create new session
        session_id = f"sess_{uuid.uuid4().hex[:8]}"
        created_at = now
        expires_at = created_at + timedelta(hours=SESSION_TTL_HOURS)
        
        new_session = Session(
            id=session_id,
            table_id=table_id,
            is_active=True,
            created_at=created_at,
            expires_at=expires_at,
            ttl_seconds_remaining=float(SESSION_TTL_HOURS * 3600)
        )
        MOCK_SESSIONS_DB[session_id] = new_session
        return new_session

    @staticmethod
    def get_session(session_id: str) -> Optional[Session]:
        """
        Retrieve details of a session by session ID, dynamically calculating remaining TTL.
        """
        sess = MOCK_SESSIONS_DB.get(session_id)
        if not sess:
            return None
            
        now = datetime.now(timezone.utc)
        remaining = (sess.expires_at - now).total_seconds()
        
        if remaining <= 0:
            sess.is_active = False
            sess.ttl_seconds_remaining = 0.0
        else:
            sess.ttl_seconds_remaining = remaining
            
        return sess
