import { useEffect, useRef, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Brain, ChevronDown, ChevronUp, Loader2, Send } from "lucide-react";
import { ThinkingLog } from "@/components/ThinkingLog";
import { CandidateComparison } from "@/components/CandidateComparison";
import { useAuth } from "@/contexts/AuthContext";
import { useAdvisorChat, ChatMessage } from "@/hooks/useAdvisorChat";
import { cn } from "@/lib/utils";
import { Link } from "react-router-dom";

// ---------------------------------------------------------------------------
// Markdown renderer — bold, inline code, newlines
// ---------------------------------------------------------------------------
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

// ---------------------------------------------------------------------------
// Sources expandable
// ---------------------------------------------------------------------------
function SourcesPanel({ sources }: { sources: ChatMessage["sources"] }) {
  const [open, setOpen] = useState(false);
  if (!sources || (sources.jobs.length === 0 && sources.courses.length === 0)) return null;
  return (
    <div className="mt-2 rounded-lg border border-border bg-card">
      <button
        onClick={() => setOpen((o) => !o)}
        className="flex w-full items-center gap-2 px-4 py-2.5 text-xs font-medium text-muted-foreground hover:text-foreground"
      >
        {open ? <ChevronUp className="h-3 w-3" /> : <ChevronDown className="h-3 w-3" />}
        Evidence — {sources.jobs.length} job{sources.jobs.length !== 1 ? "s" : ""},{" "}
        {sources.courses.length} course{sources.courses.length !== 1 ? "s" : ""}
      </button>
      {open && (
        <div className="border-t border-border px-4 pb-4 pt-3 space-y-3 text-xs">
          {sources.jobs.length > 0 && (
            <div>
              <p className="mb-1.5 font-semibold text-foreground">Jobs</p>
              {sources.jobs.map((j, i) => (
                <div key={i} className="mb-2 text-muted-foreground">
                  <span className="font-medium text-foreground">{j.title} @ {j.company}</span>{" "}
                  <span className="text-primary">({j.score.toFixed(2)})</span>
                  {j.covered.length > 0 && <div className="text-green-700">✓ {j.covered.join(", ")}</div>}
                  {j.gaps.length > 0 && <div className="text-destructive">✗ {j.gaps.join(", ")}</div>}
                </div>
              ))}
            </div>
          )}
          {sources.courses.length > 0 && (
            <div>
              <p className="mb-1.5 font-semibold text-foreground">Courses</p>
              {sources.courses.map((c, i) => (
                <div key={i} className="mb-1 text-muted-foreground">
                  <span className="font-medium text-foreground">{c.course_code}: {c.title}</span>{" "}
                  <span className="text-primary">({c.score.toFixed(2)})</span>
                  {c.teaches.length > 0 && <div>Teaches: {c.teaches.join(", ")}</div>}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}


// ---------------------------------------------------------------------------
// Message bubble — thinking phase first, then content
// ---------------------------------------------------------------------------
function MessageBubble({ msg }: { msg: ChatMessage }) {
  const isUser = msg.role === "user";
  const hasContent = msg.content.length > 0;
  const isThinking = msg.streaming && !hasContent;

  return (
    <div className={cn("flex", isUser ? "justify-end" : "justify-start")}>
      <div className={cn(
        "flex flex-col gap-1.5",
        isUser ? "items-end max-w-[75%]" : "items-start w-full max-w-[80%]",
      )}>
        {/* Content bubble — shows spinner while thinking, content while streaming */}
        <div className={cn(
          "rounded-2xl px-4 py-2.5 text-sm leading-relaxed",
          isUser
            ? "bg-primary text-primary-foreground rounded-tr-sm"
            : "bg-card border border-border text-foreground rounded-tl-sm",
        )}>
          {isThinking ? (
            <span className="flex items-center gap-2 text-muted-foreground">
              <Loader2 className="h-4 w-4 animate-spin" />
              <span className="text-xs">
                {(msg.status ?? []).at(-1) ?? "Thinking…"}
              </span>
            </span>
          ) : hasContent ? (
            <>
              <MarkdownText text={msg.content} />
              {msg.streaming && (
                <span className="ml-0.5 inline-block h-4 w-0.5 animate-pulse bg-current" />
              )}
            </>
          ) : null}
        </div>

        {/* After streaming ends: planning steps + candidate comparison + sources */}
        {!isUser && !msg.streaming && (
          <>
            <ThinkingLog steps={msg.status ?? []} />
            {msg.candidates && (
              <CandidateComparison
                selected={msg.candidates.selected}
                all={msg.candidates.all}
              />
            )}
            <SourcesPanel sources={msg.sources} />
          </>
        )}
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Starter prompts
// ---------------------------------------------------------------------------
const STARTER_PROMPTS = [
  "What jobs fit my current skills?",
  "Where are my biggest skill gaps?",
  "What courses should I take next?",
  "How can I break into machine learning?",
];

// ---------------------------------------------------------------------------
// Page
// ---------------------------------------------------------------------------
export default function Chat() {
  const { student } = useAuth();
  const [input, setInput] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const { messages, streaming, sendMessage, clearMessages } = useAdvisorChat();

  // Reset conversation whenever the logged-in student changes
  useEffect(() => {
    clearMessages();
    setInput("");
  }, [student?.student_id]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    inputRef.current?.focus();
  }, [student]);

  function handleSend(text?: string) {
    const msg = (text ?? input).trim();
    if (!msg || !student || streaming) return;
    setInput("");
    sendMessage(msg, student.student_id, null);
  }

  return (
    <div className="flex h-[calc(100vh-3.5rem)] flex-col">
      <div className="flex-1 overflow-y-auto bg-background [&::-webkit-scrollbar]:hidden" style={{ scrollbarWidth: "none" }}>
        <div className="mx-auto max-w-3xl px-4 py-6">
          {!student ? (
            <div className="flex flex-col items-center justify-center gap-4 py-24 text-center">
              <Brain className="h-16 w-16 text-primary/20" />
              <div>
                <h2 className="font-serif text-xl font-semibold text-foreground">Sign in to start</h2>
                <p className="mt-2 text-sm text-muted-foreground max-w-sm">
                  Log in with a student profile to get personalized career advice, skill gap analysis,
                  and course recommendations.
                </p>
              </div>
            </div>
          ) : messages.length === 0 ? (
            <div className="flex flex-col items-center gap-6 py-16 text-center">
              <div>
                <Brain className="mx-auto mb-4 h-12 w-12 text-primary/20" />
                <h2 className="font-serif text-xl font-semibold text-foreground">
                  Hi, {student.name.split(" ")[0]}!
                </h2>
                <p className="mt-2 text-sm text-muted-foreground">
                  Ask me about jobs that fit your skills, where your gaps are, or what to learn next.
                </p>
              </div>
              <div className="grid w-full max-w-md gap-2 sm:grid-cols-2">
                {STARTER_PROMPTS.map((p) => (
                  <button
                    key={p}
                    onClick={() => handleSend(p)}
                    className="rounded-xl border border-border bg-card px-4 py-3 text-left text-sm text-muted-foreground transition-colors hover:border-primary/40 hover:text-foreground"
                  >
                    {p}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <div className="space-y-6">
              {messages.map((msg, i) => (
                <MessageBubble key={i} msg={msg} />
              ))}
            </div>
          )}
          <div ref={bottomRef} />
        </div>
      </div>

      {student && (
        <div className="border-t border-border bg-card px-6 py-4">
          <div className="mx-auto flex max-w-3xl gap-3">
            <Input
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); handleSend(); }
              }}
              placeholder="Ask about jobs, skills, or your learning path…"
              className="flex-1"
              disabled={streaming}
            />
            <Button
              onClick={() => handleSend()}
              disabled={!input.trim() || streaming}
              className="shrink-0 gap-2"
            >
              {streaming
                ? <Loader2 className="h-4 w-4 animate-spin" />
                : <Send className="h-4 w-4" />
              }
              {!streaming && <span className="hidden sm:inline">Send</span>}
            </Button>
          </div>
          <p className="mx-auto mt-2 max-w-3xl text-center text-xs text-muted-foreground">
            Powered by your academic profile and real job postings. Browse{" "}
            <Link to="/jobs" className="text-primary hover:underline">jobs</Link> or check your{" "}
            <Link to="/profile" className="text-primary hover:underline">profile</Link>.
          </p>
        </div>
      )}
    </div>
  );
}
