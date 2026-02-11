import { cn } from "@/lib/utils";

interface SkillBarProps {
  name: string;
  confidence: number;
  status?: "covered" | "partial" | "missing";
}

export function SkillBar({ name, confidence, status }: SkillBarProps) {
  const barColor =
    status === "covered"
      ? "bg-primary"
      : status === "partial"
      ? "bg-chart-4"
      : "bg-destructive";

  return (
    <div className="space-y-1">
      <div className="flex items-center justify-between text-sm">
        <span className="font-medium text-foreground">{name}</span>
        <span className="text-muted-foreground">{confidence}%</span>
      </div>
      <div className="h-2 w-full overflow-hidden rounded-full bg-muted/30">
        <div
          className={cn("h-full rounded-full transition-all duration-500", barColor)}
          style={{ width: `${confidence}%` }}
        />
      </div>
    </div>
  );
}
