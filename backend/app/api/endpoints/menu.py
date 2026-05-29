from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from app.schemas.menu import MenuItem
from app.services.menu import MenuService

router = APIRouter()


@router.get("", response_model=List[MenuItem])
def get_menu(
    category: Optional[str] = Query(None, description="Filter menu items by category")
) -> List[MenuItem]:
    """
    GET /api/menu
    Retrieve list of dishes. Filters supported.
    """
    return MenuService.get_menu(category)


@router.get("/search", response_model=List[MenuItem])
def search_menu(
    q: str = Query(..., description="Query string to search dish names or descriptions")
) -> List[MenuItem]:
    """
    GET /api/menu/search
    Retrieve dishes matching a search string.
    """
    return MenuService.search_menu(q)
