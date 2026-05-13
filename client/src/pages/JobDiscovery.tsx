import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Building2,
  Briefcase,
  ChevronLeft,
  ChevronRight,
  MapPin,
  Search,
  SlidersHorizontal,
} from "lucide-react";
import { Link } from "react-router-dom";

interface RealJob {
  job_id: string;
  title: string;
  company: string;
  location: string;
  top_skills: string[];
}

interface JobsResponse {
  jobs: RealJob[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

interface LocationOption {
  city: string;
  count: number;
}

function JobCardReal({ job }: { job: RealJob }) {
  const city = job.location ? job.location.split(",")[0].trim() : "";
  return (
    <Link to={`/jobs/${job.job_id}`} className="block">
      <Card className="group cursor-pointer border border-border bg-white shadow-sm transition-all duration-200 hover:border-primary/40 hover:shadow-lg">
        <CardContent className="p-6">
          <div className="flex items-start gap-4">
            <div className="min-w-0 flex-1 space-y-1.5">
              <h3 className="text-lg font-semibold text-foreground transition-colors group-hover:text-primary">
                {job.title}
              </h3>
              <div className="flex flex-wrap items-center gap-4 text-sm text-muted-foreground">
                <span className="flex items-center gap-1.5">
                  <Building2 className="h-4 w-4" />
                  {job.company}
                </span>
                {city && (
                  <span className="flex items-center gap-1.5">
                    <MapPin className="h-4 w-4" />
                    {city}
                  </span>
                )}
              </div>
            </div>
          </div>
          {job.top_skills.length > 0 && (
            <div className="mt-4 flex flex-wrap gap-2">
              {job.top_skills.slice(0, 5).map((skill) => (
                <Badge key={skill} variant="secondary" className="px-3 py-1 text-xs">
                  {skill}
                </Badge>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </Link>
  );
}

function JobSkeleton() {
  return (
    <Card className="border border-border">
      <CardContent className="space-y-3 p-6">
        <Skeleton className="h-5 w-2/3" />
        <Skeleton className="h-4 w-1/2" />
        <div className="flex gap-2 pt-1">
          <Skeleton className="h-6 w-16 rounded-full" />
          <Skeleton className="h-6 w-20 rounded-full" />
          <Skeleton className="h-6 w-14 rounded-full" />
        </div>
      </CardContent>
    </Card>
  );
}

const PER_PAGE = 10;

export default function JobDiscovery() {
  const [data, setData] = useState<JobsResponse | null>(null);
  const [locations, setLocations] = useState<LocationOption[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [debouncedSearch, setDebouncedSearch] = useState("");
  const [selectedLocations, setSelectedLocations] = useState<string[]>([]);
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Load location options once
  useEffect(() => {
    fetch("/api/jobs/locations")
      .then((r) => r.json())
      .then(setLocations)
      .catch(console.error);
  }, []);

  // Debounce search input
  const handleSearchChange = useCallback((value: string) => {
    setSearch(value);
    if (debounceRef.current) clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => {
      setDebouncedSearch(value);
      setPage(1);
    }, 350);
  }, []);

  // Fetch jobs whenever page, search, or location filter changes
  useEffect(() => {
    setLoading(true);
    const params = new URLSearchParams({
      page: String(page),
      per_page: String(PER_PAGE),
    });
    if (debouncedSearch) params.set("search", debouncedSearch);
    // Send each selected city as a separate OR-style location param
    if (selectedLocations.length === 1) params.set("location", selectedLocations[0]);

    fetch(`/api/jobs?${params}`)
      .then((r) => r.json())
      .then(setData)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [page, debouncedSearch, selectedLocations]);

  function toggleLocation(city: string) {
    setSelectedLocations((prev) =>
      prev.includes(city) ? prev.filter((c) => c !== city) : [...prev, city],
    );
    setPage(1);
  }

  // Client-side multi-location filter (API only filters one city at a time)
  const displayedJobs = useMemo(() => {
    if (selectedLocations.length <= 1) return data?.jobs ?? [];
    return (data?.jobs ?? []).filter((job) => {
      const city = job.location.split(",")[0].trim();
      return selectedLocations.includes(city);
    });
  }, [data?.jobs, selectedLocations]);

  const activeFilterCount = selectedLocations.length;
  const totalPages = data?.total_pages ?? 1;
  const total = data?.total ?? 0;

  const pageWindow = useMemo(() => {
    const start = Math.max(1, page - 2);
    const end = Math.min(totalPages, page + 2);
    return Array.from({ length: end - start + 1 }, (_, i) => start + i);
  }, [page, totalPages]);

  return (
    <div className="container mx-auto max-w-5xl px-4 py-8">
      <div className="mb-8">
        <h1 className="font-serif text-3xl font-bold text-foreground">Job Discovery</h1>
        <p className="mt-1 text-muted-foreground">
          Browse real job postings matched to your skill profile.
        </p>
      </div>

      <div className="flex flex-col gap-8 lg:flex-row">
        {/* Sidebar */}
        <aside className="w-full shrink-0 lg:w-64">
          <Card>
            <CardContent className="space-y-6 p-5">
              {/* Search */}
              <div className="relative">
                <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                <Input
                  placeholder="Search jobs, skills…"
                  value={search}
                  onChange={(e) => handleSearchChange(e.target.value)}
                  className="pl-9"
                />
              </div>

              {/* Location filter */}
              <div>
                <div className="mb-3 flex items-center gap-2">
                  <SlidersHorizontal className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm font-semibold text-foreground">Location</span>
                  {activeFilterCount > 0 && (
                    <Badge variant="default" className="ml-auto text-xs">
                      {activeFilterCount}
                    </Badge>
                  )}
                </div>

                <div className="space-y-2">
                  {locations.length === 0
                    ? Array.from({ length: 6 }).map((_, i) => (
                        <Skeleton key={i} className="h-7 w-full" />
                      ))
                    : locations.map(({ city, count }) => (
                        <label
                          key={city}
                          className="flex cursor-pointer items-center gap-2 rounded-md px-2 py-1.5 text-sm text-foreground transition-colors hover:bg-accent"
                        >
                          <Checkbox
                            checked={selectedLocations.includes(city)}
                            onCheckedChange={() => toggleLocation(city)}
                          />
                          <span className="flex-1">{city}</span>
                          <span className="text-xs text-muted-foreground">{count}</span>
                        </label>
                      ))}
                </div>

                {activeFilterCount > 0 && (
                  <button
                    onClick={() => { setSelectedLocations([]); setPage(1); }}
                    className="mt-3 text-xs text-primary hover:underline"
                  >
                    Clear filters
                  </button>
                )}
              </div>
            </CardContent>
          </Card>
        </aside>

        {/* Job list */}
        <div className="flex-1 min-w-0">
          <div className="mb-4 flex items-center gap-2 text-sm text-muted-foreground">
            <Briefcase className="h-4 w-4" />
            {loading
              ? "Loading jobs…"
              : `${total.toLocaleString()} job${total !== 1 ? "s" : ""} found`}
            {debouncedSearch && !loading && (
              <span>
                for <span className="font-medium text-foreground">"{debouncedSearch}"</span>
              </span>
            )}
          </div>

          <div className="space-y-4">
            {loading
              ? Array.from({ length: PER_PAGE }).map((_, i) => <JobSkeleton key={i} />)
              : displayedJobs.map((job) => <JobCardReal key={job.job_id} job={job} />)}

            {!loading && displayedJobs.length === 0 && (
              <Card className="p-8 text-center">
                <p className="text-muted-foreground">No jobs match your current filters.</p>
              </Card>
            )}
          </div>

          {/* Pagination */}
          {!loading && totalPages > 1 && selectedLocations.length <= 1 && (
            <div className="mt-8 flex flex-col items-center gap-3">
              <div className="flex items-center gap-1">
                <Button
                  variant="outline"
                  size="icon"
                  className="h-9 w-9"
                  disabled={page === 1}
                  onClick={() => setPage((p) => Math.max(1, p - 1))}
                >
                  <ChevronLeft className="h-4 w-4" />
                </Button>

                {pageWindow[0] > 1 && (
                  <>
                    <Button variant="outline" size="sm" className="h-9 w-9" onClick={() => setPage(1)}>
                      1
                    </Button>
                    {pageWindow[0] > 2 && <span className="px-1 text-muted-foreground">…</span>}
                  </>
                )}

                {pageWindow.map((p) => (
                  <Button
                    key={p}
                    variant={p === page ? "default" : "outline"}
                    size="sm"
                    className="h-9 w-9"
                    onClick={() => setPage(p)}
                  >
                    {p}
                  </Button>
                ))}

                {pageWindow[pageWindow.length - 1] < totalPages && (
                  <>
                    {pageWindow[pageWindow.length - 1] < totalPages - 1 && (
                      <span className="px-1 text-muted-foreground">…</span>
                    )}
                    <Button
                      variant="outline"
                      size="sm"
                      className="h-9 w-9"
                      onClick={() => setPage(totalPages)}
                    >
                      {totalPages}
                    </Button>
                  </>
                )}

                <Button
                  variant="outline"
                  size="icon"
                  className="h-9 w-9"
                  disabled={page === totalPages}
                  onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                >
                  <ChevronRight className="h-4 w-4" />
                </Button>
              </div>

              <p className="text-xs text-muted-foreground">
                Page {page} of {totalPages} · {PER_PAGE} jobs per page
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
