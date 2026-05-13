import { useEffect, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { ArrowLeft, Briefcase, Building2, MapPin } from "lucide-react";
import { Link, useParams } from "react-router-dom";
import { InlineAdvisorChat } from "@/components/InlineAdvisorChat";

interface RealJobDetail {
  job_id: string;
  title: string;
  company: string;
  location: string;
  source: string;
  skills: string[];
  posted_at: string | null;
  ingested_at: string | null;
}

function DetailSkeleton() {
  return (
    <div className="space-y-4">
      <Skeleton className="h-8 w-2/3" />
      <Skeleton className="h-4 w-1/2" />
      <Skeleton className="h-32 w-full" />
    </div>
  );
}

export default function JobBreakdown() {
  const { id } = useParams<{ id: string }>();
  const [job, setJob] = useState<RealJobDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [notFound, setNotFound] = useState(false);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    setNotFound(false);
    fetch(`/api/jobs/${id}`)
      .then((r) => {
        if (r.status === 404 || !r.ok) { setNotFound(true); return null; }
        return r.json();
      })
      .then((data) => { if (data) setJob(data); })
      .catch(() => setNotFound(true))
      .finally(() => setLoading(false));
  }, [id]);

  if (notFound && !loading) {
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
    <div className="container mx-auto max-w-6xl px-4 py-8">
      <Button variant="ghost" size="sm" asChild className="mb-6">
        <Link to="/jobs">
          <ArrowLeft className="mr-1 h-4 w-4" /> Back to Jobs
        </Link>
      </Button>

      <div className="flex flex-col gap-6 lg:flex-row lg:items-start">
        {/* Left: job details */}
        <div className="flex-1 space-y-6 lg:max-w-[60%]">
          {loading ? (
            <DetailSkeleton />
          ) : job ? (
            <>
              {/* Job header */}
              <div>
                <h1 className="font-serif text-3xl font-bold text-foreground">{job.title}</h1>
                <div className="mt-2 flex flex-wrap items-center gap-4 text-sm text-muted-foreground">
                  <span className="flex items-center gap-1.5">
                    <Building2 className="h-4 w-4" />
                    {job.company}
                  </span>
                  {job.location && (
                    <span className="flex items-center gap-1.5">
                      <MapPin className="h-4 w-4" />
                      {job.location}
                    </span>
                  )}
                  {job.source && (
                    <span className="flex items-center gap-1.5">
                      <Briefcase className="h-4 w-4" />
                      via {job.source}
                    </span>
                  )}
                </div>
              </div>

              {/* Required skills */}
              <Card>
                <CardHeader className="pb-3">
                  <CardTitle className="text-base">Required Skills</CardTitle>
                </CardHeader>
                <CardContent>
                  {job.skills.length === 0 ? (
                    <p className="text-sm text-muted-foreground">No skills extracted for this job.</p>
                  ) : (
                    <div className="flex flex-wrap gap-2">
                      {job.skills.map((skill) => (
                        <Badge key={skill} variant="secondary" className="text-sm">
                          {skill}
                        </Badge>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>

              {/* Meta info */}
              <Card>
                <CardHeader className="pb-3">
                  <CardTitle className="text-base">Job Details</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Source</span>
                    <span className="font-medium capitalize">{job.source || "—"}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Location</span>
                    <span className="font-medium">{job.location || "—"}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Skills extracted</span>
                    <span className="font-medium">{job.skills.length}</span>
                  </div>
                  {job.ingested_at && (
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Indexed</span>
                      <span className="font-medium">
                        {new Date(job.ingested_at).toLocaleDateString()}
                      </span>
                    </div>
                  )}
                </CardContent>
              </Card>
            </>
          ) : null}
        </div>

        {/* Right: inline advisor chat */}
        <div className="w-full lg:w-[38%] lg:sticky lg:top-20" style={{ minHeight: "600px" }}>
          {loading ? (
            <Skeleton className="h-full w-full rounded-xl" style={{ minHeight: "600px" }} />
          ) : job ? (
            <div style={{ height: "600px" }}>
              <InlineAdvisorChat jobId={job.job_id} jobTitle={job.title} />
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
}
