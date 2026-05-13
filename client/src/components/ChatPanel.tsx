import { MessageCircle } from "lucide-react";
import { Link, useLocation } from "react-router-dom";
import { cn } from "@/lib/utils";

export function ChatPanel() {
  const { pathname } = useLocation();

  // Hide on the chat page and on job detail pages (those have their own inline chat)
  if (pathname === "/chat" || /^\/jobs\/[^/]+$/.test(pathname)) return null;

  return (
    <Link
      to="/chat"
      className={cn(
        "fixed bottom-6 right-6 z-40 flex h-14 w-14 items-center justify-center rounded-full shadow-lg transition-all",
        "bg-primary text-primary-foreground hover:bg-primary/90 hover:scale-105",
      )}
      aria-label="Open career advisor chat"
    >
      <MessageCircle className="h-6 w-6" />
    </Link>
  );
}
