import { useState, useEffect } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Label } from "@/components/ui/label";
import { Brain, Loader2 } from "lucide-react";
import { useAuth, Student } from "@/contexts/AuthContext";

interface LoginModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function LoginModal({ open, onOpenChange }: LoginModalProps) {
  const { setStudent } = useAuth();
  const [students, setStudents] = useState<Student[]>([]);
  const [selectedId, setSelectedId] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [fetchError, setFetchError] = useState("");

  useEffect(() => {
    if (!open) return;
    setLoading(true);
    setFetchError("");
    fetch("/api/students")
      .then((r) => r.json())
      .then((data) => setStudents(data))
      .catch(() => setFetchError("Could not load students. Is the server running?"))
      .finally(() => setLoading(false));
  }, [open]);

  function handleLogin() {
    const found = students.find((s) => s.student_id === selectedId);
    if (!found) return;
    setStudent(found);
    onOpenChange(false);
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-sm">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2 font-serif text-xl">
            <Brain className="h-5 w-5 text-primary" />
            Sign in as Student
          </DialogTitle>
        </DialogHeader>

        {loading && (
          <div className="flex items-center justify-center py-6">
            <Loader2 className="h-5 w-5 animate-spin text-muted-foreground" />
          </div>
        )}

        {fetchError && (
          <p className="rounded-md bg-destructive/10 px-3 py-2 text-sm text-destructive">
            {fetchError}
          </p>
        )}

        {!loading && !fetchError && (
          <div className="space-y-4 pt-2">
            <div className="space-y-1.5">
              <Label className="text-sm font-medium">Select your profile</Label>
              <Select value={selectedId} onValueChange={setSelectedId}>
                <SelectTrigger>
                  <SelectValue placeholder="Choose a student…" />
                </SelectTrigger>
                <SelectContent>
                  {students.map((s) => (
                    <SelectItem key={s.student_id} value={s.student_id}>
                      {s.name}
                      <span className="ml-1.5 text-xs text-muted-foreground">· {s.major}</span>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <Button
              className="w-full"
              disabled={!selectedId}
              onClick={handleLogin}
            >
              Sign In
            </Button>
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
}
