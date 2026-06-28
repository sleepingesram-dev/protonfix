import type { Metadata } from "next";
import "./globals.css";
import AppNav from "@/components/ui/AppNav";

export const metadata: Metadata = {
  title: "ProtonFix AI",
  description: "Linux gaming log analyzer for Proton, Steam, DXVK, VKD3D, and Vulkan issues.",
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
