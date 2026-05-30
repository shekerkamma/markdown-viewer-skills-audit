"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

interface BillingData {
  plan: string;
  ticket_limit: number;
  tickets_used: number;
  tickets_remaining: number;
  has_subscription: boolean;
}

interface BillingSectionProps {
  teamId: string;
}

export default function BillingSection({ teamId }: BillingSectionProps) {
  const [billing, setBilling] = useState<BillingData | null>(null);
  const [upgrading, setUpgrading] = useState(false);

  useEffect(() => {
    async function fetchBilling() {
      try {
        const res = await apiFetch(`/api/v1/teams/${teamId}/billing`);
        const data = await res.json();
        setBilling(data);
      } catch {
        // silently handle
      }
    }
    fetchBilling();
  }, [teamId]);

  async function handleUpgrade() {
    setUpgrading(true);
    try {
      const res = await apiFetch(`/api/v1/teams/${teamId}/billing/checkout`, {
        method: "POST",
      });
      const data = await res.json();
      if (data.checkout_url) {
        window.location.href = data.checkout_url;
      }
    } catch {
      setUpgrading(false);
    }
  }

  if (!billing) {
    return (
      <div className="h-32 animate-pulse rounded-lg border border-border bg-surface-raised" />
    );
  }

  const usagePct =
    billing.ticket_limit > 0
      ? Math.min(100, (billing.tickets_used / billing.ticket_limit) * 100)
      : 0;

  return (
    <div>
      <h2 className="mb-3 text-sm font-semibold text-on-surface">
        Plan & Billing
      </h2>

      <div className="rounded-lg border border-border bg-surface-raised p-4">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-on-surface-muted">Current plan</p>
            <p className="mt-1 text-lg font-semibold capitalize text-on-surface">
              {billing.plan}
            </p>
          </div>

          {billing.plan === "free" && (
            <button
              onClick={handleUpgrade}
              disabled={upgrading}
              className="rounded-md bg-accent px-4 py-2 text-sm font-medium text-white transition-colors hover:opacity-90 disabled:opacity-50"
            >
              {upgrading ? "Redirecting..." : "Upgrade to Team"}
            </button>
          )}
        </div>

        <div className="mt-4">
          <div className="mb-1 flex justify-between text-sm">
            <span className="text-on-surface-muted">
              Monthly ticket usage
            </span>
            <span className="font-medium text-on-surface">
              {billing.tickets_used} / {billing.ticket_limit}
            </span>
          </div>
          <div className="h-2 overflow-hidden rounded-full bg-surface-overlay">
            <div
              className={`h-full rounded-full transition-all ${
                usagePct > 90 ? "bg-error" : usagePct > 70 ? "bg-warning" : "bg-primary"
              }`}
              style={{ width: `${usagePct}%` }}
            />
          </div>
          <p className="mt-1 text-xs text-on-surface-muted">
            {billing.tickets_remaining} tickets remaining this month
          </p>
        </div>

        {billing.plan !== "free" && (
          <p className="mt-3 text-xs text-on-surface-muted">
            Manage your subscription in the Stripe customer portal.
          </p>
        )}
      </div>
    </div>
  );
}
