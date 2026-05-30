"use client";

import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { 
  X, 
  Minus, 
  Plus, 
  ShoppingBag, 
  User, 
  FileText, 
  Info, 
  Sparkles,
  ArrowRight,
  UserCheck
} from "lucide-react";
import { CartItem } from "@/types";

interface CartDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  items: CartItem[];
  onUpdateQuantity: (itemId: string, delta: number) => void;
  onSaveInstructions: (itemId: string, text: string) => void;
  onPlaceOrder: () => void;
}

export default function CartDrawer({
  isOpen,
  onClose,
  items,
  onUpdateQuantity,
  onSaveInstructions,
  onPlaceOrder
}: CartDrawerProps) {
  // Input buffer to allow typing smoothly without lagging on parent states
  const [buffer, setBuffer] = useState<Record<string, string>>({});

  // Subtotal and tax calculations (Indian 5% GST structure)
  const subtotal = items.reduce((acc, item) => acc + item.quantity * item.menu_item.price, 0);
  const gstAmount = Math.round(subtotal * 0.05 * 100) / 100;
  const grandTotal = Math.round((subtotal + gstAmount) * 100) / 100;
  const totalQuantity = items.reduce((acc, item) => acc + item.quantity, 0);

  // Helper to generate realistic group ordering names
  const getAddedByLabel = (itemId: string) => {
    // Make the first item show "Guest (Me)" and others show a simulated guest for the shared table effect
    const charCodeSum = itemId.charCodeAt(0) + itemId.charCodeAt(itemId.length - 1);
    if (charCodeSum % 3 === 0) {
      return { name: "Guest (Me)", avatarColor: "bg-orange-500/10 text-orange-400 border-orange-500/20" };
    } else if (charCodeSum % 3 === 1) {
      return { name: "Aarav (Guest 2)", avatarColor: "bg-blue-500/10 text-blue-400 border-blue-500/20" };
    } else {
      return { name: "Riya (Guest 3)", avatarColor: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20" };
    }
  };

  if (!isOpen) return null;

  return (
    <div className="absolute inset-0 bg-black/70 backdrop-blur-xs z-40 flex flex-col justify-end animate-fade-in">
      
      {/* Click outside to close */}
      <div className="absolute inset-0 -z-10" onClick={onClose}></div>

      {/* Drawer panel sliding from bottom on mobile */}
      <div className="w-full max-h-[85vh] bg-neutral-900 border-t border-neutral-850 rounded-t-3xl shadow-2xl flex flex-col relative z-50 animate-slide-in-bottom">
        
        {/* Subtle sliding notch pill at top */}
        <div className="mx-auto w-12 h-1 bg-neutral-800 rounded-full my-2.5 shrink-0"></div>

        {/* Drawer Header */}
        <div className="px-5 pb-4 border-b border-neutral-850/60 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="p-1.5 rounded-lg bg-orange-600/10 border border-orange-500/20 text-orange-500">
              <ShoppingBag className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-xs font-bold text-neutral-100 font-display">Shared Table Cart</h3>
              <p className="text-[9px] text-neutral-400">Collaborative dining session</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 hover:bg-neutral-800 rounded-full text-neutral-400 hover:text-neutral-200 transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Cart items list */}
        <div className="flex-1 p-5 overflow-y-auto no-scrollbar space-y-5">
          {items.length === 0 ? (
            <div className="text-center py-12 space-y-2">
              <ShoppingBag className="w-10 h-10 text-neutral-700 mx-auto" />
              <p className="text-xs text-neutral-400 font-medium">Your shared table cart is empty.</p>
              <Button size="sm" onClick={onClose} className="bg-neutral-850 text-neutral-300 hover:bg-neutral-800 text-[10px] h-8 rounded-lg mt-2">
                Browse Menu
              </Button>
            </div>
          ) : (
            items.map((item) => {
              const label = getAddedByLabel(item.menu_item.id);
              return (
                <div key={item.menu_item.id} className="space-y-3.5 border-b border-neutral-850/50 pb-4.5 last:border-none">
                  
                  {/* Dish Title & Price */}
                  <div className="flex justify-between items-start gap-4">
                    <div className="space-y-0.5">
                      <h4 className="text-xs font-bold text-neutral-100 font-display">{item.menu_item.name}</h4>
                      <p className="text-[10px] text-neutral-400 font-mono">₹{item.menu_item.price} each</p>
                    </div>
                    <span className="text-xs font-bold font-mono text-orange-400">
                      ₹{item.menu_item.price * item.quantity}
                    </span>
                  </div>

                  {/* AddedBy Label (Simulating Shared table sessions) */}
                  <div className="flex items-center gap-1.5">
                    <div className={`px-2 py-0.5 rounded-full border text-[8px] font-semibold flex items-center gap-1 ${label.avatarColor}`}>
                      <User className="w-2.5 h-2.5" />
                      {label.name}
                    </div>
                  </div>

                  {/* Special Instructions Input */}
                  <div className="space-y-1">
                    <div className="flex items-center gap-1 text-[9px] text-neutral-500 font-semibold uppercase tracking-wider">
                      <FileText className="w-3 h-3 text-neutral-600" /> Special Instructions
                    </div>
                    <input
                      type="text"
                      value={buffer[item.menu_item.id] ?? item.special_instructions ?? ""}
                      onChange={(e) => {
                        const val = e.target.value;
                        setBuffer(prev => ({ ...prev, [item.menu_item.id]: val }));
                        onSaveInstructions(item.menu_item.id, val);
                      }}
                      placeholder="e.g. Medium spicy, no dairy garnish..."
                      className="w-full bg-neutral-950 border border-neutral-850 rounded-xl px-3 py-1.5 text-[10px] text-neutral-300 focus:outline-none focus:border-orange-500 placeholder-neutral-700 font-medium"
                    />
                  </div>

                  {/* Stepper Controls */}
                  <div className="flex justify-between items-center pt-1.5">
                    <span className="text-[8px] text-neutral-500 italic flex items-center gap-1">
                      <Info className="w-2.5 h-2.5 text-neutral-600" /> Autosaves changes
                    </span>

                    <div className="flex items-center gap-2 bg-neutral-950 border border-neutral-850 rounded-lg p-0.5">
                      <button
                        onClick={() => onUpdateQuantity(item.menu_item.id, -1)}
                        className="w-5.5 h-5.5 rounded bg-neutral-900 flex items-center justify-center hover:bg-neutral-800 text-neutral-400"
                      >
                        <Minus className="w-2.5 h-2.5" />
                      </button>
                      <span className="text-[10px] font-mono font-bold px-1 text-neutral-200">{item.quantity}</span>
                      <button
                        onClick={() => onUpdateQuantity(item.menu_item.id, 1)}
                        className="w-5.5 h-5.5 rounded bg-neutral-900 flex items-center justify-center hover:bg-neutral-800 text-neutral-400"
                      >
                        <Plus className="w-2.5 h-2.5" />
                      </button>
                    </div>
                  </div>
                </div>
              );
            })
          )}

          {/* Pricing Summary (GST breakdown) */}
          {items.length > 0 && (
            <div className="p-4 rounded-2xl bg-neutral-950 border border-neutral-850/60 space-y-2.5 font-mono text-[10px]">
              <div className="flex justify-between text-neutral-400">
                <span>Items Subtotal</span>
                <span>₹{subtotal.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-neutral-400">
                <span>Restaurant GST (5% Total)</span>
                <span>₹{gstAmount.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-neutral-300 border-t border-neutral-900 pt-2 font-bold text-xs">
                <span className="text-orange-400 font-display">GRAND TOTAL</span>
                <span className="text-orange-400">₹{grandTotal.toFixed(2)}</span>
              </div>
            </div>
          )}
        </div>

        {/* Action Button Footer */}
        {items.length > 0 && (
          <div className="p-4 bg-neutral-950 border-t border-neutral-850/60 flex flex-col gap-2">
            <Button
              onClick={onPlaceOrder}
              className="w-full bg-[#bc470a] hover:bg-[#a13b08] text-white font-bold h-11 rounded-xl text-xs active:scale-95 shadow-md shadow-orange-600/10 flex items-center justify-center gap-1.5"
            >
              Place Kitchen Order <ArrowRight className="w-4 h-4" />
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}
