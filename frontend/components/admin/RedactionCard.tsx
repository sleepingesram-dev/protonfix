import type { RedactionReport } from "@/types/diagnosis";

import Card from "@/components/ui/Card";

type Props = {
  redaction?: RedactionReport;
};

export default function RedactionCard({ redaction }: Props) {
  if (!redaction) {
    return null;
  }

  return (
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
  );
}
