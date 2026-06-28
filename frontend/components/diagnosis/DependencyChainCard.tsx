import Card from "@/components/ui/Card";
import type { FingerprintResult } from "@/types/diagnosis";

type DependencyChainCardProps = {
    chain?: string[];
    fingerprints?: FingerprintResult[];
};

export default function DependencyChainCard({
    chain = [],
    fingerprints = [],
}: DependencyChainCardProps) {
    if (chain.length === 0) return null;

    const fingerprintMap = new Map(
        fingerprints.map((fp) => [fp.fingerprint, fp])
    );

    return (
        <Card>
        <h3 className="mb-4 text-xl font-bold">Root Cause Chain</h3>

        <div className="flex flex-col gap-2">
        {chain.map((item, index) => (
            <div key={item} className="flex flex-col items-center">
            <div className="rounded-lg border border-zinc-700 bg-zinc-900 px-4 py-2">
            {fingerprintMap.get(item)?.metadata?.display_name ??
                item.replace(/_/g, " ")}
                </div>

                {index < chain.length - 1 && (
                    <div className="py-2 text-2xl text-zinc-500">↓</div>
                )}
                </div>
        ))}
        </div>
        </Card>
    );
}
