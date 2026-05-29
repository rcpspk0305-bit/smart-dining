from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.schemas.menu import MenuItem

router = APIRouter()

# Global mock menu database
MOCK_MENU_DB: List[MenuItem] = [
    MenuItem(
        id="m1",
        name="Truffle Parmesan Fries",
        description="Hand-cut russet potatoes tossed in pure white truffle oil, shaved aged parmigiano-reggiano, and chopped fresh rosemary.",
        price=12.00,
        category="starters",
        tags=["Classic", "Truffle"],
        is_available=True,
        is_vegetarian=True,
        is_spicy=False,
    ),
    MenuItem(
        id="m2",
        name="Gourmet Wagyu Slider Trio",
        description="Minced premium wagyu beef patties, melted sharp cheddar, caramelized sweet onions, and microgreens on toasted brioche.",
        price=24.00,
        category="starters",
        tags=["Signature", "Beef"],
        is_available=True,
        is_vegetarian=False,
        is_spicy=False,
    ),
    MenuItem(
        id="m3",
        name="Signature Dry Aged Ribeye",
        description="28-day dry aged USDA prime ribeye seared in garlic herb butter. Served with roasted bone marrow.",
        price=58.00,
        category="mains",
        tags=["Aged", "Spicy"],
        is_available=True,
        is_vegetarian=False,
        is_spicy=True,
    ),
    MenuItem(
        id="m4",
        name="Wild Mushroom Gnocchi",
        description="Pan-seared potato gnocchi served with a medley of wild chanterelle mushrooms in a rich sage butter reduction.",
        price=28.00,
        category="mains",
        tags=["Local", "Vegetarian"],
        is_available=True,
        is_vegetarian=True,
        is_spicy=False,
    ),
    MenuItem(
        id="m5",
        name="Molten Lava Chocolate Soufflé",
        description="Warm Belgian dark chocolate cake with a molten center. Served with organic Madagascar vanilla bean gelato.",
        price=14.00,
        category="desserts",
        tags=["Sweet", "Chocolate"],
        is_available=True,
        is_vegetarian=True,
        is_spicy=False,
    ),
    MenuItem(
        id="m6",
        name="Smoked Rosemary Old Fashioned",
        description="Premium Kentucky bourbon, bitters, and orange peel smoked tableside with dried rosemary branches.",
        price=18.00,
        category="beverages",
        tags=["Alcoholic", "Smoked"],
        is_available=True,
        is_vegetarian=False,
        is_spicy=False,
    )
]

@router.get("/", response_model=List[MenuItem])
def get_menu_items(
    category: Optional[str] = Query(None, description="Filter menu items by category"),
    search: Optional[str] = Query(None, description="Search menu name or description")
) -> List[MenuItem]:
    """
    Retrieve active menu items with optional category filtering and search queries.
    """
    items = MOCK_MENU_DB
    if category:
        items = [i for i in items if i.category.lower() == category.lower()]
    if search:
        search_lower = search.lower()
        items = [
            i for i in items 
            if search_lower in i.name.lower() or search_lower in i.description.lower()
        ]
    return items


@router.get("/{item_id}", response_model=MenuItem)
def get_menu_item_by_id(item_id: str) -> MenuItem:
    """
    Retrieve details for a specific menu item.
    """
    for item in MOCK_MENU_DB:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Menu item not found")
