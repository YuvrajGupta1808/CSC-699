import { useEffect, useRef, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Brain, ChevronDown, ChevronUp, Loader2, Send, Trash2 } from "lucide-react";
import { ThinkingLog } from "@/components/ThinkingLog";
import { CandidateComparison } from "@/components/CandidateComparison";
import { useAuth } from "@/contexts/AuthContext";
import { useAdvisorChat, ChatMessage } from "@/hooks/useAdvisorChat";
import { cn } from "@/lib/utils";

function MarkdownText({ text }: { text: string }) {
  const parts = text.split(/(\*\*[^*]+\*\*|`[^`]+`|\n)/g);
  return (
    <>
      {parts.map((seg, i) => {
        if (seg.startsWith("**") && seg.endsWith("**"))
          return <strong key={i}>{seg.slice(2, -2)}</strong>;
        if (seg.startsWith("`") && seg.endsWith("`"))
          return (
            <code key={i} className="rounded bg-muted px-1 py-0.5 font-mono text-xs">
              {seg.slice(1, -1)}
            </code>
          );
        if (seg === "\n") return <br key={i} />;
        return <span key={i}>{seg}</span>;
      })}
    </>
  );
}

function SourcesPanel({ sources }: { sources: ChatMessage["sources"] }) {
  const [open, setOpen] = useState(false);
  if (!sources || (sources.jobs.length === 0 && sources.courses.length === 0)) return null;
  return (
    <div className="mt-1.5 rounded-lg bg-muted/50 text-xs overflow-hidden">
      <button
        onClick={() => setOpen((o) => !o)}
        className="flex w-full items-center gap-1.5 px-3 py-2 text-muted-foreground hover:text-foreground transition-colors"
      >
        {open ? <ChevronUp className="h-3 w-3" /> : <ChevronDown className="h-3 w-3" />}
        {sources.jobs.length} job{sources.jobs.length !== 1 ? "s" : ""},{" "}
        {sources.courses.length} course{sources.courses.length !== 1 ? "s" : ""}
      </button>
      {open && (
        <div className="px-3 pb-3 space-y-2 border-t border-border/50">
          <div className="pt-2" />
          {sources.jobs.map((j, i) => (
            <div key={i}>
              <span className="font-medium text-foreground">{j.title} @ {j.company}</span>
              {j.gaps.length > 0 && <div className="text-destructive/80 mt-0.5">Gaps: {j.gaps.slice(0, 4).join(", ")}</div>}
              {j.covered.length > 0 && <div className="text-green-700 dark:text-green-400 mt-0.5">Covered: {j.covered.slice(0, 4).join(", ")}</div>}
            </div>
          ))}
          {sources.courses.map((c, i) => (
            <div key={i}>
              <span className="font-medium text-foreground">{c.course_code}: {c.title}</span>
              {c.teaches.length > 0 && <div className="text-muted-foreground mt-0.5">Teaches: {c.teaches.join(", ")}</div>}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}



function Bubble({ msg }: { msg: ChatMessage }) {
  const isUser = msg.role === "user";
  const hasContent = (msg.content ?? "").length > 0;
  const isThinking = msg.streaming && !hasContent;

  return (
    <div className={cn("flex flex-col gap-1", isUser ? "items-end" : "items-start w-full")}>
      {/* Content bubble — spinner while thinking, text while streaming/done */}
      <div className={cn(
        "max-w-[90%] rounded-2xl px-3.5 py-2.5 text-sm leading-relaxed",
        isUser
          ? "bg-primary text-primary-foreground rounded-tr-sm"
          : "bg-white border border-border/60 text-foreground shadow-sm rounded-tl-sm",
      )}>
        {isThinking ? (
          <span className="flex items-center gap-1.5 text-muted-foreground">
            <Loader2 className="h-3.5 w-3.5 animate-spin" />
            <span className="text-xs">{(msg.status ?? []).at(-1) ?? "Thinking…"}</span>
          </span>
        ) : hasContent ? (
          <>
            <MarkdownText text={msg.content ?? ""} />
            {msg.streaming && (
              <span className="ml-0.5 inline-block h-3.5 w-0.5 animate-pulse bg-current" />
            )}
          </>
        ) : null}
      </div>

      {/* After complete: planning steps + candidate comparison + sources */}
      {!isUser && !msg.streaming && (
        <>
          <ThinkingLog steps={msg.status ?? []} compact />
          {msg.candidates && (
            <CandidateComparison
              selected={msg.candidates.selected}
              all={msg.candidates.all}
              compact
            />
          )}
          <SourcesPanel sources={msg.sources} />
        </>
      )}
    </div>
  );
}

interface InlineAdvisorChatProps {
  jobId: string;
  jobTitle: string;
}

export function InlineAdvisorChat({ jobId, jobTitle }: InlineAdvisorChatProps) {
  const { student } = useAuth();
  const [input, setInput] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const { messages, streaming, sendMessage, clearMessages } = useAdvisorChat();

  // Reset when the student or the job being viewed changes
  useEffect(() => {
    clearMessages();
    setInput("");
  }, [student?.student_id, jobId]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  function handleSend() {
    const text = input.trim();
    if (!text || !student || streaming) return;
    setInput("");
    sendMessage(text, student.student_id, jobId);
  }

  return (
    <div className="flex h-full flex-col rounded-2xl bg-[hsl(var(--card))] shadow-md overflow-hidden">
      {/* Header — no bottom border, blends into content */}
      <div className="flex items-center justify-between px-4 pt-4 pb-3">
        <div className="flex items-center gap-2">
          <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-primary/10">
            <Brain className="h-4 w-4 text-primary" />
          </div>
          <span className="text-sm font-semibold text-foreground">Advisor</span>
          <span className="max-w-[130px] truncate rounded-md bg-muted px-2 py-0.5 text-xs text-muted-foreground">
            {jobTitle}
          </span>
        </div>
        {messages.length > 0 && (
          <Button
            variant="ghost"
            size="icon"
            className="h-7 w-7 text-muted-foreground hover:text-foreground"
            onClick={clearMessages}
            title="Clear chat"
          >
            <Trash2 className="h-3.5 w-3.5" />
          </Button>
        )}
      </div>

      {/* Thin divider */}
      <div className="mx-4 h-px bg-border/50" />

      {!student ? (
        <div className="flex flex-1 flex-col items-center justify-center gap-3 p-6 text-center">
          <Brain className="h-10 w-10 text-primary/20" />
          <div>
            <p className="text-sm font-medium text-foreground">Sign in to chat</p>
            <p className="mt-1 text-xs text-muted-foreground">
              Log in with a student profile to ask about this job.
            </p>
          </div>
        </div>
      ) : (
        <>
          {/* Messages */}
          <ScrollArea className="flex-1 px-4 py-3">
            {messages.length === 0 && (
              <div className="flex flex-col items-center justify-center gap-3 py-12 text-center">
                <Brain className="h-8 w-8 text-primary/20" />
                <div>
                  <p className="text-sm font-medium text-foreground">Ask about this job</p>
                  <p className="mt-1.5 text-xs text-muted-foreground leading-relaxed">
                    "Am I a good fit?" · "What skills should I build?" · "How can I prepare?"
                  </p>
                </div>
              </div>
            )}
            <div className="space-y-4">
              {messages.map((msg, i) => (
                <Bubble key={i} msg={msg} />
              ))}
            </div>
            <div ref={bottomRef} />
          </ScrollArea>

          {/* Input — seamless bottom, no visible border */}
          <div className="px-4 pb-4 pt-2">
            <div className="flex items-center gap-2 rounded-xl border border-border/70 bg-background px-3 py-2 focus-within:border-primary/50 focus-within:ring-1 focus-within:ring-primary/20 transition-all">
              <input
                ref={inputRef}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); handleSend(); }
                }}
                placeholder="Ask about this job…"
                className="flex-1 bg-transparent text-sm outline-none placeholder:text-muted-foreground disabled:opacity-50"
                disabled={streaming}
              />
              <button
                onClick={handleSend}
                disabled={!input.trim() || streaming}
                className={cn(
                  "flex h-7 w-7 shrink-0 items-center justify-center rounded-lg transition-colors",
                  input.trim() && !streaming
                    ? "bg-primary text-primary-foreground hover:bg-primary/90"
                    : "text-muted-foreground/40 cursor-not-allowed",
                )}
              >
                {streaming
                  ? <Loader2 className="h-3.5 w-3.5 animate-spin" />
                  : <Send className="h-3.5 w-3.5" />
                }
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
