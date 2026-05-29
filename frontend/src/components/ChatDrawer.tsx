"use client";

import React, { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { 
  X, 
  Send, 
  Sparkles, 
  User, 
  ArrowRight,
  TrendingUp,
  Flame,
  Leaf,
  Plus,
  Compass
} from "lucide-react";
import { ChatMessage, MenuItem } from "@/types";
// Let's create a local mapping inside the component or export it, but since we have SEED_MENU in page.tsx, we can pass a function `onAddById(itemId: string)` or a mapping dictionary to Cart!
// That's extremely elegant: the parent page passes `onAddToCartById(itemId: string)`!


interface ChatDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  messages: ChatMessage[];
  onSendMessage: (text: string) => void;
  onAddToCartById: (itemId: string) => void;
  isTyping: boolean;
}

// Quick suggestion chips mapper
const SUGGESTION_CHIPS = [
  { label: "Spicy 🌶️", prompt: "Suggest some spicy items!" },
  { label: "Light 🥗", prompt: "Show me light and healthy options." },
  { label: "Filling 🍲", prompt: "What are some heavy and filling mains?" },
  { label: "Dessert 🍰", prompt: "Show me sweet desserts." },
  { label: "Drinks 🍹", prompt: "Suggest cold and hot beverages." },
  { label: "Best Sellers 🌟", prompt: "What are your bestselling dishes?" }
];

// Helper database of seed dishes to resolve matching recommendation cards
const DISH_LOOKUP: Record<string, { name: string; price: number; desc: string; tags: string[] }> = {
  "m1": { name: "Paneer Tikka Multani", price: 320.0, desc: "Tandoori paneer marinated in yellow chili hung curd", tags: ["veg", "chef_special"] },
  "m2": { name: "Crispy Lotus Stem Honey Chili", price: 280.0, desc: "Crisp lotus stems tossed in sweet honey chili", tags: ["veg", "light"] },
  "m3": { name: "Dahi Ke Sholay", price: 260.0, desc: "Crispy rolls stuffed with spiced hung curd", tags: ["veg", "bestseller"] },
  "m4": { name: "Bhatti Ka Murgh Tikka", price: 380.0, desc: "Boneless chicken marinated in black pepper yogurt", tags: ["non-veg", "spicy"] },
  "m5": { name: "Tandoori Fish Amritsari", price: 450.0, desc: "Fish marinated in carom seeds, pan-fried", tags: ["non-veg", "light"] },
  "m6": { name: "Mutton Seekh Kebab", price: 420.0, desc: "Minced lamb seasoned with aromatic tandoor spices", tags: ["non-veg", "spicy", "bestseller"] },
  "m7": { name: "Dal Makhani Gourmet", price: 340.0, desc: "Black lentils slow-cooked overnight with heavy butter", tags: ["veg", "bestseller"] },
  "m8": { name: "Paneer Butter Masala", price: 360.0, desc: "Cottage cheese cubes in cream cashew nut gravy", tags: ["veg"] },
  "m9": { name: "Subz Miloni Diwani", price: 310.0, desc: "Assorted vegetables in smooth spinach gravy", tags: ["veg", "light"] },
  "m10": { name: "Signature Butter Chicken", price: 440.0, desc: "Tandoori chicken shreds in frothed rich tomato butter gravy", tags: ["non-veg", "bestseller", "chef_special"] },
  "m11": { name: "Kashmiri Mutton Rogan Josh", price: 520.0, desc: "Mutton chunks slow-cooked in kashmiri chilies and saffron", tags: ["non-veg", "spicy", "chef_special"] },
  "m12": { name: "Chicken Tikka Masala", price: 420.0, desc: "Char-grilled chicken cubes tossed in thick bell pepper gravy", tags: ["non-veg", "spicy"] },
  "m13": { name: "Butter Garlic Naan", price: 80.0, desc: "Flatbread topped with garlic and butter", tags: ["veg"] },
  "m14": { name: "Gourmet Chicken Dum Biryani", price: 410.0, desc: "Aromatic basmati rice layered with juicy chicken", tags: ["non-veg", "bestseller", "chef_special"] },
  "m17": { name: "Gulab Jamun with Rabri Trio", price: 180.0, desc: "Milk dumplings in rose syrup over kesar rabri", tags: ["veg", "bestseller"] },
  "m18": { name: "Elaneer Payasam", price: 190.0, desc: "Chilled dessert with coconut milk and tender pulp", tags: ["veg", "light"] },
  "m19": { name: "Kesari Masala Chai", price: 90.0, desc: "Brewed tea leaves with cardamom and saffron milk", tags: ["veg"] },
  "m21": { name: "Royal Mango Lassi", price: 160.0, desc: "Creamy frothed curd blended with mango and saffron", tags: ["veg", "bestseller"] },
  "m22": { name: "Mint Masala Shikanji", price: 120.0, desc: "Mint lemonade with black salt soda base", tags: ["veg", "light"] },
  "m23": { name: "Smoked Rosemary Berry Cooler", price: 180.0, desc: "Muddled blackberries and lemon frothed tableside", tags: ["veg", "light", "chef_special"] },
  "m24": { name: "Executive Veg Thali", price: 490.0, desc: "Thali featuring paneer masala, dal makhani, roti, and sweets", tags: ["veg", "bestseller"] },
  "m25": { name: "Royal Non-Veg Kebab Platter", price: 790.0, desc: "Platter with murgh tikka, mutton kebabs, amritsari fish", tags: ["non-veg", "spicy", "chef_special"] }
};

