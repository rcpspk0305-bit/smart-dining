from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Literal, Optional
from app.schemas.cart import CartItem

OrderStatusType = Literal["pending", "PENDING", "confirmed", "preparing", "served", "completed", "cancelled"]


class OrderCreate(BaseModel):
    verification_token: Optional[str] = Field(None, examples=["token_xyz789"])


class Order(BaseModel):
    id: str
    session_id: str
    table_id: str
    items: List[CartItem]
    status: OrderStatusType = "PENDING"
    total_price: float
    created_at: datetime
    phone_number: Optional[str] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "order_7890",
                "session_id": "sess_abc123",
                "table_id": "T4",
                "items": [
                  {
                    "menu_item": {
                      "id": "m1",
                      "name": "Paneer Tikka Multani",
                      "category": "Veg Starters",
                      "price": 320.0,
                      "description": "Paneer cubes marinated in yogurt and yellow chili paste, grilled in tandoor.",
                      "image_url": "https://images.unsplash.com/photo-1565557623262-b51c2513a641",
                      "tags": ["veg", "chef_special", "shareable"],
                      "allergens": ["Dairy"],
                      "available": True,
                      "popular_score": 4.8,
                      "complementary_items": ["m6", "m10"]
                    },
                    "quantity": 1,
                    "special_instructions": "No onion"
                  }
                ],
                "status": "pending",
                "total_price": 336.0,
                "created_at": "2026-05-29T10:10:00Z",
                "phone_number": "+15555550199"
            }
        }
class OrderStatusUpdate(BaseModel):
    status: OrderStatusType
