"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import type { HistoryEntry } from "@/types/diagnosis";
import { getHistory } from "@/lib/api";
import SeverityBadge from "@/components/ui/SeverityBadge";
import ConfidenceBadge from "@/components/ui/ConfidenceBadge";
import { humanizeFingerprint } from "@/lib/fingerprints";

export default function HistoryPage() {
  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getHistory()
      .then(setHistory)
      .catch((err) =>
        setError(err instanceof Error ? err.message : "Failed to load history.")
      )
      .finally(() => setLoading(false));
  }, []);

  return (
    <main className="min-h-screen bg-zinc-950 p-8 text-white">
      <div className="mx-auto max-w-6xl">
        <div className="mb-8">
          <p className="mb-2 text-sm font-semibold uppercase tracking-wide text-blue-400">
            ProtonFix AI
          </p>
          <h1 className="mb-3 text-4xl font-bold">Diagnosis History</h1>
          <p className="max-w-3xl text-zinc-400">
            Previously analyzed logs saved from this local ProtonFix instance.
          </p>
        </div>

        <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-6">
          {loading ? (
            <p className="text-zinc-400">Loading history...</p>
          ) : error ? (
            <p className="text-red-400">{error}</p>
          ) : history.length === 0 ? (
            <p className="text-zinc-400">No saved diagnoses yet.</p>
          ) : (
            <div className="space-y-3">
              {history.map((item) => (
                <Link
                  key={item.id}
                  href={`/history/${item.id}`}
                  className="block rounded-lg border border-zinc-800 bg-zinc-950 p-4 transition hover:border-blue-500/50 hover:bg-zinc-900"
                >
                  <div className="flex flex-col justify-between gap-3 md:flex-row md:items-start">
                    <div className="min-w-0">
                      <p className="text-xs text-zinc-600">
                        {item.created_at?.slice(0, 16).replace("T", " ")} UTC
                      </p>
                      <h2 className="mt-1 truncate text-lg font-bold">
                        {item.game || "Unknown Game"}
                      </h2>
                      <p className="mt-1 truncate text-sm text-zinc-400">
                        {item.filename || "Unknown file"}
                      </p>
                      <p className="mt-1 text-xs text-zinc-600">
                        AppID: {item.appid || "—"} · Proton:{" "}
                        {item.proton_version || "—"}
                      </p>
                      <p className="mt-2 line-clamp-2 text-sm text-zinc-300">
                        {item.summary}
                      </p>

                      <div className="mt-3 flex flex-wrap items-center gap-2">
                        <SeverityBadge severity={item.severity} />
                        {item.confidence != null && (
                          <ConfidenceBadge confidence={item.confidence} />
                        )}
                        {item.primary_fingerprint && (
                          <span className="rounded-full border border-zinc-700 px-2 py-1 text-xs text-zinc-400">
                            {humanizeFingerprint(item.primary_fingerprint)}
                          </span>
                        )}
                      </div>
                    </div>

                    <div className="shrink-0 text-right text-sm text-blue-400">
                      View →
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
