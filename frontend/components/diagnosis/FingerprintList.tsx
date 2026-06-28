import FingerprintCard from "@/components/diagnosis/FingerprintCard";
import type { Fingerprint } from "@/types/diagnosis";

type FingerprintListProps = {
  fingerprints: Fingerprint[];
  copied: string | null;
  onCopy: (text: string, label: string) => void;
};

export default function FingerprintList({
  fingerprints = [],
  copied,
  onCopy,
}: FingerprintListProps) {
  return (
    <div>
      <h3 className="mb-3 text-xl font-bold">
        Known Issues Found
      </h3>

      <div className="grid gap-4 md:grid-cols-2">
        {fingerprints.length > 0 ? (
          fingerprints.map((item, index) => (
            <FingerprintCard
              key={index}
              item={item}
              index={index}
              copied={copied}
              onCopy={onCopy}
            />
          ))
        ) : (
          <p className="text-zinc-400">
            No known issue fingerprints were detected.
          </p>
        )}
      </div>
    </div>
  );
}
