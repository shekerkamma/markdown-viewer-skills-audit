const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function LoginPage() {
  return (
    <main className="flex min-h-screen items-center justify-center">
      <div className="w-full max-w-sm rounded-lg border border-border bg-surface-raised p-8 text-center">
        <h1 className="mb-2 text-2xl font-bold tracking-tight text-on-surface">
          TicketForge
        </h1>
        <p className="mb-8 text-sm text-on-surface-muted">
          From ticket to PR. Automatically.
        </p>
        <a
          href={`${API_URL}/api/auth/github`}
          className="inline-flex h-9 items-center rounded-md bg-primary px-4 text-sm font-medium text-white transition-colors hover:bg-primary-hover"
        >
          Sign in with GitHub
        </a>
      </div>
    </main>
  );
}
