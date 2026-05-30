"use client";

import { useParams } from "next/navigation";
import { useState, useMemo, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { 
  Sparkles, 
  ShoppingBag, 
  X, 
  Plus, 
  Minus, 
  CheckCircle2, 
  AlertCircle, 
  Search, 
  Check, 
  Flame, 
  Leaf, 
  UtensilsCrossed 
} from "lucide-react";
import { MenuItem, ChatMessage, CartItem } from "@/types";
import CartDrawer from "@/components/CartDrawer";
import CheckoutModal from "@/components/CheckoutModal";
import ChatDrawer from "@/components/ChatDrawer";
import { API_BASE_URL, WS_BASE_URL } from "@/lib/config";

// Authentic 25 Indian restaurant menu items loaded directly for standalone or integrated frontend excellence!
const SEED_MENU: MenuItem[] = [
  {
    id: "m1",
    name: "Paneer Tikka Multani",
    category: "Veg Starters",
    price: 320.0,
    description: "Fresh cottage cheese cubes marinated in spiced hung yogurt, cream cheese, yellow chili powder, and cooked in tandoor.",
    image_url: "https://images.unsplash.com/photo-1565557623262-b51c2513a641?q=80&w=600",
    tags: ["veg", "chef_special", "shareable"],
    allergens: ["Dairy", "Mustard"],
    available: true,
    popular_score: 4.8,
    complementary_items: ["m22", "m21"]
  },
  {
    id: "m2",
    name: "Crispy Lotus Stem Honey Chili",
    category: "Veg Starters",
    price: 280.0,
    description: "Crisp lotus stems tossed in sweet honey, dry red chilies, spring greens, and toasted sesame seeds.",
    image_url: "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?q=80&w=600",
    tags: ["veg", "light", "quick_serve"],
    allergens: ["Sesame", "Soy"],
    available: true,
    popular_score: 4.6,
    complementary_items: ["m23"]
  },
  {
    id: "m3",
    name: "Dahi Ke Sholay",
    category: "Veg Starters",
    price: 260.0,
    description: "Crispy bread rolls stuffed with spiced hung curd, bell peppers, fresh coriander, and deep-fried to golden perfection.",
    image_url: "https://images.unsplash.com/photo-1601050690597-df056fb4ce78?q=80&w=600",
    tags: ["veg", "bestseller", "quick_serve"],
    allergens: ["Dairy", "Gluten"],
    available: true,
    popular_score: 4.7,
    complementary_items: ["m21"]
  },
  {
    id: "m4",
    name: "Bhatti Ka Murgh Tikka",
    category: "Non-Veg Starters",
    price: 380.0,
    description: "Succulent boneless chicken chunks marinated in black pepper, coriander seeds, yogurt, and slow-grilled.",
    image_url: "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?q=80&w=600",
    tags: ["non-veg", "spicy", "shareable", "chef_special"],
    allergens: ["Dairy", "Mustard"],
    available: true,
    popular_score: 4.9,
    complementary_items: ["m14", "m22"]
  },
  {
    id: "m5",
    name: "Tandoori Fish Amritsari",
    category: "Non-Veg Starters",
    price: 450.0,
    description: "Fresh fish chunks marinated in carom seeds, chickpea flour, ajwain spices, and pan-fried to crisp perfection.",
    image_url: "https://images.unsplash.com/photo-1534604973900-c43ab4c2e0ab?q=80&w=600",
    tags: ["non-veg", "light", "quick_serve"],
    allergens: ["Fish", "Gluten"],
    available: true,
    popular_score: 4.5,
    complementary_items: ["m22"]
  },
  {
    id: "m6",
    name: "Mutton Seekh Kebab",
    category: "Non-Veg Starters",
    price: 420.0,
    description: "Finely minced goat shoulder seasoned with aromatic spices, fresh mint, and skewers grilled in charcoal tandoor.",
    image_url: "https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?q=80&w=600",
    tags: ["non-veg", "spicy", "bestseller", "shareable"],
    allergens: ["Dairy"],
    available: true,
    popular_score: 4.8,
    complementary_items: ["m14", "m22"]
  },
  {
    id: "m7",
    name: "Dal Makhani Gourmet",
    category: "Mains (Veg)",
    price: 340.0,
    description: "Black lentils slow-cooked overnight on red-hot embers with heavy butter, tomato puree, and fenugreek greens.",
    image_url: "https://images.unsplash.com/photo-1546833999-b9f581a1996d?q=80&w=600",
    tags: ["veg", "bestseller", "shareable"],
    allergens: ["Dairy"],
    available: true,
    popular_score: 4.9,
    complementary_items: ["m13", "m15"]
  },
  {
    id: "m8",
    name: "Paneer Butter Masala",
    category: "Mains (Veg)",
    price: 360.0,
    description: "Soft cottage cheese cubes simmered in a silky, rich, sweet-spicy tomato, cream, cashew nut paste gravy.",
    image_url: "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?q=80&w=600",
    tags: ["veg", "shareable"],
    allergens: ["Dairy", "Nuts"],
    available: true,
    popular_score: 4.7,
    complementary_items: ["m13", "m16"]
  },
  {
    id: "m9",
    name: "Subz Miloni Diwani",
    category: "Mains (Veg)",
    price: 310.0,
    description: "Assorted green garden vegetables cooked in a smooth, vibrant, spicy spinach and green onion gravy.",
    image_url: "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?q=80&w=600",
    tags: ["veg", "light"],
    allergens: ["Dairy"],
    available: true,
    popular_score: 4.4,
    complementary_items: ["m13", "m15"]
  },
  {
    id: "m10",
    name: "Signature Butter Chicken",
    category: "Mains (Non-Veg)",
    price: 440.0,
    description: "Clay-oven roasted chicken tandoori shreds cooked inside a rich, mildly spiced, creamy tomato sauce loaded with white butter.",
    image_url: "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?q=80&w=600",
    tags: ["non-veg", "bestseller", "shareable", "chef_special"],
    allergens: ["Dairy", "Nuts"],
    available: true,
    popular_score: 5.0,
    complementary_items: ["m13", "m14"]
  },
  {
    id: "m11",
    name: "Kashmiri Mutton Rogan Josh",
    category: "Mains (Non-Veg)",
    price: 520.0,
    description: "Slow-cooked tender baby mutton chunks in flavored gravy of kashmiri chilies, saffron, ginger, and wild spices.",
    image_url: "https://images.unsplash.com/photo-1544025162-d76694265947?q=80&w=600",
    tags: ["non-veg", "spicy", "chef_special"],
    allergens: [],
    available: true,
    popular_score: 4.8,
    complementary_items: ["m13", "m16"]
  },
  {
    id: "m12",
    name: "Chicken Tikka Masala",
    category: "Mains (Non-Veg)",
    price: 420.0,
    description: "Char-grilled chicken cubes tossed in a thick, semi-dry gravy of toasted onions, green bell peppers, tomato pieces, and green chilies.",
    image_url: "https://images.unsplash.com/photo-1565557623262-b51c2513a641?q=80&w=600",
    tags: ["non-veg", "spicy", "shareable"],
    allergens: ["Dairy"],
    available: true,
    popular_score: 4.6,
    complementary_items: ["m13", "m14"]
  },
  {
    id: "m13",
    name: "Butter Garlic Naan",
    category: "Breads & Rice",
    price: 80.0,
    description: "Leavened flour flatbread topped with chopped fresh garlic, coriander leaves, and generous glaze of butter cooked in tandoor.",
    image_url: "https://images.unsplash.com/photo-1601050690597-df056fb4ce78?q=80&w=600",
    tags: ["veg", "quick_serve"],
    allergens: ["Gluten", "Dairy"],
    available: true,
    popular_score: 4.9,
    complementary_items: ["m10", "m8", "m7"]
  },
  {
    id: "m14",
    name: "Gourmet Chicken Dum Biryani",
    category: "Breads & Rice",
    price: 410.0,
    description: "Aromatic long-grain basmati rice layered with juicy spiced chicken, slow-cooked in sealed clay pot (dum) with saffron and fried mint leaves.",
    image_url: "https://images.unsplash.com/photo-1633945274405-b6c8069047b0?q=80&w=600",
    tags: ["non-veg", "bestseller", "shareable", "chef_special"],
    allergens: ["Dairy"],
    available: true,
    popular_score: 4.9,
    complementary_items: ["m22", "m21"]
  },
  {
    id: "m17",
    name: "Gulab Jamun with Rabri Trio",
    category: "Desserts",
    price: 180.0,
    description: "Golden-fried condensed milk dumplings soaked in sticky rose cardamom syrup, served over thick chilled kesar rabri.",
    image_url: "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?q=80&w=600",
    tags: ["veg", "bestseller", "quick_serve"],
    allergens: ["Dairy", "Gluten", "Nuts"],
    available: true,
    popular_score: 4.9,
    complementary_items: ["m19"]
  },
  {
    id: "m18",
    name: "Elaneer Payasam",
    category: "Desserts",
    price: 190.0,
    description: "A chilled classic dessert made of tender coconut meat, condensed cardamom milk, coconut cream, and dry nuts.",
    image_url: "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?q=80&w=600",
    tags: ["veg", "light", "chef_special"],
    allergens: ["Dairy", "Nuts"],
    available: true,
    popular_score: 4.8,
    complementary_items: []
  },
  {
    id: "m19",
    name: "Kesari Masala Chai",
    category: "Beverages (Hot)",
    price: 90.0,
    description: "Freshly brewed loose-leaf Indian tea leaves infused with ground green cardamom, cinnamon, saffron, and whole creamy milk.",
    image_url: "https://images.unsplash.com/photo-1576092768241-dec231879fc3?q=80&w=600",
    tags: ["veg", "quick_serve"],
    allergens: ["Dairy"],
    available: true,
    popular_score: 4.8,
    complementary_items: ["m3", "m17"]
  },
  {
    id: "m21",
    name: "Royal Mango Lassi",
    category: "Beverages (Cold)",
    price: 160.0,
    description: "Creamy frothed curd blended with premium alphanso mango pulp, saffron sprigs, chopped pistachio garnish.",
    image_url: "https://images.unsplash.com/photo-1572490122747-3968b75cc699?q=80&w=600",
    tags: ["veg", "bestseller", "quick_serve"],
    allergens: ["Dairy", "Nuts"],
    available: true,
    popular_score: 4.9,
    complementary_items: ["m1", "m3"]
  },
  {
    id: "m22",
    name: "Mint Masala Shikanji",
    category: "Beverages (Cold)",
    price: 120.0,
    description: "Thirst-quenching iced lemonade blended with fresh mint leaves, roasted cumin powder, and black salt soda base.",
    image_url: "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?q=80&w=600",
    tags: ["veg", "light", "quick_serve"],
    allergens: [],
    available: true,
    popular_score: 4.6,
    complementary_items: ["m4", "m6", "m14"]
  },
  {
    id: "m23",
    name: "Smoked Rosemary Berry Cooler",
    category: "Beverages (Cold)",
    price: 180.0,
    description: "Muddled blackberries, elderflower cordial, pressed lemon, topped with carbonated water and smoked tableside with fresh dry rosemary.",
    image_url: "https://images.unsplash.com/photo-1536935338788-846bb9981813?q=80&w=600",
    tags: ["veg", "light", "chef_special"],
    allergens: [],
    available: true,
    popular_score: 4.8,
    complementary_items: ["m2", "m5"]
  },
  {
    id: "m24",
    name: "Executive Veg Thali",
    category: "Combos & Deals",
    price: 490.0,
    description: "Complete Veg Thali featuring Paneer Butter Masala, Dal Makhani, mixed vegetable dry curry, steamed basmati rice, butter roti, salad, and sweet gulab jamun.",
    image_url: "https://images.unsplash.com/photo-1546833999-b9f581a1996d?q=80&w=600",
    tags: ["veg", "bestseller", "shareable"],
    allergens: ["Dairy", "Gluten", "Nuts"],
    available: true,
    popular_score: 4.9,
    complementary_items: ["m21"]
  },
  {
    id: "m25",
    name: "Royal Non-Veg Kebab Platter",
    category: "Combos & Deals",
    price: 790.0,
    description: "Assorted sharing tray containing 3 pieces Bhatti Murgh Tikka, 3 pieces Mutton Seekh Kebabs, 3 pieces Fish Amritsari, garlic naan, and mint chutney.",
    image_url: "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?q=80&w=600",
    tags: ["non-veg", "spicy", "shareable", "chef_special"],
    allergens: ["Dairy", "Gluten", "Fish", "Mustard"],
    available: true,
    popular_score: 5.0,
    complementary_items: ["m22", "m23"]
  }
];

// Centralized available categories
const CATEGORIES = [
  "All",
  "Veg Starters",
  "Non-Veg Starters",
  "Mains (Veg)",
  "Mains (Non-Veg)",
  "Breads & Rice",
  "Desserts",
  "Beverages (Hot)",
  "Beverages (Cold)",
  "Combos & Deals"
];

// Centralized allergen constants
const ALLERGENS = ["Dairy", "Nuts", "Gluten", "Fish", "Mustard", "Sesame", "Soy"];

export default function TableSession() {
  const { tableId } = useParams();
  
  // UI States
  const [activeCategory, setActiveCategory] = useState<string>("All");
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [excludedAllergens, setExcludedAllergens] = useState<string[]>([]);
  const [cart, setCart] = useState<CartItem[]>([]);
  const [isCartOpen, setIsCartOpen] = useState<boolean>(false);
  const [isChatOpen, setIsChatOpen] = useState<boolean>(false);
  const [isCheckoutOpen, setIsCheckoutOpen] = useState<boolean>(false);
  
  // Collaborative & Live Backend Sync States
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [isBackendMode, setIsBackendMode] = useState<boolean>(false);
  const [activeUsersCount, setActiveUsersCount] = useState<number>(1);
  const [isGlowActive, setIsGlowActive] = useState<boolean>(false);
  const [glowAction, setGlowAction] = useState<string>("");

  // Unread Dot State (Simulating Zara having recommendations on page load!)
  const [hasUnreadSuggestions, setHasUnreadSuggestions] = useState<boolean>(true);
  
  // AI Chat States
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "1",
      sender: "assistant",
      content: "Namaste! I am Zara, your frothed tableside dining guide. I can recommend premium wine pairings, tailor dishes for your food allergies, or page a waiter. What are you craving today?",
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ]);
  const [isTyping, setIsTyping] = useState<boolean>(false);

  // Success state hooks
  const [orderPlaced, setOrderPlaced] = useState<boolean>(false);
  const [placedOrderId, setPlacedOrderId] = useState<string>("");

  // Synchronize with backend if running
  useEffect(() => {
    let ws: WebSocket | null = null;
    let reconnectTimeout: any = null;

    async function initSession() {
      try {
        // Try to fetch session from backend
        const res = await fetch(`${API_BASE_URL}/api/table/${tableId}/session`);
        if (!res.ok) throw new Error("Backend REST offline");
        const sessionData = await res.json();
        
        setSessionId(sessionData.id);
        setIsBackendMode(true);

        // Fetch current cart items
        const cartRes = await fetch(`${API_BASE_URL}/api/session/${sessionData.id}/cart`);
        if (cartRes.ok) {
          const cartData = await cartRes.json();
          setCart(cartData.items || []);
        }

        // Establish WebSocket connection for real-time updates
        const connectWS = () => {
          const wsUrl = `${WS_BASE_URL}/api/ws/table/${tableId}`;
          ws = new WebSocket(wsUrl);

          ws.onopen = () => {
            console.log("WebSocket connected to table:", tableId);
          };

          ws.onmessage = (event) => {
            try {
              const data = JSON.parse(event.data);
              console.log("WebSocket event received:", data);

              if (data.event === "user_joined" || data.event === "user_left") {
                setActiveUsersCount(data.active_users || 1);
              } else if (data.event === "cart_updated") {
                // Flash glow border/animation to show incoming table change!
                setGlowAction(data.action || "item_added");
                setIsGlowActive(true);
                setTimeout(() => setIsGlowActive(false), 1500);

                // Update the shared cart state
                if (data.cart && data.cart.items) {
                  setCart(data.cart.items);
                }
              } else if (data.event === "order_placed") {
                // Automatically transition to order success state for all guests!
                setPlacedOrderId(data.order_id);
                setOrderPlaced(true);
                setCart([]);
                setIsCartOpen(false);
                setIsCheckoutOpen(false);
              }
            } catch (err) {
              console.error("Error parsing WebSocket message:", err);
            }
          };

          ws.onerror = (err) => {
            console.error("WebSocket error:", err);
          };

          ws.onclose = () => {
            console.log("WebSocket closed, retrying in 3s...");
            reconnectTimeout = setTimeout(connectWS, 3000);
          };
        };

        connectWS();

      } catch (err) {
        console.warn("FastAPI backend not reachable. Falling back to frontend mock standalone state machine.", err);
        setIsBackendMode(false);
      }
    }

    initSession();

    return () => {
      if (ws) {
        ws.onclose = null;
        ws.close();
      }
      if (reconnectTimeout) clearTimeout(reconnectTimeout);
    };
  }, [tableId]);

  // Toggle Excluded Allergens
  const toggleAllergen = (allergen: string) => {
    setExcludedAllergens((prev) =>
      prev.includes(allergen) ? prev.filter((a) => a !== allergen) : [...prev, allergen]
    );
  };

  // Filter Menu Items recursively based on: active category, search, and allergen exclusion
  const filteredMenu = useMemo(() => {
    return SEED_MENU.filter((item) => {
      // 1. Category check
      if (activeCategory !== "All" && item.category !== activeCategory) {
        return false;
      }
      
      // 2. Search check
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const matchesName = item.name.toLowerCase().includes(q);
        const matchesDesc = item.description.toLowerCase().includes(q);
        const matchesTags = item.tags.some(t => t.toLowerCase().includes(q));
        if (!matchesName && !matchesDesc && !matchesTags) return false;
      }

      // 3. Allergen check (if item contains any of the excluded allergens, filter it out!)
      const containsExcluded = item.allergens.some(a => excludedAllergens.includes(a));
      if (containsExcluded) return false;

      return true;
    });
  }, [activeCategory, searchQuery, excludedAllergens]);

  // AI Pick for You Section: Top-rated dishes matching allergen constraints
  const aiPicks = useMemo(() => {
    return SEED_MENU.filter((item) => {
      // Must be highly rated and NOT contain any excluded allergens
      const isHighlyRated = item.popular_score >= 4.8;
      const containsExcluded = item.allergens.some(a => excludedAllergens.includes(a));
      return isHighlyRated && !containsExcluded;
    }).slice(0, 3);
  }, [excludedAllergens]);

  // Cart operations
  const addToCart = async (item: MenuItem, notes?: string) => {
    if (isBackendMode && sessionId) {
      try {
        const payload = {
          menu_item_id: item.id,
          quantity: 1,
          special_instructions: notes || null
        };
        const response = await fetch(`${API_BASE_URL}/api/session/${sessionId}/cart`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        if (response.ok) {
          const updatedCart = await response.json();
          setCart(updatedCart.items || []);
          return;
        }
      } catch (err) {
        console.error("Failed to add item to backend cart, falling back to local:", err);
      }
    }

    // Standalone fallback
    setCart((prev) => {
      const existing = prev.find((i) => i.menu_item.id === item.id);
      if (existing) {
        return prev.map((i) =>
          i.menu_item.id === item.id 
            ? { ...i, quantity: i.quantity + 1, special_instructions: notes || i.special_instructions } 
            : i
        );
      }
      return [...prev, { menu_item: item, quantity: 1, special_instructions: notes }];
    });
  };

  // Add to cart by Item ID (useful for Zara recommendation cards inside chat!)
  const handleAddToCartById = (itemId: string) => {
    const dish = SEED_MENU.find(d => d.id === itemId);
    if (dish) {
      addToCart(dish, "Added from Zara Recommendations");
    }
  };

  const updateQuantity = async (itemId: string, delta: number) => {
    const currentItem = cart.find(i => i.menu_item.id === itemId);
    if (!currentItem) return;

    const nextQty = currentItem.quantity + delta;

    if (isBackendMode && sessionId) {
      try {
        if (nextQty <= 0) {
          const response = await fetch(`${API_BASE_URL}/api/session/${sessionId}/cart/${itemId}`, {
            method: "DELETE"
          });
          if (response.ok) {
            const updatedCart = await response.json();
            setCart(updatedCart.items || []);
            return;
          }
        } else {
          const payload = {
            quantity: nextQty,
            special_instructions: currentItem.special_instructions || null
          };
          const response = await fetch(`${API_BASE_URL}/api/session/${sessionId}/cart/${itemId}`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
          });
          if (response.ok) {
            const updatedCart = await response.json();
            setCart(updatedCart.items || []);
            return;
          }
        }
      } catch (err) {
        console.error("Failed to update backend cart, falling back to local:", err);
      }
    }

    // Standalone fallback
    setCart((prev) => {
      return prev
        .map((i) => {
          if (i.menu_item.id === itemId) {
            return nextQty <= 0 ? null : { ...i, quantity: nextQty };
          }
          return i;
        })
        .filter((i): i is CartItem => i !== null);
    });
  };

  // Last-Write-Wins special instructions update
  const saveInstructions = async (itemId: string, text: string) => {
    const currentItem = cart.find(i => i.menu_item.id === itemId);
    if (!currentItem) return;

    if (isBackendMode && sessionId) {
      try {
        const payload = {
          quantity: currentItem.quantity,
          special_instructions: text || null
        };
        const response = await fetch(`${API_BASE_URL}/api/session/${sessionId}/cart/${itemId}`, {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        if (response.ok) {
          const updatedCart = await response.json();
          setCart(updatedCart.items || []);
          return;
        }
      } catch (err) {
        console.error("Failed to save special instructions to backend, falling back to local:", err);
      }
    }

    // Standalone fallback
    setCart((prev) =>
      prev.map((i) =>
        i.menu_item.id === itemId ? { ...i, special_instructions: text } : i
      )
    );
  };

  // Cart pricing totals (Indian 5% GST structure)
  const subtotal = cart.reduce((acc, item) => acc + item.quantity * item.menu_item.price, 0);
  const gstAmount = Math.round(subtotal * 0.05 * 100) / 100;
  const grandTotal = Math.round((subtotal + gstAmount) * 100) / 100;
  const totalQuantity = cart.reduce((acc, item) => acc + item.quantity, 0);

  // Send message to AI guide (Zara)
  const handleSendMessage = async (text: string) => {
    if (!text.trim()) return;

    const userMsg: ChatMessage = {
      id: Math.random().toString(),
      sender: "user",
      content: text,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages((prev) => [...prev, userMsg]);
    setIsTyping(true);

    if (isBackendMode && sessionId) {
      try {
        const response = await fetch(`${API_BASE_URL}/api/session/${sessionId}/ai/chat`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: text })
        });
        if (response.ok) {
          const chatRes = await response.json();
          const aiMsg: ChatMessage = {
            id: Math.random().toString(),
            sender: "assistant",
            content: chatRes.message,
            timestamp: new Date(chatRes.timestamp || new Date()).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
          };
          setMessages((prev) => [...prev, aiMsg]);
          setIsTyping(false);

          if (!isChatOpen) {
            setHasUnreadSuggestions(true);
          }
          return;
        }
      } catch (err) {
        console.error("Failed to fetch AI chat from backend, falling back to mock:", err);
      }
    }

    // Simulate AI response based on keyword matching
    setTimeout(() => {
      let aiReply = "That sounds delicious! Would you like me to add that to your cart or recommend a beverage pairing?";
      const lower = text.toLowerCase();
      
      if (lower.includes("recommend") || lower.includes("suggest") || lower.includes("bestseller")) {
        aiReply = "I highly recommend our Signature Butter Chicken (m10), cooked inside a rich creamy tomato sauce loaded with white butter. Pair it with a fresh Butter Garlic Naan (m13) and a frothed Royal Mango Lassi (m21)!";
      } else if (lower.includes("vegetarian") || lower.includes("veg")) {
        aiReply = "For vegetarian mains, our Dal Makhani Gourmet (m7) is slow-cooked overnight on embers and is extremely popular. The Paneer Tikka Multani (m1) is an excellent starter choice!";
      } else if (lower.includes("spicy") || lower.includes("heat")) {
        aiReply = "If you like heat, the Kashmiri Mutton Rogan Josh (m11) or the Bhatti Ka Murgh Tikka (m4) starter are loaded with aromatic whole spices.";
      } else if (lower.includes("allergy") || lower.includes("allergic") || lower.includes("gluten") || lower.includes("dairy")) {
        aiReply = "I can filter out dishes containing allergens immediately! Use the Exclude Allergen tags at the top, and the menu grid will hide any unsafe items instantly.";
      } else if (lower.includes("water") || lower.includes("waiter") || lower.includes("bill") || lower.includes("service")) {
        aiReply = "I have flagged Table " + tableId + " to page our active waiting staff. A server will assist you with fresh water / services shortly.";
      }

      const aiMsg: ChatMessage = {
        id: Math.random().toString(),
        sender: "assistant",
        content: aiReply,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages((prev) => [...prev, aiMsg]);
      setIsTyping(false);

      // Trigger unread suggestions indicator if Zara generates a suggestion while chat is closed
      if (!isChatOpen) {
        setHasUnreadSuggestions(true);
      }
    }, 1200);
  };

  const handleOrderSuccess = (orderId: string) => {
    setPlacedOrderId(orderId);
    setOrderPlaced(true);
    setCart([]);
  };

  const handleOpenChat = () => {
    setIsChatOpen(true);
    setHasUnreadSuggestions(false); // Reset unread dot when chat drawer is opened!
  };

  return (
    <div className="flex-1 flex flex-col justify-between h-screen relative bg-neutral-950 text-neutral-200 overflow-hidden font-sans">
      
      {/* Header showing restaurant and table */}
      <header className="px-5 py-4 border-b border-neutral-800/60 bg-neutral-900/90 backdrop-blur-md sticky top-0 z-30 flex items-center justify-between shadow-sm">
        <div className="flex items-center gap-2.5">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-orange-600 to-amber-500 flex items-center justify-center font-bold text-white text-sm shadow-md shadow-orange-500/10">
            {tableId}
          </div>
          <div>
            <h1 className="text-sm font-display font-bold text-neutral-100 uppercase tracking-wider">Gourmet AI Café</h1>
            <div className="flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
              <span className="text-[10px] font-medium text-neutral-400">Active table session</span>
            </div>
          </div>
        </div>
        
        <div className="flex items-center gap-3">
          {/* Header Ask Zara Trigger with unread indicator */}
          <button 
            aria-label="Ask Zara AI Assistant"
            onClick={handleOpenChat}
            className="relative px-3 py-1.5 bg-[#bc470a]/15 hover:bg-[#bc470a]/25 text-orange-300 border border-orange-500/20 rounded-xl text-[10px] font-bold flex items-center gap-1 active:scale-95 transition-all h-8"
          >
            <Sparkles className="w-3.5 h-3.5 text-orange-300 animate-pulse" /> Ask Zara
            {hasUnreadSuggestions && (
              <span className="absolute -top-1 -right-1 w-2.5 h-2.5 rounded-full bg-red-500 border border-neutral-900 animate-ping"></span>
            )}
          </button>
        </div>
      </header>

      {/* Collaborative Table Banner */}
      <div className={`px-5 py-2.5 bg-neutral-900/60 border-b border-neutral-850/80 backdrop-blur-md flex items-center justify-between transition-all duration-500 ${isGlowActive ? "ring-2 ring-emerald-500/80 animate-pulse bg-emerald-950/20" : ""}`}>
        <div className="flex items-center gap-2">
          <div className="flex -space-x-1.5 overflow-hidden">
            {Array.from({ length: Math.min(activeUsersCount, 4) }).map((_, i) => (
              <div
                key={i}
                className={`inline-block h-5 w-5 rounded-full ring-2 ring-neutral-950 bg-gradient-to-tr ${
                  i === 0 ? "from-orange-600 to-amber-500" :
                  i === 1 ? "from-emerald-600 to-teal-500" :
                  i === 2 ? "from-blue-600 to-indigo-500" :
                  "from-purple-600 to-pink-500"
                } flex items-center justify-center text-[8px] font-bold text-white uppercase`}
              >
                {String.fromCharCode(65 + i)}
              </div>
            ))}
            {activeUsersCount > 4 && (
              <div className="inline-block h-5 w-5 rounded-full ring-2 ring-neutral-950 bg-neutral-800 flex items-center justify-center text-[8px] font-bold text-neutral-400">
                +{activeUsersCount - 4}
              </div>
            )}
          </div>
          <span className="text-[10px] font-bold text-neutral-300 font-sans tracking-wide">
            {activeUsersCount} {activeUsersCount === 1 ? "Guest" : "Guests"} online at table {tableId}
          </span>
        </div>
        
        {isGlowActive ? (
          <div className="flex items-center gap-1.5 animate-bounce">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-ping"></span>
            <span className="text-[9px] font-bold text-emerald-400 font-mono uppercase tracking-wider">
              {glowAction === "item_added" ? "Item Added!" : glowAction === "item_removed" ? "Item Removed!" : "Cart Updated!"}
            </span>
          </div>
        ) : (
          <div className="flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
            <span className="text-[9px] font-semibold text-neutral-400">Live Collaborative Sync</span>
          </div>
        )}
      </div>

      {/* Main content scroll viewport */}
      <div className="flex-1 overflow-y-auto no-scrollbar pb-32">
        
        {/* Banner with search */}
        <div className="p-5 bg-gradient-to-b from-neutral-900/50 to-transparent border-b border-neutral-950 space-y-4">
          <div className="relative">
            <Search className="absolute left-3.5 top-3 w-4 h-4 text-neutral-500" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search biryani, paneer, drinks, tags..."
              className="w-full pl-10 pr-4 py-2.5 bg-neutral-900/80 border border-neutral-800/80 rounded-2xl text-xs text-neutral-100 placeholder-neutral-500 focus:outline-none focus:border-orange-500 focus:ring-1 focus:ring-orange-500/30 transition-all font-medium"
            />
            {searchQuery && (
              <button 
                onClick={() => setSearchQuery("")} 
                className="absolute right-3 top-3.5 text-neutral-500 hover:text-neutral-300"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            )}
          </div>
        </div>

        {/* Allergen Exclude Toggles */}
        <div className="px-5 py-1 space-y-2">
          <div className="flex items-center justify-between text-xs text-neutral-400">
            <span className="font-semibold flex items-center gap-1.5">
              <AlertCircle className="w-3.5 h-3.5 text-orange-500/80" /> Exclude Allergens
            </span>
            {excludedAllergens.length > 0 && (
              <button 
                onClick={() => setExcludedAllergens([])} 
                className="text-[10px] text-orange-400 font-semibold hover:underline"
              >
                Clear all
              </button>
            )}
          </div>
          <div className="flex gap-2 overflow-x-auto no-scrollbar py-1">
            {ALLERGENS.map((all) => {
              const active = excludedAllergens.includes(all);
              return (
                <button
                  key={all}
                  onClick={() => toggleAllergen(all)}
                  className={`px-3 py-1.5 rounded-xl text-[10px] font-semibold border transition-all flex items-center gap-1 ${
                    active
                      ? "bg-red-950/40 border-red-500/40 text-red-400 shadow-sm"
                      : "bg-neutral-900/40 border-neutral-800/60 text-neutral-400 hover:text-neutral-200"
                  }`}
                >
                  {active && <Check className="w-3 h-3 text-red-400" />} {all}
                </button>
              );
            })}
          </div>
        </div>

        {/* AI Pick For You Section */}
        {aiPicks.length > 0 && (
          <div className="mt-5 px-5 space-y-3">
            <div className="flex items-center gap-1.5 text-xs font-bold text-orange-400 uppercase tracking-wide">
              <Sparkles className="w-4 h-4 text-orange-500" /> AI Pick For You
            </div>
            
            <div className="flex gap-4 overflow-x-auto no-scrollbar py-1">
              {aiPicks.map((pick) => (
                <div
                  key={pick.id}
                  className="w-64 shrink-0 rounded-2xl bg-gradient-to-b from-neutral-900/60 to-neutral-950 border border-neutral-800/80 p-3.5 flex flex-col justify-between gap-3 shadow-inner relative overflow-hidden"
                >
                  <div className="absolute top-2 right-2 bg-orange-600/10 border border-orange-500/20 text-orange-400 px-2 py-0.5 rounded-full text-[9px] font-bold font-mono">
                    ★ {pick.popular_score.toFixed(1)}
                  </div>
                  
                  <div className="space-y-1">
                    <h2 className="text-xs font-display font-bold text-neutral-100 pr-10">{pick.name}</h2>
                    <p className="text-[10px] text-neutral-400 leading-relaxed line-clamp-2 pr-2">{pick.description}</p>
                  </div>
                  
                  <div className="flex items-center justify-between pt-2 border-t border-neutral-900/60">
                    <span className="text-xs font-mono font-bold text-orange-400">₹{pick.price}</span>
                    <Button
                      size="sm"
                      onClick={() => addToCart(pick, "Recommended by Zara")}
                      className="bg-[#bc470a] hover:bg-[#a13b08] text-white font-bold h-7 rounded-lg text-[10px] px-3 active:scale-95 shadow shadow-orange-600/20"
                    >
                      Quick Add
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Category Filter Scrollbar */}
        <div className="sticky top-[67px] bg-neutral-950/95 backdrop-blur z-20 border-y border-neutral-900/60 px-5 py-3.5 flex gap-2 overflow-x-auto no-scrollbar mt-6">
          {CATEGORIES.map((cat) => (
            <button
              key={cat}
              onClick={() => setActiveCategory(cat)}
              className={`px-4 py-1.5 rounded-xl text-xs font-semibold transition-all whitespace-nowrap ${
                activeCategory === cat
                  ? "bg-[#bc470a] text-white shadow-md shadow-orange-600/10"
                  : "bg-neutral-900/60 border border-neutral-800/40 text-neutral-400 hover:text-neutral-200"
              }`}
            >
              {cat}
            </button>
          ))}
        </div>

        {/* Menu Grid & Cards */}
        <div className="p-5 space-y-4">
          
          {orderPlaced && (
            <div className="p-4 rounded-2xl bg-emerald-950/20 border border-emerald-500/20 flex gap-3 animate-fade-in">
              <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
              <div>
                <h4 className="text-xs font-bold text-emerald-300">Kitchen Ticket Registered!</h4>
                <p className="text-[10px] text-emerald-400/80 mt-0.5">
                  Order **{placedOrderId}** has been sent to chef. Feel free to continue adding items or ask AI for service!
                </p>
                <Button 
                  size="sm" 
                  variant="ghost" 
                  onClick={() => setOrderPlaced(false)}
                  className="text-[10px] text-emerald-400 font-semibold h-6 px-0 mt-2 hover:bg-transparent"
                >
                  Dismiss
                </Button>
              </div>
            </div>
          )}

          {filteredMenu.length === 0 ? (
            <div className="p-12 text-center space-y-2 border border-dashed border-neutral-800 rounded-2xl">
              <UtensilsCrossed className="w-8 h-8 text-neutral-600 mx-auto" />
              <p className="text-xs text-neutral-400 font-medium">No dishes match your active filter criteria.</p>
              <button 
                onClick={() => { setActiveCategory("All"); setExcludedAllergens([]); setSearchQuery(""); }} 
                className="text-[10px] text-orange-400 font-bold hover:underline mt-1"
              >
                Reset filters
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 gap-4">
              {filteredMenu.map((dish) => (
                <div
                  key={dish.id}
                  className="p-3.5 rounded-2xl bg-neutral-900/30 border border-neutral-900/60 glass-panel flex gap-3.5 hover:border-neutral-800 transition-all duration-300"
                >
                  {/* Dish Mock Image */}
                  <div className="w-20 h-20 rounded-xl bg-neutral-950 border border-neutral-800 shrink-0 overflow-hidden relative group">
                    <img 
                      src={dish.image_url} 
                      alt={dish.name}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                    {dish.tags.includes("bestseller") && (
                      <span className="absolute bottom-1 left-1 bg-amber-500 text-black text-[7px] font-bold px-1 rounded-sm uppercase tracking-wide">
                        Bestseller
                      </span>
                    )}
                  </div>

                  <div className="flex-1 flex flex-col justify-between gap-2.5">
                    <div className="space-y-1">
                      <div className="flex items-start justify-between gap-2">
                        <div className="flex items-center gap-1.5">
                          <h2 className="text-xs font-display font-bold text-neutral-100">{dish.name}</h2>
                          <div className="flex gap-0.5">
                            {dish.tags.includes("veg") && <Leaf className="w-3 h-3 text-emerald-500" title="Veg" />}
                            {dish.tags.includes("spicy") && <Flame className="w-3 h-3 text-red-500" title="Spicy" />}
                          </div>
                        </div>
                        <span className="text-xs font-bold font-mono text-orange-400">₹{dish.price}</span>
                      </div>
                      <p className="text-[10px] text-neutral-400 leading-relaxed font-light line-clamp-2">{dish.description}</p>
                    </div>

                    <div className="flex justify-between items-center pt-1.5 border-t border-neutral-900/40">
                      {/* Dish tags */}
                      <div className="flex gap-1 overflow-x-auto no-scrollbar">
                        {dish.tags.filter(t => t !== "veg" && t !== "non-veg").slice(0, 2).map((t) => (
                          <span
                            key={t}
                            className="px-1.5 py-0.5 rounded bg-neutral-900/80 border border-neutral-800 text-[8px] font-semibold text-[#a6a6a6] uppercase tracking-wider whitespace-nowrap"
                          >
                            {t.replace("_", " ")}
                          </span>
                        ))}
                      </div>

                      {/* Add controls */}
                      {cart.find((i) => i.menu_item.id === dish.id) ? (
                        <div className="flex items-center gap-2 bg-neutral-900/60 border border-neutral-800/80 rounded-lg p-0.5">
                          <button
                            onClick={() => updateQuantity(dish.id, -1)}
                            className="w-5 h-5 rounded bg-neutral-950 flex items-center justify-center hover:bg-neutral-800 active:scale-90"
                          >
                            <Minus className="w-2.5 h-2.5 text-neutral-400" />
                          </button>
                          <span className="text-[11px] font-mono font-bold px-1 text-neutral-200">
                            {cart.find((i) => i.menu_item.id === dish.id)?.quantity}
                          </span>
                          <button
                            onClick={() => addToCart(dish)}
                            className="w-5 h-5 rounded bg-neutral-950 flex items-center justify-center hover:bg-neutral-800 active:scale-90"
                          >
                            <Plus className="w-2.5 h-2.5 text-neutral-400" />
                          </button>
                        </div>
                      ) : (
                        <Button
                          size="sm"
                          onClick={() => addToCart(dish)}
                          className="h-7 bg-neutral-900 hover:bg-[#bc470a] border border-neutral-800 text-neutral-300 hover:text-white rounded-lg text-[10px] font-bold px-3 active:scale-95 transition-all"
                        >
                          Add
                        </Button>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Floating Cart Trigger */}
      {totalQuantity > 0 && !isCartOpen && !isChatOpen && (
        <div className="absolute bottom-6 left-4 right-4 bg-[#bc470a] hover:bg-[#a13b08] border border-orange-500/20 text-white rounded-2xl shadow-xl shadow-orange-950/40 p-4.5 z-20 flex justify-between items-center transition-all duration-300 animate-slide-in-bottom">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-black/20 rounded-xl">
              <ShoppingBag className="w-5 h-5 text-white" />
            </div>
            <div>
              <p className="text-xs text-orange-200 font-semibold">{totalQuantity} items added</p>
              <p className="text-sm font-bold font-mono">₹{grandTotal} <span className="text-[10px] text-orange-200 font-normal">(Incl. 5% GST)</span></p>
            </div>
          </div>
          <Button 
            onClick={() => setIsCartOpen(true)}
            className="bg-white hover:bg-orange-50 text-[#bc470a] font-bold px-4 py-2 h-9 rounded-xl shadow-sm text-xs"
          >
            Review Cart
          </Button>
        </div>
      )}

      {/* Floating Sparkles AI Zara Trigger with glowing unread dot */}
      {!isChatOpen && (
        <button
          aria-label="Ask Zara AI"
          onClick={handleOpenChat}
          className="absolute bottom-6 right-6 w-12 h-12 rounded-full bg-gradient-to-tr from-[#bc470a] to-[#a13b08] flex items-center justify-center text-white shadow-xl shadow-orange-950/20 hover:scale-105 active:scale-95 transition-all z-20 border border-orange-500/20"
        >
          <Sparkles className="w-5 h-5 text-white animate-pulse" />
          {hasUnreadSuggestions && (
            <span className="absolute top-0 right-0 w-3.5 h-3.5 rounded-full bg-red-500 border-2 border-neutral-900 animate-ping"></span>
          )}
        </button>
      )}

      {/* Slide-Over Cart Review Panel */}
      <CartDrawer
        isOpen={isCartOpen}
        onClose={() => setIsCartOpen(false)}
        items={cart}
        onUpdateQuantity={(itemId, delta) => updateQuantity(itemId, delta)}
        onSaveInstructions={(itemId, text) => saveInstructions(itemId, text)}
        onPlaceOrder={() => { setIsCartOpen(false); setIsCheckoutOpen(true); }}
      />

      {/* Reusable Checkout Modal Flow Component */}
      <CheckoutModal
        isOpen={isCheckoutOpen}
        onClose={() => setIsCheckoutOpen(false)}
        grandTotal={grandTotal}
        onSuccess={handleOrderSuccess}
        sessionId={sessionId}
        isBackendMode={isBackendMode}
      />

      {/* Overhalled AI Chat Zara Drawer Component with unread and cards support! */}
      <ChatDrawer
        isOpen={isChatOpen}
        onClose={() => setIsChatOpen(false)}
        messages={messages}
        onSendMessage={handleSendMessage}
        onAddToCartById={handleAddToCartById}
        isTyping={isTyping}
      />
    </div>
  );
}
