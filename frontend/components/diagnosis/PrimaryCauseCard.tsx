import ConfidenceBadge from "@/components/ui/ConfidenceBadge";
import SeverityBadge from "@/components/ui/SeverityBadge";
import { humanizeFingerprint } from "@/lib/fingerprints";
import type { Fingerprint } from "@/types/diagnosis";

type PrimaryCauseCardProps = {
  fingerprint?: Fingerprint | null;
};

export default function PrimaryCauseCard({
  fingerprint,
}: PrimaryCauseCardProps) {
  if (!fingerprint) return null;

  return (
    <div className="rounded-lg border border-blue-700 bg-zinc-950 p-4">
      <p className="mb-2 text-sm font-semibold uppercase tracking-wide text-blue-400">
        Primary Cause
      </p>

      <h3 className="text-2xl font-bold">
        {fingerprint.metadata?.display_name ?? humanizeFingerprint(fingerprint.fingerprint)}
      </h3>

      <p className="mt-1 text-xs text-zinc-500">
        {fingerprint.fingerprint}
      </p>

      <div className="mt-3 flex flex-wrap gap-2">
        <SeverityBadge severity={fingerprint.severity} />
        <ConfidenceBadge confidence={fingerprint.confidence} />
      </div>

      <p className="mt-3 text-zinc-300">
        {fingerprint.explanation}
      </p>

      <p className="mt-3 text-sm text-zinc-400">
        Category: {fingerprint.category}
      </p>
    </div>
  );
}
