import type { Metadata, Viewport } from "next";
import "./globals.css";
import AppNav from "@/components/ui/AppNav";

export const metadata: Metadata = {
  title: "ProtonFix",
  description: "Linux gaming log analyzer for Proton, Steam, DXVK, VKD3D, and Vulkan issues.",
  openGraph: {
    title: "ProtonFix",
    description: "Linux gaming log analyzer for Proton, Steam, DXVK, VKD3D, and Vulkan issues.",
    type: "website",
  },
  twitter: {
    card: "summary",
    title: "ProtonFix",
    description: "Linux gaming log analyzer for Proton, Steam, DXVK, VKD3D, and Vulkan issues.",
  },
};

export const viewport: Viewport = {
  themeColor: "#2563eb",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body className="bg-zinc-950">
        <AppNav />
        {children}
      </body>
    </html>
  );
}
