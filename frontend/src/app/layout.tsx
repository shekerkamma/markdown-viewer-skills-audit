import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "TicketForge — From ticket to PR. Automatically.",
  description:
    "TicketForge turns GitHub issues into merged pull requests using a multi-agent AI pipeline. Label a bug, get a PR. Free for up to 20 tickets/month.",
  openGraph: {
    title: "TicketForge — From ticket to PR. Automatically.",
    description:
      "Multi-agent AI pipeline that turns GitHub issues into merged pull requests. Label a bug, get a PR.",
    siteName: "TicketForge",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "TicketForge — From ticket to PR. Automatically.",
    description:
      "Multi-agent AI pipeline that turns GitHub issues into merged pull requests. Label a bug, get a PR.",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="font-sans antialiased">{children}</body>
    </html>
  );
}
