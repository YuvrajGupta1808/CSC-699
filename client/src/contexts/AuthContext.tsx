import { createContext, useContext, useState, ReactNode } from "react";

export interface Student {
  student_id: string;
  name: string;
  major: string;
}

interface AuthContextValue {
  student: Student | null;
  setStudent: (s: Student | null) => void;
}

const AuthContext = createContext<AuthContextValue>({
  student: null,
  setStudent: () => {},
});

export function AuthProvider({ children }: { children: ReactNode }) {
  const [student, setStudent] = useState<Student | null>(null);
  return (
    <AuthContext.Provider value={{ student, setStudent }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
