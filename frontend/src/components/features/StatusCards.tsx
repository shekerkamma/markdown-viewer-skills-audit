"use client";

interface StatusCardProps {
  label: string;
  count: number;
  color: string;
  onClick?: () => void;
}

function StatusCard({ label, count, color, onClick }: StatusCardProps) {
  return (
    <button
      onClick={onClick}
      className="rounded-lg border border-border bg-surface-raised p-4 text-left transition-colors hover:bg-surface-overlay"
    >
      <p className="text-sm text-on-surface-muted">{label}</p>
      <p className={`mt-1 text-2xl font-semibold ${color}`}>{count}</p>
    </button>
  );
}

interface StatusCardsProps {
  counts: Record<string, number>;
  onFilterByStatus?: (status: string) => void;
}

const STATUS_CONFIG: { key: string; label: string; color: string }[] = [
  { key: "pending", label: "Pending", color: "text-on-surface-muted" },
  { key: "analyzing", label: "Analyzing", color: "text-info" },
  { key: "generating", label: "Generating", color: "text-info" },
  { key: "reviewing", label: "Reviewing", color: "text-warning" },
  { key: "pr_created", label: "PR Created", color: "text-success" },
  { key: "escalated", label: "Escalated", color: "text-error" },
  { key: "failed", label: "Failed", color: "text-error" },
];

export default function StatusCards({ counts, onFilterByStatus }: StatusCardsProps) {
  return (
    <div className="grid grid-cols-2 gap-3 sm:grid-cols-4 lg:grid-cols-7">
      {STATUS_CONFIG.map(({ key, label, color }) => (
        <StatusCard
          key={key}
          label={label}
          count={counts[key] || 0}
          color={color}
          onClick={() => onFilterByStatus?.(key)}
        />
      ))}
    </div>
  );
}
