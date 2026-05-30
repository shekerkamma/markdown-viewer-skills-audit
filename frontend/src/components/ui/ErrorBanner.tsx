"use client";

import { useEffect, useState } from "react";

interface ErrorBannerProps {
  message: string;
  onRetry?: () => void;
  autoRetrySeconds?: number;
}

export default function ErrorBanner({
  message,
  onRetry,
  autoRetrySeconds = 5,
}: ErrorBannerProps) {
  const [countdown, setCountdown] = useState(autoRetrySeconds);

  useEffect(() => {
    if (!onRetry || autoRetrySeconds <= 0) return;

    setCountdown(autoRetrySeconds);
    const interval = setInterval(() => {
      setCountdown((prev) => {
        if (prev <= 1) {
          clearInterval(interval);
          onRetry();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [onRetry, autoRetrySeconds]);

  return (
    <div className="rounded-md border border-error/20 bg-error-subtle px-4 py-3">
      <div className="flex items-center justify-between">
        <p className="text-sm text-error">{message}</p>
        {onRetry && (
          <button
            onClick={onRetry}
            className="ml-4 text-sm font-medium text-error underline hover:no-underline"
          >
            Retry{countdown > 0 ? ` (${countdown}s)` : ""}
          </button>
        )}
      </div>
    </div>
  );
}
