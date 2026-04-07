# GenAI Retrieval Layer — Implementation Plan

## Scope (Current Phase)
Retrieval-only. No full Self-RAG loop yet. Focus:
- Push structured data to Supabase
- Embed data into local Qdrant
- Simple Streamlit chat grounded in retrieved evidence via Ollama

---

## File Structure

```
CSC-699/
├── ingest.py                      # Single pipeline: seed Supabase + embed into Qdrant
│
├── db/
│   ├── supabase_client.py         # Supabase connection singleton
│   └── qdrant_client.py           # Qdrant connection singleton (localhost:6333)
│
├── retrieval/
│   ├── embedder.py                # Ollama nomic-embed-text wrapper
│   ├── search.py                  # Qdrant semantic search → top-k results
│   └── context_builder.py         # Fetch full rows from Supabase to enrich results
│
├── streamlit_app/
│   └── app.py                     # Chat UI: student selector + optional job + chat
│
├── .env                           # SUPABASE_URL, SUPABASE_KEY
└── requirements.txt
```

---

## ingest.py — Execution Order

```
1. Connect Supabase
        ↓
2. Run JobSkill.sql schema (jobs, students, courses tables)
        ↓
3. Parse data/jobs.csv
   → upsert into Supabase jobs table
        ↓
4. Parse data/sfsu_csc_courses_clean_skills.csv
   → upsert into Supabase courses table
        ↓
5. Insert 3 fake students with different skill/course profiles
        ↓
6. Connect Qdrant (localhost:6333)
   → create jobs_collection (vector size: 768)
   → create courses_collection (vector size: 768)
        ↓
7. Fetch all jobs from Supabase
   → for each job: embed (title + description + skills_jobs_json) via Ollama
   → upsert point into jobs_collection
   payload: { job_id, title, company, skills }
        ↓
8. Fetch all courses from Supabase
   → for each course: embed (title + description + skills_courses_json) via Ollama
   → upsert point into courses_collection
   payload: { course_id, course_code, title, skills }
```

---

## Fake Students (seeded by ingest.py)

| Name       | Year     | Courses Done                       | Key Skills                              |
|------------|----------|------------------------------------|-----------------------------------------|
| Alex Chen  | Junior   | CSC 101, 220, 315, 340             | Python, Java, Data Structures, Algorithms |
| Maria Gomez| Senior   | CSC 220, 415, 510, 600             | ML, Python, Databases, OS               |
| Sam Patel  | Sophomore| CSC 101, 110, 215                  | Java, Programming Fundamentals          |

---

## Graph Flow (Detailed)

This is the retrieval graph. Each box is a LangGraph node. Arrows are conditional edges.

