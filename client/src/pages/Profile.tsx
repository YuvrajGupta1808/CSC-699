import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Progress } from "@/components/ui/progress";
import { studentProfile } from "@/data/mock-data";
import { BookOpen, CheckCircle2, FileText, MessageSquare, Send, Sparkles, Upload, User } from "lucide-react";
import { useState } from "react";

const skillCategories = [
  { label: "Languages", skills: ["Python", "Java", "JavaScript", "SQL", "C++"] },
  { label: "Frameworks & Tools", skills: ["TensorFlow", "PyTorch", "React", "Git", "Docker", "PostgreSQL"] },
  { label: "Concepts", skills: ["Machine Learning", "Deep Learning", "Data Structures", "Algorithms", "REST APIs"] },
];

export default function Profile() {
  const completionItems = [
    { label: "Transcript", done: studentProfile.transcriptUploaded },
    { label: "Resume", done: studentProfile.resumeUploaded },
    { label: "Courses", done: studentProfile.completedCourses.length > 0 },
    { label: "Skills", done: studentProfile.skills.length > 0 },
  ];
  const [messages, setMessages] = useState([
    { role: "assistant", content: "Hi! I'm your career assistant. How can I help you today?" }
  ]);
  const [inputValue, setInputValue] = useState("");

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim()) return;
    
    // Add user message
    const newMessages = [...messages, { role: "user", content: inputValue }];
    setMessages(newMessages);
    setInputValue("");
    
    // Simple bot response demo
    setTimeout(() => {
      setMessages(prev => [...prev, { 
        role: "assistant", 
        content: "That's a great question! Based on your profile, I recommend looking into Data Science and Machine Learning roles." 
      }]);
    }, 1000);
  };

  const completionPct = Math.round(
    (completionItems.filter((i) => i.done).length / completionItems.length) * 100
  );

  return (
    <div className="container mx-auto max-w-5xl px-4 py-8">
      <div className="mb-8">
        <h1 className="font-serif text-3xl font-bold text-foreground">Student Profile</h1>
        <p className="mt-1 text-muted-foreground">
          Your academic background and skills used for job matching.
        </p>
      </div>

      <Card className="mb-8 overflow-hidden border-primary/20">
        <div className="flex flex-col gap-6 p-6 sm:flex-row sm:items-center">
          <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-full bg-accent">
            <User className="h-8 w-8 text-accent-foreground" />
          </div>
          <div className="flex-1 space-y-1">
            <h2 className="text-xl font-bold text-foreground">{studentProfile.name}</h2>
            <p className="text-sm text-muted-foreground">
              {studentProfile.major} · {studentProfile.year} · GPA {studentProfile.gpa}
            </p>
          </div>
          <div className="w-full sm:w-48">
            <div className="mb-1 flex items-center justify-between text-xs text-muted-foreground">
              <span>Profile Completion</span>
              <span className="font-semibold text-foreground">{completionPct}%</span>
            </div>
            <Progress value={completionPct} className="h-2" />
          </div>
        </div>
      </Card>

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="space-y-6 lg:col-span-2">
          <Card>
            <CardHeader className="flex flex-row items-center gap-3 space-y-0 pb-4">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-accent">
                <BookOpen className="h-4 w-4 text-accent-foreground" />
              </div>
              <CardTitle className="text-lg">Completed Courses</CardTitle>
              <Badge variant="secondary" className="ml-auto text-xs">
                {studentProfile.completedCourses.length} courses
              </Badge>
            </CardHeader>
            <CardContent>
              <div className="grid gap-2 sm:grid-cols-2">
                {studentProfile.completedCourses.map((course) => (
                  <div
                    key={course}
                    className="flex items-center gap-2 rounded-lg border border-border/50 bg-background px-3 py-2.5 text-sm transition-colors hover:border-primary/30"
                  >
                    <CheckCircle2 className="h-3.5 w-3.5 shrink-0 text-primary" />
                    <span className="text-foreground">{course}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center gap-3 space-y-0 pb-4">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-accent">
                <Sparkles className="h-4 w-4 text-accent-foreground" />
              </div>
              <CardTitle className="text-lg">Skills</CardTitle>
            </CardHeader>
            <CardContent className="space-y-5">
              {skillCategories.map((cat) => (
                <div key={cat.label}>
                  <h4 className="mb-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                    {cat.label}
                  </h4>
                  <div className="flex flex-wrap gap-1.5">
                    {cat.skills
                      .filter((s) => studentProfile.skills.includes(s))
                      .map((skill) => (
                        <Badge key={skill} variant="secondary" className="text-xs">
                          {skill}
                        </Badge>
                      ))}
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>

        <div className="space-y-6">
          <Card className="flex flex-col h-[400px] border-primary/10 shadow-sm">
            <CardHeader className="flex flex-row items-center gap-3 space-y-0 pb-4">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10">
                <MessageSquare className="h-4 w-4 text-primary" />
              </div>
              <CardTitle className="text-lg">Career Assistant</CardTitle>
            </CardHeader>
            <CardContent className="flex-1 overflow-y-auto space-y-4 min-h-0 px-6">
              <div className="flex flex-col gap-3">
                {messages.map((m, i) => (
                  <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-[85%] rounded-2xl px-3 py-2 text-sm ${
                      m.role === 'user' 
                        ? 'bg-primary text-primary-foreground rounded-tr-none' 
                        : 'bg-accent text-accent-foreground rounded-tl-none'
                    }`}>
                      {m.content}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
            <CardFooter className="border-t p-4">
              <form onSubmit={handleSendMessage} className="flex w-full items-center gap-2">
                <Input 
                  placeholder="Type your message..." 
                  value={inputValue} 
                  onChange={(e) => setInputValue(e.target.value)}
                  className="flex-1 bg-background"
                />
                <Button type="submit" size="icon" className="shrink-0" disabled={!inputValue.trim()}>
                  <Send className="h-4 w-4" />
                </Button>
              </form>
            </CardFooter>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center gap-3 space-y-0 pb-4">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-accent">
                <FileText className="h-4 w-4 text-accent-foreground" />
              </div>
              <CardTitle className="text-lg">Documents</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex items-center justify-between rounded-lg border border-border/50 bg-background p-3">
                <div className="flex items-center gap-2 text-sm">
                  <Upload className="h-4 w-4 text-muted-foreground" />
                  <span className="text-foreground">Transcript</span>
                </div>
                <Badge variant={studentProfile.transcriptUploaded ? "default" : "outline"}>
                  {studentProfile.transcriptUploaded ? "Uploaded" : "Pending"}
                </Badge>
              </div>
              <div className="flex items-center justify-between rounded-lg border border-border/50 bg-background p-3">
                <div className="flex items-center gap-2 text-sm">
                  <Upload className="h-4 w-4 text-muted-foreground" />
                  <span className="text-foreground">Resume</span>
                </div>
                <Badge variant={studentProfile.resumeUploaded ? "default" : "outline"}>
                  {studentProfile.resumeUploaded ? "Uploaded" : "Pending"}
                </Badge>
              </div>
              <Button variant="outline" className="w-full" size="sm">
                Upload Document
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
