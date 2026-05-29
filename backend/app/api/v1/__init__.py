from fastapi import APIRouter
from app.api.v1.endpoints import menu, session, cart, chat, otp, order

api_router = APIRouter()

api_router.include_router(session.router, prefix="/session", tags=["Session"])
api_router.include_router(menu.router, prefix="/menu", tags=["Menu"])
api_router.include_router(cart.router, prefix="/cart", tags=["Cart"])
api_router.include_router(otp.router, prefix="/otp", tags=["OTP Security"])
api_router.include_router(order.router, prefix="/order", tags=["Orders"])
api_router.include_router(chat.router, prefix="/chat", tags=["AI Chat Assistant"])
