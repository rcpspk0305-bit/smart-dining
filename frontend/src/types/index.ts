export interface MenuItem {
  id: string;
  name: string;
  category: string;
  price: number;
  description: string;
  image_url?: string;
  tags: string[];
  allergens: string[];
  available: boolean;
  popular_score: number;
  complementary_items: string[];
}

export interface Session {
  id: string;
  table_id: string;
  is_active: boolean;
  created_at: string;
  expires_at: string;
  ttl_seconds_remaining: number;
}

export interface CartItem {
  menu_item: MenuItem;
  quantity: number;
  special_instructions?: string;
}

export interface CartResponse {
  session_id: string;
  table_id: string;
  items: CartItem[];
  subtotal: number;
  gst_amount: number;
  grand_total: number;
  total_quantity: number;
}

export type MessageSender = "user" | "assistant";

export interface ChatMessage {
  id: string;
  sender: MessageSender;
  content: string;
  timestamp: string;
}

export interface OTPSendRequest {
  phone_number: string;
}

export interface OTPVerifyRequest {
  phone_number: string;
  otp_code: string;
}

export interface OTPResponse {
  success: boolean;
  message: string;
  verification_token?: string;
}

export type OrderStatus = "pending" | "confirmed" | "preparing" | "served" | "completed" | "cancelled";

export interface Order {
  id: string;
  session_id: string;
  table_id: string;
  items: CartItem[];
  status: OrderStatus;
  total_price: number;
  created_at: string;
  phone_number?: string;
}
