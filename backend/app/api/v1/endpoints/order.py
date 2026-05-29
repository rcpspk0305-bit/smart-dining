import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from app.schemas.order import Order, OrderCreate
from app.api.v1.endpoints.cart import MOCK_CARTS, calculate_cart_totals
from app.api.v1.endpoints.session import MOCK_SESSIONS
from app.core.security import verify_token

router = APIRouter()

# In-memory mock orders database mapping order_id -> Order
MOCK_ORDERS = {}

@router.post("/", response_model=Order)
def place_order(payload: OrderCreate) -> Order:
    """
    Submit active session cart items to create a kitchen dining order.
    Requires validation of the OTP JWT verification token.
    """
    # 1. Validate JWT verification token
    phone_number = verify_token(payload.verification_token)
    if not phone_number:
        raise HTTPException(
            status_code=401, 
            detail="Unauthorized. Active verified phone session is required to place orders."
        )

    session_id = payload.session_id

    # 2. Get Active Session details
    session = MOCK_SESSIONS.get(session_id)
    if not session or not session.is_active:
        raise HTTPException(status_code=404, detail="Active table session not found")

    # 3. Pull cart items
    cart = calculate_cart_totals(session_id)
    if not cart.items:
        raise HTTPException(status_code=400, detail="Cannot place order. Dining cart is empty.")

    # 4. Create Order
    order_id = f"order_{uuid.uuid4().hex[:6]}"
    new_order = Order(
        id=order_id,
        session_id=session_id,
        table_id=session.table_id,
        items=cart.items,
        status="pending",
        total_price=cart.total_price,
        created_at=datetime.now(timezone.utc),
        phone_number=phone_number
    )

    MOCK_ORDERS[order_id] = new_order

    # Clear active session cart after order placement
    MOCK_CARTS[session_id] = []

    return new_order


@router.get("/{order_id}", response_model=Order)
def get_order(order_id: str) -> Order:
    """
    Fetch order detail and tracking status.
    """
    if order_id in MOCK_ORDERS:
        return MOCK_ORDERS[order_id]
    
    raise HTTPException(status_code=404, detail="Order not found")
