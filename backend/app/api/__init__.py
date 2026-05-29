from fastapi import APIRouter
from app.api.endpoints import menu, session, cart, chat, otp, order

api_router = APIRouter()

api_router.include_router(menu.router, prefix="/menu", tags=["Menu"])
api_router.include_router(session.router, tags=["Table Session"])
api_router.include_router(cart.router, tags=["Cart"])
api_router.include_router(chat.router, tags=["AI Chat Assistant"])
api_router.include_router(otp.router, prefix="/otp", tags=["OTP Security"])
api_router.include_router(order.router, tags=["Orders"])
