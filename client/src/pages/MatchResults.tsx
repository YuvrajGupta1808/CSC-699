import { MatchMatrix } from "@/components/MatchMatrix";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { mockJobs } from "@/data/mock-data";
import { ArrowLeft } from "lucide-react";
import { Link, useParams } from "react-router-dom";

export default function MatchResults() {
  const { id } = useParams();
  const job = id ? mockJobs.find((j) => j.id === id) : mockJobs[0];

  if (!job) {
    return (
      <div className="container mx-auto px-4 py-16 text-center">
        <p className="text-muted-foreground">No match data found.</p>
        <Button variant="outline" asChild className="mt-4">
          <Link to="/jobs">Browse Jobs</Link>
        </Button>
      </div>
    );
  }

  const clusterScores = job.skills.map((group) => {
    const avg = Math.round(
      group.skills.reduce((sum, s) => sum + s.confidence, 0) / group.skills.length
    );
    const coveredCount = group.skills.filter((s) => s.status === "covered").length;
    return { category: group.category, avg, covered: coveredCount, total: group.skills.length };
  });

  const overallCovered = job.skills.flatMap((g) => g.skills).filter((s) => s.status === "covered").length;
  const overallTotal = job.skills.flatMap((g) => g.skills).length;

  return (
    <div className="container mx-auto max-w-4xl px-4 py-8">
      <Button variant="ghost" size="sm" asChild className="mb-6">
        <Link to={id ? `/jobs/${id}` : "/jobs"}>
          <ArrowLeft className="mr-1 h-4 w-4" /> Back
        </Link>
      </Button>

      <div className="mb-8 text-center">
        <h1 className="font-serif text-3xl font-bold text-foreground">
          Here's how well you match this role.
        </h1>
        <p className="mt-2 text-lg text-muted-foreground">
          {job.title} at {job.company}
        </p>
        <div className="mt-4 inline-flex items-baseline gap-1 rounded-full border border-primary/20 bg-accent px-5 py-2">
          <span className="text-4xl font-bold text-primary">{job.matchScore}%</span>
          <span className="text-sm text-accent-foreground">overall alignment</span>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-5">
        <Card className="lg:col-span-3">
          <CardHeader className="pb-3">
            <CardTitle className="text-base">Skill Match Matrix</CardTitle>
          </CardHeader>
          <CardContent>
            <MatchMatrix skillGroups={job.skills} />
          </CardContent>
        </Card>

        <Card className="lg:col-span-2">
          <CardHeader className="pb-3">
            <CardTitle className="text-base">Score Breakdown</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="rounded-lg border border-border bg-background p-4 text-center">
              <div className="text-sm text-muted-foreground">Skills Covered</div>
              <div className="mt-1 text-2xl font-bold text-foreground">
                {overallCovered} / {overallTotal}
              </div>
            </div>

            {clusterScores.map((c) => (
              <div key={c.category} className="space-y-1">
                <div className="flex items-center justify-between text-sm">
                  <span className="font-medium text-foreground">{c.category}</span>
                  <span className="text-muted-foreground">
                    {c.covered}/{c.total} skills · {c.avg}%
                  </span>
                </div>
                <div className="h-2 w-full overflow-hidden rounded-full bg-muted/30">
                  <div
                    className="h-full rounded-full bg-primary transition-all"
                    style={{ width: `${c.avg}%` }}
                  />
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
