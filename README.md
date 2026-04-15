# JobSkill - Personalized Job Recommendation System

A web-based intelligent career alignment platform that matches students' academic profiles with job opportunities through skill analysis and personalized recommendations.

## Overview

JobSkill analyzes academic transcripts, resumes, and job postings to provide personalized job recommendations. The system uses natural language processing to extract skills from documents and calculates alignment scores between candidate profiles and job requirements, helping students identify career opportunities and skill gaps.

## Key Features

- **Premium Upload Experience**: Modern, interactive document upload interface with visual feedback and drag-and-drop support
- **Profile Analysis**: Upload and parse academic transcripts and resumes to build comprehensive skill profiles
- **Job Matching**: Intelligent matching algorithm that compares candidate skills with job requirements
- **Skill Gap Analysis**: Identify missing skills and receive recommendations for courses to bridge gaps
- **Match Visualization**: Interactive matrix showing alignment between your skills and job requirements
- **Job Discovery**: Browse and filter job opportunities based on match scores
- **Detailed Breakdowns**: View skill-by-skill comparison for each job posting
- **Career Assistant Chat**: Interactive AI-powered chat for personalized career guidance and matching advice

## System Architecture

### Frontend (Client)
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Routing**: React Router v6
- **Styling**: Tailwind CSS with shadcn/ui components
- **State Management**: Tanstack Query
- **UI Components**: Radix UI primitives

### Backend & Retrieval (`server/`)
- **Python** pipeline seeds jobs/courses/students into Supabase, embeds with Ollama (`nomic-embed-text`), and stores vectors in **Qdrant**
- **LangGraph** orchestrates planner -> retrieval -> evidence bundle -> multi-candidate generation -> critique/ranking -> final response
- **Streamlit** chat UI runs the advisor workflow and exposes evidence + scorecard per answer
- **LangSmith** tracing is supported via environment variables for observability
- See **`PLAN.md`** for retrieval design and workflow details

### Data Processing
- Natural Language Processing for skill extraction
- Transcript and resume parsing
- Job posting analysis
- Skill matching algorithms

## Project Structure

```
.
├── client/                 # Frontend application
│   ├── src/
│   │   ├── components/    # Reusable UI components
│   │   ├── pages/         # Page components
│   │   │   ├── Index.tsx          # Landing page
│   │   │   ├── Upload.tsx         # Profile upload
│   │   │   ├── JobDiscovery.tsx   # Job browsing
│   │   │   ├── MatchResults.tsx   # Match visualization
│   │   │   ├── JobBreakdown.tsx   # Detailed analysis
│   │   │   └── Profile.tsx        # User profile
│   │   ├── data/          # Mock data and types
│   │   ├── lib/           # Utility functions
│   │   └── hooks/         # Custom React hooks
│   └── public/            # Static assets
├── server/                # Python: ingestion, retrieval graph, Streamlit advisor
│   ├── ingest.py
│   ├── db/                # Supabase & Qdrant clients
│   ├── retrieval/         # Embeddings, search, planner, graph, critique, observability
│   ├── streamlit_app/     # Advisor UI
│   └── requirements.txt
├── data/                  # Job postings, course skills, SQL schema
│   ├── jobs.csv
│   ├── sfsu_csc_courses_clean_skills.csv
│   ├── JobSkill.sql
│   └── courses/           # Course data maintenance helpers
│       ├── sync_courses_to_supabase.py
│       └── update_course_skills_from_syllabi.py
├── qdrant/
│   └── rebuild_course_vectors.py
├── PLAN.md                # Retrieval-layer implementation plan
└── PPM-personalized job recommendation.pdf  # Project documentation

```

## Getting Started

### Prerequisites

- Node.js 18 or higher
- npm or yarn package manager

**Backend / retrieval prerequisites:** Python 3.10+, [Ollama](https://ollama.com/) (embeddings + chat), Qdrant on `localhost:6333`, and a Supabase project.

### Installation

1. Clone the repository:
```bash
git clone https://github.com/YuvrajGupta1808/CSC-699.git
cd CSC-699
```

2. Install dependencies:
```bash
cd client
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open your browser and navigate to:
```
http://localhost:5173
```

### Backend (server)

From the repository root:

```bash
cd server
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Configure `.env` at the repo root with:

```bash
SUPABASE_URL=...
SUPABASE_KEY=...
QDRANT_URL=http://localhost:6333            # optional override
OLLAMA_URL=http://localhost:11434           # optional override
OLLAMA_EMBED_MODEL=nomic-embed-text         # optional override
OLLAMA_CHAT_MODEL=llama3.2                  # optional override
RETRIEVAL_TOP_K_JOBS=5                      # optional override
RETRIEVAL_TOP_K_COURSES=5                   # optional override
LANGSMITH_TRACING=false                     # optional
LANGSMITH_PROJECT=jobskill                  # optional
LANGSMITH_API_KEY=...                       # required only if tracing enabled
```

Run Qdrant + Ollama, seed data, then start the advisor UI:

```bash
docker run -d --name qdrant -p 6333:6333 qdrant/qdrant
ollama serve
ollama pull nomic-embed-text
ollama pull llama3.2
```

Then:

```bash
python ingest.py
streamlit run streamlit_app/app.py
```

Open:
`http://localhost:8501` (or the next free Streamlit port).

### Data/Vector Maintenance Helpers

Run from repo root (with `server/.venv` activated and `PYTHONPATH=server`):

```bash
python data/courses/update_course_skills_from_syllabi.py              # refresh curated course skills in CSV
PYTHONPATH=server python data/courses/sync_courses_to_supabase.py     # sync course catalog to Supabase
PYTHONPATH=server python qdrant/rebuild_course_vectors.py             # rebuild courses_collection vectors
```

### Available Scripts

```bash
npm run dev          # Start development server on port 5173
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint
npm test             # Run tests
npm run test:watch   # Run tests in watch mode
```

## Usage

1. **Upload Your Profile**: Navigate to the Upload page and submit your academic transcript and resume
2. **Browse Jobs**: Explore available job postings in the Job Discovery section
3. **View Matches**: See your match scores and alignment with different positions
4. **Analyze Skills**: Review detailed skill breakdowns to understand requirements
5. **Identify Gaps**: Discover which skills you need to develop for target roles

## Technology Stack

### Frontend
- React 18
- TypeScript
- Vite
- React Router
- Tailwind CSS
- shadcn/ui
- Radix UI
- Tanstack Query
- Lucide Icons

### Backend & data
- Python, Supabase, Qdrant, Streamlit, pandas
- Ollama for embeddings and chat models
- LangGraph for workflow orchestration
- LangSmith for tracing/observability (optional)

### Development Tools
- ESLint for code linting
- Vitest for testing
- TypeScript for type safety

## Features in Detail

### Skill Extraction
The system analyzes uploaded documents to extract:
- Technical skills from coursework
- Programming languages and frameworks
- Soft skills and competencies
- Academic achievements

### Matching Algorithm
Calculates alignment scores based on:
- Skill overlap between profile and job requirements
- Skill proficiency levels
- Required vs. preferred qualifications
- Experience and education requirements

### Visualization
- Interactive skill matrix showing match percentages
- Skill bar charts for individual competencies
- Color-coded match indicators
- Gap analysis visualizations

## Contact

For more information, refer to the project documentation in `PPM-personalized job recommendation.pdf`.
