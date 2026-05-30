"use client";

import { useEffect, useState, useCallback } from "react";
import { apiFetch } from "@/lib/api";

interface AnalyticsData {
  period: string;
  tickets_processed: number;
  prs_created: number;
  prs_merged: number;
  escalations: number;
  acceptance_rate: number;
  avg_fix_time_seconds: number;
  tokens_used: number;
  estimated_hours_saved: number;
}

const PERIODS = [
  { value: "7d", label: "7 days" },
  { value: "30d", label: "30 days" },
  { value: "90d", label: "90 days" },
];

function formatDuration(seconds: number): string {
  if (seconds < 60) return `${seconds}s`;
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  if (mins < 60) return `${mins}m ${secs}s`;
  const hrs = Math.floor(mins / 60);
  return `${hrs}h ${mins % 60}m`;
}

function formatTokens(tokens: number): string {
  if (tokens < 1000) return tokens.toString();
  if (tokens < 1_000_000) return `${(tokens / 1000).toFixed(1)}k`;
  return `${(tokens / 1_000_000).toFixed(2)}M`;
}

interface MetricCardProps {
  label: string;
  value: string | number;
  subtitle?: string;
  color?: string;
}

function MetricCard({ label, value, subtitle, color = "text-on-surface" }: MetricCardProps) {
  return (
    <div className="rounded-lg border border-border bg-surface-raised p-4">
      <p className="text-sm text-on-surface-muted">{label}</p>
      <p className={`mt-1 text-2xl font-semibold ${color}`}>{value}</p>
      {subtitle && (
        <p className="mt-1 text-xs text-on-surface-muted">{subtitle}</p>
      )}
    </div>
  );
}

