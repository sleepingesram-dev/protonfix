import Link from "next/link";
import type { Stats, HistoryEntry } from "@/types/diagnosis";

import Card from "@/components/ui/Card";
import StatCard from "@/components/ui/StatCard";
import SeverityBadge from "@/components/ui/SeverityBadge";
import ConfidenceBadge from "@/components/ui/ConfidenceBadge";
import { humanizeFingerprint } from "@/lib/fingerprints";

type DashboardProps = {
  stats: Stats | null;
  history: HistoryEntry[];
  loading: boolean;
};

export default function Dashboard({ stats, history, loading }: DashboardProps) {
  if (loading) {
    return (
      <section className="mb-8">
        <Card>
          <p className="text-zinc-400">Loading dashboard...</p>
        </Card>
      </section>
    );
  }

  return (
    <section className="mb-8 space-y-6">
      <Card>
        <h2 className="mb-4 text-xl font-semibold text-white">
          Quick Stats
        </h2>

        <div className="grid gap-4 md:grid-cols-3">
          <StatCard
            title="Total Logs"
            value={stats?.total_logs ?? 0}
          />

          <StatCard
            title="Known Issue Hits"
            value={stats?.known_issue_used ?? 0}
          />

          <StatCard
            title="AI Analyses"
            value={stats?.ai_used ?? 0}
          />
        </div>
      </Card>

      <Card>
        <div className="mb-4 flex items-center justify-between">
          <div>
            <h2 className="text-xl font-semibold text-white">
              Recent Diagnoses
            </h2>

            <p className="mt-1 text-sm text-zinc-500">
              The latest saved troubleshooting results.
            </p>
          </div>

          <Link
            href="/history"
            className="text-sm font-medium text-blue-400 hover:text-blue-300"
          >
            View All →
          </Link>
        </div>

        {history.length === 0 ? (
          <div className="rounded-lg border border-zinc-800 bg-zinc-950 p-6 text-center text-zinc-500">
            No diagnoses yet. Upload a log first, because apparently the machine refuses to debug vibes.
          </div>
        ) : (
          <div className="space-y-3">
            {history.slice(0, 5).map((item) => (
              <Link
                key={item.id}
                href={`/history/${item.id}`}
                className="block rounded-lg border border-zinc-800 bg-zinc-950 p-4 transition hover:border-blue-500/50 hover:bg-zinc-900"
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="min-w-0">
                    <p className="truncate font-medium text-white">
                      {item.game || "Unknown Game"}
                    </p>

                    <p className="mt-1 truncate text-sm text-zinc-500">
                      {item.filename || "Unknown log file"}
                    </p>

                    <div className="mt-3 flex flex-wrap gap-2">
                      {item.severity && (
                        <SeverityBadge severity={item.severity} />
                      )}

                      {item.confidence && (
                        <ConfidenceBadge confidence={item.confidence} />
                      )}

                      {item.primary_fingerprint && (
                        <span className="rounded-full border border-zinc-700 px-2 py-1 text-xs text-zinc-400">
                          {humanizeFingerprint(item.primary_fingerprint)}
                        </span>
                      )}
                    </div>
                  </div>

                  <div className="shrink-0 text-right text-sm">
                    <p className="text-zinc-400">
                      {item.ai_used ? "AI Analysis" : "Known Issue"}
                    </p>

                    <p className="mt-1 text-blue-400">
                      View →
                    </p>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </Card>
    </section>
  );
}
