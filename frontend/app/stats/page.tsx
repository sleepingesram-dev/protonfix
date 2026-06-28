"use client";

import { useEffect, useState } from "react";
import Card from "@/components/ui/Card";
import StatCard from "@/components/ui/StatCard";
import type { Stats } from "@/types/diagnosis";
import { getStats } from "@/lib/api";

function StatsList({
  title,
  data,
}: {
  title: string;
  data: Record<string, number>;
}) {
  return (
    <Card>
      <h2 className="mb-4 text-xl font-bold">{title}</h2>

      {Object.entries(data || {})
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10)
        .map(([name, count]) => (
          <div key={name} className="mb-2 flex justify-between gap-4">
            <span className="break-all">{name}</span>
            <span>{count}</span>
          </div>
        ))}
    </Card>
  );
}

export default function StatsPage() {
  const [stats, setStats] = useState<Stats | null>(null);

  useEffect(() => {
    async function loadStats() {
      try {
        const data = await getStats();
        setStats(data);
      } catch (err) {
        console.error(err);
      }
    }

    loadStats();
  }, []);

  if (!stats) {
    return (
      <main className="min-h-screen bg-zinc-950 p-8 text-white">
        Loading stats...
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-zinc-950 p-8 text-white">
      <div className="mx-auto max-w-6xl">
        <p className="mb-2 text-sm font-semibold uppercase tracking-wide text-blue-400">
          ProtonFix AI
        </p>

        <h1 className="mb-3 text-4xl font-bold">ProtonFix Statistics</h1>

        <p className="mb-8 max-w-3xl text-zinc-400">
          Usage stats from analyzed logs, known issue matches, and AI fallback
          calls.
        </p>

        <div className="mb-8 grid gap-4 md:grid-cols-3">
          <StatCard title="Total Logs" value={stats.total_logs} />
          <StatCard title="Known Issue Hits" value={stats.known_issue_used} />
          <StatCard title="AI Analyses" value={stats.ai_used} />
        </div>

        <div className="grid gap-6 md:grid-cols-2">
          <StatsList title="Top Fingerprints" data={stats.fingerprints} />
          <StatsList title="Top Games" data={stats.games} />
          <StatsList title="Proton Versions" data={stats.proton_versions} />
          <StatsList title="Categories" data={stats.categories} />
        </div>
      </div>
    </main>
  );
}
