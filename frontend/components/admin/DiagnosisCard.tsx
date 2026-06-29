import type { DiagnosisResult } from "@/types/diagnosis";

import Card from "@/components/ui/Card";
import SeverityBadge from "@/components/ui/SeverityBadge";

type Props = {
  diagnosis: DiagnosisResult;
};

export default function DiagnosisCard({ diagnosis }: Props) {
  return (
    <Card>
      <h2 className="mb-4 text-xl font-bold">Diagnosis Result</h2>

      <div className="grid gap-4 md:grid-cols-2">
        <div className="space-y-2 text-sm">
          <p>
            <strong>Source:</strong>{" "}
            {diagnosis.ai_used
              ? "AI Analysis"
              : diagnosis.used_known_issue
                ? "Known Issue Match"
                : "Deterministic Engine"}
          </p>

          <p className="flex items-center gap-2">
            <strong>Severity:</strong>
            <SeverityBadge severity={diagnosis.severity} />
          </p>

          <p>
            <strong>Confidence:</strong>{" "}
            {diagnosis.parsed?.primary_fingerprint != null
              ? `${diagnosis.parsed.primary_fingerprint.confidence}%`
              : diagnosis.confidence}
          </p>

          {diagnosis.version && (
            <p>
              <strong>ProtonFix:</strong> v{diagnosis.version}
            </p>
          )}
        </div>

        <div>
          <p className="mb-1 text-sm font-semibold text-zinc-400">
            Probable Cause
          </p>
          <p className="text-sm text-zinc-300">
            {diagnosis.probable_cause}
          </p>
        </div>
      </div>

      <div className="mt-4">
        <p className="mb-1 text-sm font-semibold text-zinc-400">
          Summary
        </p>
        <p className="text-sm text-zinc-300">{diagnosis.summary}</p>
      </div>

      {diagnosis.fix_steps.length > 0 && (
        <div className="mt-4">
          <p className="mb-2 text-sm font-semibold">Fix Steps</p>
          <ol className="ml-5 list-decimal space-y-1 text-sm text-zinc-300">
            {diagnosis.fix_steps.map((step, i) => (
              <li key={i}>{step}</li>
            ))}
          </ol>
        </div>
      )}

      {diagnosis.warnings.length > 0 && (
        <div className="mt-4">
          <p className="mb-2 text-sm font-semibold text-yellow-400">
            Warnings
          </p>
          <ul className="ml-5 list-disc space-y-1 text-sm text-zinc-300">
            {diagnosis.warnings.map((warning, i) => (
              <li key={i}>{warning}</li>
            ))}
          </ul>
        </div>
      )}
    </Card>
  );
}