export default function ChatDrawer({
  isOpen,
  onClose,
  messages,
  onSendMessage,
  onAddToCartById,
  isTyping
}: ChatDrawerProps) {
  const [inputText, setInputText] = useState<string>("");
  const chatEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll chat log when new messages are added
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  const handleSend = () => {
    if (!inputText.trim()) return;
    onSendMessage(inputText);
    setInputText("");
  };

  const handleChipClick = (prompt: string) => {
    onSendMessage(prompt);
  };

  // Helper to parse potential recommendation IDs inside assistant replies
  const resolveSuggestions = (content: string) => {
    // Dynamically search content for our seeded dish IDs to render frothed cards!
    const suggestions: Array<{ id: string; name: string; price: number; desc: string; tags: string[] }> = [];
    const lower = content.toLowerCase();
    
    Object.keys(DISH_LOOKUP).forEach(key => {
      const nameLower = DISH_LOOKUP[key].name.toLowerCase();
      // If the reply explicitly mentions the dish name, render a beautiful card inside the chat log!
      if (lower.includes(nameLower) || lower.includes(key)) {
        suggestions.push({ id: key, ...DISH_LOOKUP[key] });
      }
    });
    return suggestions;
  };

  if (!isOpen) return null;

  return (
    <div className="absolute inset-0 bg-black/75 backdrop-blur-xs z-40 flex flex-col justify-end animate-fade-in font-sans">
      
      {/* Overlay click to close */}
      <div className="absolute inset-0 -z-10" onClick={onClose}></div>

      {/* Slide-over panel */}
      <div className="w-full h-[75vh] bg-neutral-900 border-t border-neutral-850 rounded-t-3xl shadow-2xl flex flex-col relative z-50 animate-slide-in-bottom">
        
        {/* Notch notch */}
        <div className="mx-auto w-12 h-1 bg-neutral-800 rounded-full my-2.5 shrink-0"></div>

        {/* Zara Header */}
        <div className="px-5 pb-4 border-b border-neutral-850/60 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-orange-600 to-amber-500 flex items-center justify-center text-white border border-orange-500/20 shadow-md">
              <Sparkles className="w-4 h-4 text-white animate-pulse" />
            </div>
            <div>
              <h3 className="text-xs font-bold text-neutral-100 font-display">Zara — AI Dining Guide</h3>
              <div className="flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                <span className="text-[9px] text-neutral-400">Zara is active at Table</span>
              </div>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 hover:bg-neutral-800 rounded-full text-neutral-400 hover:text-neutral-200 transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Chat History View */}
        <div className="flex-1 p-5 overflow-y-auto no-scrollbar space-y-4 bg-neutral-900/40">
          {messages.map((msg) => {
            const isUser = msg.sender === "user";
            const cards = !isUser ? resolveSuggestions(msg.content) : [];
            
            return (
              <div
                key={msg.id}
                className={`flex gap-3 max-w-[90%] ${isUser ? "ml-auto flex-row-reverse" : "mr-auto"}`}
              >
                {/* Avatar */}
                <div
                  className={`w-7 h-7 rounded-full shrink-0 flex items-center justify-center text-[10px] font-bold ${
                    isUser ? "bg-neutral-800 text-neutral-400 border border-neutral-700" : "bg-orange-600 text-white shadow shadow-orange-600/10"
                  }`}
                >
                  {isUser ? <User className="w-3.5 h-3.5" /> : <Sparkles className="w-3.5 h-3.5" />}
                </div>

                {/* Bubble Container */}
                <div className="space-y-3">
                  {/* Chat bubble text */}
                  <div
                    className={`p-3 rounded-2xl text-[11px] leading-relaxed shadow-sm ${
                      isUser
                        ? "bg-orange-600 text-white rounded-tr-none"
                        : "bg-neutral-950/90 border border-neutral-850 text-neutral-200 rounded-tl-none glass-panel"
                    }`}
                  >
                    <p>{msg.content}</p>
                    <span className="block text-[8px] text-neutral-500 mt-1.5 text-right font-mono font-medium">
                      {msg.timestamp}
                    </span>
                  </div>

                  {/* Horizontal Scroll Recommendation Cards Inside Chat Bubble */}
                  {!isUser && cards.length > 0 && (
                    <div className="flex gap-3 overflow-x-auto no-scrollbar py-1 max-w-[280px]">
                      {cards.map((card) => (
                        <div
                          key={card.id}
                          className="w-56 shrink-0 rounded-2xl bg-neutral-950 border border-neutral-850 p-3 flex flex-col justify-between gap-2.5 shadow-md"
                        >
                          <div className="space-y-1">
                            <div className="flex items-start justify-between gap-1">
                              <h5 className="text-[10px] font-bold text-neutral-100 font-display line-clamp-1 pr-2">
                                {card.name}
                              </h5>
                              <span className="text-[10px] font-bold font-mono text-orange-400 shrink-0">
                                ₹{card.price}
                              </span>
                            </div>
                            <p className="text-[9px] text-neutral-400 leading-normal line-clamp-2">
                              {card.desc}
                            </p>
                          </div>

                          <div className="flex justify-between items-center pt-1.5 border-t border-neutral-900">
                            <div className="flex gap-0.5">
                              {card.tags.includes("veg") && <Leaf className="w-3 h-3 text-emerald-500" />}
                              {card.tags.includes("spicy") && <Flame className="w-3 h-3 text-red-500" />}
                            </div>
                            
                            <Button
                              size="sm"
                              onClick={() => {
                                onAddToCartById(card.id);
                                alert(`Succesfully added ${card.name} to your cart via Zara!`);
                              }}
                              className="bg-orange-600 hover:bg-orange-500 text-white font-bold h-6 rounded-md text-[9px] px-2.5 active:scale-95 transition-all flex items-center gap-1 shadow shadow-orange-600/10"
                            >
                              <Plus className="w-2.5 h-2.5" /> Quick Add
                            </Button>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            );
          })}
          
          {isTyping && (
            <div className="flex gap-3 max-w-[85%] mr-auto items-center animate-pulse">
              <div className="w-7 h-7 rounded-full bg-orange-600/20 text-orange-400 flex items-center justify-center">
                <Sparkles className="w-3.5 h-3.5 animate-spin" />
              </div>
              <div className="p-3 bg-neutral-950/60 border border-neutral-850 text-neutral-500 rounded-2xl rounded-tl-none text-[10px] font-mono italic">
                Zara is curating recommendations...
              </div>
            </div>
          )}
          <div ref={chatEndRef}></div>
        </div>

        {/* Suggestion Chips */}
        <div className="px-5 py-2.5 border-t border-neutral-850/60 bg-neutral-950/50 flex gap-2 overflow-x-auto no-scrollbar shrink-0">
          <span className="text-[9px] text-neutral-500 font-bold uppercase tracking-wider flex items-center gap-1 shrink-0">
            <Compass className="w-3 h-3 text-neutral-600" /> Suggest:
          </span>
          {SUGGESTION_CHIPS.map((chip) => (
            <button
              key={chip.label}
              onClick={() => handleChipClick(chip.prompt)}
              className="px-3 py-1 rounded-full bg-neutral-900 border border-neutral-800 text-[9px] font-semibold text-neutral-400 hover:text-neutral-200 transition-colors whitespace-nowrap hover:border-neutral-700"
            >
              {chip.label}
            </button>
          ))}
        </div>

        {/* Chat Text Input footer */}
        <div className="p-4 bg-neutral-950 border-t border-neutral-850/60 flex gap-2 shrink-0">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder="Ask Zara for wine pairings, allergy updates, or calls..."
            className="flex-1 bg-neutral-900 border border-neutral-850 text-xs rounded-xl px-4 py-2.5 focus:outline-none focus:border-orange-500 text-neutral-200 placeholder-neutral-600 font-medium"
          />
          <button
            onClick={handleSend}
            disabled={!inputText.trim() || isTyping}
            className="p-2.5 rounded-xl bg-orange-600 hover:bg-orange-500 text-white shadow-md active:scale-95 disabled:opacity-50 transition-transform"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
