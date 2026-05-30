"use client";

interface Ticket {
  id: string;
  repo_full_name: string;
  issue_number: number;
  title: string;
  status: string;
  created_at: string;
  latest_run: {
    id: string;
    status: string;
    pr_url: string | null;
    duration_seconds: number | null;
  } | null;
}

interface TicketTableProps {
  tickets: Ticket[];
  onTicketClick?: (ticketId: string) => void;
}

const STATUS_BADGE: Record<string, { bg: string; text: string }> = {
  pending: { bg: "bg-surface-overlay", text: "text-on-surface-muted" },
  analyzing: { bg: "bg-info-subtle", text: "text-info" },
  generating: { bg: "bg-info-subtle", text: "text-info" },
  reviewing: { bg: "bg-warning-subtle", text: "text-warning" },
  pr_created: { bg: "bg-success-subtle", text: "text-success" },
  escalated: { bg: "bg-error-subtle", text: "text-error" },
  failed: { bg: "bg-error-subtle", text: "text-error" },
};

export default function TicketTable({ tickets, onTicketClick }: TicketTableProps) {
  if (tickets.length === 0) {
    return (
      <div className="rounded-lg border border-border bg-surface-raised p-8 text-center">
        <p className="text-on-surface-muted">
          No tickets processed yet. Bug issues with your configured labels will
          appear here automatically.
        </p>
      </div>
    );
  }

  return (
    <div className="overflow-x-auto rounded-lg border border-border">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-border bg-surface-raised text-left text-on-surface-muted">
            <th className="px-4 py-3 font-medium">Issue #</th>
            <th className="px-4 py-3 font-medium">Title</th>
            <th className="px-4 py-3 font-medium">Repo</th>
            <th className="px-4 py-3 font-medium">Status</th>
            <th className="px-4 py-3 font-medium">Time</th>
            <th className="px-4 py-3 font-medium">PR</th>
          </tr>
        </thead>
        <tbody>
          {tickets.map((ticket) => {
            const badge = STATUS_BADGE[ticket.status] || STATUS_BADGE.pending;
            const duration = ticket.latest_run?.duration_seconds;
            const timeStr = duration
              ? duration < 60
                ? `${duration}s`
                : `${Math.round(duration / 60)}m`
              : "—";

            return (
              <tr
                key={ticket.id}
                onClick={() => onTicketClick?.(ticket.id)}
                className="cursor-pointer border-b border-border transition-colors last:border-b-0 hover:bg-surface-raised"
              >
                <td className="px-4 py-3 font-mono text-on-surface-muted">
                  #{ticket.issue_number}
                </td>
                <td className="max-w-xs truncate px-4 py-3 text-on-surface">
                  {ticket.title}
                </td>
                <td className="px-4 py-3 text-on-surface-muted">
                  {ticket.repo_full_name}
                </td>
                <td className="px-4 py-3">
                  <span
                    className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${badge.bg} ${badge.text}`}
                  >
                    {ticket.status}
                  </span>
                </td>
                <td className="px-4 py-3 text-on-surface-muted">{timeStr}</td>
                <td className="px-4 py-3">
                  {ticket.latest_run?.pr_url ? (
                    <a
                      href={ticket.latest_run.pr_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      onClick={(e) => e.stopPropagation()}
                      className="text-primary hover:text-primary-hover"
                    >
                      View PR
                    </a>
                  ) : (
                    <span className="text-on-surface-muted">—</span>
                  )}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
