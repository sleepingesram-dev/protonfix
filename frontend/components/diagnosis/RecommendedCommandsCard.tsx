type RecommendedCommandsCardProps = {
  commands?: string[];
  copied: string | null;
  onCopy: (text: string, label: string) => void;
};

export default function RecommendedCommandsCard({
  commands = [],
  copied,
  onCopy,
}: RecommendedCommandsCardProps) {
  const commandText = commands.join("\n");

  return (
    <div className="rounded-lg border border-zinc-800 bg-zinc-950 p-4">
      <div className="mb-3 flex items-center justify-between gap-2">
        <h3 className="text-xl font-bold">Recommended Commands</h3>

        {commands.length > 0 && (
          <button
            onClick={() => onCopy(commandText, "main-commands")}
            className="rounded bg-zinc-800 px-3 py-1 text-sm font-semibold hover:bg-zinc-700"
          >
            {copied === "main-commands" ? "Copied" : "Copy Commands"}
          </button>
        )}
      </div>

      {commands.length > 0 ? (
        <pre className="overflow-x-auto rounded-lg bg-black p-4 text-sm">
          {commandText}
        </pre>
      ) : (
        <p className="text-zinc-400">No commands recommended.</p>
      )}
    </div>
  );
}
