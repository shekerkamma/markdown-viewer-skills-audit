"use client";

import { useEffect, useState, useCallback } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { apiFetch } from "@/lib/api";
import TicketTable from "@/components/features/TicketTable";

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

const STATUSES = [
  "all",
  "pending",
  "analyzing",
  "generating",
  "reviewing",
  "pr_created",
  "escalated",
  "failed",
];

export default function TicketsPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [loading, setLoading] = useState(true);
  const [status, setStatus] = useState(searchParams.get("status") || "all");
  const [nextCursor, setNextCursor] = useState<string | null>(null);

  const fetchTickets = useCallback(
    async (cursor?: string) => {
      try {
        const teamsRes = await apiFetch("/api/v1/teams");
        const teams = (await teamsRes.json()).teams || [];
        if (teams.length === 0) {
          setLoading(false);
          return;
        }

        const teamId = teams[0].id;
        let url = `/api/v1/teams/${teamId}/tickets?limit=50`;
        if (status !== "all") url += `&status=${status}`;
        if (cursor) url += `&cursor=${cursor}`;

        const res = await apiFetch(url);
        const data = await res.json();

        if (cursor) {
          setTickets((prev) => [...prev, ...(data.tickets || [])]);
        } else {
          setTickets(data.tickets || []);
        }
        setNextCursor(data.next_cursor);
      } catch {
        // silently handle
      } finally {
        setLoading(false);
      }
    },
    [status]
  );

  useEffect(() => {
    setLoading(true);
    fetchTickets();
  }, [fetchTickets]);

  return (
    <div>
      <h1 className="mb-4 text-xl font-semibold text-on-surface">Tickets</h1>

      <div className="mb-4 flex gap-2">
        {STATUSES.map((s) => (
          <button
            key={s}
            onClick={() => setStatus(s)}
            className={`rounded-md px-3 py-1.5 text-xs font-medium transition-colors ${
              status === s
                ? "bg-primary text-white"
                : "bg-surface-raised text-on-surface-muted hover:bg-surface-overlay"
            }`}
          >
            {s === "all" ? "All" : s.replace("_", " ")}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="space-y-2">
          {Array.from({ length: 5 }).map((_, i) => (
            <div
              key={i}
              className="h-12 animate-pulse rounded-lg border border-border bg-surface-raised"
            />
          ))}
        </div>
      ) : (
        <>
          <TicketTable
            tickets={tickets}
            onTicketClick={(id) => router.push(`/dashboard/tickets/${id}`)}
          />
          {nextCursor && (
            <button
              onClick={() => fetchTickets(nextCursor)}
              className="mt-4 rounded-md bg-surface-raised px-4 py-2 text-sm text-on-surface-muted hover:bg-surface-overlay"
            >
              Load more
            </button>
          )}
        </>
      )}
    </div>
  );
}
