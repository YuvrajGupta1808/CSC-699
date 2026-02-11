import { SkillBar } from "@/components/SkillBar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { mockJobs } from "@/data/mock-data";
import { ArrowLeft } from "lucide-react";
import { Link, useParams } from "react-router-dom";

const methodColors: Record<string, string> = {
  "keyword-based": "bg-chart-5/20 text-chart-5 border-chart-5/30",
  "embedding-based": "bg-chart-3/20 text-chart-3 border-chart-3/30",
  "llm-extracted": "bg-primary/20 text-primary border-primary/30",
};

export default function JobBreakdown() {
  const { id } = useParams();
  const job = mockJobs.find((j) => j.id === id);

  if (!job) {
    return (
      <div className="container mx-auto px-4 py-16 text-center">
        <p className="text-muted-foreground">Job not found.</p>
        <Button variant="outline" asChild className="mt-4">
          <Link to="/jobs">Back to Jobs</Link>
        </Button>
      </div>
    );
  }

  return (
    <div className="container mx-auto max-w-3xl px-4 py-8">
      <Button variant="ghost" size="sm" asChild className="mb-6">
        <Link to="/jobs">
          <ArrowLeft className="mr-1 h-4 w-4" /> Back to Jobs
        </Link>
      </Button>

      <div className="mb-8 flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="font-serif text-3xl font-bold text-foreground">{job.title}</h1>
          <p className="mt-1 text-muted-foreground">
            {job.company} · {job.location}
          </p>
        </div>
        <div className="text-right">
          <div className="text-3xl font-bold text-primary">{job.matchScore}%</div>
          <div className="text-sm text-muted-foreground">match score</div>
        </div>
      </div>

      {/* Extraction Method */}
      <Card className="mb-6">
        <CardHeader className="pb-3">
          <CardTitle className="text-base">⚙️ Extraction Method</CardTitle>
        </CardHeader>
        <CardContent>
          <Badge
            variant="outline"
            className={`${methodColors[job.extractionMethod]} border text-sm`}
          >
            {job.extractionMethod}
          </Badge>
          <p className="mt-2 text-sm text-muted-foreground">
            Skills were extracted using the <strong>{job.extractionMethod}</strong> approach.
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-base">🧠 Extracted Job Skills</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {job.skills.map((group) => (
            <div key={group.category}>
              <h4 className="mb-3 text-sm font-semibold uppercase tracking-wider text-muted-foreground">
                {group.category}
              </h4>
              <div className="space-y-3">
                {group.skills.map((skill) => (
                  <SkillBar
                    key={skill.name}
                    name={skill.name}
                    confidence={skill.confidence}
                    status={skill.status}
                  />
                ))}
              </div>
            </div>
          ))}
        </CardContent>
      </Card>



    </div>
  );
}
