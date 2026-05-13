import { useState } from "react";
import { ChevronDown, ChevronUp, Trophy } from "lucide-react";
import { CandidateResult } from "@/hooks/useAdvisorChat";
import { cn } from "@/lib/utils";

interface CandidateComparisonProps {
  selected: CandidateResult;
  all: CandidateResult[];
  compact?: boolean;
}

function ScoreBar({ value, max = 10 }: { value: number; max?: number }) {
  return (
    <div className="h-1 w-full overflow-hidden rounded-full bg-muted">
      <div
        className="h-full rounded-full bg-primary/60 transition-all"
        style={{ width: `${(value / max) * 100}%` }}
      />
    </div>
  );
}

export function CandidateComparison({ selected, all, compact = false }: CandidateComparisonProps) {
  const [open, setOpen] = useState(false);

  if (!all.length) return null;

  return (
    <div className={cn("w-full", compact ? "max-w-full" : "max-w-[80%]")}>
      <button
        onClick={() => setOpen((o) => !o)}
        className="flex items-center gap-2 rounded-lg px-3 py-1.5 text-xs text-muted-foreground hover:text-foreground transition-colors"
      >
        <Trophy className="h-3 w-3 shrink-0 text-primary/60" />
        <span className="font-medium">
          Self-RAG selection — {selected.label} won ({selected.total}/10)
        </span>
        {open ? <ChevronUp className="h-3 w-3 shrink-0" /> : <ChevronDown className="h-3 w-3 shrink-0" />}
      </button>

      {open && (
        <div className="mt-1 rounded-lg bg-muted/40 px-3 py-3 space-y-3">
          {all.map((c) => (
            <div key={c.label} className={cn("space-y-1.5 rounded-lg p-2", c.selected && "bg-primary/5 ring-1 ring-primary/20")}>
              <div className="flex items-center justify-between gap-2">
                <div className="flex items-center gap-1.5 min-w-0">
                  {c.selected && <Trophy className="h-3 w-3 shrink-0 text-primary" />}
                  <span className={cn("text-xs font-semibold truncate", c.selected ? "text-foreground" : "text-muted-foreground")}>
                    {c.label}
                  </span>
                  <span className="text-xs text-muted-foreground truncate hidden sm:inline">— {c.evidence}</span>
                </div>
                <span className={cn("text-xs font-bold tabular-nums shrink-0", c.selected ? "text-primary" : "text-muted-foreground")}>
                  {c.total}/10
                </span>
              </div>

              <div className="grid grid-cols-3 gap-2 text-xs text-muted-foreground">
                <div>
                  <div className="mb-0.5 flex justify-between">
                    <span>Relevance</span><span>{c.relevance}</span>
                  </div>
                  <ScoreBar value={c.relevance} />
                </div>
                <div>
                  <div className="mb-0.5 flex justify-between">
                    <span>Support</span><span>{c.support}</span>
                  </div>
                  <ScoreBar value={c.support} />
                </div>
                <div>
                  <div className="mb-0.5 flex justify-between">
                    <span>Utility</span><span>{c.utility}</span>
                  </div>
                  <ScoreBar value={c.utility} />
                </div>
              </div>

              {c.selected && c.critique && (
                <p className="text-xs text-muted-foreground italic leading-relaxed pt-0.5">
                  "{c.critique}"
                </p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