```
┌──────────────────────────────────────────────────────────────┐
│                        Graph State                           │
│  student_id, student_profile, optional_job_id,              │
│  conversation_history, user_message,                         │
│  query_embedding, evidence_bundle,                           │
│  prompt, llm_response                                        │
└──────────────────────────────────────────────────────────────┘

[START]
   │
   ▼
┌──────────────────────┐
│   intent_node        │
│                      │
│  - Read user_message │
│  - Read student      │
│    profile from      │
│    session state     │
│  - Classify intent:  │
│    · job_match       │
│    · skill_gap       │
│    · course_path     │
│    · general         │
│  - Output: intent,   │
│    retrieval_targets │
│    (jobs / courses / │
│     both)            │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   embed_node         │
│                      │
│  - Take user_message │
│  - Call Ollama       │
│    nomic-embed-text  │
│  - Output:           │
│    query_embedding   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────────────────────────────────────┐
│   retrieve_node                                      │
│                                                      │
│  - Use query_embedding + retrieval_targets           │
│    to decide which Qdrant collections to search      │
│                                                      │
│  IF intent = job_match or general:                   │
│    → search jobs_collection (top 5)                  │
│    → if optional_job_id is set, boost that job       │
│                                                      │
│  IF intent = skill_gap or course_path or general:    │
│    → search courses_collection (top 5)               │
│                                                      │
│  → fetch full rows from Supabase for each result id  │
│    (get skills_jobs_json, skills_courses_json, etc.) │
│                                                      │
│  Output: evidence_bundle = {                         │
│    student: { ...profile, completed_courses },       │
│    jobs:    [ { job_id, title, skills, score } ],    │
│    courses: [ { course_code, title, skills, score }] │
│  }                                                   │
└──────────┬───────────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────────┐
│   context_builder_node                               │
│                                                      │
│  - Compute skill overlap:                            │
│    student skills ∩ job required skills = covered    │
│    job required skills - student skills = gaps       │
│                                                      │
│  - Map gaps → which retrieved courses cover them     │
│                                                      │
│  - Build structured context string:                  │
│    "Student: Alex, Skills: [...], Gaps: [...]        │
│     Relevant Jobs: [...], Suggested Courses: [...]"  │
│                                                      │
│  Output: structured_context                          │
└──────────┬───────────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────────┐
│   generate_node                                      │
│                                                      │
│  - Build prompt:                                     │
│    SYSTEM: You are a career advisor. Answer only     │
│    from the evidence provided. Be specific.          │
│    CONTEXT: {structured_context}                     │
│    HISTORY: {last 4 turns}                           │
│    USER: {user_message}                              │
│                                                      │
│  - Call Ollama llama3.2 (streaming)                  │
│  - Output: llm_response                              │
└──────────┬───────────────────────────────────────────┘
           │
           ▼
┌──────────────────────┐
│   respond_node       │
│                      │
│  - Append response   │
│    to conversation   │
│    history           │
│  - Return response + │
│    evidence_bundle   │
│    (for UI sources)  │
└──────────┬───────────┘
           │
          [END]
```

### Conditional Edge: retrieve_node → skip retrieve

```
intent_node decides retrieval_targets:

  IF intent = "general" AND conversation already has evidence
      → skip to generate_node (use existing evidence_bundle)

  ELSE
      → go to embed_node → retrieve_node (normal path)
```

---

## Streamlit app.py — UI Layout

```
┌─────────────────────────────────────────┐
│         Student Advisor Chat            │
├─────────────────────────────────────────┤
│  Student:   [ Alex Chen ▼      ]        │
│  Job filter:[ Any              ▼ ]      │
├─────────────────────────────────────────┤
│                                         │
│  You: What skills am I missing          │
│       for an ML engineer role?          │
│                                         │
│  Advisor: Based on your profile,        │
│  you have Python and Data Structures    │
│  but are missing: TensorFlow,           │
│  Linear Algebra, Model Evaluation...   │
│  ▼ Sources (2 jobs, 3 courses)          │
│    · ML Engineer @ Stripe               │
│    · CSC 510 - Machine Learning         │
│    · CSC 600 - Deep Learning            │
│                                         │
├─────────────────────────────────────────┤
│  [ Type your question... ]   [Send]     │
└─────────────────────────────────────────┘
```

**Session state:**
- `student_id` — set when student is selected from dropdown
- `student_profile` — loaded from Supabase on selection
- `optional_job_id` — set when job filter is chosen (can be None)
- `conversation_history` — list of `{role, content}` dicts
- `last_evidence_bundle` — shown in "Sources" expander

---

## Prerequisites

```bash
# Qdrant (Docker)
docker run -p 6333:6333 qdrant/qdrant

# Ollama models
ollama pull nomic-embed-text   # for embeddings (768-dim)
ollama pull llama3.2           # for chat generation
```

---

## Dependencies (requirements.txt)

```
supabase
qdrant-client
langchain-ollama
langgraph
langchain-community
streamlit
pandas
python-dotenv
httpx
```

---

## Build Order

| Step | File | Action |
|------|------|--------|
| 1 | `.env` | Add SUPABASE_URL, SUPABASE_KEY |
| 2 | `db/supabase_client.py` | Supabase singleton |
| 3 | `db/qdrant_client.py` | Qdrant singleton |
| 4 | `ingest.py` | Run once to seed Supabase + Qdrant |
| 5 | `retrieval/embedder.py` | Ollama embed wrapper |
| 6 | `retrieval/search.py` | Qdrant search logic |
| 7 | `retrieval/context_builder.py` | Skill gap + context string builder |
| 8 | `streamlit_app/app.py` | Chat UI wired to retrieval graph |
