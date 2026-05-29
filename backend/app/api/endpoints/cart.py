import asyncio
from fastapi import APIRouter, HTTPException
from app.schemas.cart import CartItemCreate, CartItemUpdate, CartResponse
from app.services.cart import CartService
from app.services.session import SessionService
from app.services.websocket_manager import manager

router = APIRouter()


def _broadcast_cart_change(session_id: str, action: str):
    """
    Non-blocking helper to broadcast updated cart details to all table clients.
    """
    session = SessionService.get_session(session_id)
    if session:
        cart_data = CartService.get_cart_response(session_id)
        # Serialize cart_data using Pydantic serialization
        message = {
            "event": "cart_updated",
            "table_id": session.table_id,
            "action": action,
            "cart": {
                "session_id": cart_data.session_id,
                "table_id": cart_data.table_id,
                "items": [
                    {
                        "menu_item": {
                            "id": item.menu_item.id,
                            "name": item.menu_item.name,
                            "category": item.menu_item.category,
                            "price": item.menu_item.price,
                            "description": item.menu_item.description,
                            "image_url": item.menu_item.image_url,
                            "tags": item.menu_item.tags,
                            "allergens": item.menu_item.allergens,
                            "available": item.menu_item.available,
                            "popular_score": item.menu_item.popular_score,
                            "complementary_items": item.menu_item.complementary_items
                        },
                        "quantity": item.quantity,
                        "special_instructions": item.special_instructions
                    } for item in cart_data.items
                ],
                "subtotal": cart_data.subtotal,
                "gst_amount": cart_data.gst_amount,
                "grand_total": cart_data.grand_total,
                "total_quantity": cart_data.total_quantity
            }
        }
        # Schedule the coroutine asynchronously
        asyncio.create_task(manager.broadcast(session.table_id, message))


@router.get("/session/{sessionId}/cart", response_model=CartResponse)
def get_session_cart(sessionId: str) -> CartResponse:
    """
    GET /api/session/{sessionId}/cart
    Retrieve the active shopping cart details, including subtotal, 5% GST breakdown, and grand total.
    """
    session = SessionService.get_session(sessionId)
    if not session:
        raise HTTPException(status_code=404, detail="Active table session not found")
        
    return CartService.get_cart_response(sessionId)


@router.post("/session/{sessionId}/cart", response_model=CartResponse)
def add_item_to_cart(sessionId: str, payload: CartItemCreate) -> CartResponse:
    """
    POST /api/session/{sessionId}/cart
    Add a new dish item or increment its quantity. Special instructions support included.
    Uses Last-Write-Wins logic for item comments.
    """
    session = SessionService.get_session(sessionId)
    if not session:
        raise HTTPException(status_code=404, detail="Active table session not found")
        
    try:
        res = CartService.add_item_to_cart(
            session_id=sessionId,
            menu_item_id=payload.menu_item_id,
            quantity=payload.quantity,
            special_instructions=payload.special_instructions
        )
        # Broadcast real-time change
        _broadcast_cart_change(sessionId, "item_added")
        return res
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/session/{sessionId}/cart/{cartItemId}", response_model=CartResponse)
def update_cart_item(sessionId: str, cartItemId: str, payload: CartItemUpdate) -> CartResponse:
    """
    PATCH /api/session/{sessionId}/cart/{cartItemId}
    Last-Write-Wins: Overwrites the cart item's quantity and instructions directly.
    """
    session = SessionService.get_session(sessionId)
    if not session:
        raise HTTPException(status_code=404, detail="Active table session not found")
        
    res = CartService.update_cart_item(
        session_id=sessionId,
        cart_item_id=cartItemId,
        quantity=payload.quantity,
        special_instructions=payload.special_instructions
    )
    # Broadcast real-time change
    _broadcast_cart_change(sessionId, "item_updated")
    return res


@router.delete("/session/{sessionId}/cart/{cartItemId}", response_model=CartResponse)
def delete_cart_item(sessionId: str, cartItemId: str) -> CartResponse:
    """
    DELETE /api/session/{sessionId}/cart/{cartItemId}
    Remove a specific item from the active table cart.
    """
    session = SessionService.get_session(sessionId)
    if not session:
        raise HTTPException(status_code=404, detail="Active table session not found")
        
    res = CartService.delete_cart_item(sessionId, cartItemId)
    # Broadcast real-time change
    _broadcast_cart_change(sessionId, "item_removed")
    return res
