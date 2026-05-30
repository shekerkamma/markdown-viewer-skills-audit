"use client";

import { useState } from "react";

interface EventEntry {
  id: string;
  agent_name: string;
  event_type: string;
  payload: Record<string, unknown>;
  timestamp: string;
}

interface EventLogProps {
  events: EventEntry[];
}

const EVENT_TYPE_COLORS: Record<string, string> = {
  action: "text-primary",
  observation: "text-on-surface-muted",
  decision: "text-accent",
  error: "text-error",
};

export default function EventLog({ events }: EventLogProps) {
  const [expandedId, setExpandedId] = useState<string | null>(null);

  if (events.length === 0) {
    return (
      <div className="rounded-lg border border-border bg-surface p-8 text-center">
        <p className="text-on-surface-muted">No events recorded for this run.</p>
      </div>
    );
  }

  return (
    <div className="border border-border bg-surface" role="log" aria-label="Pipeline event log">
      {events.map((event) => {
        const time = new Date(event.timestamp).toLocaleTimeString();
        const color = EVENT_TYPE_COLORS[event.event_type] || "text-on-surface-muted";
        const isExpanded = expandedId === event.id;

        return (
          <div key={event.id} className="border-b border-border last:border-b-0">
            <button
              onClick={() => setExpandedId(isExpanded ? null : event.id)}
              aria-expanded={isExpanded}
              aria-label={`${event.event_type} event from ${event.agent_name} at ${time}`}
              className="flex w-full items-start gap-3 px-4 py-2 text-left font-mono text-xs transition-colors hover:bg-surface-overlay"
            >
              <span className="shrink-0 text-on-surface-muted">{time}</span>
              <span className={`shrink-0 font-semibold ${color}`}>
                [{event.event_type}]
              </span>
              <span className="shrink-0 text-primary">{event.agent_name}</span>
              <span className="truncate text-on-surface">
                {String(
                  event.payload.observation ||
                    event.payload.decision ||
                    event.payload.action_type ||
                    event.payload.error ||
                    event.event_type
                )}
              </span>
            </button>
            {isExpanded && (
              <div className="border-t border-border bg-surface px-4 py-3">
                <pre className="overflow-x-auto font-mono text-xs text-on-surface-muted">
                  {JSON.stringify(event.payload, null, 2)}
                </pre>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
