"use client";

import { useState } from "react";
import { apiFetch } from "@/lib/api";

interface AddRepoDialogProps {
  teamId: string;
  isOpen: boolean;
  onClose: () => void;
  onRepoAdded: () => void;
}

export default function AddRepoDialog({
  teamId,
  isOpen,
  onClose,
  onRepoAdded,
}: AddRepoDialogProps) {
  const [repoName, setRepoName] = useState("");
  const [labels, setLabels] = useState("bug");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!repoName.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const triggerLabels = labels
        .split(",")
        .map((l) => l.trim())
        .filter(Boolean);

      const res = await apiFetch(`/api/v1/teams/${teamId}/repos`, {
        method: "POST",
        body: JSON.stringify({
          github_repo_full_name: repoName.trim(),
          trigger_labels: triggerLabels,
        }),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Failed to connect repository");
      }

      setRepoName("");
      setLabels("bug");
      onRepoAdded();
      onClose();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to connect repository");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="w-full max-w-md rounded-lg border border-border bg-surface-overlay p-6">
        <h2 className="mb-4 text-lg font-semibold text-on-surface">
          Add Repository
        </h2>

        <form onSubmit={handleSubmit}>
          <label className="mb-1 block text-xs text-on-surface-muted">
            Repository (owner/name)
          </label>
          <input
            value={repoName}
            onChange={(e) => setRepoName(e.target.value)}
            placeholder="org/repo"
            className="mb-4 h-9 w-full rounded-md border border-border bg-surface px-3 text-sm text-on-surface focus:outline-none focus:ring-2 focus:ring-primary/40"
          />

          <label className="mb-1 block text-xs text-on-surface-muted">
            Trigger labels (comma-separated)
          </label>
          <input
            value={labels}
            onChange={(e) => setLabels(e.target.value)}
            placeholder="bug, fix-me"
            className="mb-4 h-9 w-full rounded-md border border-border bg-surface px-3 text-sm text-on-surface focus:outline-none focus:ring-2 focus:ring-primary/40"
          />

          {error && (
            <p className="mb-3 text-xs text-error">{error}</p>
          )}

          <div className="flex justify-end gap-3">
            <button
              type="button"
              onClick={onClose}
              className="rounded-md px-4 py-2 text-sm text-on-surface-muted hover:text-on-surface"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading || !repoName.trim()}
              className="rounded-md bg-primary px-4 py-2 text-sm font-medium text-white hover:bg-primary-hover disabled:bg-border disabled:text-on-surface-muted"
            >
              {loading ? "Connecting..." : "Connect"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