export default function AnalyticsPage() {
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [period, setPeriod] = useState("30d");
  const [loading, setLoading] = useState(true);
  const [teamId, setTeamId] = useState<string | null>(null);

  const fetchAnalytics = useCallback(async () => {
    try {
      const teamsRes = await apiFetch("/api/v1/teams");
      const teamsData = await teamsRes.json();
      const teams = teamsData.teams || [];
      if (teams.length === 0) {
        setLoading(false);
        return;
      }

      const currentTeamId = teams[0].id;
      setTeamId(currentTeamId);

      const res = await apiFetch(
        `/api/v1/teams/${currentTeamId}/analytics?period=${period}`
      );
      const analyticsData = await res.json();
      setData(analyticsData);
    } catch {
      // silently retry on next interval
    } finally {
      setLoading(false);
    }
  }, [period]);

  useEffect(() => {
    setLoading(true);
    fetchAnalytics();
  }, [fetchAnalytics]);

  if (loading) {
    return (
      <div>
        <h1 className="mb-4 text-xl font-semibold text-on-surface">Analytics</h1>
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
          {Array.from({ length: 8 }).map((_, i) => (
            <div
              key={i}
              className="h-24 animate-pulse rounded-lg border border-border bg-surface-raised"
            />
          ))}
        </div>
      </div>
    );
  }

  if (!teamId) {
    return (
      <div>
        <h1 className="mb-4 text-xl font-semibold text-on-surface">Analytics</h1>
        <div className="rounded-lg border border-border bg-surface-raised p-8 text-center">
          <p className="text-on-surface-muted">
            No team found. Create a team to view analytics.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-4 flex items-center justify-between">
        <h1 className="text-xl font-semibold text-on-surface">Analytics</h1>
        <div className="flex items-center gap-2">
          <button
            onClick={async () => {
              if (!teamId) return;
              const res = await apiFetch(
                `/api/v1/teams/${teamId}/analytics/export?period=${period}&format=csv`
              );
              const blob = await res.blob();
              const url = URL.createObjectURL(blob);
              const a = document.createElement("a");
              a.href = url;
              a.download = `ticketforge-analytics-${period}.csv`;
              a.click();
              URL.revokeObjectURL(url);
            }}
            className="rounded-md border border-border px-3 py-1 text-sm text-on-surface-muted hover:text-on-surface"
          >
            Export CSV
          </button>
        <div className="flex gap-1 rounded-md border border-border bg-surface-raised p-1">
          {PERIODS.map((p) => (
            <button
              key={p.value}
              onClick={() => setPeriod(p.value)}
              className={`rounded px-3 py-1 text-sm font-medium transition-colors ${
                period === p.value
                  ? "bg-primary text-white"
                  : "text-on-surface-muted hover:text-on-surface"
              }`}
            >
              {p.label}
            </button>
          ))}
        </div>
        </div>
      </div>

      {data && (
        <>
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
            <MetricCard
              label="Tickets Processed"
              value={data.tickets_processed}
              color="text-on-surface"
            />
            <MetricCard
              label="PRs Created"
              value={data.prs_created}
              color="text-info"
            />
            <MetricCard
              label="PRs Merged"
              value={data.prs_merged}
              color="text-success"
            />
            <MetricCard
              label="Escalations"
              value={data.escalations}
              color={data.escalations > 0 ? "text-warning" : "text-on-surface-muted"}
            />
            <MetricCard
              label="Acceptance Rate"
              value={`${data.acceptance_rate}%`}
              color={data.acceptance_rate >= 70 ? "text-success" : "text-warning"}
            />
            <MetricCard
              label="Avg Fix Time"
              value={formatDuration(data.avg_fix_time_seconds)}
              color="text-on-surface"
            />
            <MetricCard
              label="Tokens Used"
              value={formatTokens(data.tokens_used)}
              subtitle={`~$${((data.tokens_used / 1_000_000) * 8).toFixed(2)} est. cost`}
              color="text-on-surface"
            />
            <MetricCard
              label="Hours Saved"
              value={data.estimated_hours_saved.toFixed(1)}
              subtitle={`~$${(data.estimated_hours_saved * 75).toLocaleString()} value`}
              color="text-accent"
            />
          </div>

          <div className="mt-6 grid gap-3 lg:grid-cols-2">
            <div className="rounded-lg border border-border bg-surface-raised p-4">
              <h3 className="mb-3 text-sm font-semibold text-on-surface">
                Pipeline Outcomes
              </h3>
              <div className="space-y-2">
                <ProgressBar
                  label="Merged"
                  value={data.prs_merged}
                  total={data.tickets_processed}
                  color="bg-success"
                />
                <ProgressBar
                  label="PR Created (pending)"
                  value={data.prs_created - data.prs_merged}
                  total={data.tickets_processed}
                  color="bg-info"
                />
                <ProgressBar
                  label="Escalated"
                  value={data.escalations}
                  total={data.tickets_processed}
                  color="bg-warning"
                />
              </div>
            </div>

            <div className="rounded-lg border border-border bg-surface-raised p-4">
              <h3 className="mb-3 text-sm font-semibold text-on-surface">
                Efficiency Summary
              </h3>
              <dl className="space-y-3">
                <div className="flex justify-between">
                  <dt className="text-sm text-on-surface-muted">Throughput</dt>
                  <dd className="text-sm font-medium text-on-surface">
                    {data.tickets_processed} tickets / {PERIODS.find((p) => p.value === period)?.label}
                  </dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-sm text-on-surface-muted">Success rate</dt>
                  <dd className="text-sm font-medium text-on-surface">
                    {data.tickets_processed > 0
                      ? ((data.prs_merged / data.tickets_processed) * 100).toFixed(1)
                      : "0.0"}
                    %
                  </dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-sm text-on-surface-muted">Avg tokens / ticket</dt>
                  <dd className="text-sm font-medium text-on-surface">
                    {data.tickets_processed > 0
                      ? formatTokens(Math.round(data.tokens_used / data.tickets_processed))
                      : "0"}
                  </dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-sm text-on-surface-muted">ROI (hours saved / cost)</dt>
                  <dd className="text-sm font-medium text-accent">
                    {data.tokens_used > 0
                      ? `${((data.estimated_hours_saved * 75) / ((data.tokens_used / 1_000_000) * 8)).toFixed(1)}x`
                      : "N/A"}
                  </dd>
                </div>
              </dl>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

function ProgressBar({
  label,
  value,
  total,
  color,
}: {
  label: string;
  value: number;
  total: number;
  color: string;
}) {
  const pct = total > 0 ? (value / total) * 100 : 0;
  return (
    <div>
      <div className="mb-1 flex justify-between text-sm">
        <span className="text-on-surface-muted">{label}</span>
        <span className="font-medium text-on-surface">
          {value} ({pct.toFixed(0)}%)
        </span>
      </div>
      <div className="h-2 overflow-hidden rounded-full bg-surface-overlay">
        <div
          className={`h-full rounded-full ${color}`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}
