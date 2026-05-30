"use client";

import { useEffect, useState, useCallback } from "react";
import { useParams, useRouter } from "next/navigation";
import { apiFetch } from "@/lib/api";
import EventLog from "@/components/features/EventLog";
import PipelineRunCard from "@/components/features/PipelineRunCard";

interface TicketDetail {
  id: string;
  issue_number: number;
  github_issue_url: string;
  title: string;
  body: string | null;
  labels: string[];
  status: string;
  created_at: string;
}

interface PipelineRun {
  id: string;
  status: string;
  started_at: string | null;
  duration_seconds: number | null;
  pr_url: string | null;
  pr_number: number | null;
  escalation_reason: string | null;
}

interface EventEntry {
  id: string;
  agent_name: string;
  event_type: string;
  payload: Record<string, unknown>;
  timestamp: string;
}

export default function TicketDetailPage() {
  const params = useParams();
  const router = useRouter();
  const ticketId = params.id as string;

  const [ticket, setTicket] = useState<TicketDetail | null>(null);
  const [runs, setRuns] = useState<PipelineRun[]>([]);
  const [events, setEvents] = useState<EventEntry[]>([]);
  const [selectedRunId, setSelectedRunId] = useState<string | null>(null);
  const [teamId, setTeamId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchTicket = useCallback(async () => {
    try {
      const teamsRes = await apiFetch("/api/v1/teams");
      const teams = (await teamsRes.json()).teams || [];
      if (teams.length === 0) return;

      const tid = teams[0].id;
      setTeamId(tid);

      const res = await apiFetch(`/api/v1/teams/${tid}/tickets/${ticketId}`);
      const data = await res.json();
      setTicket(data.ticket);
      setRuns(data.pipeline_runs || []);

      if (data.pipeline_runs?.length > 0) {
        const latestRun = data.pipeline_runs[0];
        setSelectedRunId(latestRun.id);
        await fetchEvents(tid, ticketId, latestRun.id);
      }
    } catch {
      // silently handle
    } finally {
      setLoading(false);
    }
  }, [ticketId]);

  const fetchEvents = async (tid: string, tktId: string, runId: string) => {
    try {
      const res = await apiFetch(
        `/api/v1/teams/${tid}/tickets/${tktId}/runs/${runId}/events?limit=100`
      );
      const data = await res.json();
      setEvents(data.events || []);
    } catch {
      setEvents([]);
    }
  };

  const handleRetry = async () => {
    if (!teamId) return;
    try {
      await apiFetch(`/api/v1/teams/${teamId}/tickets/${ticketId}/retry`, {
        method: "POST",
      });
      await fetchTicket();
    } catch {
      // silently handle
    }
  };

  const handleSelectRun = async (runId: string) => {
    setSelectedRunId(runId);
    if (teamId) {
      await fetchEvents(teamId, ticketId, runId);
    }
  };

  useEffect(() => {
    fetchTicket();
  }, [fetchTicket]);

  if (loading) {
    return (
      <div>
        <div className="h-8 w-64 animate-pulse rounded bg-surface-raised" />
        <div className="mt-4 h-48 animate-pulse rounded-lg bg-surface-raised" />
      </div>
    );
  }

  if (!ticket) {
    return <p className="text-on-surface-muted">Ticket not found.</p>;
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
  const badge = STATUS_BADGE[ticket.status] || STATUS_BADGE.pending;

  return (
    <div>
      <div className="mb-4 flex items-center gap-3">
        <button
          onClick={() => router.push("/dashboard/tickets")}
          className="text-sm text-on-surface-muted hover:text-on-surface"
        >
          &larr; Tickets
        </button>
      </div>

      <div className="mb-4 flex items-start justify-between">
        <div>
          <h1 className="text-xl font-semibold text-on-surface">
            #{ticket.issue_number}: {ticket.title}
          </h1>
          <a
            href={ticket.github_issue_url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-primary hover:text-primary-hover"
          >
            View on GitHub
          </a>
        </div>
        <div className="flex items-center gap-3">
          <span
            className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${badge.bg} ${badge.text}`}
          >
            {ticket.status}
          </span>
          {(ticket.status === "escalated" || ticket.status === "failed") && (
            <button
              onClick={handleRetry}
              className="rounded-md bg-primary px-3 py-1.5 text-xs font-medium text-white hover:bg-primary-hover"
            >
              Retry
            </button>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <div className="space-y-3">
          <h2 className="text-sm font-semibold text-on-surface">Pipeline Runs</h2>
          {runs.map((run) => (
            <PipelineRunCard
              key={run.id}
              run={run}
              isSelected={selectedRunId === run.id}
              onClick={() => handleSelectRun(run.id)}
            />
          ))}
        </div>

        <div className="lg:col-span-2">
          <h2 className="mb-3 text-sm font-semibold text-on-surface">Event Log</h2>
          <EventLog events={events} />
        </div>
      </div>
    </div>
  );
}
