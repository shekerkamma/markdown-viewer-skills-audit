"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

const navItems = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/dashboard/tickets", label: "Tickets" },
  { href: "/dashboard/analytics", label: "Analytics" },
  { href: "/dashboard/settings", label: "Settings" },
];

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const [authenticated, setAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("ticketforge_token");
    if (!token) {
      router.replace("/");
    } else {
      setAuthenticated(true);
    }
  }, [router]);

  if (!authenticated) return null;

  return (
    <div className="flex min-h-screen">
      <nav className="w-60 border-r border-border bg-surface p-4">
        <div className="mb-8">
          <h2 className="text-lg font-semibold text-on-surface">TicketForge</h2>
        </div>
        <ul className="space-y-1">
          {navItems.map((item) => (
            <li key={item.href}>
              <Link
                href={item.href}
                className="block rounded-md px-3 py-2 text-sm text-on-surface-muted transition-colors hover:bg-surface-overlay hover:text-on-surface"
              >
                {item.label}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
      <main className="flex-1 p-6">{children}</main>
    </div>
  );
}
