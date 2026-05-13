import { useEffect, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { BookOpen, CheckCircle2, FileText, Loader2, Sparkles, Upload, User } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import { Link } from "react-router-dom";

interface FullProfile {
  student_id: string;
  name: string;
  major: string;
  skills: string[];
  completed_courses: string[];
}

const FAKE_DOCS = [
  { label: "Transcript", uploaded: true },
  { label: "Resume", uploaded: false },
];

export default function Profile() {
  const { student } = useAuth();
  const [profile, setProfile] = useState<FullProfile | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!student) { setProfile(null); return; }
    setLoading(true);
    setError("");
    fetch(`/api/students/${student.student_id}`)
      .then((r) => r.json())
      .then(setProfile)
      .catch(() => setError("Could not load profile."))
      .finally(() => setLoading(false));
  }, [student]);

  if (!student) {
    return (
      <div className="container mx-auto max-w-5xl px-4 py-24 text-center">
        <User className="mx-auto mb-4 h-12 w-12 text-muted-foreground/30" />
        <h2 className="font-serif text-2xl font-bold text-foreground">No profile loaded</h2>
        <p className="mt-2 text-muted-foreground">Sign in to view your student profile.</p>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
      </div>
    );
  }

  if (error || !profile) {
    return (
      <div className="container mx-auto max-w-5xl px-4 py-24 text-center">
        <p className="text-destructive">{error || "Profile unavailable."}</p>
      </div>
    );
  }

  const completionItems = [
    { label: "Major on file", done: !!profile.major },
    { label: "Skills profiled", done: profile.skills.length > 0 },
    { label: "Courses logged", done: profile.completed_courses.length > 0 },
    { label: "Transcript uploaded", done: FAKE_DOCS[0].uploaded },
  ];
  const completionPct = Math.round(
    (completionItems.filter((i) => i.done).length / completionItems.length) * 100,
  );

  return (
    <div className="container mx-auto max-w-5xl px-4 py-8">
      <div className="mb-8">
        <h1 className="font-serif text-3xl font-bold text-foreground">Student Profile</h1>
        <p className="mt-1 text-muted-foreground">
          Your academic background and skills used for job matching.
        </p>
      </div>

      {/* Identity card */}
      <Card className="mb-8 overflow-hidden border-primary/20">
        <div className="flex flex-col gap-6 p-6 sm:flex-row sm:items-center">
          <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-full bg-accent">
            <span className="font-serif text-xl font-bold text-accent-foreground">
              {profile.name.split(" ").map((n) => n[0]).join("").slice(0, 2)}
            </span>
          </div>
          <div className="flex-1 space-y-1">
            <h2 className="text-xl font-bold text-foreground">{profile.name}</h2>
            <p className="text-sm text-muted-foreground">{profile.major}</p>
          </div>
          <div className="w-full sm:w-48">
            <div className="mb-1 flex items-center justify-between text-xs text-muted-foreground">
              <span>Profile Completion</span>
              <span className="font-semibold text-foreground">{completionPct}%</span>
            </div>
            <Progress value={completionPct} className="h-2" />
            <div className="mt-2 space-y-1">
              {completionItems.map((item) => (
                <div key={item.label} className="flex items-center gap-1.5 text-xs text-muted-foreground">
                  <CheckCircle2
                    className={`h-3 w-3 ${item.done ? "text-primary" : "text-border"}`}
                  />
                  {item.label}
                </div>
              ))}
            </div>
          </div>
        </div>
      </Card>

      <div className="grid gap-6 lg:grid-cols-3">
        {/* Left: courses + skills */}
        <div className="space-y-6 lg:col-span-2">
          <Card>
            <CardHeader className="flex flex-row items-center gap-3 space-y-0 pb-4">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-accent">
                <BookOpen className="h-4 w-4 text-accent-foreground" />
              </div>
              <CardTitle className="text-lg">Completed Courses</CardTitle>
              <Badge variant="secondary" className="ml-auto text-xs">
                {profile.completed_courses.length} courses
              </Badge>
            </CardHeader>
            <CardContent>
              {profile.completed_courses.length === 0 ? (
                <p className="text-sm text-muted-foreground">No courses on record yet.</p>
              ) : (
                <div className="grid gap-2 sm:grid-cols-2">
                  {profile.completed_courses.map((course) => (
                    <div
                      key={course}
                      className="flex items-center gap-2 rounded-lg border border-border/50 bg-background px-3 py-2.5 text-sm transition-colors hover:border-primary/30"
                    >
                      <CheckCircle2 className="h-3.5 w-3.5 shrink-0 text-primary" />
                      <span className="text-foreground">{course}</span>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center gap-3 space-y-0 pb-4">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-accent">
                <Sparkles className="h-4 w-4 text-accent-foreground" />
              </div>
              <CardTitle className="text-lg">Skills</CardTitle>
              <Badge variant="secondary" className="ml-auto text-xs">
                {profile.skills.length} skills
              </Badge>
            </CardHeader>
            <CardContent>
              {profile.skills.length === 0 ? (
                <p className="text-sm text-muted-foreground">No skills profiled yet.</p>
              ) : (
                <div className="flex flex-wrap gap-2">
                  {profile.skills.map((skill) => (
                    <Badge key={skill} variant="secondary" className="text-xs">
                      {skill}
                    </Badge>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Right: documents */}
        <div className="space-y-6">
          <Card>
            <CardHeader className="flex flex-row items-center gap-3 space-y-0 pb-4">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-accent">
                <FileText className="h-4 w-4 text-accent-foreground" />
              </div>
              <CardTitle className="text-lg">Documents</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {FAKE_DOCS.map((doc) => (
                <div
                  key={doc.label}
                  className="flex items-center justify-between rounded-lg border border-border/50 bg-background p-3"
                >
                  <div className="flex items-center gap-2 text-sm">
                    <Upload className="h-4 w-4 text-muted-foreground" />
                    <span className="text-foreground">{doc.label}</span>
                  </div>
                  <Badge variant={doc.uploaded ? "default" : "outline"}>
                    {doc.uploaded ? "Uploaded" : "Pending"}
                  </Badge>
                </div>
              ))}
              <Button variant="outline" className="w-full" size="sm" asChild>
                <Link to="/upload">Upload Document</Link>
              </Button>
            </CardContent>
          </Card>

          <Card className="border-primary/10">
            <CardContent className="p-5 text-center">
              <p className="text-sm font-medium text-foreground">Want personalized advice?</p>
              <p className="mt-1 text-xs text-muted-foreground">
                Chat with the AI advisor about your skills and career goals.
              </p>
              <Button className="mt-3 w-full" size="sm" asChild>
                <Link to="/chat">Open Advisor Chat</Link>
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
