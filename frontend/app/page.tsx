"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { analyzeLog as analyzeLogApi, getStats, getHistory, } from "@/lib/api";
import type { DiagnosisResult, Stats, HistoryEntry, } from "@/types/diagnosis";
import DependencyChainCard from "@/components/diagnosis/DependencyChainCard";
import Card from "@/components/ui/Card";
import StatCard from "@/components/ui/StatCard";
import SeverityBadge from "@/components/ui/SeverityBadge";
import ConfidenceBadge from "@/components/ui/ConfidenceBadge";
import Dashboard from "@/components/dashboard/Dashboard";
import { humanizeFingerprint } from "@/lib/fingerprints";
import DiagnosisSummary from "@/components/diagnosis/DiagnosisSummary";
import FingerprintList from "@/components/diagnosis/FingerprintList";
import PrimaryCauseCard from "@/components/diagnosis/PrimaryCauseCard";
import ErrorInfoGrid from "@/components/diagnosis/ErrorInfoGrid";
import FixStepsCard from "@/components/diagnosis/FixStepsCard";
import RecommendedCommandsCard from "@/components/diagnosis/RecommendedCommandsCard";
import WarningsCard from "@/components/diagnosis/WarningsCard";

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

function getConfidenceBadge(confidence: number | undefined) {
  if (!confidence) return null;

  return (
    <span className="rounded bg-blue-900 px-2 py-1 text-xs font-bold text-blue-200">
      {confidence}% confidence
    </span>
  );
}

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<DiagnosisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState<string | null>(null);
  const [stats, setStats] = useState<Stats | null>(null);
  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const [dashboardLoading, setDashboardLoading] = useState(true);

  useEffect(() => {
    async function loadDashboardData() {
      try {
        const [statsData, historyData] = await Promise.all([
          getStats(),
                                                           getHistory(),
        ]);

        setStats(statsData);
        setHistory(Array.isArray(historyData) ? historyData : []);
      } catch (err) {
        console.error("Failed to load dashboard data:", err);
      } finally {
        setDashboardLoading(false);
      }
    }

    loadDashboardData();
  }, []);

  async function copyText(text: string, label: string) {
    await navigator.clipboard.writeText(text);
    setCopied(label);

    setTimeout(() => {
      setCopied(null);
    }, 1500);
  }

  async function handleAnalyzeLog() {
    if (!file) return;

    setLoading(true);
    setResult(null);

    try {
      const data = await analyzeLogApi(file);
      setResult(data);
    } catch (error) {
      setResult({
        filename: file.name,
        characters: 0,

        summary: "The frontend could not reach the backend server.",
        probable_cause:
        "The FastAPI backend may not be running, or CORS may be misconfigured.",

        confidence: "high",
        severity: "high",

        used_known_issue: false,
        known_issue_id: undefined,

        detected_errors: ["Failed to fetch backend response."],

        fix_steps: [
          "Make sure the backend server is running.",
          "Open http://127.0.0.1:8000 in your browser and confirm it loads.",
          "Restart the backend with: python -m uvicorn main:app --reload",
        ],

        recommended_commands: [
          "cd ~/protonfix-ai/backend",
          "source .venv/bin/activate.fish",
          "python -m uvicorn main:app --reload",
        ],

        extra_info_needed: [],
        warnings: [],

        parsed: {
          game: null,
          appid: null,
          proton_version: null,
          dxvk_version: null,
          vkd3d_version: null,
          gpu: null,
          errors: [],
          fingerprints: [],
          primary_fingerprint: null,
        },

        known_issue: null,
        ai_used: false,
        ai_result: null,
      });
    } finally {
      setLoading(false);
    }
  }

  const primaryFingerprint = result?.parsed?.primary_fingerprint;

  return (
    <main className="min-h-screen bg-zinc-950 p-8 text-white">
      <div className="mx-auto max-w-6xl">
        <div className="mb-8 grid gap-6 lg:grid-cols-[1.4fr_0.6fr]">
          <div className="rounded-2xl border border-zinc-800 bg-gradient-to-br from-zinc-900 to-zinc-950 p-6">
            <p className="mb-2 text-sm font-semibold uppercase tracking-wide text-blue-400">
              Linux Gaming Troubleshooter
            </p>

            <h1 className="mb-3 text-4xl font-bold">
              Diagnose Proton logs fast.
            </h1>

            <p className="max-w-3xl text-zinc-400">
              Upload a Steam, Proton, Wine, DXVK, VKD3D, Vulkan, or Gamescope
              log. ProtonFix checks known Linux gaming failures first, then only
              uses AI when no deterministic fix is found.
            </p>

            <div className="mt-5 flex flex-wrap gap-2 text-sm">
              <span className="rounded-full border border-blue-800 bg-blue-950 px-3 py-1 text-blue-200">
                Fingerprint-first
              </span>

              <span className="rounded-full border border-zinc-700 bg-zinc-900 px-3 py-1 text-zinc-300">
                Low API cost
              </span>

              <span className="rounded-full border border-zinc-700 bg-zinc-900 px-3 py-1 text-zinc-300">
                AI fallback
              </span>

              <span className="rounded-full border border-zinc-700 bg-zinc-900 px-3 py-1 text-zinc-300">
                SQLite history
              </span>
            </div>
          </div>

          <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-6">
            <p className="text-sm font-semibold uppercase tracking-wide text-zinc-500">
              Current Build
            </p>

            <p className="mt-2 text-3xl font-bold text-white">v0.7</p>

            <div className="mt-4 space-y-2 text-sm text-zinc-400">
              <p>✓ 71 fingerprints</p>
              <p>✓ Confidence scoring</p>
              <p>✓ Primary cause ranking</p>
              <p>✓ Diagnosis history</p>
            </div>
          </div>
        </div>

        <div className="mb-6 rounded-2xl border border-zinc-800 bg-zinc-900 p-6">
          <div className="grid gap-6 lg:grid-cols-[1fr_auto] lg:items-center">
            <div>
              <p className="mb-2 text-xl font-bold">Upload Log File</p>

              <p className="mb-4 max-w-2xl text-sm text-zinc-400">
                Drop in a Steam, Proton, Wine, DXVK, VKD3D, Vulkan, Gamescope,
                or GameMode log. ProtonFix will save it, parse it, fingerprint
                it, and generate a diagnosis.
              </p>

              <label className="block cursor-pointer rounded-xl border border-dashed border-zinc-700 bg-zinc-950 p-6 transition hover:border-blue-600 hover:bg-zinc-900">
                <input
                  type="file"
                  accept=".txt,.log"
                  onChange={(e) => setFile(e.target.files?.[0] || null)}
                  className="hidden"
                />

                <div className="flex flex-col gap-2">
                  <p className="font-semibold text-zinc-200">
                    {file ? file.name : "Choose a .log or .txt file"}
                  </p>

                  <p className="text-sm text-zinc-500">
                    {file
                      ? "Ready to analyze."
                      : "Click here to select a log file from your system."}
                  </p>
                </div>
              </label>
            </div>

            <div className="flex flex-col gap-3">
              <button
                onClick={handleAnalyzeLog}
                disabled={!file || loading}
                className="rounded-xl bg-blue-600 px-6 py-3 text-base font-bold hover:bg-blue-500 disabled:bg-zinc-700 disabled:text-zinc-400"
              >
                {loading ? "Analyzing..." : "Analyze Log"}
              </button>

              <p className="max-w-xs text-xs text-zinc-500">
                Known fixes are checked first. AI is only used if no known issue
                matches.
              </p>
            </div>
          </div>
        </div>

        <Dashboard
          stats={stats}
          history={history}
          loading={dashboardLoading}
        />

        {result && (
          <div className="space-y-6 rounded-xl border border-zinc-800 bg-zinc-900 p-6">

            <DiagnosisSummary result={result} />

            <PrimaryCauseCard fingerprint={primaryFingerprint} />

            <DependencyChainCard
              chain={result.dependency_chain}
              fingerprints={result.parsed.fingerprints}
            />

            <FingerprintList
              fingerprints={result.parsed?.fingerprints || []}
              copied={copied}
              onCopy={copyText}
            />

            <ErrorInfoGrid
              errors={result.detected_errors}
              extraInfo={result.extra_info_needed}
            />

            <FixStepsCard steps={result.fix_steps} />

            <RecommendedCommandsCard
              commands={result.recommended_commands}
              copied={copied}
              onCopy={copyText}
            />

            <WarningsCard
              warnings={result.warnings}
            />
          </div>
        )}
      </div>
    </main>
  );
}
