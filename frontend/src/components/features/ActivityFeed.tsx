"use client";

interface ActivityEvent {
  id: string;
  agent_name: string;
  event_type: string;
  payload: Record<string, unknown>;
  timestamp: string;
}

interface ActivityFeedProps {
  events: ActivityEvent[];
  onEventClick?: (event: ActivityEvent) => void;
}

const EVENT_TYPE_COLORS: Record<string, string> = {
  action: "text-primary",
  observation: "text-on-surface-muted",
  decision: "text-accent",
  error: "text-error",
};

export default function ActivityFeed({ events, onEventClick }: ActivityFeedProps) {
  if (events.length === 0) {
    return (
      <div className="rounded-lg border border-border bg-surface-raised p-8 text-center">
        <p className="text-on-surface-muted">No activity yet.</p>
      </div>
    );
  }

  return (
    <div className="rounded-lg border border-border bg-surface-raised">
      {events.map((event) => {
        const time = new Date(event.timestamp).toLocaleTimeString();
        const color = EVENT_TYPE_COLORS[event.event_type] || "text-on-surface-muted";
        const summary =
          (event.payload as Record<string, string>).observation ||
          (event.payload as Record<string, string>).decision ||
          (event.payload as Record<string, string>).action_type ||
          (event.payload as Record<string, string>).error ||
          event.event_type;

        return (
          <button
            key={event.id}
            onClick={() => onEventClick?.(event)}
            className="flex w-full items-start gap-3 border-b border-border px-4 py-2 text-left font-mono text-xs transition-colors last:border-b-0 hover:bg-surface-overlay"
          >
            <span className="shrink-0 text-on-surface-muted">{time}</span>
            <span className={`shrink-0 ${color}`}>{event.agent_name}</span>
            <span className="truncate text-on-surface">{String(summary)}</span>
          </button>
        );
      })}
    </div>
  );
}
