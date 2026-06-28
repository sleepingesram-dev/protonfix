import SeverityBadge from "@/components/ui/SeverityBadge";
import { humanizeFingerprint } from "@/lib/fingerprints";
import type { DiagnosisResult } from "@/types/diagnosis";

type DiagnosisSummaryProps = {
  result: DiagnosisResult;
};

export default function DiagnosisSummary({ result }: DiagnosisSummaryProps) {
  const sourceLabel = result.used_known_issue
    ? `Known Issue Engine (${humanizeFingerprint(result.known_issue_id)})`
    : result.ai_used
      ? "AI Analysis"
      : "Deterministic Engine";

  return (
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
            <strong>Confidence:</strong> {result.confidence}
          </p>

          <p className="mt-2 flex items-center gap-2">
            <strong>Severity:</strong>
            <SeverityBadge severity={result.severity} />
          </p>

          <p className="mt-2">
            <strong>Diagnosis Source:</strong> {sourceLabel}
          </p>
        </div>

        <div className="rounded-lg border border-zinc-800 bg-zinc-950 p-4">
          <p>
            <strong>Probable Cause:</strong>
          </p>

          <p className="mt-2 text-zinc-300">
            {result.probable_cause}
          </p>
        </div>
      </div>

      <div className="mt-4 rounded-lg border border-zinc-800 bg-zinc-950 p-4">
        <p>
          <strong>Summary:</strong>
        </p>

        <p className="mt-2 text-zinc-300">
          {result.summary}
        </p>
      </div>
    </div>
  );
}
