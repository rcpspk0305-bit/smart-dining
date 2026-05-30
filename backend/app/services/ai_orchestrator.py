import re
import json
import httpx
from datetime import datetime, timezone
from typing import List, Dict, Any, Tuple, Optional
from app.core.config import settings
from app.schemas.chat import ChatResponse, ChatSuggestion
from app.schemas.menu import MenuItem
from app.services.menu import MenuService
from app.services.cart import CartService

# In-memory chat memory database mapping session_id -> list of normalized context dicts
SESSION_AI_MEMORY: Dict[str, List[Dict[str, Any]]] = {}

# Warm frothed conversational translations by language dialect
RESPONSES_BY_LANG = {
    "hinglish": {
        "welcome": "Namaste! Main aapka AI dining guide Zara hoon. Aaj Table par kya khaana pasand karenge?",
        "waiter": "Bilkul, maine table ke liye service staff ko page kar diya hai. Woh jaldi hi aayenge.",
        "status": "Aapka order kitchen mein prep ho raha hai, bas thodi hi der mein table par serve hoga!",
        "recommend": "Paneer lovers ke liye humara Paneer Tikka Multani best hai! Aur agar chicken pasand hai toh Butter Chicken try kijiye."
    },
    "telugu_english": {
        "welcome": "Namaskaram! Nenu mee AI dining guide Zara. Emi tinalani undi meeku ee roju?",
        "waiter": "Sure andi, nenu waiter alert chesanu. Valu thwaralone mee table daggara untaru.",
        "status": "Mee order kitchen lo ready avthundi, inka konni nimishala lo serve avthundi!",
        "recommend": "Gourmet Dum Biryani chala popular andi, thappakunda try cheyyandi. Cold drinks lo Royal Mango Lassi baguntundi."
    },
    "english": {
        "welcome": "Hello! I am Zara, your tableside AI guide. What are you in the mood for today?",
        "waiter": "Certainly, I have paged our service staff to assist your table immediately.",
        "status": "Your kitchen order ticket is currently in preparation and will be served shortly!",
        "recommend": "I highly recommend our signature Bhatti Ka Murgh Tikka or the rich Dal Makhani Gourmet."
    }
}


