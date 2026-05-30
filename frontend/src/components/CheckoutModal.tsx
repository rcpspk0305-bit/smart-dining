"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { 
  X, 
  Phone, 
  User, 
  Key, 
  CheckCircle2, 
  Clock, 
  ShieldCheck, 
  TrendingUp,
  Receipt,
  Sparkles,
  ArrowRight
} from "lucide-react";
import { API_BASE_URL } from "@/lib/config";

interface CheckoutModalProps {
  isOpen: boolean;
  onClose: () => void;
  grandTotal: number;
  onSuccess: (orderId: string) => void;
  sessionId?: string | null;
  isBackendMode?: boolean;
}

export default function CheckoutModal({
  isOpen,
  onClose,
  grandTotal,
  onSuccess,
  sessionId = null,
  isBackendMode = false
}: CheckoutModalProps) {
  // Input fields
  const [customerName, setCustomerName] = useState<string>("");
  const [phoneNumber, setPhoneNumber] = useState<string>("");
  const [otpCode, setOtpCode] = useState<string>("");

  // Step states
  const [otpSent, setOtpSent] = useState<boolean>(false);
  const [isVerifying, setIsVerifying] = useState<boolean>(false);
  const [isSuccess, setIsSuccess] = useState<boolean>(false);
  const [generatedOrderId, setGeneratedOrderId] = useState<string>("");
  const [estimatedWaitTime, setEstimatedWaitTime] = useState<number>(15);

  const handleSendOtp = () => {
    if (!customerName.trim() || !phoneNumber.trim()) {
      alert("Please enter both your name and phone number!");
      return;
    }
    setOtpSent(true);
  };

  const handleVerifyAndOrder = async () => {
    if (otpCode !== "123456") {
      alert("Invalid verification code! In demo mode, enter OTP code 123456 to authenticate.");
      return;
    }

    setIsVerifying(true);

    if (isBackendMode && sessionId) {
      try {
        const response = await fetch(`${API_BASE_URL}/api/session/${sessionId}/order`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ verification_token: "mock_jwt_token_123" })
        });
        if (response.ok) {
          const orderData = await response.json();
          const waitTime = Math.floor(Math.random() * 11) + 15;
          setGeneratedOrderId(orderData.id);
          setEstimatedWaitTime(waitTime);
          setIsVerifying(false);
          setIsSuccess(true);
          return;
        }
      } catch (err) {
        console.error("Failed to place order in backend, falling back to mock:", err);
      }
    }

    // Simulate short network dispatch delay for high fidelity experience
    setTimeout(() => {
      const orderId = "ORD-" + Math.random().toString(36).substring(2, 8).toUpperCase();
      const waitTime = Math.floor(Math.random() * 11) + 15;
      
      setGeneratedOrderId(orderId);
      setEstimatedWaitTime(waitTime);
      setIsVerifying(false);
      setIsSuccess(true);
    }, 1200);
  };

  const handleBypassCheckout = async () => {
    setIsVerifying(true);

    if (isBackendMode && sessionId) {
      try {
        const response = await fetch(`${API_BASE_URL}/api/session/${sessionId}/order`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ verification_token: null })
        });
        if (response.ok) {
          const orderData = await response.json();
          setGeneratedOrderId(orderData.id);
          setEstimatedWaitTime(12);
          setIsVerifying(false);
          setIsSuccess(true);
          return;
        }
      } catch (err) {
        console.error("Failed to place order bypass in backend, falling back to mock:", err);
      }
    }

    setTimeout(() => {
      const orderId = "ORD-DEMO" + Math.random().toString(36).substring(2, 6).toUpperCase();
      const waitTime = 12;
      setGeneratedOrderId(orderId);
      setEstimatedWaitTime(waitTime);
      setIsVerifying(false);
      setIsSuccess(true);
    }, 800);
  };

  const handleCloseSuccess = () => {
    onSuccess(generatedOrderId);
    // Reset all internal states
    setCustomerName("");
    setPhoneNumber("");
    setOtpCode("");
    setOtpSent(false);
    setIsSuccess(false);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="absolute inset-0 bg-black/85 backdrop-blur-sm z-50 flex items-center justify-center p-6 animate-fade-in">
      <div className="w-full max-w-sm bg-neutral-900 border border-neutral-800 rounded-3xl p-5 shadow-2xl relative overflow-hidden">
        
        {/* Glowing visual backdrop */}
        <div className="absolute top-0 inset-x-0 h-1.5 bg-gradient-to-r from-orange-600 via-amber-500 to-orange-600"></div>

        {!isSuccess ? (
          <>
            {/* Header */}
            <div className="flex justify-between items-start mb-6">
              <div>
                <h3 className="text-sm font-bold text-neutral-100 font-display flex items-center gap-1.5">
                  <ShieldCheck className="w-4 h-4 text-orange-500" /> Secure Checkout
                </h3>
                <p className="text-[10px] text-neutral-400">Authenticate session to submit order</p>
              </div>
              <button
                onClick={onClose}
                className="p-1 rounded-full hover:bg-neutral-800 text-neutral-400 hover:text-neutral-200 transition-colors"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* Content Forms */}
            <div className="space-y-4">
              
              {/* Display Total Price */}
              <div className="p-3.5 rounded-2xl bg-neutral-950 border border-neutral-800 flex items-center justify-between font-mono text-[11px]">
                <span className="text-neutral-500 font-display flex items-center gap-1.5">
                  <Receipt className="w-3.5 h-3.5 text-neutral-600" /> Order Total
                </span>
                <span className="text-orange-400 font-bold font-display text-xs">₹{grandTotal.toFixed(2)}</span>
              </div>

              {!otpSent ? (
                <div className="space-y-4 animate-fade-in">
                  {/* Name Input */}
                  <div className="space-y-1">
                    <label className="text-[9px] text-neutral-500 font-bold uppercase tracking-wider block">
                      Your Name
                    </label>
                    <div className="relative">
                      <User className="absolute left-3.5 top-3 w-3.5 h-3.5 text-neutral-600" />
                      <input
                        type="text"
                        value={customerName}
                        onChange={(e) => setCustomerName(e.target.value)}
                        placeholder="Enter full name"
                        className="w-full bg-neutral-950 border border-neutral-800 rounded-xl pl-10 pr-4 py-2.5 text-xs text-neutral-200 focus:outline-none focus:border-orange-500 font-medium"
                      />
                    </div>
                  </div>

                  {/* Phone Input */}
                  <div className="space-y-1">
                    <label className="text-[9px] text-neutral-500 font-bold uppercase tracking-wider block">
                      Phone Number
                    </label>
                    <div className="relative">
                      <Phone className="absolute left-3.5 top-3 w-3.5 h-3.5 text-neutral-600" />
                      <input
                        type="tel"
                        value={phoneNumber}
                        onChange={(e) => setPhoneNumber(e.target.value)}
                        placeholder="+91 (555) 000-0000"
                        className="w-full bg-neutral-950 border border-neutral-800 rounded-xl pl-10 pr-4 py-2.5 text-xs text-neutral-200 focus:outline-none focus:border-orange-500 font-bold font-mono placeholder-neutral-700"
                      />
                    </div>
                  </div>

                  <Button
                    onClick={handleSendOtp}
                    disabled={!customerName.trim() || !phoneNumber.trim()}
                    className="w-full bg-[#bc470a] hover:bg-[#a13b08] text-white font-bold h-10 rounded-xl text-xs active:scale-95 transition-all shadow shadow-orange-600/10"
                  >
                    Send Verification OTP
                  </Button>

                  <div className="relative flex py-1 items-center">
                    <div className="flex-grow border-t border-neutral-800"></div>
                    <span className="flex-shrink mx-4 text-[8px] text-neutral-500 font-bold uppercase tracking-wider">Demo mode</span>
                    <div className="flex-grow border-t border-neutral-800"></div>
                  </div>

                  <Button
                    onClick={handleBypassCheckout}
                    variant="outline"
                    className="w-full border-neutral-800 hover:bg-neutral-800 text-neutral-400 hover:text-white font-bold h-10 rounded-xl text-xs active:scale-95"
                  >
                    {isVerifying ? "Processing..." : "Skip Verification & Order"}
                  </Button>
                </div>
              ) : (
                <div className="space-y-4 animate-fade-in">
                  {/* OTP Code input */}
                  <div className="space-y-1 text-center">
                    <p className="text-[10px] text-orange-400 font-bold font-mono flex items-center justify-center gap-1">
                      <Sparkles className="w-3 h-3 text-orange-400" /> Mock OTP Dispatched! Enter **123456**
                    </p>
                    <div className="relative mt-2">
                      <Key className="absolute left-3.5 top-3 w-3.5 h-3.5 text-neutral-600" />
                      <input
                        type="text"
                        maxLength={6}
                        value={otpCode}
                        onChange={(e) => setOtpCode(e.target.value)}
                        placeholder="Enter 6-digit code"
                        className="w-full bg-neutral-950 border border-neutral-800 rounded-xl pl-10 pr-4 py-2.5 text-sm tracking-widest text-center text-orange-400 font-bold font-mono focus:outline-none focus:border-orange-500"
                      />
                    </div>
                  </div>

                  <Button
                    onClick={handleVerifyAndOrder}
                    disabled={otpCode.length < 6 || isVerifying}
                    className="w-full bg-[#bc470a] hover:bg-[#a13b08] text-white font-bold h-10 rounded-xl text-xs active:scale-95 shadow shadow-orange-600/10"
                  >
                    {isVerifying ? "Processing Order..." : "Verify & Place Order"}
                  </Button>

                  <button
                    onClick={() => setOtpSent(false)}
                    className="w-full text-center text-[10px] text-neutral-500 hover:text-neutral-300 font-medium"
                  >
                    ← Edit Name or Phone number
                  </button>
                </div>
              )}
            </div>
          </>
        ) : (
          /* GORGEOUS SUCCESS SCREEN */
          <div className="text-center py-6 space-y-5 animate-fade-in">
            {/* Checked Circle Animated */}
            <div className="inline-flex p-3 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-500 mb-1 animate-pulse">
              <CheckCircle2 className="w-12 h-12 text-emerald-400" />
            </div>

            <div className="space-y-1">
              <h3 className="text-base font-bold text-neutral-100 font-display">Kitchen Ticket Placed!</h3>
              <p className="text-[10px] text-neutral-400">
                Your order is registered and has been dispatched to our chef.
              </p>
            </div>

            {/* Bill info card */}
            <div className="p-4 rounded-2xl bg-neutral-950 border border-neutral-800 text-left space-y-3 font-mono text-[10px]">
              <div className="flex justify-between items-center text-neutral-500">
                <span>Order ID</span>
                <span className="text-neutral-100 font-bold">{generatedOrderId}</span>
              </div>
              <div className="flex justify-between items-center text-neutral-500">
                <span>Paid Amount</span>
                <span className="text-orange-400 font-bold">₹{grandTotal.toFixed(2)}</span>
              </div>
              <div className="flex justify-between items-center text-neutral-500 border-t border-neutral-900 pt-2.5">
                <span className="flex items-center gap-1"><Clock className="w-3.5 h-3.5 text-neutral-600" /> Wait Time</span>
                <span className="text-emerald-400 font-bold flex items-center gap-1">
                  <TrendingUp className="w-3.5 h-3.5" /> ~{estimatedWaitTime} mins
                </span>
              </div>
            </div>

            <Button
              onClick={handleCloseSuccess}
              className="w-full bg-[#bc470a] hover:bg-[#a13b08] text-white font-bold h-11 rounded-xl text-xs active:scale-95 shadow-md shadow-orange-600/10 flex items-center justify-center gap-1.5"
            >
              Back to Dining Menu <ArrowRight className="w-4 h-4" />
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}
