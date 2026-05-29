import asyncio
from fastapi import APIRouter, HTTPException
from app.schemas.order import Order, OrderCreate
from app.services.order import OrderService
from app.services.session import SessionService
from app.services.websocket_manager import manager

router = APIRouter()


@router.post("/session/{sessionId}/order", response_model=Order)
def place_order(sessionId: str, payload: OrderCreate) -> Order:
    """
    POST /api/session/{sessionId}/order
    Submit cart items to place a kitchen dining order.
    Requires phone verification JWT verification_token.
    """
    try:
        order = OrderService.create_order(
            session_id=sessionId,
            verification_token=payload.verification_token
        )
        
        # Broadcast real-time order placement to all clients on the table
        session = SessionService.get_session(sessionId)
        if session:
            event_payload = {
                "event": "order_placed",
                "table_id": session.table_id,
                "order_id": order.id,
                "total": order.total_price
            }
            asyncio.create_task(manager.broadcast(session.table_id, event_payload))
            
        return order
    except PermissionError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/order/{orderId}", response_model=Order)
def get_order(orderId: str) -> Order:
    """
    GET /api/order/{orderId}
    Fetch order status and tracking details.
    """
    order = OrderService.get_order(orderId)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
