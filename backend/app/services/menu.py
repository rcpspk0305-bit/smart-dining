from typing import List, Optional
from app.schemas.menu import MenuItem
from app.core.seed_data import SEED_MENU_ITEMS as MOCK_MENU_DB


class MenuService:
    @staticmethod
    def get_menu(category: Optional[str] = None) -> List[MenuItem]:
        """
        Get all available menu items or filter by category.
        """
        if category:
            # Match case-insensitively and strip spaces
            cat_clean = category.strip().lower()
            return [i for i in MOCK_MENU_DB if i.category.strip().lower() == cat_clean]
        return MOCK_MENU_DB

    @staticmethod
    def search_menu(query: str) -> List[MenuItem]:
        """
        Search dishes by name, description, or tag keywords.
        """
        q_lower = query.strip().lower()
        return [
            i for i in MOCK_MENU_DB
            if q_lower in i.name.lower() 
            or q_lower in i.description.lower() 
            or any(q_lower in tag.lower() for tag in i.tags)
        ]

    @staticmethod
    def get_item(item_id: str) -> Optional[MenuItem]:
        """
        Retrieve details of a single dish.
        """
        for item in MOCK_MENU_DB:
            if item.id == item_id:
                return item
        return None
