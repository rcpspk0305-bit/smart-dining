import uuid
from datetime import datetime, timezone
from typing import Dict, Optional
from app.schemas.order import Order
from app.services.session import SessionService
from app.services.cart import CartService
from app.core.security import verify_token

# Central in-memory mock database mapping order_id -> Order
MOCK_ORDERS_DB: Dict[str, Order] = {}


class OrderService:
    @staticmethod
    def create_order(session_id: str, verification_token: Optional[str] = None) -> Order:
        """
        Creates a kitchen order ticket from the active table session cart.
        To keep the implementation demo-friendly, we do not strictly require 
        a valid OTP token; we fallback to a default demo phone number if missing.
        """
        # 1. Decode phone number if token is provided, otherwise fallback to demo number
        phone_number = None
        if verification_token and verification_token.strip():
            phone_number = verify_token(verification_token)
            
        if not phone_number:
            # Graceful fallback for demo friendliness
            phone_number = "+919999999999"

        # 2. Get active table session details
        session = SessionService.get_session(session_id)
        if not session or not session.is_active:
            raise ValueError("Active table session not found or has expired")

        # 3. Pull cart items list
        cart_items = CartService.get_cart_items(session_id)
        if not cart_items:
            raise ValueError("Cannot place order. Active dining cart is empty.")

        # 4. Calculate subtotal & grand total (including 5% GST)
        subtotal = sum(item.menu_item.price * item.quantity for item in cart_items)
        grand_total = round(subtotal * 1.05, 2)

        # 5. Create Order ticket
        order_id = f"order_{uuid.uuid4().hex[:6]}"
        new_order = Order(
            id=order_id,
            session_id=session_id,
            table_id=session.table_id,
            items=cart_items.copy(),
            status="PENDING",
            total_price=grand_total,
            created_at=datetime.now(timezone.utc),
            phone_number=phone_number
        )

        MOCK_ORDERS_DB[order_id] = new_order

        # Clear cart upon success
        CartService.clear_cart(session_id)

        return new_order

    @staticmethod
    def get_order(order_id: str) -> Optional[Order]:
        """
        Retrieve order status and details by order ID.
        """
        return MOCK_ORDERS_DB.get(order_id)
