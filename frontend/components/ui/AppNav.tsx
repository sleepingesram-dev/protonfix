"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const VERSION = "0.7.0";

const NAV_LINKS = [
  { href: "/analyze", label: "Analyze" },
  { href: "/history", label: "History" },
  { href: "/stats", label: "Stats" },
  { href: "/submit", label: "Submit Log" },
  { href: "/admin", label: "Admin" },
];

export default function AppNav() {
  const pathname = usePathname();

  return (
    <header className="border-b border-zinc-800 bg-zinc-950/95 px-8 py-4 text-white">
      <div className="mx-auto flex max-w-6xl flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <Link href="/" className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600 font-mono text-xl font-bold shadow-lg shadow-blue-950/40">
            PF
          </div>
          <div>
            <p className="text-lg font-bold leading-tight">ProtonFix</p>
            <p className="text-xs text-zinc-500">Linux Gaming Troubleshooter</p>
          </div>
        </Link>

        <nav className="flex flex-wrap gap-2">
          {NAV_LINKS.map(({ href, label }) => {
            const active =
              pathname === href ||
              (href !== "/" && pathname.startsWith(href));
            return (
              <Link
                key={href}
                href={href}
                className={`rounded-lg px-3 py-2 text-sm font-semibold transition-colors ${
                  active
                    ? "bg-blue-600 text-white"
                    : "bg-zinc-900 text-zinc-200 hover:bg-zinc-800"
                }`}
              >
                {label}
              </Link>
            );
          })}
          <span className="rounded-lg border border-zinc-800 px-3 py-2 text-sm font-semibold text-zinc-500">
            v{VERSION}
          </span>
        </nav>
      </div>
    </header>
  );
}
