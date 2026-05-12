# JobSkill — Personalized Career Advisor

A personalized career advisor for CS students. Given a student profile (skills, completed courses), it retrieves relevant job postings and courses, analyzes skill gaps, and generates grounded recommendations via a LangGraph multi-candidate workflow.

---

## Architecture

```
client/               React + TypeScript frontend (Vite, Tailwind, shadcn/ui)
server/               Python backend
  ingest.py           One-shot pipeline: seed Supabase → embed → index Weaviate
  db/                 Supabase + Weaviate client singletons
  retrieval/          Core RAG pipeline
    planner.py        LLM-based intent classification + top-k routing
    search.py         Hybrid search (BM25 + semantic) via Weaviate, RRF reranking
    graph.py          LangGraph workflow: plan → retrieve → generate → critique → select
    candidates.py     Three evidence views (job-specific, cluster, course-path)
    critique.py       Support / relevance / utility scoring with structured citations
    context_builder.py  Supabase enrichment, stale-hit warnings
    embedder.py       Ollama nomic-embed-text (768-dim), LRU-cached
    llm.py            Ollama chat generation
    planner.py        LLM classifier with keyword fallback
    skills.py         Skill normalization + alias resolution
    observability.py  LangSmith tracing helpers
  eval/               Evaluation scripts and fixtures
  tests/              Unit + integration test suite
  streamlit_app/      Streamlit advisor chat UI
weaviate/             Index rebuild scripts (run after schema/data changes)
  index_jobs.py
  index_courses.py
data/                 Source data (read-only after first ingest)
  jobs.csv
  courses_catalog.csv
  schema.sql
syllabus/             Course syllabi used to build courses_catalog.csv
```

---

## Prerequisites

| Dependency | Purpose |
|---|---|
| Python 3.10+ | Backend |
| [Ollama](https://ollama.com/) | Embeddings (`nomic-embed-text`) + chat (`llama3.2`, `deepseek-r1:1.5b`) |
| Docker | Weaviate vector store |
| Supabase project | Persistent job/course/student records |
| Node.js 18+ | Frontend |

---

## Setup

### 1. Clone and configure

```bash
git clone https://github.com/YuvrajGupta1808/CSC-699.git
cd CSC-699
```

Create `.env` at the repo root:

```bash
SUPABASE_URL=...
SUPABASE_KEY=...

WEAVIATE_URL=http://localhost:8080
HYBRID_ALPHA=0.6                     # BM25/semantic blend (0=BM25, 1=semantic)

OLLAMA_URL=http://localhost:11434
OLLAMA_EMBED_MODEL=nomic-embed-text
OLLAMA_CHAT_MODEL=llama3.2
OLLAMA_CRITIQUE_MODEL=deepseek-r1:1.5b

RETRIEVAL_TOP_K_JOBS=5
RETRIEVAL_TOP_K_COURSES=5

LANGSMITH_TRACING=false              # set true to enable tracing
LANGSMITH_PROJECT=jobskill
LANGSMITH_API_KEY=...
```

### 2. Start services

```bash
# Weaviate (hybrid vector store)
docker run -d --name weaviate -p 8080:8080 -p 50051:50051 \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  -e DEFAULT_VECTORIZER_MODULE=none \
  -e ENABLE_MODULES="" \
  cr.weaviate.io/semitechnologies/weaviate:1.28.2

# Ollama models
ollama pull nomic-embed-text
ollama pull llama3.2
ollama pull deepseek-r1:1.5b
```

### 3. Install Python dependencies

```bash
cd server
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Seed data and build the index

```bash
# From repo root — seeds Supabase, then indexes Weaviate
PYTHONPATH=server python server/ingest.py

# To re-index Weaviate only (skip Supabase seeding):
PYTHONPATH=server python server/ingest.py --weaviate-only
```

### 5. Start the advisor UI

```bash
cd server
streamlit run streamlit_app/app.py
# → http://localhost:8501
```

### 6. Frontend (optional)

```bash
cd client
npm install
npm run dev
# → http://localhost:5173
```

---

## Re-indexing Weaviate

Run these after changing `jobs.csv`, `courses_catalog.csv`, or the embedding model:

```bash
PYTHONPATH=server python weaviate/index_jobs.py
PYTHONPATH=server python weaviate/index_courses.py
```

---

## Evaluation

```bash
# Planner intent + retrieval logic checks
PYTHONPATH=server python server/eval/evaluate.py

# End-to-end multi-turn advisor evaluation
PYTHONPATH=server python server/eval/live_conversation_eval.py

# 30-question gold eval (writes server/tests/gold_results.md)
cd server && python tests/gold_questions.py

# Full unit test suite
cd server && python -m pytest tests/ -q
```

---

## Retrieval Design

**Hybrid search** (Weaviate): every query runs BM25 (keyword matching on stored chunk text) and dense vector search (nomic-embed-text embeddings) simultaneously, fused at `HYBRID_ALPHA`. This fixes the pure-semantic limitation where exact skill names or course codes (e.g. `CSC 317`, `Kubernetes`) were averaged away in embedding centroids.

**Chunked indexing**: long job descriptions are split into 1400-char overlapping chunks; each chunk is one Weaviate object. At query time, chunk hits are max-pooled per record before RRF reranking.

**RRF reranking**: hybrid score + student-skill overlap + query-skill overlap are fused via Reciprocal Rank Fusion (k=60).

**LangGraph workflow**: `plan → search_jobs → search_courses → build_bundle → build_candidate_views → generate_candidates → critique_candidates → refine_retrieval → select_candidate`. If the best candidate has low support (< 6/10) and there are uncovered job gap skills, a targeted second retrieval pass is triggered before final selection.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, TypeScript, Vite, Tailwind CSS, shadcn/ui |
| Backend | Python, FastAPI (planned), Streamlit |
| Vector store | Weaviate (hybrid BM25 + semantic) |
| Embeddings | Ollama `nomic-embed-text` (768-dim) |
| LLM | Ollama `llama3.2` (chat), `deepseek-r1:1.5b` (critique) |
| Orchestration | LangGraph |
| Database | Supabase (PostgreSQL) |
| Observability | LangSmith |
