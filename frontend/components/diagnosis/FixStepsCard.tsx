type FixStepsCardProps = {
  steps?: string[];
};

export default function FixStepsCard({ steps = [] }: FixStepsCardProps) {
  return (
    <div className="rounded-lg border border-zinc-800 bg-zinc-950 p-4">
      <h3 className="mb-3 text-xl font-bold">Fix Steps</h3>

      {steps.length > 0 ? (
        <ol className="ml-6 list-decimal text-zinc-300">
          {steps.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ol>
      ) : (
        <p className="text-zinc-400">No fix steps returned.</p>
      )}
    </div>
  );
}
