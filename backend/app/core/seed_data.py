from typing import List
from app.schemas.menu import MenuItem

SEED_MENU_ITEMS: List[MenuItem] = [
    # Veg Starters
    MenuItem(
        id="m1",
        name="Paneer Tikka Multani",
        category="Veg Starters",
        price=320.0,
        description="Fresh cottage cheese cubes marinated in spiced hung yogurt, cream cheese, yellow chili powder, and cooked in tandoor.",
        image_url="https://images.unsplash.com/photo-1565557623262-b51c2513a641?q=80&w=600",
        tags=["veg", "chef_special", "shareable"],
        allergens=["Dairy", "Mustard"],
        available=True,
        popular_score=4.8,
        complementary_items=["m22", "m21"]
    ),
    MenuItem(
        id="m2",
        name="Crispy Lotus Stem Honey Chili",
        category="Veg Starters",
        price=280.0,
        description="Crisp lotus stems tossed in sweet honey, dry red chilies, spring greens, and toasted sesame seeds.",
        image_url="https://images.unsplash.com/photo-1512621776951-a57141f2eefd?q=80&w=600",
        tags=["veg", "light", "quick_serve"],
        allergens=["Sesame", "Soy"],
        available=True,
        popular_score=4.6,
        complementary_items=["m23"]
    ),
    MenuItem(
        id="m3",
        name="Dahi Ke Sholay",
        category="Veg Starters",
        price=260.0,
        description="Crispy bread rolls stuffed with spiced hung curd, bell peppers, fresh coriander, and deep-fried to golden perfection.",
        image_url="https://images.unsplash.com/photo-1601050690597-df056fb4ce78?q=80&w=600",
        tags=["veg", "bestseller", "quick_serve"],
        allergens=["Dairy", "Gluten"],
        available=True,
        popular_score=4.7,
        complementary_items=["m21"]
    ),

    # Non-Veg Starters
    MenuItem(
        id="m4",
        name="Bhatti Ka Murgh Tikka",
        category="Non-Veg Starters",
        price=380.0,
        description="Succulent boneless chicken chunks marinated in black pepper, coriander seeds, yogurt, and slow-grilled.",
        image_url="https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?q=80&w=600",
        tags=["non-veg", "spicy", "shareable", "chef_special"],
        allergens=["Dairy", "Mustard"],
        available=True,
        popular_score=4.9,
        complementary_items=["m14", "m22"]
    ),
    MenuItem(
        id="m5",
        name="Tandoori Fish Amritsari",
        category="Non-Veg Starters",
        price=450.0,
        description="Fresh fish chunks marinated in carom seeds, chickpea flour, ajwain spices, and pan-fried to crisp perfection.",
        image_url="https://images.unsplash.com/photo-1534604973900-c43ab4c2e0ab?q=80&w=600",
        tags=["non-veg", "light", "quick_serve"],
        allergens=["Fish", "Gluten"],
        available=True,
        popular_score=4.5,
        complementary_items=["m22"]
    ),
    MenuItem(
        id="m6",
        name="Mutton Seekh Kebab",
        category="Non-Veg Starters",
        price=420.0,
        description="Finely minced goat shoulder seasoned with aromatic spices, fresh mint, and skewers grilled in charcoal tandoor.",
        image_url="https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?q=80&w=600",
        tags=["non-veg", "spicy", "bestseller", "shareable"],
        allergens=["Dairy"],
        available=True,
        popular_score=4.8,
        complementary_items=["m14", "m22"]
    ),

    # Mains (Veg)
    MenuItem(
        id="m7",
        name="Dal Makhani Gourmet",
        category="Mains (Veg)",
        price=340.0,
        description="Black lentils slow-cooked overnight on red-hot embers with heavy butter, tomato puree, and fenugreek greens.",
        image_url="https://images.unsplash.com/photo-1546833999-b9f581a1996d?q=80&w=600",
        tags=["veg", "bestseller", "shareable"],
        allergens=["Dairy"],
        available=True,
        popular_score=4.9,
        complementary_items=["m13", "m15"]
    ),
    MenuItem(
        id="m8",
        name="Paneer Butter Masala",
        category="Mains (Veg)",
        price=360.0,
        description="Soft cottage cheese cubes simmered in a silky, rich, sweet-spicy tomato, cream, cashew nut paste gravy.",
        image_url="https://images.unsplash.com/photo-1631452180519-c014fe946bc7?q=80&w=600",
        tags=["veg", "shareable"],
        allergens=["Dairy", "Nuts"],
        available=True,
        popular_score=4.7,
        complementary_items=["m13", "m16"]
    ),
    MenuItem(
        id="m9",
        name="Subz Miloni Diwani",
        category="Mains (Veg)",
        price=310.0,
        description="Assorted green garden vegetables cooked in a smooth, vibrant, spicy spinach and green onion gravy.",
        image_url="https://images.unsplash.com/photo-1512621776951-a57141f2eefd?q=80&w=600",
        tags=["veg", "light"],
        allergens=["Dairy"],
        available=True,
        popular_score=4.4,
        complementary_items=["m13", "m15"]
    ),

    # Mains (Non-Veg)
    MenuItem(
        id="m10",
        name="Signature Butter Chicken",
        category="Mains (Non-Veg)",
        price=440.0,
        description="Clay-oven roasted chicken tandoori shreds cooked inside a rich, mildly spiced, creamy tomato sauce loaded with white butter.",
        image_url="https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?q=80&w=600",
        tags=["non-veg", "bestseller", "shareable", "chef_special"],
        allergens=["Dairy", "Nuts"],
        available=True,
        popular_score=5.0,
        complementary_items=["m13", "m14"]
    ),
    MenuItem(
        id="m11",
        name="Kashmiri Mutton Rogan Josh",
        category="Mains (Non-Veg)",
        price=520.0,
        description="Slow-cooked tender baby mutton chunks in flavored gravy of kashmiri chilies, saffron, ginger, and wild spices.",
        image_url="https://images.unsplash.com/photo-1544025162-d76694265947?q=80&w=600",
        tags=["non-veg", "spicy", "chef_special"],
        allergens=[],
        available=True,
        popular_score=4.8,
        complementary_items=["m13", "m16"]
    ),
    MenuItem(
        id="m12",
        name="Chicken Tikka Masala",
        category="Mains (Non-Veg)",
        price=420.0,
        description="Char-grilled chicken cubes tossed in a thick, semi-dry gravy of toasted onions, green bell peppers, tomato pieces, and green chilies.",
        image_url="https://images.unsplash.com/photo-1565557623262-b51c2513a641?q=80&w=600",
        tags=["non-veg", "spicy", "shareable"],
        allergens=["Dairy"],
        available=True,
        popular_score=4.6,
        complementary_items=["m13", "m14"]
    ),

    # Breads & Rice
    MenuItem(
        id="m13",
        name="Butter Garlic Naan",
        category="Breads & Rice",
        price=80.0,
        description="Leavened flour flatbread topped with chopped fresh garlic, coriander leaves, and generous glaze of butter cooked in tandoor.",
        image_url="https://images.unsplash.com/photo-1601050690597-df056fb4ce78?q=80&w=600",
        tags=["veg", "quick_serve"],
        allergens=["Gluten", "Dairy"],
        available=True,
        popular_score=4.9,
        complementary_items=["m10", "m8", "m7"]
    ),
    MenuItem(
        id="m14",
        name="Gourmet Chicken Dum Biryani",
        category="Breads & Rice",
        price=410.0,
        description="Aromatic long-grain basmati rice layered with juicy spiced chicken, slow-cooked in sealed clay pot (dum) with saffron and fried mint leaves.",
        image_url="https://images.unsplash.com/photo-1633945274405-b6c8069047b0?q=80&w=600",
        tags=["non-veg", "bestseller", "shareable", "chef_special"],
        allergens=["Dairy"],
        available=True,
        popular_score=4.9,
        complementary_items=["m22", "m21"]
    ),
    MenuItem(
        id="m15",
        name="Steamed Basmati Rice",
        category="Breads & Rice",
        price=140.0,
        description="Fluffy, high-grade long-grain steamed basmati rice with a touch of ghee and wild cumin greens.",
        image_url="https://images.unsplash.com/photo-1536304997881-a372c179924b?q=80&w=600",
        tags=["veg", "light", "quick_serve"],
        allergens=["Dairy"],
        available=True,
        popular_score=4.3,
        complementary_items=["m7", "m9"]
    ),
    MenuItem(
        id="m16",
        name="Laccha Paratha",
        category="Breads & Rice",
        price=70.0,
        description="Layered, flaky whole-wheat Indian flatbread cooked with ghee in charcoal clay oven.",
        image_url="https://images.unsplash.com/photo-1601050690597-df056fb4ce78?q=80&w=600",
        tags=["veg", "quick_serve"],
        allergens=["Gluten", "Dairy"],
        available=True,
        popular_score=4.6,
        complementary_items=["m11", "m7"]
    ),

    # Desserts
    MenuItem(
        id="m17",
        name="Gulab Jamun with Rabri Trio",
        category="Desserts",
        price=180.0,
        description="Golden-fried condensed milk dumplings soaked in sticky rose cardamom syrup, served over thick chilled kesar rabri.",
        image_url="https://images.unsplash.com/photo-1589301760014-d929f3979dbc?q=80&w=600",
        tags=["veg", "bestseller", "quick_serve"],
        allergens=["Dairy", "Gluten", "Nuts"],
        available=True,
        popular_score=4.9,
        complementary_items=["m19"]
    ),
    MenuItem(
        id="m18",
        name="Elaneer Payasam",
        category="Desserts",
        price=190.0,
        description="A chilled classic dessert made of tender coconut meat, condensed cardamom milk, coconut cream, and dry nuts.",
        image_url="https://images.unsplash.com/photo-1589301760014-d929f3979dbc?q=80&w=600",
        tags=["veg", "light", "chef_special"],
        allergens=["Dairy", "Nuts"],
        available=True,
        popular_score=4.8,
        complementary_items=[]
    ),

    # Beverages (Hot)
    MenuItem(
        id="m19",
        name="Kesari Masala Chai",
        category="Beverages (Hot)",
        price=90.0,
        description="Freshly brewed loose-leaf Indian tea leaves infused with ground green cardamom, cinnamon, saffron, and whole creamy milk.",
        image_url="https://images.unsplash.com/photo-1576092768241-dec231879fc3?q=80&w=600",
        tags=["veg", "quick_serve"],
        allergens=["Dairy"],
        available=True,
        popular_score=4.8,
        complementary_items=["m3", "m17"]
    ),
    MenuItem(
        id="m20",
        name="Mysore Filter Coffee",
        category="Beverages (Hot)",
        price=110.0,
        description="Authentic south Indian decoction made from premium chicory-blended coffee beans, frothed with hot creamy milk.",
        image_url="https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?q=80&w=600",
        tags=["veg", "quick_serve"],
        allergens=["Dairy"],
        available=True,
        popular_score=4.7,
        complementary_items=["m3"]
    ),

    # Beverages (Cold)
    MenuItem(
        id="m21",
        name="Royal Mango Lassi",
        category="Beverages (Cold)",
        price=160.0,
        description="Creamy frothed curd blended with premium alphanso mango pulp, saffron sprigs, chopped pistachio garnish.",
        image_url="https://images.unsplash.com/photo-1572490122747-3968b75cc699?q=80&w=600",
        tags=["veg", "bestseller", "quick_serve"],
        allergens=["Dairy", "Nuts"],
        available=True,
        popular_score=4.9,
        complementary_items=["m1", "m3"]
    ),
    MenuItem(
        id="m22",
        name="Mint Masala Shikanji",
        category="Beverages (Cold)",
        price=120.0,
        description="Thirst-quenching iced lemonade blended with fresh mint leaves, roasted cumin powder, and black salt soda base.",
        image_url="https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?q=80&w=600",
        tags=["veg", "light", "quick_serve"],
        allergens=[],
        available=True,
        popular_score=4.6,
        complementary_items=["m4", "m6", "m14"]
    ),
    MenuItem(
        id="m23",
        name="Smoked Rosemary Berry Cooler",
        category="Beverages (Cold)",
        price=180.0,
        description="Muddled blackberries, elderflower cordial, pressed lemon, topped with carbonated water and smoked tableside with fresh dry rosemary.",
        image_url="https://images.unsplash.com/photo-1536935338788-846bb9981813?q=80&w=600",
        tags=["veg", "light", "chef_special"],
        allergens=[],
        available=True,
        popular_score=4.8,
        complementary_items=["m2", "m5"]
    ),

    # Combos & Deals
    MenuItem(
        id="m24",
        name="Executive Veg Thali",
        category="Combos & Deals",
        price=490.0,
        description="Complete gourmet experience featuring half-portion Paneer Butter Masala, Dal Makhani, mixed vegetable dry curry, steamed basmati rice, 1 butter roti, salad, papad, and 1 sweet gulab jamun.",
        image_url="https://images.unsplash.com/photo-1546833999-b9f581a1996d?q=80&w=600",
        tags=["veg", "bestseller", "shareable"],
        allergens=["Dairy", "Gluten", "Nuts"],
        available=True,
        popular_score=4.9,
        complementary_items=["m21"]
    ),
    MenuItem(
        id="m25",
        name="Royal Non-Veg Kebab Platter",
        category="Combos & Deals",
        price=790.0,
        description="Assorted sharing starter tray containing 3 pieces Bhatti Murgh Tikka, 3 pieces Mutton Seekh Kebabs, 3 pieces Tandoori Amritsari Fish, served with charcoal mint chutney, salad, and garlic naan bread.",
        image_url="https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?q=80&w=600",
        tags=["non-veg", "spicy", "shareable", "chef_special"],
        allergens=["Dairy", "Gluten", "Fish", "Mustard"],
        available=True,
        popular_score=5.0,
        complementary_items=["m22", "m23"]
    )
]
