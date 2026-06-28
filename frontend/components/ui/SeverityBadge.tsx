type SeverityBadgeProps = {
  severity: string;
};

export default function SeverityBadge({ severity }: SeverityBadgeProps) {
  const level = severity?.toLowerCase();

  if (level === "high") {
    return (
      <span className="rounded bg-red-900 px-2 py-1 text-xs font-bold text-red-200">
        🔴 HIGH
      </span>
    );
  }

  if (level === "medium") {
    return (
      <span className="rounded bg-yellow-900 px-2 py-1 text-xs font-bold text-yellow-200">
        🟡 MEDIUM
      </span>
    );
  }

  return (
    <span className="rounded bg-green-900 px-2 py-1 text-xs font-bold text-green-200">
      🟢 LOW
    </span>
  );
}
