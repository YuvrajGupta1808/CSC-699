CREATE TABLE "jobs" (
  "job_id" uuid PRIMARY KEY,
  "source" text,
  "title" text,
  "company" text,
  "location" text,
  "description" text,
  "skills_jobs" text[],
  "posted_at" timestamptz,
  "ingested_at" timestamptz
);

CREATE TABLE "students" (
  "student_id" uuid PRIMARY KEY,
  "name" text,
  "major" text,
  "completed_courses" text[],
  "skill_profile" text[],
  "last_recommendations" text[],
  "updated_at" timestamptz
);

CREATE TABLE "courses" (
  "course_id" uuid PRIMARY KEY,
  "course_code" text UNIQUE,
  "title" text,
  "description" text,
  "skills_courses" text[],
  "updated_at" timestamptz
);
