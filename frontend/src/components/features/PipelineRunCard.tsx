"use client";

interface PipelineRun {
  id: string;
  status: string;
  started_at: string | null;
  duration_seconds: number | null;
  pr_url: string | null;
  pr_number: number | null;
  escalation_reason: string | null;
}

interface PipelineRunCardProps {
  run: PipelineRun;
  isSelected: boolean;
  onClick: () => void;
}

const STATUS_BADGE: Record<string, { bg: string; text: string }> = {
  running: { bg: "bg-info-subtle", text: "text-info" },
  completed: { bg: "bg-success-subtle", text: "text-success" },
  failed: { bg: "bg-error-subtle", text: "text-error" },
  escalated: { bg: "bg-warning-subtle", text: "text-warning" },
};

export default function PipelineRunCard({
  run,
  isSelected,
  onClick,
}: PipelineRunCardProps) {
  const badge = STATUS_BADGE[run.status] || STATUS_BADGE.running;
  const duration = run.duration_seconds;
  const timeStr = duration
    ? duration < 60
      ? `${duration}s`
      : `${Math.round(duration / 60)}m ${duration % 60}s`
    : "running...";
  const startedAt = run.started_at
    ? new Date(run.started_at).toLocaleString()
    : "";

  return (
    <button
      onClick={onClick}
      className={`w-full rounded-lg border p-4 text-left transition-colors ${
        isSelected
          ? "border-primary bg-surface-overlay"
          : "border-border bg-surface-raised hover:bg-surface-overlay"
      }`}
    >
      <div className="flex items-center justify-between">
        <span
          className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${badge.bg} ${badge.text}`}
        >
          {run.status}
        </span>
        <span className="text-xs text-on-surface-muted">{timeStr}</span>
      </div>

      <p className="mt-2 text-xs text-on-surface-muted">{startedAt}</p>

      {run.pr_url && (
        <a
          href={run.pr_url}
          target="_blank"
          rel="noopener noreferrer"
          onClick={(e) => e.stopPropagation()}
          className="mt-2 inline-block text-xs text-primary hover:text-primary-hover"
        >
          View PR #{run.pr_number}
        </a>
      )}

      {run.escalation_reason && (
        <p className="mt-2 text-xs text-error">{run.escalation_reason}</p>
      )}
    </button>
  );
}
