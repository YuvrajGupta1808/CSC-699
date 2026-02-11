
const titles = [
  "Software Engineer", "Senior Software Engineer", "Staff Software Engineer", "Principal Software Engineer",
  "Frontend Engineer", "Senior Frontend Engineer", "Backend Engineer", "Senior Backend Engineer",
  "Full-Stack Engineer", "Senior Full-Stack Engineer",
  "Data Scientist", "Senior Data Scientist", "Lead Data Scientist",
  "Machine Learning Engineer", "Senior ML Engineer", "ML Research Scientist",
  "DevOps Engineer", "Senior DevOps Engineer", "Site Reliability Engineer", "Senior SRE",
  "Security Engineer", "Senior Security Engineer", "Application Security Engineer",
  "Cloud Engineer", "Senior Cloud Engineer", "Cloud Architect",
  "Data Engineer", "Senior Data Engineer", "Lead Data Engineer",
  "iOS Engineer", "Android Engineer", "Mobile Engineer",
  "Engineering Manager", "Senior Engineering Manager", "Director of Engineering",
  "QA Engineer", "Senior QA Engineer", "SDET",
  "Platform Engineer", "Infrastructure Engineer",
  "Product Manager - Technical", "Technical Program Manager",
  "Solutions Architect", "Systems Engineer",
  "Software Engineer Intern", "Data Science Intern", "ML Intern", "Security Intern"
];

const bigTech = [
  "Google", "Meta", "Amazon", "Apple", "Microsoft", "Stripe", "Netflix", "Uber",
  "Airbnb", "Salesforce", "Adobe", "Oracle", "Intel", "NVIDIA", "IBM",
  "Snap Inc.", "Spotify", "Palantir", "Databricks", "Snowflake",
  "Coinbase", "Block (Square)", "Robinhood", "Doordash", "Lyft",
  "LinkedIn", "Twitter (X)", "Pinterest", "Reddit", "Dropbox",
  "Cloudflare", "Datadog", "MongoDB Inc.", "Elastic", "Confluent"
];
const other = [
  "Figma", "Notion", "Vercel", "Retool", "Plaid", "Anduril",
  "Scale AI", "Anthropic", "OpenAI", "Cohere", "Rippling",
  "Gusto", "Brex", "Ramp", "Faire", "Vanta"
];

const companies = [...bigTech, ...bigTech, ...other]; // weight big tech ~2x

const locations = [
  "San Francisco, CA", "Mountain View, CA", "Sunnyvale, CA", "Menlo Park, CA", "San Jose, CA",
  "Cupertino, CA", "Los Angeles, CA", "San Diego, CA",
  "Seattle, WA", "Bellevue, WA", "Redmond, WA",
  "New York, NY", "Brooklyn, NY",
  "Austin, TX", "Dallas, TX", "Houston, TX",
  "Boston, MA", "Cambridge, MA",
  "Chicago, IL", "Denver, CO", "Boulder, CO",
  "Atlanta, GA", "Raleigh, NC", "Washington, DC",
  "Pittsburgh, PA", "Portland, OR", "Miami, FL",
  "Remote (US)"
];

const employmentTypes = ["Full-time", "Full-time", "Full-time", "Full-time", "Contract", "Internship"];

const experienceLevels = ["Entry-level", "Mid-level", "Mid-level", "Senior", "Senior", "Lead", "Principal"];

const sources = ["LinkedIn", "LinkedIn", "LinkedIn", "Indeed", "Glassdoor", "Company Website"];

function pick(arr) { return arr[Math.floor(Math.random() * arr.length)]; }

function randomDate() {
  const now = Date.now();
  const thirtyDaysMs = 30 * 24 * 60 * 60 * 1000;
  const d = new Date(now - Math.floor(Math.random() * thirtyDaysMs));
  return d.toISOString().split("T")[0];
}

