import { cn } from "@/lib/utils";
import type { SkillGroup } from "@/data/mock-data";

interface MatchMatrixProps {
  skillGroups: SkillGroup[];
}

export function MatchMatrix({ skillGroups }: MatchMatrixProps) {
  return (
    <div className="space-y-6">
      {skillGroups.map((group) => (
        <div key={group.category}>
          <h4 className="mb-3 text-sm font-semibold uppercase tracking-wider text-muted-foreground">
            {group.category}
          </h4>
          <div className="flex flex-wrap gap-2">
            {group.skills.map((skill) => (
              <div
                key={skill.name}
                className={cn(
                  "rounded-lg border px-3 py-2 text-sm font-medium transition-colors",
                  skill.status === "covered" &&
                    "border-primary/30 bg-primary/10 text-primary",
                  skill.status === "partial" &&
                    "border-chart-4/30 bg-chart-4/10 text-chart-4",
                  skill.status === "missing" &&
                    "border-destructive/30 bg-destructive/10 text-destructive"
                )}
              >
                {skill.name}
              </div>
            ))}
          </div>
        </div>
      ))}
      <div className="flex items-center gap-4 rounded-lg border border-border bg-card p-3 text-xs text-muted-foreground">
        <span className="flex items-center gap-1.5">
          <span className="h-3 w-3 rounded-sm bg-primary/20 border border-primary/30" /> Covered
        </span>
        <span className="flex items-center gap-1.5">
          <span className="h-3 w-3 rounded-sm bg-chart-4/20 border border-chart-4/30" /> Partial
        </span>
        <span className="flex items-center gap-1.5">
          <span className="h-3 w-3 rounded-sm bg-destructive/20 border border-destructive/30" /> Missing
        </span>
      </div>
    </div>
  );
}
