from fastapi import APIRouter, HTTPException
from app.schemas.cart import Cart, CartItemCreate, CartItem
from app.api.v1.endpoints.menu import MOCK_MENU_DB

router = APIRouter()

# In-memory mock carts storage mapping session_id -> list of items
MOCK_CARTS = {}

def calculate_cart_totals(session_id: str) -> Cart:
    items = MOCK_CARTS.get(session_id, [])
    total_price = 0.0
    total_quantity = 0
    for item in items:
        total_price += item.menu_item.price * item.quantity
        total_quantity += item.quantity
    
    return Cart(
        session_id=session_id,
        items=items,
        total_price=total_price,
        total_quantity=total_quantity
    )


@router.get("/{session_id}", response_model=Cart)
def get_session_cart(session_id: str) -> Cart:
    """
    Fetch the shopping cart corresponding to a specific table session.
    """
    if session_id not in MOCK_CARTS:
        MOCK_CARTS[session_id] = []
    return calculate_cart_totals(session_id)


@router.post("/items", response_model=Cart)
def update_cart_item(payload: CartItemCreate, session_id: str) -> Cart:
    """
    Add or update item quantity within the active session's cart.
    """
    # Verify menu item exists
    matching_menu_item = next((item for item in MOCK_MENU_DB if item.id == payload.menu_item_id), None)
    if not matching_menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")

    if session_id not in MOCK_CARTS:
        MOCK_CARTS[session_id] = []

    # Update or add
    existing_item = next((item for item in MOCK_CARTS[session_id] if item.menu_item.id == payload.menu_item_id), None)
    if existing_item:
        existing_item.quantity = payload.quantity
        existing_item.customization_notes = payload.customization_notes
    else:
        new_item = CartItem(
            menu_item=matching_menu_item,
            quantity=payload.quantity,
            customization_notes=payload.customization_notes
        )
        MOCK_CARTS[session_id].append(new_item)

    # Clean empty quantities
    MOCK_CARTS[session_id] = [i for i in MOCK_CARTS[session_id] if i.quantity > 0]

    return calculate_cart_totals(session_id)


@router.post("/clear", response_model=Cart)
def clear_cart(session_id: str) -> Cart:
    """
    Clear all items in the active session's cart.
    """
    MOCK_CARTS[session_id] = []
    return calculate_cart_totals(session_id)
