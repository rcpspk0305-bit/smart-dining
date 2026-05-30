import type { Metadata, Viewport } from "next";
import { Inter, Plus_Jakarta_Sans } from "next/font/google";
import "./globals.css";

const inter = Inter({ 
  subsets: ["latin"],
  variable: "--font-sans" 
});

const plusJakarta = Plus_Jakarta_Sans({
  subsets: ["latin"],
  variable: "--font-display",
  weight: ["400", "500", "600", "700", "800"]
});

export const metadata: Metadata = {
  title: "Gourmet AI - Smart Dining Assistant",
  description: "An AI-powered mobile-first table dining and self-ordering assistant",
  manifest: "/manifest.json",
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 5,
  userScalable: true,
  themeColor: "#bc470a"
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${inter.variable} ${plusJakarta.variable} dark`}>
      <body className="font-sans antialiased min-h-screen bg-neutral-950 text-neutral-50 selection:bg-orange-500/20">
        <main className="max-w-md mx-auto min-h-screen bg-neutral-900 border-x border-neutral-800 shadow-2xl relative flex flex-col">
          {children}
        </main>
      </body>
    </html>
  );
}