// Build all 100 jobs metadata first, then generate descriptions with AI
const entryTitles = [
  "Software Engineer Intern", "Data Science Intern", "ML Intern", "Security Intern",
  "Junior Software Engineer", "Junior Frontend Engineer", "Junior Backend Engineer",
  "Junior Data Scientist", "Junior DevOps Engineer", "Junior QA Engineer",
  "Software Engineer", "Frontend Engineer", "Backend Engineer", "Full-Stack Engineer",
  "Data Scientist", "Machine Learning Engineer", "DevOps Engineer",
  "Security Engineer", "Cloud Engineer", "Data Engineer",
  "iOS Engineer", "Android Engineer", "Mobile Engineer", "QA Engineer",
  "Platform Engineer", "Infrastructure Engineer", "SDET", "Systems Engineer"
];
const seniorTitles = [
  "Senior Software Engineer", "Staff Software Engineer", "Principal Software Engineer",
  "Senior Frontend Engineer", "Senior Backend Engineer", "Senior Full-Stack Engineer",
  "Senior Data Scientist", "Lead Data Scientist", "Senior ML Engineer", "ML Research Scientist",
  "Senior DevOps Engineer", "Senior SRE", "Senior Security Engineer",
  "Senior Cloud Engineer", "Cloud Architect", "Senior Data Engineer", "Lead Data Engineer",
  "Engineering Manager", "Senior Engineering Manager", "Director of Engineering",
  "Senior QA Engineer", "Technical Program Manager", "Solutions Architect"
];

const jobsMeta = [];
// 70 entry-level jobs
for (let i = 0; i < 70; i++) {
  const title = pick(entryTitles);
  const empType = title.includes("Intern") ? "Internship" : pick(["Full-time", "Full-time", "Full-time", "Contract"]);
  jobsMeta.push({
    id: generate.uuid(),
    title,
    company: pick(companies),
    location: pick(locations),
    empType,
    expLevel: "Entry-level",
    postedDate: randomDate(),
    source: pick(sources)
  });
}
// 30 other levels
for (let i = 0; i < 30; i++) {
  const title = pick(seniorTitles);
  let expLevel = pick(["Mid-level", "Senior", "Senior", "Lead", "Principal"]);
  if (title.includes("Principal") || title.includes("Director")) expLevel = "Principal";
  else if (title.includes("Lead") || title.includes("Manager")) expLevel = pick(["Senior", "Lead"]);
  else if (title.includes("Staff")) expLevel = "Senior";
  jobsMeta.push({
    id: generate.uuid(),
    title,
    company: pick(companies),
    location: pick(locations),
    empType: "Full-time",
    expLevel,
    postedDate: randomDate(),
    source: pick(sources)
  });
}

// Sort by posted_date ascending
jobsMeta.sort((a, b) => a.postedDate.localeCompare(b.postedDate));

// Generate descriptions in batches using AI
const BATCH = 100;
let completed = 0;

sendProgressUpdate("Generating job descriptions", 0);

const promises = jobsMeta.map(async (job) => {
  const desc = await generate.textUsingAi({
    prompt: `Write a realistic job posting description for the following role. Include sections: About the Role, Responsibilities (5-7 bullet points), Qualifications (5-7 bullet points), Nice to Have (3-4 bullet points), and a brief Benefits section. Make it sound authentic like a real ${job.company} posting.

Title: ${job.title}
Company: ${job.company}
Location: ${job.location}
Employment Type: ${job.empType}
Experience Level: ${job.expLevel}

Write it as plain text with clear section headers. Keep it between 300-500 words.`,
    schema: { type: "string" }
  });
  completed++;
  sendProgressUpdate("Generating job descriptions", Math.round((completed / 100) * 100));
  return { ...job, desc };
});

const results = await Promise.all(promises);

sendProgressUpdate("Inserting into database", 95);

for (const r of results) {
  db.update(
    `INSERT INTO jobs (job_id, title, company, location, employment_type, experience_level, job_description_raw, posted_date, source) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`,
    r.id, r.title, r.company, r.location, r.empType, r.expLevel, r.desc, r.postedDate, r.source
  );
}

sendProgressUpdate("Done", 100);
sendResult(`Inserted ${results.length} job listings.`);
