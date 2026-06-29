import Card from "@/components/ui/Card";

type Props = {
  parsed?: Record<string, unknown>;
};

export default function ParsedMetadata({ parsed }: Props) {
  if (!parsed || Object.keys(parsed).length === 0) {
    return null;
  }

  return (
    <Card>
      <h2 className="mb-4 text-lg font-semibold">Parsed Metadata</h2>

      <div className="grid gap-3 md:grid-cols-2">
        {Object.entries(parsed)
          .filter(([key]) => key !== "primary_fingerprint")
          .map(([key, value]) => (
            <div
              key={key}
              className="rounded border border-zinc-800 bg-zinc-950 p-3"
            >
              <p className="mb-1 text-xs uppercase tracking-wide text-zinc-500">
                {key.replaceAll("_", " ")}
              </p>

              <p className="font-mono text-sm text-zinc-300 whitespace-pre-wrap break-words">
                {value == null || value === ""
                  ? "Unknown"
                  : typeof value === "object"
                    ? JSON.stringify(value, null, 2)
                    : String(value)}
              </p>
            </div>
          ))}
      </div>
    </Card>
  );
}
