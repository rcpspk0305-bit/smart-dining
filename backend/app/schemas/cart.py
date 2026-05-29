from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.menu import MenuItem


class CartItemCreate(BaseModel):
    menu_item_id: str = Field(..., examples=["m1"])
    quantity: int = Field(..., ge=1, examples=[1])
    special_instructions: Optional[str] = Field(None, max_length=200, examples=["No onion, no garlic"])


class CartItemUpdate(BaseModel):
    quantity: int = Field(..., ge=0, examples=[2])
    special_instructions: Optional[str] = Field(None, max_length=200, examples=["Make it extra spicy"])


class CartItem(BaseModel):
    menu_item: MenuItem
    quantity: int
    special_instructions: Optional[str] = None

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    session_id: str
    table_id: str
    items: List[CartItem] = Field(default_factory=list)
    subtotal: float = Field(0.0, description="Sum of (item price * quantity) in INR")
    gst_amount: float = Field(0.0, description="5% GST on subtotal in INR")
    grand_total: float = Field(0.0, description="Subtotal + GST in INR")
    total_quantity: int = Field(0, description="Total items in cart")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "session_id": "sess_abc123",
                "table_id": "T4",
                "items": [
                    {
                        "menu_item": {
                            "id": "m1",
                            "name": "Paneer Tikka Multani",
                            "category": "Veg Starters",
                            "price": 320.0,
                            "description": "Fresh cottage cheese cubes marinated in spiced hung yogurt, cream cheese, yellow chili powder, and cooked in tandoor.",
                            "image_url": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?q=80&w=600",
                            "tags": ["veg", "chef_special", "shareable"],
                            "allergens": ["Dairy", "Mustard"],
                            "available": True,
                            "popular_score": 4.8,
                            "complementary_items": ["m22", "m21"]
                        },
                        "quantity": 2,
                        "special_instructions": "No onion, no garlic"
                    }
                ],
                "subtotal": 640.0,
                "gst_amount": 32.0,
                "grand_total": 672.0,
                "total_quantity": 2
            }
        }
