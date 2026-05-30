"use client";

import { useEffect, useState, useCallback } from "react";
import { apiFetch } from "@/lib/api";
import RepoList from "@/components/features/RepoList";
import AddRepoDialog from "@/components/features/AddRepoDialog";
import BillingSection from "@/components/features/BillingSection";

interface Repo {
  id: string;
  full_name: string;
  is_active: boolean;
  trigger_labels: string[];
}

export default function SettingsPage() {
  const [repos, setRepos] = useState<Repo[]>([]);
  const [teamId, setTeamId] = useState<string | null>(null);
  const [showAddDialog, setShowAddDialog] = useState(false);
  const [loading, setLoading] = useState(true);

  const fetchRepos = useCallback(async () => {
    try {
      const teamsRes = await apiFetch("/api/v1/teams");
      const teams = (await teamsRes.json()).teams || [];
      if (teams.length === 0) {
        setLoading(false);
        return;
      }

      const tid = teams[0].id;
      setTeamId(tid);

      const res = await apiFetch(`/api/v1/teams/${tid}/repos`);
      const data = await res.json();
      setRepos(data.repositories || []);
    } catch {
      // silently handle
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchRepos();
  }, [fetchRepos]);

  return (
    <div>
      <div className="mb-4 flex items-center justify-between">
        <h1 className="text-xl font-semibold text-on-surface">Settings</h1>
        {teamId && (
          <button
            onClick={() => setShowAddDialog(true)}
            className="rounded-md bg-primary px-4 py-2 text-sm font-medium text-white hover:bg-primary-hover"
          >
            Add Repository
          </button>
        )}
      </div>

      <h2 className="mb-3 text-sm font-semibold text-on-surface">Repositories</h2>

      {loading ? (
        <div className="space-y-3">
          {Array.from({ length: 3 }).map((_, i) => (
            <div
              key={i}
              className="h-20 animate-pulse rounded-lg border border-border bg-surface-raised"
            />
          ))}
        </div>
      ) : teamId ? (
        <RepoList teamId={teamId} repos={repos} onRepoUpdated={fetchRepos} />
      ) : (
        <p className="text-on-surface-muted">No team found. Sign in again.</p>
      )}

      {teamId && (
        <>
          <div className="mt-8 border-t border-border pt-6">
            <BillingSection teamId={teamId} />
          </div>

          <AddRepoDialog
            teamId={teamId}
            isOpen={showAddDialog}
            onClose={() => setShowAddDialog(false)}
            onRepoAdded={fetchRepos}
          />
        </>
      )}
    </div>
  );
}
