import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { CheckCircle2, FileText, GraduationCap, MessageSquare, Upload as UploadIcon } from "lucide-react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Upload() {
  const navigate = useNavigate();
  const [transcript, setTranscript] = useState<File | null>(null);
  const [resume, setResume] = useState<File | null>(null);
  const [additionalInfo, setAdditionalInfo] = useState("");

  const handleFile = (
    e: React.ChangeEvent<HTMLInputElement>,
    setter: (f: File | null) => void
  ) => {
    const file = e.target.files?.[0] ?? null;
    setter(file);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    navigate("/profile");
  };

  return (
    <div className="container mx-auto min-h-[calc(100vh-3.5rem)] max-w-5xl px-4 py-8">
      <div className="mb-8">
        <h1 className="font-serif text-3xl font-bold text-foreground">Upload Your Info</h1>
        <p className="mt-1 text-muted-foreground">
          We just need your transcript, resume, and any extra context.
        </p>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="grid gap-6 lg:grid-cols-2">
          <Card>
            <CardHeader className="flex flex-row items-center gap-3 space-y-0 pb-4">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-accent">
                <GraduationCap className="h-4 w-4 text-accent-foreground" />
              </div>
              <CardTitle className="text-lg">Transcript</CardTitle>
            </CardHeader>
            <CardContent>
              <label className="flex cursor-pointer flex-col items-center gap-3 rounded-lg border-2 border-dashed border-border p-10 transition-colors hover:border-primary/40 hover:bg-accent/30">
                {transcript ? (
                  <>
                    <CheckCircle2 className="h-8 w-8 text-primary" />
                    <span className="text-sm font-medium text-foreground">{transcript.name}</span>
                    <span className="text-xs text-muted-foreground">Click to replace</span>
                  </>
                ) : (
                  <>
                    <UploadIcon className="h-8 w-8 text-muted-foreground" />
                    <span className="text-sm text-muted-foreground">
                      Drop your transcript here or click to browse
                    </span>
                    <span className="text-xs text-muted-foreground">PDF, DOCX, or image</span>
                  </>
                )}
                <input
                  type="file"
                  className="hidden"
                  accept=".pdf,.docx,.doc,.png,.jpg,.jpeg"
                  onChange={(e) => handleFile(e, setTranscript)}
                />
              </label>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center gap-3 space-y-0 pb-4">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-accent">
                <FileText className="h-4 w-4 text-accent-foreground" />
              </div>
              <CardTitle className="text-lg">Resume</CardTitle>
            </CardHeader>
            <CardContent>
              <label className="flex cursor-pointer flex-col items-center gap-3 rounded-lg border-2 border-dashed border-border p-10 transition-colors hover:border-primary/40 hover:bg-accent/30">
                {resume ? (
                  <>
                    <CheckCircle2 className="h-8 w-8 text-primary" />
                    <span className="text-sm font-medium text-foreground">{resume.name}</span>
                    <span className="text-xs text-muted-foreground">Click to replace</span>
                  </>
                ) : (
                  <>
                    <UploadIcon className="h-8 w-8 text-muted-foreground" />
                    <span className="text-sm text-muted-foreground">
                      Drop your resume here or click to browse
                    </span>
                    <span className="text-xs text-muted-foreground">PDF or DOCX</span>
                  </>
                )}
                <input
                  type="file"
                  className="hidden"
                  accept=".pdf,.docx,.doc"
                  onChange={(e) => handleFile(e, setResume)}
                />
              </label>
            </CardContent>
          </Card>
        </div>

        <Card className="mt-6">
          <CardHeader className="flex flex-row items-center gap-3 space-y-0 pb-4">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-accent">
              <MessageSquare className="h-4 w-4 text-accent-foreground" />
            </div>
            <CardTitle className="text-lg">Additional Info</CardTitle>
          </CardHeader>
          <CardContent>
            <Label htmlFor="additional" className="sr-only">
              Additional information
            </Label>
            <Textarea
              id="additional"
              placeholder="Any extra context — certifications, projects, goals, preferences…"
              value={additionalInfo}
              onChange={(e) => setAdditionalInfo(e.target.value)}
              className="min-h-[120px] resize-none"
            />
          </CardContent>
        </Card>

        <Button type="submit" size="lg" className="mt-6 w-full">
          Submit &amp; View Profile
        </Button>
      </form>
    </div>
  );
}
