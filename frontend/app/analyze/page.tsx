"use client";

import { useEffect, useState } from "react";

import { analyzeLog as analyzeLogApi, getStats, getHistory } from "@/lib/api";
import type { DiagnosisResult, Stats, HistoryEntry } from "@/types/diagnosis";
import DependencyChainCard from "@/components/diagnosis/DependencyChainCard";
import Dashboard from "@/components/dashboard/Dashboard";
import DiagnosisSummary from "@/components/diagnosis/DiagnosisSummary";
import ExportButton from "@/components/diagnosis/ExportButton";
import FingerprintList from "@/components/diagnosis/FingerprintList";
import PrimaryCauseCard from "@/components/diagnosis/PrimaryCauseCard";
import ErrorInfoGrid from "@/components/diagnosis/ErrorInfoGrid";
import FixStepsCard from "@/components/diagnosis/FixStepsCard";
import RecommendedCommandsCard from "@/components/diagnosis/RecommendedCommandsCard";
import WarningsCard from "@/components/diagnosis/WarningsCard";
import ErrorBanner from "@/components/ui/ErrorBanner";

const MAX_FILE_BYTES = 10 * 1024 * 1024; // 10 MB

function LoadingSkeleton() {
  return (
    <div className="animate-pulse space-y-6 rounded-xl border border-zinc-800 bg-zinc-900 p-6">
      <div className="flex items-center justify-between">
        <div className="h-7 w-36 rounded bg-zinc-800" />
        <div className="h-6 w-48 rounded-lg bg-zinc-800" />
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        <div className="h-32 rounded-lg bg-zinc-800" />
        <div className="h-32 rounded-lg bg-zinc-800" />
      </div>
      <div className="h-20 rounded-lg bg-zinc-800" />
      <div className="h-28 rounded-lg bg-zinc-800" />
      <div className="h-16 rounded-lg bg-zinc-800" />
    </div>
  );
}

export default function AnalyzePage() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<DiagnosisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [dragOver, setDragOver] = useState(false);
  const [copied, setCopied] = useState<string | null>(null);
  const [stats, setStats] = useState<Stats | null>(null);
  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const [dashboardLoading, setDashboardLoading] = useState(true);

  useEffect(() => {
    Promise.all([getStats(), getHistory()])
      .then(([s, h]) => {
        setStats(s);
        setHistory(Array.isArray(h) ? h : []);
      })
      .catch((err) => console.error("Dashboard load failed:", err))
      .finally(() => setDashboardLoading(false));
  }, []);

  function validateAndSetFile(f: File) {
    if (f.size > MAX_FILE_BYTES) {
      setError(`File too large (${(f.size / 1024 / 1024).toFixed(1)} MB). Maximum is 10 MB.`);
      return;
    }
    setError(null);
    setFile(f);
  }

  function handleDragOver(e: React.DragEvent) {
    e.preventDefault();
    setDragOver(true);
  }

  function handleDragLeave() {
    setDragOver(false);
  }

  function handleDrop(e: React.DragEvent) {
    e.preventDefault();
    setDragOver(false);
    const dropped = e.dataTransfer.files[0];
    if (dropped) validateAndSetFile(dropped);
  }

  async function copyText(text: string, label: string) {
    await navigator.clipboard.writeText(text);
    setCopied(label);
    setTimeout(() => setCopied(null), 1500);
  }

  async function handleAnalyzeLog() {
    if (!file) return;
    setLoading(true);
    setResult(null);
    setError(null);
    try {
      const data = await analyzeLogApi(file);
      setResult(data);
    } catch (err) {
      const msg =
        err instanceof Error ? err.message : "Unknown error";
      setError(
        `Analysis failed: ${msg}. Make sure the backend is running on port 8000.`
      );
    } finally {
      setLoading(false);
    }
  }

  const primaryFingerprint = result?.parsed?.primary_fingerprint;

  return (
    <main className="min-h-screen bg-zinc-950 p-8 text-white">
      <div className="mx-auto max-w-6xl">
        {/* Hero */}
        <div className="mb-8 grid gap-6 lg:grid-cols-[1.4fr_0.6fr]">
          <div className="rounded-2xl border border-zinc-800 bg-gradient-to-br from-zinc-900 to-zinc-950 p-6">
            <p className="mb-2 text-sm font-semibold uppercase tracking-wide text-blue-400">
              Linux Gaming Troubleshooter
            </p>
            <h1 className="mb-3 text-4xl font-bold">Diagnose Proton logs fast.</h1>
            <p className="max-w-3xl text-zinc-400">
              Upload a Steam, Proton, Wine, DXVK, VKD3D, Vulkan, or Gamescope log.
              ProtonFix checks known Linux gaming failures first, then only uses AI
              when no deterministic fix is found.
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

        {/* Upload */}
        <div className="mb-6 rounded-2xl border border-zinc-800 bg-zinc-900 p-6">
          {error && (
            <div className="mb-4">
              <ErrorBanner message={error} onDismiss={() => setError(null)} />
            </div>
          )}

          <div className="grid gap-6 lg:grid-cols-[1fr_auto] lg:items-start">
            <div>
              <p className="mb-2 text-xl font-bold">Upload Log File</p>
              <p className="mb-4 max-w-2xl text-sm text-zinc-400">
                Drop in a Steam, Proton, Wine, DXVK, VKD3D, Vulkan, Gamescope, or
                GameMode log. Max 10 MB.
              </p>

              <label
                className={`block cursor-pointer rounded-xl border border-dashed p-6 transition ${
                  dragOver
                    ? "border-blue-500 bg-blue-950/20"
                    : "border-zinc-700 bg-zinc-950 hover:border-blue-600 hover:bg-zinc-900"
                }`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
              >
                <input
                  type="file"
                  accept=".txt,.log"
                  onChange={(e) => {
                    const f = e.target.files?.[0];
                    if (f) validateAndSetFile(f);
                  }}
                  className="hidden"
                />
                <div className="flex flex-col gap-1">
                  <p className="font-semibold text-zinc-200">
                    {file ? file.name : "Choose or drag a .log or .txt file"}
                  </p>
                  <p className="text-sm text-zinc-500">
                    {file
                      ? `${(file.size / 1024).toFixed(1)} KB — ready to analyze`
                      : "Click to browse, or drag a file here"}
                  </p>
                </div>
              </label>
            </div>

            <div className="flex flex-col gap-3 pt-10">
              <button
                onClick={handleAnalyzeLog}
                disabled={!file || loading}
                className="rounded-xl bg-blue-600 px-6 py-3 text-base font-bold hover:bg-blue-500 disabled:bg-zinc-700 disabled:text-zinc-400"
              >
                {loading ? "Analyzing..." : "Analyze Log"}
              </button>
              <p className="max-w-xs text-xs text-zinc-500">
                Known fixes are checked first. AI is only used as a fallback.
              </p>
            </div>
          </div>
        </div>

        {/* Dashboard */}
        <Dashboard stats={stats} history={history} loading={dashboardLoading} />

        {/* Loading skeleton */}
        {loading && <LoadingSkeleton />}

        {/* Results */}
        {result && !loading && (
          <div className="space-y-6 rounded-xl border border-zinc-800 bg-zinc-900 p-6">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <span className="text-xs text-zinc-500">
                Diagnosis #{result.history_id ?? "—"}
              </span>
              <ExportButton result={result} />
            </div>

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

            <WarningsCard warnings={result.warnings} />
          </div>
        )}
      </div>
    </main>
  );
}
