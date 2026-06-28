"use client";

import { useEffect, useState } from "react";
import type { HistoryEntry } from "@/types/diagnosis";
import { getHistory } from "@/lib/api";

type HistoryItem = HistoryEntry;

function getSeverityBadge(severity: string) {
  const level = severity?.toLowerCase();

  if (level === "high") {
    return (
      <span className="rounded bg-red-900 px-2 py-1 text-xs font-bold text-red-200">
        🔴 HIGH
      </span>
    );
  }

  if (level === "medium") {
    return (
      <span className="rounded bg-yellow-900 px-2 py-1 text-xs font-bold text-yellow-200">
        🟡 MEDIUM
      </span>
    );
  }

  return (
    <span className="rounded bg-green-900 px-2 py-1 text-xs font-bold text-green-200">
      🟢 LOW
    </span>
  );
}

export default function HistoryPage() {
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadHistory() {
      try {
        const data = await getHistory();
        setHistory(data);
      } catch (error) {
        console.error(error);
      }

      setLoading(false);
    }

    loadHistory();
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
          ) : history.length === 0 ? (
            <p className="text-zinc-400">No saved diagnoses yet.</p>
          ) : (
            <div className="space-y-4">
              {history.map((item) => (
                <div
                  key={item.id}
                  className="rounded-lg border border-zinc-800 bg-zinc-950 p-4"
                >
                  <div className="flex flex-col justify-between gap-3 md:flex-row md:items-start">
                    <div>
                      <p className="text-sm text-zinc-500">
                        {item.created_at}
                      </p>

                      <h2 className="mt-1 text-xl font-bold">
                        {item.game || "Unknown Game"}
                      </h2>

                      <p className="mt-1 text-sm text-zinc-400">
                        File: {item.filename || "Unknown"}
                      </p>

                      <p className="mt-1 text-sm text-zinc-400">
                        AppID: {item.appid || "Unknown"} · Proton:{" "}
                        {item.proton_version || "Unknown"}
                      </p>

                      <p className="mt-3 text-zinc-300">
                        {item.summary}
                      </p>

                      <p className="mt-2 text-sm text-blue-400">
                        Primary: {item.primary_fingerprint || "None"}
                        {item.confidence
                          ? ` · ${item.confidence}% confidence`
                          : ""}
                      </p>
                    </div>

                    <div className="flex flex-col items-start gap-3 md:items-end">
                      {getSeverityBadge(item.severity)}

                      <a
                        href={`/history/${item.id}`}
                        className="rounded bg-blue-600 px-3 py-2 text-sm font-semibold hover:bg-blue-500"
                      >
                        View Diagnosis
                      </a>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
