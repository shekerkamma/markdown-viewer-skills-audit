"use client";

interface EmptyStateProps {
  title: string;
  message: string;
  action?: {
    label: string;
    onClick: () => void;
  };
}

export default function EmptyState({ title, message, action }: EmptyStateProps) {
  return (
    <div className="rounded-lg border border-border bg-surface-raised p-8 text-center">
      <h3 className="text-sm font-semibold text-on-surface">{title}</h3>
      <p className="mt-2 text-sm text-on-surface-muted">{message}</p>
      {action && (
        <button
          onClick={action.onClick}
          className="mt-4 inline-flex h-9 items-center rounded-md bg-primary px-4 text-sm font-medium text-white transition-colors hover:bg-primary-hover"
        >
          {action.label}
        </button>
      )}
    </div>
  );
}
