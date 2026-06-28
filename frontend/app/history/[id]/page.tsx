"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { getHistoryEntry } from "@/lib/api";

type Result = any;

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

function humanizeFingerprint(fingerprint: string) {
  const names: Record<string, string> = {
    VULKAN_DRIVER_MISSING: "Missing or Broken Vulkan Driver",
    VULKAN_INIT_FAILURE: "Vulkan Initialization Failure",
    DXVK_ADAPTER_FAILURE: "DXVK Graphics Adapter Failure",
    WINE_CRASH: "Wine Crash",
  };

  return names[fingerprint] || fingerprint.replaceAll("_", " ");
}

export default function HistoryDetailPage() {
  const params = useParams<{ id: string }>();
  const diagnosisId = params.id;

  const [result, setResult] = useState<Result | null>(null);
  const [loading, setLoading] = useState(true);
  const [copied, setCopied] = useState<string | null>(null);

  async function copyText(text: string, label: string) {
    await navigator.clipboard.writeText(text);
    setCopied(label);

    setTimeout(() => {
      setCopied(null);
    }, 1500);
  }

  useEffect(() => {
    async function loadDiagnosis() {
      try {
        const data = await getHistoryEntry(diagnosisId);
        setResult(data);
      } catch (error) {
        console.error(error);
        setResult(null);
      }

      setLoading(false);
    }

    if (diagnosisId) {
      loadDiagnosis();
    }
  }, [diagnosisId]);

  if (loading) {
    return (
      <main className="min-h-screen bg-zinc-950 p-8 text-white">
        Loading diagnosis...
      </main>
    );
  }

  if (!result) {
    return (
      <main className="min-h-screen bg-zinc-950 p-8 text-white">
        Diagnosis not found.
      </main>
    );
  }

  const primaryFingerprint = result?.parsed?.primary_fingerprint;

  return (
    <main className="min-h-screen bg-zinc-950 p-8 text-white">
      <div className="mx-auto max-w-6xl">
        <div className="mb-8">
          <p className="mb-2 text-sm font-semibold uppercase tracking-wide text-blue-400">
            ProtonFix AI
          </p>

          <h1 className="mb-3 text-4xl font-bold">Saved Diagnosis</h1>

          <p className="max-w-3xl text-zinc-400">
            Full saved report from diagnosis history.
          </p>

          <div className="mt-4 flex gap-3">
            <a
              href="/"
              className="rounded bg-zinc-800 px-3 py-2 text-sm font-semibold hover:bg-zinc-700"
            >
              Analyze
            </a>

            <a
              href="/history"
              className="rounded bg-zinc-800 px-3 py-2 text-sm font-semibold hover:bg-zinc-700"
            >
              History
            </a>

            <a
              href="/stats"
              className="rounded bg-zinc-800 px-3 py-2 text-sm font-semibold hover:bg-zinc-700"
            >
              Stats
            </a>
          </div>
        </div>

        <div className="space-y-6 rounded-xl border border-zinc-800 bg-zinc-900 p-6">
          <div>
            <h2 className="mb-4 text-2xl font-bold">Diagnosis</h2>

            <div className="grid gap-4 md:grid-cols-2">
              <div className="rounded-lg border border-zinc-800 bg-zinc-950 p-4">
                <p>
                  <strong>File:</strong> {result.filename || "Unknown"}
                </p>

                <p className="mt-2">
                  <strong>Characters:</strong> {result.characters || "N/A"}
                </p>

                <p className="mt-2">
                  <strong>Game:</strong> {result.parsed?.game || "Unknown"}
                </p>

                <p className="mt-2">
                  <strong>AppID:</strong> {result.parsed?.appid || "Unknown"}
                </p>

                <p className="mt-2">
                  <strong>Proton:</strong>{" "}
                  {result.parsed?.proton_version || "Unknown"}
                </p>

                <p className="mt-2">
                  <strong>Confidence:</strong> {result.confidence}
                </p>

                <p className="mt-2 flex items-center gap-2">
                  <strong>Severity:</strong> {getSeverityBadge(result.severity)}
                </p>

                <p className="mt-2">
                  <strong>Diagnosis Source:</strong>{" "}
                  {result.used_known_issue
                    ? `Known Issue Engine (${result.known_issue_id})`
                    : "AI Analysis"}
                </p>
              </div>

              <div className="rounded-lg border border-zinc-800 bg-zinc-950 p-4">
                <p>
                  <strong>Probable Cause:</strong>
                </p>

                <p className="mt-2 text-zinc-300">{result.probable_cause}</p>
              </div>
            </div>

            <div className="mt-4 rounded-lg border border-zinc-800 bg-zinc-950 p-4">
              <p>
                <strong>Summary:</strong>
              </p>

              <p className="mt-2 text-zinc-300">{result.summary}</p>
            </div>

            {primaryFingerprint && (
              <div className="mt-4 rounded-lg border border-blue-700 bg-zinc-950 p-4">
                <p className="mb-2 text-sm font-semibold uppercase tracking-wide text-blue-400">
                  Primary Cause
                </p>

                <h3 className="text-2xl font-bold">
                  {humanizeFingerprint(primaryFingerprint.fingerprint)}
                </h3>

                <p className="mt-1 text-xs text-zinc-500">
                  {primaryFingerprint.fingerprint}
                </p>

                <div className="mt-3 flex flex-wrap gap-2">
                  {getSeverityBadge(primaryFingerprint.severity)}
                  {getConfidenceBadge(primaryFingerprint.confidence)}
                </div>

                <p className="mt-3 text-zinc-300">
                  {primaryFingerprint.explanation}
                </p>

                <p className="mt-3 text-sm text-zinc-400">
                  Category: {primaryFingerprint.category}
                </p>
              </div>
            )}
          </div>

          <div>
            <h3 className="mb-3 text-xl font-bold">Known Issues Found</h3>

            <div className="grid gap-4 md:grid-cols-2">
              {result.parsed?.fingerprints?.length > 0 ? (
                result.parsed.fingerprints.map((item: any, index: number) => {
                  const commandText = item.safe_commands?.join("\n") || "";

                  return (
                    <div
                      key={index}
                      className="h-fit rounded-lg border border-zinc-700 bg-zinc-950 p-4"
                    >
                      <div className="mb-2 flex items-start justify-between gap-2">
                        <div>
                          <h4 className="text-lg font-bold">
                            {humanizeFingerprint(item.fingerprint)}
                          </h4>

                          <p className="text-xs text-zinc-500">
                            {item.fingerprint}
                          </p>

                          <div className="mt-2">
                            {getConfidenceBadge(item.confidence)}
                          </div>
                        </div>

                        {getSeverityBadge(item.severity)}
                      </div>

                      <p className="text-sm text-zinc-400">{item.category}</p>

                      <p className="mt-3 text-zinc-300">{item.explanation}</p>

                      <div className="mt-4">
                        <strong>Known Fixes:</strong>

                        <ul className="mt-2 ml-6 list-disc text-zinc-300">
                          {item.known_fix?.map(
                            (fix: string, fixIndex: number) => (
                              <li key={fixIndex}>{fix}</li>
                            )
                          )}
                        </ul>
                      </div>

                      {item.safe_commands?.length > 0 && (
                        <div className="mt-4">
                          <div className="mb-2 flex items-center justify-between gap-2">
                            <strong>Commands:</strong>

                            <button
                              onClick={() =>
                                copyText(commandText, `issue-${index}`)
                              }
                              className="rounded bg-zinc-800 px-3 py-1 text-xs font-semibold hover:bg-zinc-700"
                            >
                              {copied === `issue-${index}`
                                ? "Copied"
                                : "Copy Commands"}
                            </button>
                          </div>

                          <pre className="overflow-x-auto rounded bg-black p-3 text-xs">
                            {commandText}
                          </pre>
                        </div>
                      )}
                    </div>
                  );
                })
              ) : (
                <p className="text-zinc-400">
                  No known issue fingerprints were detected.
                </p>
              )}
            </div>
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            <div className="rounded-lg border border-zinc-800 bg-zinc-950 p-4">
              <h3 className="mb-3 text-xl font-bold">Detected Errors</h3>

              {result.detected_errors?.length > 0 ? (
                <ul className="ml-6 list-disc text-zinc-300">
                  {result.detected_errors.map((item: string, index: number) => (
                    <li key={index}>{item}</li>
                  ))}
                </ul>
              ) : (
                <p className="text-zinc-400">No errors detected.</p>
              )}
            </div>

            <div className="rounded-lg border border-zinc-800 bg-zinc-950 p-4">
              <h3 className="mb-3 text-xl font-bold">Extra Info Needed</h3>

              {result.extra_info_needed?.length > 0 ? (
                <ul className="ml-6 list-disc text-zinc-300">
                  {result.extra_info_needed.map(
                    (item: string, index: number) => (
                      <li key={index}>{item}</li>
                    )
                  )}
                </ul>
              ) : (
                <p className="text-zinc-400">No extra info needed.</p>
              )}
            </div>
          </div>

          <div className="rounded-lg border border-zinc-800 bg-zinc-950 p-4">
            <h3 className="mb-3 text-xl font-bold">Fix Steps</h3>

            {result.fix_steps?.length > 0 ? (
              <ol className="ml-6 list-decimal text-zinc-300">
                {result.fix_steps.map((item: string, index: number) => (
                  <li key={index}>{item}</li>
                ))}
              </ol>
            ) : (
              <p className="text-zinc-400">No fix steps returned.</p>
            )}
          </div>

          <div className="rounded-lg border border-zinc-800 bg-zinc-950 p-4">
            <div className="mb-3 flex items-center justify-between gap-2">
              <h3 className="text-xl font-bold">Recommended Commands</h3>

              {result.recommended_commands?.length > 0 && (
                <button
                  onClick={() =>
                    copyText(
                      result.recommended_commands.join("\n"),
                      "main-commands"
                    )
                  }
                  className="rounded bg-zinc-800 px-3 py-1 text-sm font-semibold hover:bg-zinc-700"
                >
                  {copied === "main-commands" ? "Copied" : "Copy Commands"}
                </button>
              )}
            </div>

            {result.recommended_commands?.length > 0 ? (
              <pre className="overflow-x-auto rounded-lg bg-black p-4 text-sm">
                {result.recommended_commands.join("\n")}
              </pre>
            ) : (
              <p className="text-zinc-400">No commands recommended.</p>
            )}
          </div>

          <div className="rounded-lg border border-zinc-800 bg-zinc-950 p-4">
            <h3 className="mb-3 text-xl font-bold">Warnings</h3>

            {result.warnings?.length > 0 ? (
              <ul className="ml-6 list-disc text-zinc-300">
                {result.warnings.map((item: string, index: number) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            ) : (
              <p className="text-zinc-400">No warnings found.</p>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
