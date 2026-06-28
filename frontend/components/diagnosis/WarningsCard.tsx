type WarningsCardProps = {
  warnings?: string[];
};

export default function WarningsCard({
  warnings = [],
}: WarningsCardProps) {
  return (
    <div className="rounded-lg border border-zinc-800 bg-zinc-950 p-4">
      <h3 className="mb-3 text-xl font-bold">
        Warnings
      </h3>

      {warnings.length > 0 ? (
        <ul className="ml-6 list-disc text-zinc-300">
          {warnings.map((warning, index) => (
            <li key={index}>{warning}</li>
          ))}
        </ul>
      ) : (
        <p className="text-zinc-400">
          No warnings.
        </p>
      )}
    </div>
  );
}
