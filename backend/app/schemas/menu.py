from pydantic import BaseModel, Field
from typing import List, Optional


class MenuItemBase(BaseModel):
    name: str = Field(..., examples=["Paneer Tikka Multani"])
    category: str = Field(..., examples=["Veg Starters"])
    price: float = Field(..., gt=0.0, description="Price in INR", examples=[320.0])
    description: str = Field(..., examples=["Paneer cubes marinated in yogurt and yellow chili paste, grilled in tandoor."])
    image_url: Optional[str] = Field(None, examples=["https://images.unsplash.com/photo-1565557623262-b51c2513a641"])
    tags: List[str] = Field(default_factory=list, examples=[["veg", "chef_special", "shareable"]])
    allergens: List[str] = Field(default_factory=list, examples=[["Dairy"]])
    available: bool = True
    popular_score: float = Field(default=4.5, ge=0.0, le=5.0, examples=[4.8])
    complementary_items: List[str] = Field(default_factory=list, examples=[["m6", "m10"]])


class MenuItemCreate(MenuItemBase):
    pass


class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    tags: Optional[List[str]] = None
    allergens: Optional[List[str]] = None
    available: Optional[bool] = None
    popular_score: Optional[float] = None
    complementary_items: Optional[List[str]] = None


class MenuItem(MenuItemBase):
    id: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
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
            }
        }
