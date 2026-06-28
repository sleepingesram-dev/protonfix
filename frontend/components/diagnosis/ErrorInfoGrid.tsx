type ErrorInfoGridProps = {
  errors?: string[];
  extraInfo?: string[];
};

export default function ErrorInfoGrid({
  errors = [],
  extraInfo = [],
}: ErrorInfoGridProps) {
  return (
    <div className="grid gap-4 md:grid-cols-2">
      <div className="rounded-lg border border-zinc-800 bg-zinc-950 p-4">
        <h3 className="mb-3 text-lg font-bold">
          Detected Errors
        </h3>

        {errors.length > 0 ? (
          <ul className="list-disc space-y-2 pl-5">
            {errors.map((error, index) => (
              <li key={index}>{error}</li>
            ))}
          </ul>
        ) : (
          <p className="text-zinc-400">
            No explicit errors detected.
          </p>
        )}
      </div>

      <div className="rounded-lg border border-zinc-800 bg-zinc-950 p-4">
        <h3 className="mb-3 text-lg font-bold">
          Extra Info Needed
        </h3>

        {extraInfo.length > 0 ? (
          <ul className="list-disc space-y-2 pl-5">
            {extraInfo.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        ) : (
          <p className="text-zinc-400">
            No additional information required.
          </p>
        )}
      </div>
    </div>
  );
}
