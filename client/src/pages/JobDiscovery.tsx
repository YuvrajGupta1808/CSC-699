import { JobCard } from "@/components/JobCard";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { mockJobs } from "@/data/mock-data";
import { Briefcase, Search, SlidersHorizontal } from "lucide-react";
import { useMemo, useState } from "react";

const roleTypes = ["Software", "Data", "Machine Learning", "Security"];
const locations = ["Mountain View, CA", "Menlo Park, CA", "Los Gatos, CA", "Austin, TX", "San Francisco, CA"];

export default function JobDiscovery() {
  const [search, setSearch] = useState("");
  const [selectedRoles, setSelectedRoles] = useState<string[]>([]);
  const [selectedLocations, setSelectedLocations] = useState<string[]>([]);

  const toggle = (list: string[], item: string) =>
    list.includes(item) ? list.filter((i) => i !== item) : [...list, item];

  const filteredJobs = useMemo(() => {
    return mockJobs
      .filter((job) => {
        if (search && !job.title.toLowerCase().includes(search.toLowerCase()) && !job.company.toLowerCase().includes(search.toLowerCase())) return false;
        if (selectedRoles.length && !selectedRoles.includes(job.roleType)) return false;
        if (selectedLocations.length && !selectedLocations.includes(job.location)) return false;
        return true;
      })
      .sort((a, b) => b.matchScore - a.matchScore);
  }, [search, selectedRoles, selectedLocations]);

  const activeFilterCount = selectedRoles.length + selectedLocations.length;

  return (
    <div className="container mx-auto max-w-5xl px-4 py-8">
      <div className="mb-8">
        <h1 className="font-serif text-3xl font-bold text-foreground">Job Discovery</h1>
        <p className="mt-1 text-muted-foreground">
          Browse jobs ranked by how well they match your skill profile.
        </p>
      </div>

      <div className="flex flex-col gap-8 lg:flex-row">
        <aside className="w-full shrink-0 lg:w-64">
          <Card>
            <CardContent className="p-5 space-y-6">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                <Input
                  placeholder="Search jobs..."
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  className="pl-9"
                />
              </div>

              <div className="flex items-center gap-2">
                <SlidersHorizontal className="h-4 w-4 text-muted-foreground" />
                <span className="text-sm font-semibold text-foreground">Filters</span>
                {activeFilterCount > 0 && (
                  <Badge variant="default" className="ml-auto text-xs">
                    {activeFilterCount}
                  </Badge>
                )}
              </div>

              <div>
                <Label className="mb-2 block text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Role Type
                </Label>
                <div className="space-y-2">
                  {roleTypes.map((role) => (
                    <label key={role} className="flex cursor-pointer items-center gap-2 rounded-md px-2 py-1.5 text-sm text-foreground transition-colors hover:bg-accent">
                      <Checkbox
                        checked={selectedRoles.includes(role)}
                        onCheckedChange={() => setSelectedRoles((r) => toggle(r, role))}
                      />
                      {role}
                    </label>
                  ))}
                </div>
              </div>

              <div>
                <Label className="mb-2 block text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Location
                </Label>
                <div className="space-y-2">
                  {locations.map((loc) => (
                    <label key={loc} className="flex cursor-pointer items-center gap-2 rounded-md px-2 py-1.5 text-sm text-foreground transition-colors hover:bg-accent">
                      <Checkbox
                        checked={selectedLocations.includes(loc)}
                        onCheckedChange={() => setSelectedLocations((l) => toggle(l, loc))}
                      />
                      {loc}
                    </label>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        </aside>

        <div className="flex-1 space-y-4">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <Briefcase className="h-4 w-4" />
            {filteredJobs.length} job{filteredJobs.length !== 1 && "s"} found
          </div>
          {filteredJobs.map((job) => (
            <JobCard key={job.id} job={job} />
          ))}
          {filteredJobs.length === 0 && (
            <Card className="p-8 text-center">
              <p className="text-muted-foreground">No jobs match your current filters.</p>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
