import { useState } from "react";
import { ChevronDown, ChevronUp, ListTree } from "lucide-react";
import { cn } from "@/lib/utils";

interface ThinkingLogProps {
  steps: string[];
  compact?: boolean;
}

/**
 * Shown only after a response is fully complete.
 * Starts collapsed — user can open it to see the planning steps.
 */
export function ThinkingLog({ steps, compact = false }: ThinkingLogProps) {
  const [open, setOpen] = useState(false);

  if (!steps.length) return null;

  return (
    <div className={cn("w-full", compact ? "max-w-full" : "max-w-[80%]")}>
      <button
        onClick={() => setOpen((o) => !o)}
        className={cn(
          "flex items-center gap-2 rounded-lg px-3 py-1.5 text-left transition-colors",
          "text-muted-foreground hover:text-foreground",
          compact ? "text-xs" : "text-xs",
        )}
      >
        <ListTree className="h-3 w-3 shrink-0 text-muted-foreground/60" />
        <span className="font-medium">
          {open ? "Hide" : "Show"} planning steps ({steps.length})
        </span>
        {open
          ? <ChevronUp className="h-3 w-3 shrink-0" />
          : <ChevronDown className="h-3 w-3 shrink-0" />
        }
      </button>

      {open && (
        <div className="mt-1 rounded-lg bg-muted/40 px-3 py-2.5 space-y-1.5">
          {steps.map((step, i) => (
            <div key={i} className="flex items-start gap-2 text-xs text-muted-foreground">
              <span className="mt-0.5 shrink-0 font-mono text-muted-foreground/40">{i + 1}.</span>
              <span className="leading-relaxed">{step}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
