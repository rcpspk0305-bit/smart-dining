"use client";

import Link from "next/link";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Utensils, QrCode, Sparkles, MapPin, ArrowRight } from "lucide-react";

export default function Home() {
  const [demoTable, setDemoTable] = useState("T4");

  return (
    <div className="flex-1 flex flex-col justify-between p-6 pb-12 bg-gradient-to-b from-neutral-900 via-neutral-900 to-black text-white">
      {/* Header Info */}
      <div className="space-y-4 pt-8 text-center">
        <div className="inline-flex items-center justify-center p-3 rounded-full bg-orange-500/10 border border-orange-500/20 text-orange-500 mb-2 animate-bounce">
          <Utensils className="h-8 w-8" />
        </div>
        <h1 className="text-3xl font-display font-extrabold tracking-tight bg-gradient-to-r from-orange-400 via-amber-400 to-orange-500 bg-clip-text text-transparent">
          Gourmet AI
        </h1>
        <p className="text-sm text-neutral-400 max-w-xs mx-auto">
          Experience AI-driven ordering, tailored suggestions, and instant server assistance directly from your table.
        </p>
      </div>

      {/* Visual QR mock */}
      <div className="my-8 flex flex-col items-center justify-center p-8 rounded-2xl bg-neutral-900/50 border border-neutral-800 glass-panel shadow-inner relative overflow-hidden group">
        <div className="absolute inset-0 bg-gradient-to-tr from-orange-500/10 to-transparent opacity-50"></div>
        <div className="w-48 h-48 border-2 border-dashed border-neutral-700 rounded-xl flex items-center justify-center relative p-4 bg-neutral-950/80 group-hover:border-orange-500/50 transition-colors duration-300">
          <QrCode className="w-32 h-32 text-neutral-500 group-hover:text-orange-500 transition-colors duration-300 animate-pulse" />
          {/* Subtle corners overlay */}
          <div className="absolute top-2 left-2 w-4 h-4 border-t-2 border-l-2 border-orange-500"></div>
          <div className="absolute top-2 right-2 w-4 h-4 border-t-2 border-r-2 border-orange-500"></div>
          <div className="absolute bottom-2 left-2 w-4 h-4 border-b-2 border-l-2 border-orange-500"></div>
          <div className="absolute bottom-2 right-2 w-4 h-4 border-b-2 border-r-2 border-orange-500"></div>
        </div>
        <span className="text-xs text-neutral-400 mt-4 flex items-center gap-1.5 font-medium">
          <Sparkles className="w-3.5 h-3.5 text-orange-400" /> Scan QR at Table to Begin
        </span>
      </div>

      {/* Action / Simulation controls */}
      <div className="space-y-4">
        <div className="p-4 rounded-xl bg-neutral-950/80 border border-neutral-800 space-y-3">
          <div className="flex items-center gap-2 text-xs font-semibold text-orange-400 uppercase tracking-wider">
            <MapPin className="w-3.5 h-3.5" /> Simulation Controls
          </div>
          <p className="text-xs text-neutral-400">
            For testing, enter a mock Table ID below to simulate sitting at a specific table.
          </p>
          <div className="flex gap-2">
            <input
              suppressHydrationWarning
              type="text"
              value={demoTable}
              onChange={(e) => setDemoTable(e.target.value.toUpperCase())}
              placeholder="e.g. T4"
              className="flex-1 px-3 py-2 text-sm rounded bg-neutral-900 border border-neutral-800 focus:outline-none focus:border-orange-500 text-center font-bold font-display uppercase tracking-widest text-orange-300"
            />
            <Link 
              href={`/table/${demoTable}`}
              className="font-semibold bg-[#bc470a] hover:bg-[#a13b08] text-white flex items-center justify-center gap-1.5 shadow-lg shadow-orange-500/20 active:scale-95 h-10 px-5 rounded-md text-sm transition-colors duration-200"
            >
              Sit Down <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>

        <p className="text-[10px] text-center text-neutral-500 font-mono">
          Antigravity Dining Framework v1.0.0
        </p>
      </div>
    </div>
  );
}
