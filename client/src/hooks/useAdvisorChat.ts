import { useState, useRef, useCallback } from "react";

export interface ChatSource {
  title: string;
  company: string;
  score: number;
  covered: string[];
  gaps: string[];
}

export interface ChatCourse {
  course_code: string;
  title: string;
  score: number;
  teaches: string[];
}

export interface ChatScores {
  relevance: number;
  support: number;
  utility: number;
  total: number;
  critique?: string;
}

export interface CandidateResult {
  label: string;
  evidence: string;
  total: number;
  relevance: number;
  support: number;
  utility: number;
  critique: string;
  selected: boolean;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  status?: string[];
  sources?: { jobs: ChatSource[]; courses: ChatCourse[] };
  candidates?: { selected: CandidateResult; all: CandidateResult[] };
  streaming?: boolean;
}

export function useAdvisorChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [streaming, setStreaming] = useState(false);
  const sessionIdRef = useRef(`ui-${crypto.randomUUID()}`);
  const abortRef = useRef<AbortController | null>(null);

  const sendMessage = useCallback(
    async (
      text: string,
      studentId: string,
      selectedJobId?: string | null,
    ) => {
      if (streaming) return;

      const history = messages.map((m) => ({ role: m.role, content: m.content }));
      setMessages((prev) => [...prev, { role: "user", content: text }]);
      setStreaming(true);

      const assistantIdx = messages.length + 1;
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "", status: [], streaming: true },
      ]);

      abortRef.current = new AbortController();

      try {
        const response = await fetch("/api/chat/stream", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            student_id: studentId,
            message: text,
            session_id: sessionIdRef.current,
            selected_job_id: selectedJobId ?? null,
            conversation_history: history,
          }),
          signal: abortRef.current.signal,
        });

        const reader = response.body!.getReader();
        const decoder = new TextDecoder();
        let buffer = "";

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          buffer += decoder.decode(value, { stream: true });

          const lines = buffer.split("\n\n");
          buffer = lines.pop() ?? "";

          for (const block of lines) {
            const dataLine = block.trim();
            if (!dataLine.startsWith("data: ")) continue;
            const raw = dataLine.slice(6);
            let event: Record<string, unknown>;
            try {
              event = JSON.parse(raw);
            } catch {
              continue;
            }

            const { type } = event;

            if (type === "status") {
              setMessages((prev) => {
                const copy = [...prev];
                const msg = { ...copy[assistantIdx] };
                msg.status = [...(msg.status ?? []), event.message as string];
                copy[assistantIdx] = msg;
                return copy;
              });
            } else if (type === "token") {
              setMessages((prev) => {
                const copy = [...prev];
                const msg = { ...copy[assistantIdx] };
                msg.content = msg.content + (event.content as string);
                copy[assistantIdx] = msg;
                return copy;
              });
            } else if (type === "sources") {
              setMessages((prev) => {
                const copy = [...prev];
                const msg = { ...copy[assistantIdx] };
                msg.sources = {
                  jobs: (event.jobs as ChatSource[]) ?? [],
                  courses: (event.courses as ChatCourse[]) ?? [],
                };
                copy[assistantIdx] = msg;
                return copy;
              });
            } else if (type === "candidates") {
              setMessages((prev) => {
                const copy = [...prev];
                const msg = { ...copy[assistantIdx] };
                msg.candidates = {
                  selected: event.selected as CandidateResult,
                  all: event.all as CandidateResult[],
                };
                copy[assistantIdx] = msg;
                return copy;
              });
            } else if (type === "done") {
              setMessages((prev) => {
                const copy = [...prev];
                const msg = { ...copy[assistantIdx] };
                msg.streaming = false;
                copy[assistantIdx] = msg;
                return copy;
              });
            } else if (type === "error") {
              setMessages((prev) => {
                const copy = [...prev];
                const msg = { ...copy[assistantIdx] };
                msg.content = `Error: ${event.message}`;
                msg.streaming = false;
                copy[assistantIdx] = msg;
                return copy;
              });
            }
          }
        }
      } catch (err: unknown) {
        if (err instanceof Error && err.name !== "AbortError") {
          setMessages((prev) => {
            const copy = [...prev];
            const msg = { ...copy[assistantIdx] };
            msg.content = "Connection error. Is the server running?";
            msg.streaming = false;
            copy[assistantIdx] = msg;
            return copy;
          });
        }
      } finally {
        setStreaming(false);
        setMessages((prev) => {
          const copy = [...prev];
          if (copy[assistantIdx]) {
            copy[assistantIdx] = { ...copy[assistantIdx], streaming: false };
          }
          return copy;
        });
      }
    },
    [messages, streaming],
  );

  const clearMessages = useCallback(() => {
    setMessages([]);
    sessionIdRef.current = `ui-${crypto.randomUUID()}`;
  }, []);

  const abort = useCallback(() => {
    abortRef.current?.abort();
  }, []);

  return { messages, streaming, sendMessage, clearMessages, abort };
}
