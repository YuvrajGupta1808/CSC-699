import { Button } from "@/components/ui/button";
import { ArrowRight, BookOpen, Brain, Target, Upload } from "lucide-react";
import { Link } from "react-router-dom";

const steps = [
  {
    icon: Upload,
    step: "01",
    title: "Upload Your Profile",
    description: "Submit your transcript and resume to build your academic profile.",
  },
  {
    icon: Brain,
    step: "02",
    title: "Analyze Job Postings",
    description: "Our engine extracts skills from real job postings using natural language processing.",
  },
  {
    icon: Target,
    step: "03",
    title: "See Your Match",
    description: "Get a detailed alignment score and know exactly where you stand.",
  },
  {
    icon: BookOpen,
    step: "04",
    title: "Close the Gaps",
    description: "Discover which courses to take next to boost your match.",
  },
];

export default function Index() {
  return (
    <div className="flex min-h-[calc(100vh-3.5rem)] flex-col">
      <section className="flex flex-1 items-center justify-center px-4 py-24">
        <div className="mx-auto max-w-2xl text-center">
          <p className="mb-4 text-sm font-medium uppercase tracking-widest text-primary">
            Intelligent Career Alignment
          </p>
          <h1 className="mb-6 font-serif text-4xl font-bold leading-tight tracking-tight text-foreground sm:text-5xl">
            Find jobs that fit your skills.
            <br />
            <span className="text-muted-foreground">Learn what's missing.</span>
          </h1>
          <p className="mx-auto mb-10 max-w-lg text-muted-foreground">
            Upload your transcript and resume. We'll match you to real job postings and show you exactly which skills to develop.
          </p>
          <div className="flex flex-wrap items-center justify-center gap-3">
            <Button size="lg" asChild>
              <Link to="/upload" className="gap-2">
                Get Started
                <ArrowRight className="h-4 w-4" />
              </Link>
            </Button>
            <Button variant="outline" size="lg" asChild>
              <Link to="/jobs">Browse Jobs</Link>
            </Button>
          </div>
        </div>
      </section>

      <section className="border-t border-border px-4 py-16">
        <div className="container mx-auto max-w-4xl">
          <h2 className="mb-2 text-center font-serif text-2xl font-bold text-foreground">
            How it works
          </h2>
          <p className="mb-12 text-center text-sm text-muted-foreground">
            Four simple steps to career clarity.
          </p>
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {steps.map((s) => (
              <div key={s.step} className="relative rounded-xl border border-border bg-card p-6">
                <span className="mb-3 block font-mono text-xs text-muted-foreground">
                  {s.step}
                </span>
                <s.icon className="mb-3 h-5 w-5 text-primary" />
                <h3 className="mb-1 text-sm font-semibold text-foreground">{s.title}</h3>
                <p className="text-xs leading-relaxed text-muted-foreground">{s.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
