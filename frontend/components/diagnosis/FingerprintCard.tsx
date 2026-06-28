import ConfidenceBadge from "@/components/ui/ConfidenceBadge";
import SeverityBadge from "@/components/ui/SeverityBadge";
import { humanizeFingerprint } from "@/lib/fingerprints";
import type { Fingerprint } from "@/types/diagnosis";

type FingerprintCardProps = {
  item: Fingerprint;
  index: number;
  copied: string | null;
  onCopy: (text: string, label: string) => void;
};

export default function FingerprintCard({
  item,
  index,
  copied,
  onCopy,
}: FingerprintCardProps) {
  const commandText = item.safe_commands?.join("\n") || "";

  return (
    <div className="h-fit rounded-lg border border-zinc-700 bg-zinc-950 p-4">
      <div className="mb-2 flex items-start justify-between gap-2">
        <div>
          <h4 className="text-lg font-bold">
            {item.metadata?.display_name ?? humanizeFingerprint(item.fingerprint)}
          </h4>

          <p className="text-xs text-zinc-500">
            {item.fingerprint}
          </p>

          <div className="mt-2">
            <ConfidenceBadge confidence={item.confidence} />
          </div>
        </div>

        <SeverityBadge severity={item.severity} />
      </div>

      <p className="text-sm text-zinc-400">
        {item.category}
      </p>

      <p className="mt-3 text-zinc-300">
        {item.metadata?.short_description ?? item.explanation}
      </p>

      <div className="mt-4">
        <strong>Known Fixes:</strong>

        <ul className="mt-2 ml-6 list-disc text-zinc-300">
          {item.known_fix?.map((fix: string, fixIndex: number) => (
            <li key={fixIndex}>{fix}</li>
          ))}
        </ul>
      </div>

      {item.safe_commands?.length > 0 && (
        <div className="mt-4">
          <div className="mb-2 flex items-center justify-between gap-2">
            <strong>Commands:</strong>

            <button
              onClick={() => onCopy(commandText, `issue-${index}`)}
              className="rounded bg-zinc-800 px-3 py-1 text-xs font-semibold hover:bg-zinc-700"
            >
              {copied === `issue-${index}` ? "Copied" : "Copy Commands"}
            </button>
          </div>

          <pre className="overflow-x-auto rounded bg-black p-3 text-xs">
            {commandText}
          </pre>
        </div>
      )}
    </div>
  );
}
