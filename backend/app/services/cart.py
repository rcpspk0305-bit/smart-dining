from typing import List, Optional, Dict, Tuple
from app.schemas.cart import CartItem, CartResponse
from app.services.menu import MenuService
from app.services.session import SessionService

# In-memory cart database keyed by concatenated "session_id:table_id"
# Maps "session_id:table_id" -> list of CartItem objects
MOCK_CARTS_DB: Dict[str, List[CartItem]] = {}


class CartService:
    @staticmethod
    def _get_cart_key(session_id: str) -> str:
        """
        Helper method to retrieve or construct the combined session and table key.
        """
        session = SessionService.get_session(session_id)
        table_id = session.table_id if session else "demo_table"
        return f"{session_id}:{table_id}"

    @staticmethod
    def get_cart_items(session_id: str) -> List[CartItem]:
        """
        Fetch all items added to the table session's cart.
        """
        key = CartService._get_cart_key(session_id)
        if key not in MOCK_CARTS_DB:
            MOCK_CARTS_DB[key] = []
        return MOCK_CARTS_DB[key]

    @staticmethod
    def get_cart_response(session_id: str) -> CartResponse:
        """
        Builds a full CartResponse containing subtotal, 5% GST, grand total, and items.
        """
        session = SessionService.get_session(session_id)
        table_id = session.table_id if session else "demo_table"
        
        items = CartService.get_cart_items(session_id)
        
        subtotal = float(sum(item.menu_item.price * item.quantity for item in items))
        gst_amount = round(subtotal * 0.05, 2)
        grand_total = round(subtotal + gst_amount, 2)
        total_quantity = sum(item.quantity for item in items)
        
        return CartResponse(
            session_id=session_id,
            table_id=table_id,
            items=items,
            subtotal=subtotal,
            gst_amount=gst_amount,
            grand_total=grand_total,
            total_quantity=total_quantity
        )

    @staticmethod
    def add_item_to_cart(
        session_id: str, 
        menu_item_id: str, 
        quantity: int, 
        special_instructions: Optional[str] = None
    ) -> CartResponse:
        """
        Add a menu item to the cart. 
        If the item is already present, increments quantity.
        Uses Last-Write-Wins behavior for instructions (overwrite with latest comments).
        """
        menu_item = MenuService.get_item(menu_item_id)
        if not menu_item:
            raise ValueError(f"Menu item {menu_item_id} not found")

        items = CartService.get_cart_items(session_id)
        
        # Last-write-wins: match item
        existing = next((i for i in items if i.menu_item.id == menu_item_id), None)
        if existing:
            existing.quantity += quantity
            # Overwrite special instructions with latest write (Last-Write-Wins)
            if special_instructions is not None:
                existing.special_instructions = special_instructions
        else:
            new_item = CartItem(
                menu_item=menu_item,
                quantity=quantity,
                special_instructions=special_instructions
            )
            items.append(new_item)
            
        return CartService.get_cart_response(session_id)

    @staticmethod
    def update_cart_item(
        session_id: str, 
        cart_item_id: str, 
        quantity: int, 
        special_instructions: Optional[str] = None
    ) -> CartResponse:
        """
        Last-Write-Wins: Overwrites the cart item state (quantity and instructions) with the latest values.
        If quantity drops to 0 or less, the item is removed.
        """
        items = CartService.get_cart_items(session_id)
        existing = next((i for i in items if i.menu_item.id == cart_item_id), None)
        
        if existing:
            # Overwrite completely (Last-Write-Wins)
            existing.quantity = quantity
            if special_instructions is not None:
                existing.special_instructions = special_instructions
            
            # Clean up if empty
            if existing.quantity <= 0:
                items.remove(existing)
        else:
            # If it doesn't exist, we try to add it
            if quantity > 0:
                CartService.add_item_to_cart(
                    session_id=session_id,
                    menu_item_id=cart_item_id,
                    quantity=quantity,
                    special_instructions=special_instructions
                )
                
        return CartService.get_cart_response(session_id)

    @staticmethod
    def delete_cart_item(session_id: str, cart_item_id: str) -> CartResponse:
        """
        Remove a specific dish item from the active table cart.
        """
        items = CartService.get_cart_items(session_id)
        existing = next((i for i in items if i.menu_item.id == cart_item_id), None)
        if existing:
            items.remove(existing)
            
        return CartService.get_cart_response(session_id)

    @staticmethod
    def clear_cart(session_id: str) -> None:
        """
        Empty all items in the cart (e.g. after ordering).
        """
        key = CartService._get_cart_key(session_id)
        MOCK_CARTS_DB[key] = []
class CartItemUpdate:
    pass
