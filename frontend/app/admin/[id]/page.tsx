"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { getSubmission, diagnoseSubmission } from "@/lib/api";
import type { Submission, DiagnosisResult, RedactionReport } from "@/types/diagnosis";
import Card from "@/components/ui/Card";
import SeverityBadge from "@/components/ui/SeverityBadge";
import ErrorBanner from "@/components/ui/ErrorBanner";

const STATUS_COLORS: Record<string, string> = {
  pending: "bg-yellow-900 text-yellow-200",
  diagnosed: "bg-green-900 text-green-200",
  reviewed: "bg-blue-900 text-blue-200",
};

export default function AdminSubmissionPage() {
  const params = useParams<{ id: string }>();
  const subId = params.id;

  const [submission, setSubmission] = useState<Submission | null>(null);
  const [loading, setLoading] = useState(true);
  const [diagnosing, setDiagnosing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!subId) return;
    getSubmission(subId)
      .then(setSubmission)
      .catch((err) =>
        setError(
          err instanceof Error ? err.message : "Failed to load submission."
        )
      )
      .finally(() => setLoading(false));
  }, [subId]);

  async function runDiagnosis() {
    if (!subId) return;
    setDiagnosing(true);
    setError(null);
    try {
      const result = await diagnoseSubmission(subId);
      setSubmission((prev) =>
        prev ? { ...prev, diagnosis: result, status: "diagnosed" } : prev
      );
    } catch (err) {
      setError(
        err instanceof Error
          ? `Diagnosis failed: ${err.message}`
          : "Diagnosis failed. Is the backend running?"
      );
    } finally {
      setDiagnosing(false);
    }
  }

  if (loading) {
    return (
      <main className="min-h-screen bg-zinc-950 p-8 text-white">
        <p className="text-zinc-400">Loading submission...</p>
      </main>
    );
  }

  if (!submission && !error) {
    return (
      <main className="min-h-screen bg-zinc-950 p-8 text-white">
        <p className="text-zinc-400">Submission not found.</p>
      </main>
    );
  }

  const diag: DiagnosisResult | undefined = submission?.diagnosis;
  const redaction: RedactionReport | undefined = submission?.redaction;

  return (
    <main className="min-h-screen bg-zinc-950 p-8 text-white">
      <div className="mx-auto max-w-5xl space-y-6">
        <div>
          <p className="mb-1 text-sm font-semibold uppercase tracking-wide text-blue-400">
            Admin — Submission #{submission?.id}
          </p>
          <h1 className="mb-1 text-3xl font-bold">
            {submission?.filename || "Unnamed log"}
          </h1>
          <p className="text-sm text-zinc-500">
            Submitted{" "}
            {submission?.submitted_at?.slice(0, 16).replace("T", " ")} UTC ·
            IP hash:{" "}
            <code className="font-mono">{submission?.ip_hash}</code>
          </p>
          <a
            href="/admin"
            className="mt-3 inline-block text-sm text-blue-400 hover:text-blue-300"
          >
            ← All submissions
          </a>
        </div>

        {error && (
          <ErrorBanner message={error} onDismiss={() => setError(null)} />
        )}

        {submission && (
          <Card>
            <div className="flex items-start justify-between gap-4">
              <div>
                <h2 className="text-lg font-semibold">Submission Details</h2>
                {submission.note ? (
                  <p className="mt-2 text-zinc-300">{submission.note}</p>
                ) : (
                  <p className="mt-2 italic text-zinc-600">No note provided.</p>
                )}
              </div>
              <span
                className={`shrink-0 rounded px-2 py-1 text-xs font-semibold ${
                  STATUS_COLORS[submission.status] ??
                  "bg-zinc-800 text-zinc-400"
                }`}
              >
                {submission.status}
              </span>
            </div>

            {!diag && (
              <div className="mt-5">
                <button
                  onClick={runDiagnosis}
                  disabled={diagnosing}
                  className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-bold hover:bg-blue-500 disabled:bg-zinc-700 disabled:text-zinc-400"
                >
                  {diagnosing ? "Running diagnosis..." : "Run Diagnosis"}
                </button>
              </div>
            )}
          </Card>
        )}

        {redaction && (
          <Card>
            <h2 className="mb-3 text-base font-semibold">
              Privacy Redaction{" "}
              {redaction.was_redacted ? (
                <span className="ml-2 rounded-full bg-blue-900 px-2 py-0.5 text-xs font-semibold text-blue-200">
                  {redaction.total_redactions} removed
                </span>
              ) : (
                <span className="ml-2 rounded-full bg-zinc-800 px-2 py-0.5 text-xs text-zinc-400">
                  nothing detected
                </span>
              )}
            </h2>
            {redaction.was_redacted ? (
              <div className="space-y-1.5">
                {Object.entries(redaction.by_category).map(([cat, info]) => (
                  <div
                    key={cat}
                    className="flex items-start justify-between gap-3 rounded border border-zinc-800 bg-zinc-950 px-3 py-2 text-xs"
                  >
                    <div>
                      <span className="font-mono text-zinc-300">{cat}</span>
                      <span className="ml-2 text-zinc-500">{info.reason}</span>
                    </div>
                    <span className="shrink-0 font-semibold text-zinc-400">
                      ×{info.count}
                    </span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-sm text-zinc-500">
                No sensitive patterns detected.
              </p>
            )}
          </Card>
        )}

        {diag && (
          <Card>
            <h2 className="mb-4 text-xl font-bold">Diagnosis Result</h2>

            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-2 text-sm">
                <p>
                  <strong>Source:</strong>{" "}
                  {diag.ai_used
                    ? "AI Analysis"
                    : diag.used_known_issue
                      ? "Known Issue Match"
                      : "Deterministic Engine"}
                </p>
                <p className="flex items-center gap-2">
                  <strong>Severity:</strong>
                  <SeverityBadge severity={diag.severity} />
                </p>
                <p>
                  <strong>Confidence:</strong>{" "}
                  {diag.parsed?.primary_fingerprint != null
                    ? `${diag.parsed.primary_fingerprint.confidence}%`
                    : diag.confidence}
                </p>
                {diag.version && (
                  <p>
                    <strong>ProtonFix:</strong> v{diag.version}
                  </p>
                )}
              </div>

              <div>
                <p className="mb-1 text-sm font-semibold text-zinc-400">
                  Probable Cause
                </p>
                <p className="text-sm text-zinc-300">{diag.probable_cause}</p>
              </div>
            </div>

            <div className="mt-4">
              <p className="mb-1 text-sm font-semibold text-zinc-400">
                Summary
              </p>
              <p className="text-sm text-zinc-300">{diag.summary}</p>
            </div>

            {diag.fix_steps.length > 0 && (
              <div className="mt-4">
                <p className="mb-2 text-sm font-semibold">Fix Steps</p>
                <ol className="ml-5 list-decimal space-y-1 text-sm text-zinc-300">
                  {diag.fix_steps.map((s, i) => (
                    <li key={i}>{s}</li>
                  ))}
                </ol>
              </div>
            )}

            {diag.warnings.length > 0 && (
              <div className="mt-4">
                <p className="mb-2 text-sm font-semibold text-yellow-400">
                  Warnings
                </p>
                <ul className="ml-5 list-disc space-y-1 text-sm text-zinc-300">
                  {diag.warnings.map((w, i) => (
                    <li key={i}>{w}</li>
                  ))}
                </ul>
              </div>
            )}
          </Card>
        )}

        {submission?.log_text && (
          <Card>
            <div className="mb-3 flex items-center justify-between">
              <h2 className="text-lg font-semibold">Log Content</h2>
              <span className="text-xs text-zinc-500">
                {submission.log_text.length.toLocaleString()} chars
              </span>
            </div>
            <pre className="max-h-96 overflow-y-auto rounded bg-black p-4 text-xs text-zinc-300 whitespace-pre-wrap break-words">
              {submission.log_text}
            </pre>
          </Card>
        )}
      </div>
    </main>
  );
}
