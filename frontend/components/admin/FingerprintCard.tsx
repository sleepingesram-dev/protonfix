import Card from "@/components/ui/Card";

type Fingerprint = {
  id?: string;
  name?: string;
  description?: string;
  confidence?: number;
  severity?: string;
  evidence?: unknown;
};

type Props = {
  fingerprints?: Fingerprint[];
};

export default function FingerprintCard({ fingerprints }: Props) {
  if (!fingerprints || fingerprints.length === 0) {
    return null;
  }

  return (
    <Card>
      <h2 className="mb-4 text-lg font-semibold">Fingerprints</h2>

      <div className="space-y-3">
        {fingerprints.map((fp, index) => (
          <div
            key={fp.id ?? fp.name ?? index}
            className="rounded border border-zinc-800 bg-zinc-950 p-3"
          >
            <div className="flex items-start justify-between gap-3">
              <div>
                <p className="font-mono text-sm font-semibold text-blue-300">
                  {fp.id ?? fp.name ?? `Fingerprint ${index + 1}`}
                </p>

                {fp.description && (
                  <p className="mt-1 text-sm text-zinc-400">
                    {fp.description}
                  </p>
                )}
              </div>

              {fp.confidence != null && (
                <span className="rounded bg-zinc-800 px-2 py-1 text-xs font-semibold text-zinc-300">
                  {fp.confidence}%
                </span>
              )}
            </div>

            {fp.severity && (
              <p className="mt-2 text-xs uppercase tracking-wide text-zinc-500">
                Severity: {fp.severity}
              </p>
            )}

            {fp.evidence != null && (
              <pre className="mt-3 max-h-40 overflow-y-auto rounded bg-black p-3 text-xs text-zinc-400 whitespace-pre-wrap">
                {typeof fp.evidence === "string"
                  ? fp.evidence
                  : JSON.stringify(fp.evidence, null, 2)}
              </pre>
            )}
          </div>
        ))}
      </div>
    </Card>
  );
}
