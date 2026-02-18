import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
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
    <div className="container mx-auto min-h-[calc(100vh-3.5rem)] max-w-4xl px-4 py-12 flex flex-col items-center">
      <div className="text-center mb-12 max-w-2xl">
        <div className="inline-flex h-12 w-12 items-center justify-center rounded-2xl bg-primary/10 mb-4 animate-in fade-in zoom-in duration-500">
          <UploadIcon className="h-6 w-6 text-primary" />
        </div>
        <h1 className="font-serif text-4xl font-bold tracking-tight text-foreground sm:text-5xl"> Complete Your Profile</h1>
        <p className="mt-4 text-lg text-muted-foreground">
          Upload your documents to unlock personalized job recommendations and skill gap analysis.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="w-full space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
        <div className="grid gap-6 md:grid-cols-2">
          {/* Transcript Upload */}
          <div className="group relative">
            <div className={`absolute -inset-0.5 rounded-2xl bg-gradient-to-r from-primary/20 to-accent/20 opacity-0 blur transition duration-500 group-hover:opacity-100 ${transcript ? 'opacity-100' : ''}`} />
            <Card className="relative h-full border-primary/10 overflow-hidden bg-card/50 backdrop-blur-sm">
              <CardHeader className="pb-3 text-center">
                <div className="mx-auto flex h-10 w-10 items-center justify-center rounded-full bg-accent/50 mb-2">
                  <GraduationCap className="h-5 w-5 text-primary" />
                </div>
                <CardTitle className="text-lg">Academic Transcript</CardTitle>
              </CardHeader>
              <CardContent>
                <label className="group/dropzone relative flex cursor-pointer flex-col items-center justify-center gap-4 rounded-xl border-2 border-dashed border-primary/20 bg-background/50 p-8 transition-all hover:border-primary/50 hover:bg-accent/40">
                  {transcript ? (
                    <div className="flex flex-col items-center text-center animate-in zoom-in duration-300">
                      <div className="flex h-12 w-12 items-center justify-center rounded-full bg-primary/20 text-primary mb-2">
                        <CheckCircle2 className="h-6 w-6" />
                      </div>
                      <span className="text-sm font-semibold truncate max-w-[200px]">{transcript.name}</span>
                      <span className="text-xs text-primary font-medium mt-1">Ready to process</span>
                    </div>
                  ) : (
                    <div className="flex flex-col items-center text-center">
                      <div className="flex h-12 w-12 items-center justify-center rounded-full bg-accent/50 text-muted-foreground group-hover/dropzone:bg-primary/20 group-hover/dropzone:text-primary transition-colors">
                        <UploadIcon className="h-6 w-6" />
                      </div>
                      <p className="mt-2 text-sm font-medium">Click or drag to upload</p>
                      <p className="text-xs text-muted-foreground mt-1">PDF, DOCX (Max 10MB)</p>
                    </div>
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
          </div>

          {/* Resume Upload */}
          <div className="group relative">
            <div className={`absolute -inset-0.5 rounded-2xl bg-gradient-to-r from-accent/20 to-primary/20 opacity-0 blur transition duration-500 group-hover:opacity-100 ${resume ? 'opacity-100' : ''}`} />
            <Card className="relative h-full border-primary/10 overflow-hidden bg-card/50 backdrop-blur-sm">
              <CardHeader className="pb-3 text-center">
                <div className="mx-auto flex h-10 w-10 items-center justify-center rounded-full bg-accent/50 mb-2">
                  <FileText className="h-5 w-5 text-primary" />
                </div>
                <CardTitle className="text-lg">Professional Resume</CardTitle>
              </CardHeader>
              <CardContent>
                <label className="group/dropzone relative flex cursor-pointer flex-col items-center justify-center gap-4 rounded-xl border-2 border-dashed border-primary/20 bg-background/50 p-8 transition-all hover:border-primary/50 hover:bg-accent/40">
                  {resume ? (
                    <div className="flex flex-col items-center text-center animate-in zoom-in duration-300">
                      <div className="flex h-12 w-12 items-center justify-center rounded-full bg-primary/20 text-primary mb-2">
                        <CheckCircle2 className="h-6 w-6" />
                      </div>
                      <span className="text-sm font-semibold truncate max-w-[200px]">{resume.name}</span>
                      <span className="text-xs text-primary font-medium mt-1">Ready to process</span>
                    </div>
                  ) : (
                    <div className="flex flex-col items-center text-center">
                      <div className="flex h-12 w-12 items-center justify-center rounded-full bg-accent/50 text-muted-foreground group-hover/dropzone:bg-primary/20 group-hover/dropzone:text-primary transition-colors">
                        <UploadIcon className="h-6 w-6" />
                      </div>
                      <p className="mt-2 text-sm font-medium">Click or drag to upload</p>
                      <p className="text-xs text-muted-foreground mt-1">PDF, DOCX (Max 10MB)</p>
                    </div>
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
        </div>

        {/* Additional Context */}
        <Card className="border-primary/10 bg-card/30">
          <CardHeader className="pb-3">
            <div className="flex items-center gap-3">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10">
                <MessageSquare className="h-4 w-4 text-primary" />
              </div>
              <CardTitle className="text-lg font-medium">Additional Context</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <Textarea
              id="additional"
              placeholder="Tell us more about your career goals, specific certifications, or project experience you'd like to highlight..."
              value={additionalInfo}
              onChange={(e) => setAdditionalInfo(e.target.value)}
              className="min-h-[100px] resize-none bg-background/50 border-primary/10 focus:border-primary/30"
            />
          </CardContent>
        </Card>

        <div className="flex flex-col gap-4">
          <Button 
            type="submit" 
            size="lg" 
            className="w-full h-14 text-lg font-semibold shadow-lg shadow-primary/20 transition-all hover:scale-[1.01] active:scale-[0.99]"
            disabled={!transcript && !resume}
          >
            Process & Analyze Profile
          </Button>
          <p className="text-center text-xs text-muted-foreground px-4">
            By uploading, you agree to our Terms of Service. Your data is used only for matching purposes.
          </p>
        </div>
      </form>
    </div>
  );
}
