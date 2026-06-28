import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ProtonFix AI",
  description: "Linux gaming log analyzer for Proton, Steam, DXVK, VKD3D, and Vulkan issues.",
};

function AppNav() {
  return (
    <header className="border-b border-zinc-800 bg-zinc-950/95 px-8 py-4 text-white">
      <div className="mx-auto flex max-w-6xl flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <a href="/" className="group">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600 font-mono text-xl font-bold shadow-lg shadow-blue-950/40">
              PF
            </div>

            <div>
              <p className="text-lg font-bold leading-tight">ProtonFix AI</p>
              <p className="text-xs text-zinc-500">
                Linux Gaming Troubleshooter
              </p>
            </div>
          </div>
        </a>

        <nav className="flex flex-wrap gap-2">
          <a
            href="/"
            className="rounded-lg bg-zinc-900 px-3 py-2 text-sm font-semibold text-zinc-200 hover:bg-zinc-800"
          >
            Analyze
          </a>

          <a
            href="/history"
            className="rounded-lg bg-zinc-900 px-3 py-2 text-sm font-semibold text-zinc-200 hover:bg-zinc-800"
          >
            History
          </a>

          <a
            href="/stats"
            className="rounded-lg bg-zinc-900 px-3 py-2 text-sm font-semibold text-zinc-200 hover:bg-zinc-800"
          >
            Stats
          </a>

          <span className="rounded-lg border border-zinc-800 px-3 py-2 text-sm font-semibold text-zinc-500">
            v0.5
          </span>
        </nav>
      </div>
    </header>
  );
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="bg-zinc-950">
        <AppNav />
        {children}
      </body>
    </html>
  );
}
