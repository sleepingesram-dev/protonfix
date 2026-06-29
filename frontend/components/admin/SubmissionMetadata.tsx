import type {
  Submission,
  RedactionReport,
} from "@/types/diagnosis";

import Card from "@/components/ui/Card";

const STATUS_COLORS: Record<string, string> = {
  pending: "bg-yellow-900 text-yellow-200",
  diagnosed: "bg-green-900 text-green-200",
  reviewed: "bg-blue-900 text-blue-200",
};

type Props = {
  submission: Submission;
  redaction?: RedactionReport;
  diagnosing: boolean;
  onRunDiagnosis: () => void;
};

export default function SubmissionMetadata({
  submission,
  redaction,
  diagnosing,
  onRunDiagnosis,
}: Props) {
  return (
    <Card>
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="text-lg font-semibold">
            Submission Details
          </h2>

          {submission.note ? (
            <p className="mt-2 text-zinc-300">
              {submission.note}
            </p>
          ) : (
            <p className="mt-2 italic text-zinc-600">
              No note provided.
            </p>
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

      <div className="mt-5">
        <button
          onClick={onRunDiagnosis}
          disabled={diagnosing}
          className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-bold hover:bg-blue-500 disabled:bg-zinc-700 disabled:text-zinc-400"
        >
          {diagnosing
            ? "Running diagnosis..."
            : submission.diagnosis
              ? "Re-run Diagnosis"
              : "Run Diagnosis"}
        </button>
      </div>

      {redaction && (
        <div className="mt-6 rounded border border-zinc-800 bg-zinc-950 p-4">
          <p className="mb-2 text-sm font-semibold">
            Privacy Redaction
          </p>

          <p className="text-sm text-zinc-400">
            {redaction.was_redacted
              ? `${redaction.total_redactions} sensitive values removed`
              : "No sensitive information detected."}
          </p>
        </div>
      )}
    </Card>
  );
}