class AIOrchestrator:
    """
    Lightweight AI Orchestration Layer for Gourmet AI.
    Runs multilingual parsing, intent routing, and contextual upselling.
    Designed with a clean override boundary to plug in OpenAI later.
    """

    @staticmethod
    def sanitize_input(text: str) -> str:
        """
        Production safeguard: Strips HTML tags, XSS scripts, and limits characters to protect AI layers.
        """
        # Limit size
        text = text[:500]
        # Remove HTML tags
        text = re.sub(r'<[^>]*>', '', text)
        # Remove suspicious scripts / XSS injection patterns
        text = re.sub(r'(javascript:|onload=|onerror=|script|<script|alert\()', '', text, flags=re.IGNORECASE)
        # Filter non-printable control characters
        text = "".join(ch for ch in text if ch.isprintable() or ch in ['\n', '\r', '\t'])
        return text.strip()

    @staticmethod
    def strip_pii(text: str) -> str:
        """
        Production safeguard: Redacts email addresses and telephone numbers to maintain customer privacy.
        """
        # Redact email addresses
        text = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '[EMAIL_REDACTED]', text)
        # Redact telephone numbers (looks for 8 to 12 digits, spaces, hyphens, and optional +)
        text = re.sub(r'\+?\b\d[\d\s-]{8,12}\d\b', '[PHONE_REDACTED]', text)
        return text

    @staticmethod
    def _openai_fallback(query: str, session_id: str) -> Optional[ChatResponse]:
        """
        Unified LLM Core Engine supporting:
        1. Google Gemini API (Free Tier)
        2. OpenAI API
        3. Local Ollama (Free Offline Model)
        
        Returns ChatResponse if any LLM call succeeds, otherwise returns None to fall back to warm frothed local rules engine.
        """
        # Determine if we have a real key configured
        gemini_key = settings.GEMINI_API_KEY
        openai_key = settings.OPENAI_API_KEY
        ollama_host = settings.OLLAMA_HOST
        
        is_gemini_active = gemini_key and gemini_key != "your-gemini-api-key-here"
        is_openai_active = openai_key and openai_key != "your-openai-api-key-here"

        # Build context
        menu_items = MenuService.get_menu()
        cart_items = CartService.get_cart_items(session_id)
        
        menu_ctx = []
        for item in menu_items:
            if item.available:
                menu_ctx.append({
                    "id": item.id,
                    "name": item.name,
                    "category": item.category,
                    "price": item.price,
                    "description": item.description,
                    "tags": item.tags,
                    "allergens": item.allergens
                })
                
        cart_ctx = []
        for item in cart_items:
            cart_ctx.append({
                "id": item.menu_item.id,
                "name": item.menu_item.name,
                "quantity": item.quantity,
                "price": item.menu_item.price,
                "special_instructions": item.special_instructions
            })

        system_prompt = (
            "You are Zara, the warm, tableside AI Dining Guide at Gourmet AI.\n"
            "You assist guests directly at their table to review our menu, customize orders for allergies, recommend drinks/desserts, and handle service queries.\n"
            f"Here is our available menu database:\n{json.dumps(menu_ctx, indent=2)}\n\n"
            f"Here are the items currently in the guest's collaborative table cart:\n{json.dumps(cart_ctx, indent=2)}\n\n"
            "INSTRUCTIONS:\n"
            "1. Be extremely polite and hospitable. Mirror the guest's dialect. If they query in Hinglish (Hindi mixed with English), reply in warm Hinglish. If in Telugu-English, reply in Telugu-English. Otherwise, reply in English.\n"
            "2. Recommend specific items from our menu database. Never recommend items that are already in their cart.\n"
            "3. If they ask to call a waiter/staff, request napkin, water, or help, politely acknowledge that you are paging staff.\n"
            "4. If they ask for order status or if their food is ready, assure them that their kitchen ticket is in preparation.\n"
            "5. You MUST respond with a valid JSON object matching this structure EXACTLY:\n"
            "{\n"
            "  \"message\": \"Conversational reply to the guest...\",\n"
            "  \"suggestions\": [\n"
            "    {\n"
            "      \"itemId\": \"item ID from menu context (e.g., m10)\",\n"
            "      \"name\": \"exact item name\",\n"
            "      \"price\": numerical price,\n"
            "      \"reason\": \"Highly compelling 1-sentence pairing/upsell reason\"\n"
            "    }\n"
            "  ]\n"
            "}\n"
            "Do not output markdown format or backticks. Respond only with raw JSON."
        )

        user_prompt = f"Guest query: '{query}'"

        # Try Google Gemini first (Recommended free model tier)
        if is_gemini_active:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
                payload = {
                    "contents": [{
                        "parts": [{"text": f"{system_prompt}\n\n{user_prompt}"}]
                    }],
                    "generationConfig": {
                        "responseMimeType": "application/json"
                    }
                }
                with httpx.Client(timeout=3.0) as client:
                    resp = client.post(url, json=payload)
                    if resp.status_code == 200:
                        data = resp.json()
                        text_response = data["candidates"][0]["content"]["parts"][0]["text"]
                        parsed = json.loads(text_response.strip())
                        return ChatResponse(
                            message=parsed.get("message", ""),
                            suggestions=[
                                ChatSuggestion(
                                    itemId=s.get("itemId", ""),
                                    name=s.get("name", ""),
                                    price=float(s.get("price", 0.0)),
                                    reason=s.get("reason", "")
                                )
                                for s in parsed.get("suggestions", [])
                                if s.get("itemId")
                            ],
                            timestamp=datetime.now()
                        )
            except Exception as e:
                print(f"Gemini API fallback failed, trying next provider: {e}")

        # Try local Ollama (Free local host) next
        if ollama_host:
            try:
                url = f"{ollama_host}/v1/chat/completions"
                payload = {
                    "model": "gemma" if "gemma" in query.lower() else "llama3",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "response_format": {"type": "json_object"},
                    "temperature": 0.7
                }
                with httpx.Client(timeout=3.0) as client:
                    resp = client.post(url, json=payload)
                    if resp.status_code == 200:
                        data = resp.json()
                        text_response = data["choices"][0]["message"]["content"]
                        parsed = json.loads(text_response.strip())
                        return ChatResponse(
                            message=parsed.get("message", ""),
                            suggestions=[
                                ChatSuggestion(
                                    itemId=s.get("itemId", ""),
                                    name=s.get("name", ""),
                                    price=float(s.get("price", 0.0)),
                                    reason=s.get("reason", "")
                                )
                                for s in parsed.get("suggestions", [])
                                if s.get("itemId")
                            ],
                            timestamp=datetime.now()
                        )
            except Exception as e:
                pass

        # Try OpenAI (Fallback) next
        if is_openai_active:
            try:
                url = "https://api.openai.com/v1/chat/completions"
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {openai_key}"
                }
                payload = {
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "response_format": {"type": "json_object"},
                    "temperature": 0.7
                }
                with httpx.Client(timeout=3.0) as client:
                    resp = client.post(url, headers=headers, json=payload)
                    if resp.status_code == 200:
                        data = resp.json()
                        text_response = data["choices"][0]["message"]["content"]
                        parsed = json.loads(text_response.strip())
                        return ChatResponse(
                            message=parsed.get("message", ""),
                            suggestions=[
                                ChatSuggestion(
                                    itemId=s.get("itemId", ""),
                                    name=s.get("name", ""),
                                    price=float(s.get("price", 0.0)),
                                    reason=s.get("reason", "")
                                )
                                for s in parsed.get("suggestions", [])
                                if s.get("itemId")
                            ],
                            timestamp=datetime.now()
                        )
            except Exception as e:
                print(f"OpenAI API fallback failed: {e}")

        # Try DuckDuckGo Chat (Completely Free, No Key Required, No Setup Required)
        try:
            # 1. Fetch the x-vqd-4 token
            status_url = "https://duckduckgo.com/duckchat/v1/status"
            status_headers = {
                "x-vqd-accept": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            
            with httpx.Client(timeout=3.0) as client:
                status_resp = client.get(status_url, headers=status_headers)
                if status_resp.status_code == 200:
                    vqd_token = status_resp.headers.get("x-vqd-4")
                    if vqd_token:
                        # 2. Post chat request
                        chat_url = "https://duckduckgo.com/duckchat/v1/chat"
                        chat_headers = {
                            "x-vqd-4": vqd_token,
                            "Content-Type": "application/json",
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                            "Accept": "text/event-stream"
                        }
                        payload = {
                            "model": "gpt-4o-mini",
                            "messages": [
                                {
                                    "role": "user",
                                    "content": f"{system_prompt}\n\n{user_prompt}"
                                }
                            ]
                        }
                        
                        full_response = ""
                        with client.stream("POST", chat_url, headers=chat_headers, json=payload) as r:
                            if r.status_code == 200:
                                for line in r.iter_lines():
                                    if line.startswith("data: "):
                                        content = line[6:].strip()
                                        if content == "[DONE]":
                                            break
                                        try:
                                            chunk = json.loads(content)
                                            if "message" in chunk and chunk["message"] is not None:
                                                full_response += chunk["message"]
                                        except:
                                            pass
                        
                        if full_response:
                            cleaned = full_response.strip()
                            if cleaned.startswith("```json"):
                                cleaned = cleaned[7:]
                            elif cleaned.startswith("```"):
                                cleaned = cleaned[3:]
                            if cleaned.endswith("```"):
                                cleaned = cleaned[:-3]
                            
                            parsed = json.loads(cleaned.strip())
                            return ChatResponse(
                                message=parsed.get("message", ""),
                                suggestions=[
                                    ChatSuggestion(
                                        itemId=s.get("itemId", ""),
                                        name=s.get("name", ""),
                                        price=float(s.get("price", 0.0)),
                                        reason=s.get("reason", "")
                                    )
                                    for s in parsed.get("suggestions", [])
                                    if s.get("itemId")
                                ],
                                timestamp=datetime.now()
                            )
        except Exception as e:
            print(f"DuckDuckGo Chat API fallback failed: {e}")

        return None

    @staticmethod
    def normalize_query(query: str) -> Dict[str, Any]:
        """
        1. Multilingual Normalizer
        Normalizes typo-heavy, Hinglish, Telugu-English or English strings
        to structured JSON containing: intent, preferences, language_detected, raw_text.
        """
        raw = query.strip()
        query_lower = raw.lower()

        # Language Detection
        lang = "english"
        if any(w in query_lower for w in ["karo", "batao", "kya", "khaana", "chahiye", "hai", "mujhe", "kijiye", "bas", "aur"]):
            lang = "hinglish"
        elif any(w in query_lower for w in ["enti", "cheppu", "kavalai", "tinali", "bhojanam", "emundi", "andi"]):
            lang = "telugu_english"

        # Typo correction & feature extraction
        preferences = []
        
        # Vegetarian checks
        if any(w in query_lower for w in ["veg", "vegitarian", "shakahari", "no meat", "no nonveg"]):
            preferences.append("veg")
            
        # Non-Vegetarian checks
        if any(w in query_lower for w in ["nonveg", "chicken", "meat", "mutton", "chkn", "fish"]):
            preferences.append("non-veg")

        # Spicy checks
        if any(w in query_lower for w in ["spcy", "spicy", "hot", "teekha", "karam"]):
            preferences.append("spicy")

        # Sweet/Desserts checks
        if any(w in query_lower for w in ["sweet", "dessert", "mithai", "gulab", "payasam", "ice cream"]):
            preferences.append("sweet")

        # Intent Routing
        intent = "recommendation"
        if any(w in query_lower for w in ["water", "waiter", "napkin", "help", "staff", "bill", "service"]):
            intent = "waiter_call"
        elif any(w in query_lower for w in ["status", "ready", "cooked", "order", "wait time", "ticket"]):
            intent = "order_status"
        elif any(w in query_lower for w in ["that's all", "thats all", "nothing else", "bas aur nahi", "bas", "done"]):
            intent = "conclude_session"

        return {
            "intent": intent,
            "preferences": preferences,
            "language_detected": lang,
            "raw_text": raw
        }

    @staticmethod
    def get_upsell_suggestions(
        session_id: str, 
        user_query: str,
        language: str
    ) -> Tuple[List[ChatSuggestion], Optional[str]]:
        """
        4. Context-Aware Upsell Agent
        Triggers friendly, non-pushy upsells based on:
        - Cart total crosses 500 INR
        - Cart has mains but no beverage
        - User says "that's all" / Conclude intent
        - Evening time special suggest dessert
        - Last added item complementary links
        Never suggests items already in the cart.
        """
        cart_items = CartService.get_cart_items(session_id)
        cart_ids = [item.menu_item.id for item in cart_items]
        
        # Calculate pricing
        subtotal = sum(item.menu_item.price * item.quantity for item in cart_items)
        
        # Categories mapping
        has_mains = any("Mains" in item.menu_item.category for item in cart_items)
        has_beverages = any("Beverages" in item.menu_item.category for item in cart_items)
        
        # Evening check: local hour is after 5 PM (17:00)
        local_hour = datetime.now().hour
        is_evening = local_hour >= 17 or local_hour < 4  # Treat late night as evening too
        
        suggestions: List[ChatSuggestion] = []
        upsell_text = None

        # Helper to safely select an upsell item not in the cart
        def get_valid_upsell(item_ids: List[str]) -> Optional[MenuItem]:
            for item_id in item_ids:
                if item_id not in cart_ids:
                    item = MenuService.get_item(item_id)
                    if item and item.available:
                        return item
            return None

        # Scenario 1: User says "that's all" or conclude session -> Suggest sweet dessert
        if "bas" in user_query.lower() or "all" in user_query.lower() or "done" in user_query.lower():
            dessert = get_valid_upsell(["m17", "m18"])  # Gulab Jamun or Payasam
            if dessert:
                if language == "hinglish":
                    upsell_text = "Thik hai! Khana khatam karne se pehle kuch meetha ho jaye? Humare Gulab Jamun with Rabri ko try kijiye."
                elif language == "telugu_english":
                    upsell_text = "Sure andi! Bhojanam complete chese mundu konchem sweet thinte baguntundi. Ma special payasam try chesthara?"
                else:
                    upsell_text = "Wonderful! How about concluding your meal on a sweet note with our special Gulab Jamun with Rabri?"
                suggestions.append(
                    ChatSuggestion(
                        itemId=dessert.id,
                        name=dessert.name,
                        price=dessert.price,
                        reason=f"Perfect sweet conclusion to your table meal."
                    )
                )
                return suggestions, upsell_text

        # Scenario 2: Evening time special (Hot Chai or Payasam)
        if is_evening and not suggestions:
            chai = get_valid_upsell(["m19", "m18"])  # Kesari Chai or Payasam
            if chai:
                if language == "hinglish":
                    upsell_text = "Shaam ka waqt hai! Kya aap humari Kesari Masala Chai ya Elaneer Payasam enjoy karna chahenge?"
                elif language == "telugu_english":
                    upsell_text = "Challati saayantram andi! Ma hot Kesari Masala Chai thagithe chala refreshing ga untundi."
                else:
                    upsell_text = "It's a beautiful evening! Would you care to try our fresh hot Kesari Masala Chai or chilled Payasam?"
                suggestions.append(
                    ChatSuggestion(
                        itemId=chai.id,
                        name=chai.name,
                        price=chai.price,
                        reason="Bestselling evening comfort refreshment."
                    )
                )
                return suggestions, upsell_text

        # Scenario 3: Cart has mains but no beverages -> Recommend drink
        if has_mains and not has_beverages and not suggestions:
            drink = get_valid_upsell(["m21", "m22", "m23"])  # Mango Lassi, Shikanji, Rosemary Cooler
            if drink:
                if language == "hinglish":
                    upsell_text = "Maine dekha aapne mains add kiye hain par koi drink nahi. Humari Royal Mango Lassi ya Shikanji try karenge?"
                elif language == "telugu_english":
                    upsell_text = "Mee cart lo tasty mains unnay kani drinks levu andi. Ma Royal Mango Lassi thagithe chala fresh ga untundi."
                else:
                    upsell_text = "I noticed you have delicious mains in your cart but no drinks. How about adding a frothed Royal Mango Lassi or Mint Shikanji?"
                suggestions.append(
                    ChatSuggestion(
                        itemId=drink.id,
                        name=drink.name,
                        price=drink.price,
                        reason="Refreshing frothed beverage to pair with your curries."
                    )
                )
                return suggestions, upsell_text

        # Scenario 4: Cart subtotal crosses 500 INR -> Suggest a signature side/dessert
        if subtotal > 500.0 and not suggestions:
            special = get_valid_upsell(["m23", "m17"])  # Rosemary Cooler or Gulab Jamun
            if special:
                if language == "hinglish":
                    upsell_text = "Aapka order ₹500 cross kar gaya hai! Humare signature Smoked Rosemary Cooler se isse aur grand banayein?"
                elif language == "telugu_english":
                    upsell_text = "Mee order ₹500 cross ayyindi andi. Ma special Smoked Rosemary Cooler try chesi feast ni grand cheyyandi!"
                else:
                    upsell_text = "Since your order is over ₹500, make it a true feast by adding our tableside Smoked Rosemary Cooler!"
                suggestions.append(
                    ChatSuggestion(
                        itemId=special.id,
                        name=special.name,
                        price=special.price,
                        reason="Chef-special beverage to upgrade your dining feast."
                    )
                )
                return suggestions, upsell_text

        # Scenario 5: Fallback last added item complementary link
        if cart_items and not suggestions:
            last_item = cart_items[-1].menu_item
            if last_item.complementary_items:
                comp = get_valid_upsell(last_item.complementary_items)
                if comp:
                    if language == "hinglish":
                        upsell_text = f"Aapne {last_item.name} add kiya hai, iske sath {comp.name} ka pairing bilkul perfect rahega!"
                    elif language == "telugu_english":
                        upsell_text = f"Mee cart lo {last_item.name} undi andi. Deenitho paatu {comp.name} order chesthe inka keka!"
                    else:
                        upsell_text = f"To pair with your {last_item.name}, we highly recommend adding a frothed {comp.name}."
                    suggestions.append(
                        ChatSuggestion(
                            itemId=comp.id,
                            name=comp.name,
                            price=comp.price,
                            reason=f"Perfect flavor match for your {last_item.name}."
                        )
                    )
                    return suggestions, upsell_text

        return suggestions, upsell_text

    @staticmethod
    def get_recommendations(
        session_id: str, 
        preferences: List[str], 
        language: str
    ) -> Tuple[List[ChatSuggestion], str]:
        """
        3. Recommendation Agent
        Filters menu items matching preferences.
        Never recommends already ordered items.
        """
        menu = MenuService.get_menu()
        cart_items = CartService.get_cart_items(session_id)
        cart_ids = [item.menu_item.id for item in cart_items]

        # Filter active, non-cart items
        candidates = [item for item in menu if item.available and item.id not in cart_ids]

        # Score candidates
        scored: List[Tuple[MenuItem, float]] = []
        for item in candidates:
            score = item.popular_score
            for pref in preferences:
                if pref == "veg" and "veg" in item.tags:
                    score += 2.0
                if pref == "veg" and "non-veg" in item.tags:
                    score -= 5.0
                if pref == "non-veg" and "non-veg" in item.tags:
                    score += 2.0
                if pref == "non-veg" and "veg" in item.tags:
                    score -= 2.0
                if pref == "spicy" and "spicy" in item.tags:
                    score += 2.0
                if pref == "sweet" and "sweet" in item.tags:
                    score += 2.0
            scored.append((item, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        top_items = [x[0] for x in scored[:3]]

        suggestions = []
        for item in top_items:
            reason = "Highly rated chef special recommended by dining guests."
            if language == "hinglish":
                reason = "Humare kitchen ki best preparation hai jo guests ko bohot pasand hai!"
                if "spicy" in item.tags:
                    reason += " Yeh teekhi aur flavorful hai."
            elif language == "telugu_english":
                reason = "Mee kosam special recommendation, andharu order chese highly frothed dish idi."
                if "spicy" in item.tags:
                    reason += " Idhi spicy ga super ga untundi."

            suggestions.append(
                ChatSuggestion(
                    itemId=item.id,
                    name=item.name,
                    price=item.price,
                    reason=reason
                )
            )

        if language == "hinglish":
            message = "Aapke taste ke hisab se maine kuch top tandoori and curry items select kiye hain!"
            if not suggestions:
                message = "Aapne already humare bestselling items cart mein add kar diye hain! Roti add karke order place kijiye."
        elif language == "telugu_english":
            message = "Mee tastes daggara ga kudaradaniki konni top and most popular suggestions select chesanu andi!"
            if not suggestions:
                message = "Mee table cart lo already best items add aypoyayi, direct ga place order trigger cheyyandi."
        else:
            message = "Based on your preferences, I have selected our top-rated gourmet preparations."
            if not suggestions:
                message = "You have already added our bestselling items to your cart! Ready to review your cart?"

        return suggestions, message

    @staticmethod
    def process_chat(message: str, session_id: str) -> ChatResponse:
        """
        Main AI Orchestration entry point.
        """
        # 1. Sanitize raw user text to defend against HTML/XSS injection
        clean_message = AIOrchestrator.sanitize_input(message)
        
        # 2. Redact sensitive telephone numbers or emails before AI handling or storing logs
        scrubbed_message = AIOrchestrator.strip_pii(clean_message)

        # Clean OpenAI hook entry
        openai_res = AIOrchestrator._openai_fallback(scrubbed_message, session_id)
        if openai_res:
            return openai_res

        # 3. Normalize Query
        normalized = AIOrchestrator.normalize_query(scrubbed_message)
        lang = normalized["language_detected"]
        intent = normalized["intent"]

        # Register context in session memory
        if session_id not in SESSION_AI_MEMORY:
            SESSION_AI_MEMORY[session_id] = []
        SESSION_AI_MEMORY[session_id].append(normalized)

        suggestions = []
        
        # 2. Intent Routing
        if intent == "waiter_call":
            response_text = RESPONSES_BY_LANG[lang]["waiter"]
        elif intent == "order_status":
            response_text = RESPONSES_BY_LANG[lang]["status"]
        elif intent == "conclude_session":
            # Direct upsell flow on conclusion ("that's all")
            suggestions, response_text = AIOrchestrator.get_upsell_suggestions(
                session_id=session_id,
                user_query=message,
                language=lang
            )
            if not response_text:
                # If no dessert valid, return standard conclude
                if lang == "hinglish":
                    response_text = "Thik hai! Maine table cart ready rakha hai, aap review karke checkout kar sakte hain."
                elif lang == "telugu_english":
                    response_text = "Sure andi! Cart ready ga undi. Review chesi place order cheyyandi."
                else:
                    response_text = "Excellent! Your cart is fully reviewed and ready for you to place order."
        else:
            # First, check if there is an active context-aware upsell trigger (except if they explicitly ask for list recommendations!)
            has_explicit_pref = len(normalized["preferences"]) > 0
            
            upsell_sug, upsell_txt = [], None
            if not has_explicit_pref:
                upsell_sug, upsell_txt = AIOrchestrator.get_upsell_suggestions(
                    session_id=session_id,
                    user_query=message,
                    language=lang
                )

            if upsell_txt:
                suggestions = upsell_sug
                response_text = upsell_txt
            else:
                # Fallback to standard recommendation agent
                suggestions, response_text = AIOrchestrator.get_recommendations(
                    session_id=session_id,
                    preferences=normalized["preferences"],
                    language=lang
                )

        return ChatResponse(
            message=response_text,
            suggestions=suggestions,
            timestamp=datetime.now()
        )
