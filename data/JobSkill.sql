CREATE TABLE "jobs" (
  "job_id" uuid PRIMARY KEY,
  "source" text,
  "title" text,
  "company" text,
  "location" text,
  "description" text,
  "skills_json" jsonb,
  "posted_at" timestamptz,
  "ingested_at" timestamptz
);

CREATE TABLE "students" (
  "student_id" uuid PRIMARY KEY,
  "name" text,
  "major" text,
  "completed_courses_json" jsonb,
  "skill_profile_json" jsonb,
  "last_recommendations_json" jsonb,
  "updated_at" timestamptz
);

CREATE TABLE "courses" (
  "course_id" uuid PRIMARY KEY,
  "course_code" text UNIQUE,
  "title" text,
  "description" text,
  "skills_json" jsonb,
  "updated_at" timestamptz
);
