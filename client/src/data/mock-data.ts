export interface Job {
  id: string;
  title: string;
  company: string;
  location: string;
  roleType: string;
  matchScore: number;
  topSkills: string[];
  skills: SkillGroup[];
  extractionMethod: "keyword-based" | "embedding-based" | "llm-extracted";
}

export interface SkillGroup {
  category: string;
  skills: { name: string; confidence: number; status: "covered" | "partial" | "missing" }[];
}

export const mockJobs: Job[] = [
  {
    id: "1",
    title: "Machine Learning Engineer",
    company: "Google",
    location: "Mountain View, CA",
    roleType: "Machine Learning",
    matchScore: 87,
    topSkills: ["Python", "TensorFlow", "Deep Learning"],
    extractionMethod: "llm-extracted",
    skills: [
      {
        category: "Programming",
        skills: [
          { name: "Python", confidence: 95, status: "covered" },
          { name: "C++", confidence: 72, status: "partial" },
          { name: "SQL", confidence: 80, status: "covered" },
        ],
      },
      {
        category: "ML / AI",
        skills: [
          { name: "TensorFlow", confidence: 90, status: "covered" },
          { name: "PyTorch", confidence: 85, status: "covered" },
          { name: "Deep Learning", confidence: 88, status: "covered" },
          { name: "NLP", confidence: 70, status: "partial" },
        ],
      },
      {
        category: "Systems",
        skills: [
          { name: "Distributed Systems", confidence: 65, status: "partial" },
          { name: "Cloud Computing", confidence: 75, status: "partial" },
        ],
      },
      {
        category: "Tools",
        skills: [
          { name: "Git", confidence: 92, status: "covered" },
          { name: "Docker", confidence: 68, status: "partial" },
          { name: "Kubernetes", confidence: 45, status: "missing" },
        ],
      },
    ],
  },
  {
    id: "2",
    title: "Software Engineer, Backend",
    company: "Meta",
    location: "Menlo Park, CA",
    roleType: "Software",
    matchScore: 74,
    topSkills: ["Java", "Distributed Systems", "APIs"],
    extractionMethod: "embedding-based",
    skills: [
      {
        category: "Programming",
        skills: [
          { name: "Java", confidence: 88, status: "covered" },
          { name: "Python", confidence: 82, status: "covered" },
          { name: "Go", confidence: 55, status: "missing" },
        ],
      },
      {
        category: "Systems",
        skills: [
          { name: "Distributed Systems", confidence: 90, status: "partial" },
          { name: "Microservices", confidence: 78, status: "partial" },
          { name: "REST APIs", confidence: 92, status: "covered" },
        ],
      },
      {
        category: "Tools",
        skills: [
          { name: "Git", confidence: 95, status: "covered" },
          { name: "Docker", confidence: 80, status: "partial" },
          { name: "CI/CD", confidence: 70, status: "missing" },
        ],
      },
    ],
  },
  {
    id: "3",
    title: "Data Scientist",
    company: "Netflix",
    location: "Los Gatos, CA",
    roleType: "Data",
    matchScore: 91,
    topSkills: ["Python", "Statistics", "Machine Learning"],
    extractionMethod: "llm-extracted",
    skills: [
      {
        category: "Programming",
        skills: [
          { name: "Python", confidence: 95, status: "covered" },
          { name: "R", confidence: 70, status: "partial" },
          { name: "SQL", confidence: 90, status: "covered" },
        ],
      },
      {
        category: "ML / AI",
        skills: [
          { name: "Machine Learning", confidence: 92, status: "covered" },
          { name: "Statistics", confidence: 88, status: "covered" },
          { name: "A/B Testing", confidence: 65, status: "partial" },
        ],
      },
      {
        category: "Tools",
        skills: [
          { name: "Jupyter", confidence: 90, status: "covered" },
          { name: "Pandas", confidence: 95, status: "covered" },
          { name: "Spark", confidence: 50, status: "missing" },
        ],
      },
    ],
  },
  {
    id: "4",
    title: "Cybersecurity Analyst",
    company: "CrowdStrike",
    location: "Austin, TX",
    roleType: "Security",
    matchScore: 52,
    topSkills: ["Network Security", "SIEM", "Python"],
    extractionMethod: "keyword-based",
    skills: [
      {
        category: "Programming",
        skills: [
          { name: "Python", confidence: 80, status: "covered" },
          { name: "Bash", confidence: 60, status: "partial" },
        ],
      },
      {
        category: "Systems",
        skills: [
          { name: "Network Security", confidence: 85, status: "missing" },
          { name: "Linux Administration", confidence: 70, status: "partial" },
          { name: "Firewall Management", confidence: 65, status: "missing" },
        ],
      },
      {
        category: "Tools",
        skills: [
          { name: "SIEM Tools", confidence: 78, status: "missing" },
          { name: "Wireshark", confidence: 72, status: "missing" },
          { name: "Nmap", confidence: 60, status: "missing" },
        ],
      },
    ],
  },
  {
    id: "5",
    title: "Full Stack Developer",
    company: "Stripe",
    location: "San Francisco, CA",
    roleType: "Software",
    matchScore: 68,
    topSkills: ["React", "Node.js", "TypeScript"],
    extractionMethod: "embedding-based",
    skills: [
      {
        category: "Programming",
        skills: [
          { name: "TypeScript", confidence: 90, status: "partial" },
          { name: "JavaScript", confidence: 95, status: "covered" },
          { name: "Ruby", confidence: 60, status: "missing" },
        ],
      },
      {
        category: "Systems",
        skills: [
          { name: "REST APIs", confidence: 88, status: "covered" },
          { name: "GraphQL", confidence: 70, status: "missing" },
        ],
      },
      {
        category: "Tools",
        skills: [
          { name: "React", confidence: 92, status: "covered" },
          { name: "Node.js", confidence: 85, status: "partial" },
          { name: "PostgreSQL", confidence: 78, status: "covered" },
        ],
      },
    ],
  },
  {
    id: "6",
    title: "AI Research Intern",
    company: "OpenAI",
    location: "San Francisco, CA",
    roleType: "Machine Learning",
    matchScore: 79,
    topSkills: ["Deep Learning", "NLP", "Research"],
    extractionMethod: "llm-extracted",
    skills: [
      {
        category: "Programming",
        skills: [
          { name: "Python", confidence: 95, status: "covered" },
          { name: "C++", confidence: 65, status: "partial" },
        ],
      },
      {
        category: "ML / AI",
        skills: [
          { name: "Deep Learning", confidence: 92, status: "covered" },
          { name: "NLP", confidence: 88, status: "covered" },
          { name: "Reinforcement Learning", confidence: 75, status: "partial" },
          { name: "Transformers", confidence: 82, status: "covered" },
        ],
      },
      {
        category: "Tools",
        skills: [
          { name: "PyTorch", confidence: 90, status: "covered" },
          { name: "LaTeX", confidence: 70, status: "covered" },
          { name: "Weights & Biases", confidence: 55, status: "missing" },
        ],
      },
    ],
  },
];

export const studentProfile = {
  name: "Alex Chen",
  major: "Computer Science",
  year: "Senior",
  gpa: 3.7,
  completedCourses: [
    "CSC 220 - Data Structures",
    "CSC 340 - Programming Methodology",
    "CSC 413 - Software Development",
    "CSC 510 - Analysis of Algorithms",
    "CSC 615 - Database Systems",
    "CSC 620 - Operating Systems",
    "CSC 665 - Artificial Intelligence",
    "CSC 667 - Internet Application Development",
    "CSC 675 - Machine Learning",
    "CSC 690 - Interactive Multimedia",
    "MATH 226 - Calculus I",
    "MATH 227 - Calculus II",
    "MATH 325 - Linear Algebra",
    "MATH 471 - Probability & Statistics",
  ],
  skills: [
    "Python", "Java", "JavaScript", "SQL", "C++",
    "TensorFlow", "PyTorch", "React", "Git", "Docker",
    "Machine Learning", "Deep Learning", "Data Structures",
    "Algorithms", "REST APIs", "PostgreSQL",
  ],
  resumeUploaded: true,
  transcriptUploaded: true,
};
