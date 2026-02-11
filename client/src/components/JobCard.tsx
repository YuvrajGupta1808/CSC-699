import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import type { Job } from "@/data/mock-data";
import { cn } from "@/lib/utils";
import { Building2, MapPin } from "lucide-react";
import { Link } from "react-router-dom";

interface JobCardProps {
  job: Job;
}

function scoreColor(score: number) {
  if (score >= 80) return "text-primary";
  if (score >= 60) return "text-chart-4";
  return "text-destructive";
}

export function JobCard({ job }: JobCardProps) {
  return (
    <Link to={`/jobs/${job.id}`} className="block mb-6">
      <Card className="group cursor-pointer border border-border bg-white shadow-sm transition-all duration-200 hover:border-primary/40 hover:shadow-lg">
        <CardContent className="p-6">
          <div className="flex items-start justify-between gap-4">
            <div className="min-w-0 flex-1 space-y-2">
              <h3 className="text-lg font-semibold text-foreground group-hover:text-primary transition-colors">
                {job.title}
              </h3>
              <div className="flex flex-wrap items-center gap-4 text-sm text-muted-foreground">
                <span className="flex items-center gap-1.5">
                  <Building2 className="h-4 w-4" />
                  {job.company}
                </span>
                <span className="flex items-center gap-1.5">
                  <MapPin className="h-4 w-4" />
                  {job.location}
                </span>
              </div>
            </div>
            <div className="text-right">
              <div className={cn("text-3xl font-bold", scoreColor(job.matchScore))}>
                {job.matchScore}%
              </div>
              <div className="text-xs text-muted-foreground">match</div>
            </div>
          </div>
          <div className="mt-4 flex flex-wrap gap-2">
            {job.topSkills.map((skill) => (
              <Badge key={skill} variant="secondary" className="text-xs px-3 py-1">
                {skill}
              </Badge>
            ))}
          </div>
        </CardContent>
      </Card>
    </Link>
  );
}
