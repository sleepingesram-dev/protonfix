"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import type { Submission } from "@/types/diagnosis";
import { ApiError, getSubmissions } from "@/lib/api";
import Card from "@/components/ui/Card";
import AdminTokenForm from "@/components/admin/AdminTokenForm";

const STATUS_COLORS: Record<string, string> = {
  pending: "bg-yellow-900 text-yellow-200",
  diagnosed: "bg-green-900 text-green-200",
  reviewed: "bg-blue-900 text-blue-200",
};

export default function AdminPage() {
  const [submissions, setSubmissions] = useState<Submission[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [unauthorized, setUnauthorized] = useState(false);

  const load = useCallback(() => {
    getSubmissions()
      .then((subs) => {
        setSubmissions(subs);
        setUnauthorized(false);
        setError(null);
      })
      .catch((err) => {
        if (err instanceof ApiError && err.status === 401) {
          setUnauthorized(true);
        } else {
          setError(
            err instanceof Error ? err.message : "Failed to load submissions."
          );
        }
      })
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  function retry() {
    setLoading(true);
    setError(null);
    setUnauthorized(false);
    load();
  }

  if (unauthorized) {
    return (
      <main className="min-h-screen bg-zinc-950 p-8 text-white">
        <div className="mx-auto max-w-xl">
          <AdminTokenForm onSubmit={retry} />
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-zinc-950 p-8 text-white">
      <div className="mx-auto max-w-6xl">
        <div className="mb-8 flex flex-wrap items-start justify-between gap-4">
          <div>
            <p className="mb-2 text-sm font-semibold uppercase tracking-wide text-blue-400">
              ProtonFix
            </p>
            <h1 className="mb-2 text-4xl font-bold">Admin — Submissions</h1>
            <p className="text-zinc-400">
              Anonymously submitted logs awaiting review.
            </p>
          </div>
          <span className="rounded-lg border border-yellow-700 bg-yellow-950/40 px-3 py-1 text-xs font-semibold text-yellow-300">
            Admin Area
          </span>
        </div>

        <Card>
          {loading ? (
            <p className="text-zinc-400">Loading submissions...</p>
          ) : error ? (
            <p className="text-red-400">{error}</p>
          ) : submissions.length === 0 ? (
            <p className="text-zinc-400">No submissions yet.</p>
          ) : (
            <div className="space-y-3">
              {submissions.map((sub) => (
                <Link
                  key={sub.id}
                  href={`/admin/${sub.id}`}
                  className="block rounded-lg border border-zinc-800 bg-zinc-950 p-4 transition hover:border-blue-500/50 hover:bg-zinc-900"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="min-w-0">
                      <div className="flex items-center gap-3">
                        <span className="shrink-0 font-mono text-sm text-zinc-500">
                          #{sub.id}
                        </span>
                        <span className="truncate font-medium text-white">
                          {sub.filename || "Unnamed file"}
                        </span>
                      </div>
                      {sub.note && (
                        <p className="mt-1 truncate text-sm text-zinc-400">
                          {sub.note}
                        </p>
                      )}
                      <p className="mt-1 text-xs text-zinc-600">
                        {sub.submitted_at?.slice(0, 16).replace("T", " ")} UTC
                        {sub.log_size
                          ? ` · ${Math.round(sub.log_size / 1024)} KB`
                          : ""}
                      </p>
                    </div>
                    <span
                      className={`shrink-0 rounded px-2 py-1 text-xs font-semibold ${
                        STATUS_COLORS[sub.status] ??
                        "bg-zinc-800 text-zinc-400"
                      }`}
                    >
                      {sub.status}
                    </span>
                  </div>
                </Link>
              ))}
            </div>
          )}
        </Card>
      </div>
    </main>
  );
}
