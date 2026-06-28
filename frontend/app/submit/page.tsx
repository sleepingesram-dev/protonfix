"use client";

import { useState } from "react";
import { submitLog } from "@/lib/api";
import type { RedactionReport } from "@/types/diagnosis";
import ErrorBanner from "@/components/ui/ErrorBanner";

const MAX_FILE_BYTES = 10 * 1024 * 1024;

export default function SubmitPage() {
  const [file, setFile] = useState<File | null>(null);
  const [note, setNote] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [submissionId, setSubmissionId] = useState<number | null>(null);
  const [redaction, setRedaction] = useState<RedactionReport | null>(null);

  function handleFile(f: File) {
    if (f.size > MAX_FILE_BYTES) {
      setError(
        `File too large (${(f.size / 1024 / 1024).toFixed(1)} MB). Maximum is 10 MB.`
      );
      return;
    }
    setError(null);
    setFile(f);
  }

  async function handleSubmit() {
    if (!file) return;
    setLoading(true);
    setError(null);
    try {
      const res = await submitLog(file, note);
      setSubmissionId(res.submission_id);
      setRedaction(res.redaction ?? null);
      setFile(null);
      setNote("");
    } catch (err) {
      setError(
        err instanceof Error
          ? `Submit failed: ${err.message}`
          : "Submit failed. Is the backend running?"
      );
    } finally {
      setLoading(false);
    }
  }

  if (submissionId !== null) {
    const categories = redaction
      ? Object.entries(redaction.by_category)
      : [];

    return (
      <main className="min-h-screen bg-zinc-950 p-8 text-white">
        <div className="mx-auto max-w-2xl space-y-4">
          <div className="rounded-xl border border-green-700 bg-green-950/30 p-8 text-center">
            <div className="mb-3 text-4xl">✓</div>
            <h1 className="mb-2 text-2xl font-bold text-green-300">
              Log Submitted
            </h1>
            <p className="mb-4 text-zinc-400">
              Anonymously submitted for review.
            </p>
            <p className="font-mono text-sm text-zinc-300">
              Submission ID:{" "}
              <strong className="text-white">#{submissionId}</strong>
            </p>
          </div>

          {redaction && (
            <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-5">
              <h2 className="mb-3 text-sm font-semibold text-zinc-300">
                Privacy Redaction Report
              </h2>
              {redaction.was_redacted ? (
                <>
                  <p className="mb-3 text-sm text-zinc-400">
                    {redaction.total_redactions} item
                    {redaction.total_redactions !== 1 ? "s" : ""} removed
                    across {categories.length} categor
                    {categories.length !== 1 ? "ies" : "y"} before storage.
                    Diagnostic path structure is preserved.
                  </p>
                  <div className="space-y-2">
                    {categories.map(([cat, info]) => (
                      <div
                        key={cat}
                        className="rounded-lg border border-zinc-700 bg-zinc-950 px-4 py-2"
                      >
                        <div className="flex items-center justify-between gap-3">
                          <span className="font-mono text-xs text-zinc-400">
                            {cat}
                          </span>
                          <span className="shrink-0 rounded-full bg-zinc-800 px-2 py-0.5 text-xs font-semibold text-zinc-300">
                            ×{info.count}
                          </span>
                        </div>
                        <p className="mt-1 text-xs text-zinc-500">
                          {info.reason}
                        </p>
                      </div>
                    ))}
                  </div>
                </>
              ) : (
                <p className="text-sm text-zinc-500">
                  No sensitive patterns detected in this log.
                </p>
              )}
            </div>
          )}

          <div className="text-center">
            <button
              onClick={() => {
                setSubmissionId(null);
                setRedaction(null);
              }}
              className="rounded-lg bg-zinc-800 px-4 py-2 text-sm font-semibold hover:bg-zinc-700"
            >
              Submit Another
            </button>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-zinc-950 p-8 text-white">
      <div className="mx-auto max-w-2xl">
        <p className="mb-2 text-sm font-semibold uppercase tracking-wide text-blue-400">
          ProtonFix
        </p>
        <h1 className="mb-2 text-4xl font-bold">Submit a Log</h1>
        <p className="mb-8 text-zinc-400">
          Submit your log anonymously for the ProtonFix team to review. No
          account required. Your IP address is stored as a short one-way hash
          only.
        </p>

        <div className="space-y-5 rounded-xl border border-zinc-800 bg-zinc-900 p-6">
          {error && (
            <ErrorBanner message={error} onDismiss={() => setError(null)} />
          )}

          <div>
            <label className="mb-2 block text-sm font-semibold text-zinc-300">
              Log File <span className="text-red-400">*</span>
            </label>
            <label className="block cursor-pointer rounded-xl border border-dashed border-zinc-700 bg-zinc-950 p-5 transition hover:border-blue-600">
              <input
                type="file"
                accept=".txt,.log"
                onChange={(e) => {
                  const f = e.target.files?.[0];
                  if (f) handleFile(f);
                }}
                className="hidden"
              />
              <p className="font-semibold text-zinc-200">
                {file ? file.name : "Choose a .log or .txt file"}
              </p>
              <p className="mt-1 text-sm text-zinc-500">
                {file
                  ? `${(file.size / 1024).toFixed(1)} KB`
                  : "Click to browse — max 10 MB"}
              </p>
            </label>
          </div>

          <div>
            <label className="mb-2 block text-sm font-semibold text-zinc-300">
              Note{" "}
              <span className="font-normal text-zinc-500">(optional)</span>
            </label>
            <textarea
              value={note}
              onChange={(e) => setNote(e.target.value)}
              rows={4}
              maxLength={500}
              placeholder="Game name, what you tried, what happened..."
              className="w-full resize-none rounded-lg border border-zinc-700 bg-zinc-950 p-3 text-sm text-zinc-200 placeholder-zinc-600 focus:border-blue-600 focus:outline-none"
            />
            <p className="mt-1 text-right text-xs text-zinc-600">
              {note.length}/500
            </p>
          </div>

          <button
            onClick={handleSubmit}
            disabled={!file || loading}
            className="w-full rounded-xl bg-blue-600 py-3 font-bold hover:bg-blue-500 disabled:bg-zinc-700 disabled:text-zinc-400"
          >
            {loading ? "Submitting..." : "Submit Log Anonymously"}
          </button>
        </div>

        <p className="mt-4 text-center text-xs text-zinc-600">
          Submitted logs are used to improve ProtonFix fingerprint coverage.
          They are reviewed locally and are not shared publicly.
        </p>
      </div>
    </main>
  );
}
