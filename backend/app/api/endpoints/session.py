from fastapi import APIRouter, HTTPException
from app.schemas.session import Session
from app.services.session import SessionService

router = APIRouter()


@router.get("/table/{tableId}/session", response_model=Session)
def get_or_create_table_session(tableId: str) -> Session:
    """
    GET /api/table/{tableId}/session
    Retrieve or create the active dining session at a specified table ID.
    """
    if not tableId.strip():
        raise HTTPException(status_code=400, detail="Table ID cannot be empty")
    return SessionService.get_or_create_table_session(tableId)
