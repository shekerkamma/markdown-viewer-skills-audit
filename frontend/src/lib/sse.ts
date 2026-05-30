import { getToken } from "./auth";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface SSEEvent {
  id: string;
  agent_name: string;
  event_type: string;
  payload: Record<string, unknown>;
  timestamp: string;
}

export function createEventStream(
  teamId: string,
  onEvent: (event: SSEEvent) => void,
  onError?: () => void
): () => void {
  const token = getToken();
  if (!token) return () => {};

  // EventSource doesn't support custom headers, so we use fetch-based SSE
  const controller = new AbortController();

  async function connect() {
    try {
      const response = await fetch(
        `${API_URL}/api/v1/teams/${teamId}/events/stream`,
        {
          headers: { Authorization: `Bearer ${token}` },
          signal: controller.signal,
        }
      );

      if (!response.ok || !response.body) {
        onError?.();
        return;
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            try {
              const data = JSON.parse(line.slice(6));
              if (!data.error) {
                onEvent(data as SSEEvent);
              }
            } catch {
              // skip malformed events
            }
          }
        }
      }
    } catch (e) {
      if ((e as Error).name !== "AbortError") {
        onError?.();
      }
    }
  }

  connect();

  return () => controller.abort();
}
