type ConfidenceBadgeProps = {
  confidence?: number;
};

export default function ConfidenceBadge({
  confidence,
}: ConfidenceBadgeProps) {
  if (confidence === undefined || confidence === null) {
    return null;
  }

  return (
    <span className="rounded bg-blue-900 px-2 py-1 text-xs font-bold text-blue-200">
      {confidence}% confidence
    </span>
  );
}
