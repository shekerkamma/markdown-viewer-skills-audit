import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "TicketForge",
  description:
    "From GitHub Issue to merged PR. Automatically.",
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
