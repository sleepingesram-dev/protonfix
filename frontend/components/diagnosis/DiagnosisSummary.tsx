import SeverityBadge from "@/components/ui/SeverityBadge";
import { humanizeFingerprint } from "@/lib/fingerprints";
import type { DiagnosisResult } from "@/types/diagnosis";

type DiagnosisSummaryProps = {
  result: DiagnosisResult;
};

export default function DiagnosisSummary({ result }: DiagnosisSummaryProps) {
  const aiUsed = result.ai_used;
  const knownIssue = result.used_known_issue;
  const primaryFp = result.parsed?.primary_fingerprint;

  const sourceLabel = knownIssue
    ? `Known Issue (${humanizeFingerprint(result.known_issue_id) ?? result.known_issue_id})`
    : aiUsed
      ? "AI Analysis"
      : "Deterministic Engine";

  const sourceBadge = aiUsed
    ? "border-purple-700 bg-purple-950/60 text-purple-300"
    : knownIssue
      ? "border-green-700 bg-green-950/60 text-green-300"
      : "border-blue-700 bg-blue-950/60 text-blue-300";

  return (
    <div>
      <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
        <h2 className="text-2xl font-bold">Diagnosis</h2>
        <span className={`rounded-lg border px-3 py-1 text-sm font-semibold ${sourceBadge}`}>
          {aiUsed ? "AI" : "⚡"} {sourceLabel}
        </span>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <div className="space-y-2 rounded-lg border border-zinc-800 bg-zinc-950 p-4 text-sm">
          <p>
            <strong>File:</strong> {result.filename || "Unknown"}
          </p>
          <p>
            <strong>Size:</strong> {result.characters?.toLocaleString()} chars
          </p>
          {result.version && (
            <p>
              <strong>ProtonFix:</strong> v{result.version}
            </p>
          )}
          <p className="flex items-center gap-2">
            <strong>Severity:</strong>
            <SeverityBadge severity={result.severity} />
          </p>
          <p>
            <strong>Confidence:</strong>{" "}
            {primaryFp != null ? `${primaryFp.confidence}%` : result.confidence}
          </p>
        </div>

        <div className="rounded-lg border border-zinc-800 bg-zinc-950 p-4">
          <p className="mb-2 text-sm font-semibold text-zinc-400">Probable Cause</p>
          <p className="text-zinc-300">{result.probable_cause}</p>
        </div>
      </div>

      <div className="mt-4 rounded-lg border border-zinc-800 bg-zinc-950 p-4">
        <p className="mb-2 text-sm font-semibold text-zinc-400">Summary</p>
        <p className="text-zinc-300">{result.summary}</p>
      </div>
    </div>
  );
}
