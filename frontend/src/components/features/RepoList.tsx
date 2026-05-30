"use client";

import { useState } from "react";
import { apiFetch } from "@/lib/api";

interface Repo {
  id: string;
  full_name: string;
  is_active: boolean;
  trigger_labels: string[];
}

interface RepoListProps {
  teamId: string;
  repos: Repo[];
  onRepoUpdated: () => void;
}

export default function RepoList({ teamId, repos, onRepoUpdated }: RepoListProps) {
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editLabels, setEditLabels] = useState("");

  const handleToggle = async (repo: Repo) => {
    await apiFetch(`/api/v1/teams/${teamId}/repos/${repo.id}`, {
      method: "PATCH",
      body: JSON.stringify({ is_active: !repo.is_active }),
    });
    onRepoUpdated();
  };

  const handleSaveLabels = async (repoId: string) => {
    const labels = editLabels
      .split(",")
      .map((l) => l.trim())
      .filter(Boolean);
    await apiFetch(`/api/v1/teams/${teamId}/repos/${repoId}`, {
      method: "PATCH",
      body: JSON.stringify({ trigger_labels: labels }),
    });
    setEditingId(null);
    onRepoUpdated();
  };

  const handleDelete = async (repoId: string) => {
    await apiFetch(`/api/v1/teams/${teamId}/repos/${repoId}`, {
      method: "DELETE",
    });
    onRepoUpdated();
  };

  if (repos.length === 0) {
    return (
      <p className="text-on-surface-muted">
        No repositories connected. Click &ldquo;Add Repository&rdquo; to get started.
      </p>
    );
  }

  return (
    <div className="space-y-3">
      {repos.map((repo) => (
        <div
          key={repo.id}
          className="rounded-lg border border-border bg-surface-raised p-4"
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <button
                onClick={() => handleToggle(repo)}
                className={`h-5 w-9 rounded-full transition-colors ${
                  repo.is_active ? "bg-accent" : "bg-border"
                }`}
              >
                <span
                  className={`block h-4 w-4 rounded-full bg-white transition-transform ${
                    repo.is_active ? "translate-x-4" : "translate-x-0.5"
                  }`}
                />
              </button>
              <span className="text-sm font-medium text-on-surface">
                {repo.full_name}
              </span>
            </div>
            <button
              onClick={() => handleDelete(repo.id)}
              className="text-xs text-on-surface-muted hover:text-error"
            >
              Remove
            </button>
          </div>

          <div className="mt-3">
            {editingId === repo.id ? (
              <div className="flex items-center gap-2">
                <input
                  value={editLabels}
                  onChange={(e) => setEditLabels(e.target.value)}
                  className="h-8 flex-1 rounded-md border border-border bg-surface px-3 text-xs text-on-surface"
                  placeholder="bug, fix-me"
                />
                <button
                  onClick={() => handleSaveLabels(repo.id)}
                  className="rounded-md bg-primary px-3 py-1.5 text-xs text-white"
                >
                  Save
                </button>
                <button
                  onClick={() => setEditingId(null)}
                  className="text-xs text-on-surface-muted"
                >
                  Cancel
                </button>
              </div>
            ) : (
              <button
                onClick={() => {
                  setEditingId(repo.id);
                  setEditLabels(repo.trigger_labels.join(", "));
                }}
                className="text-xs text-on-surface-muted hover:text-on-surface"
              >
                Labels: {repo.trigger_labels.join(", ")}
              </button>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
