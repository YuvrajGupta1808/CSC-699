# Gold questions — quick index

Use this file to line up rows or slides (e.g. gold vs. model answer) with the canonical eval. Full traces, expected criteria, and model responses are in [`gold_results.md`](./gold_results.md) (run: **2026-05-12**). Definitions live in [`gold_questions.py`](./gold_questions.py).

## All 30 questions (ID → text)

| ID | Student | Category | Question |
|:---|:---|:---|:---|
| GQ-01 | Alex Chen | Specific Job Fit | Am I a good fit for the Junior Software Engineer role at Leidos? |
| GQ-02 | Maria Gomez | Specific Job Fit | Which ML engineering jobs match my profile and what's missing? |
| GQ-03 | Sam Patel | Specific Job Fit | I only have basic programming skills. What entry-level jobs are realistic for me right now? |
| GQ-04 | Alex Chen | Skill Gap Analysis | What specific skills am I missing to qualify for a full stack engineering role? |
| GQ-05 | Maria Gomez | Skill Gap Analysis | I'm strong in ML and deep learning. What gaps are blocking me from cloud engineering roles? |
| GQ-06 | Sam Patel | Skill Gap Analysis | What is the single most important skill I should learn next to become more employable? |
| GQ-07 | Alex Chen | Course Recommendation | Which courses should I take to become competitive for web development jobs? |
| GQ-08 | Sam Patel | Course Recommendation | What's the most valuable course I can take next semester to open up more job options? |
| GQ-09 | Maria Gomez | Course Recommendation | I've already taken CSC 415 and CSC 510. What advanced courses build on those for AI roles? |
| GQ-10 | Alex Chen | Career Readiness | I'm graduating in 6 months. Give me an honest assessment of my job market readiness. |
| GQ-11 | Maria Gomez | Career Readiness | Create a semester-by-semester plan to make me competitive for senior ML roles. |
| GQ-12 | Sam Patel | Career Readiness | Be honest — am I competitive for any real industry jobs right now? |
| GQ-13 | Alex Chen | Job Comparison | Between a software engineering role at Microsoft and one at a startup like Giga, which is a better fit for where I am now? |
| GQ-14 | Maria Gomez | Job Comparison | Which pays off more for my career — taking more ML courses or pivoting to cloud/DevOps? |
| GQ-15 | Alex Chen | Action Plan | What are the top 3 most impactful things I can do this semester to improve my job prospects? |
| GQ-16 | Sam Patel | Action Plan | If I can only take one more course, which one gives me the best shot at getting hired? |
| GQ-17 | Alex Chen | Domain Pivot | I want to pivot into data science. What's the gap between where I am and data science jobs? |
| GQ-18 | Maria Gomez | Domain Pivot | I'm thinking of moving into systems or embedded software. Is my background relevant at all? |
| GQ-19 | Alex Chen | Self-Assessment | What are my strongest marketable skills and which job category do they point toward? |
| GQ-20 | Maria Gomez | Self-Assessment | Given everything I've learned, what kind of engineer am I becoming and what should I double down on? |
| GQ-21 | Jordan Kim | Strong Fit | What full stack or web engineering roles am I competitive for right now? |
| GQ-22 | Marcus Webb | Strong Fit | Am I ready for a cloud or DevOps engineering role? |
| GQ-23 | Taylor Reyes | Strong Fit | Which ML or AI research engineering positions am I closest to qualifying for? |
| GQ-24 | Priya Sharma | Cross-Disciplinary | Given my biology and CS background, what unique job opportunities exist for me? |
| GQ-25 | Priya Sharma | Cross-Disciplinary | Which courses would strengthen my data science skills specifically for biomedical research? |
| GQ-26 | Jordan Kim | Skill Gap with Job Context | What skills am I missing to land a senior software engineer role? |
| GQ-27 | Marcus Webb | Skill Gap with Job Context | I want to move into ML engineering — what's the gap between my DevOps background and those roles? |
| GQ-28 | Taylor Reyes | Skill Gap with Job Context | What skills do I still need to qualify for production ML engineering at a top tech company? |
| GQ-29 | Alex Chen | Retrieval Precision | What Python-specific courses do I still need? |
| GQ-30 | Sam Patel | Retrieval Precision | Are there any jobs that only require Java? |

## Scores from latest report (for “what didn’t work”)

Legend in report: ≥8 strong, 6–8 mixed, &lt;6 weak.

| ID | Total /10 | Note |
|:---|:---:|:---|
| GQ-01 | 8.2 | |
| GQ-02 | 9.2 | |
| GQ-03 | 6.95 | |
| GQ-04 | 8.95 | |
| GQ-05 | 8.4 | |
| GQ-06 | 7.65 | |
| GQ-07 | 9.1 | |
| GQ-08 | 10.0 | |
| GQ-09 | 8.2 | |
| GQ-10 | 7.3 | |
| GQ-11 | 8.7 | |
| GQ-12 | 5.25 | Lowest; honesty / evidence for weak profile |
| GQ-13 | 6.2 | Microsoft vs startup comparison |
| GQ-14 | 9.2 | |
| GQ-15 | 8.95 | |
| GQ-16 | 9.15 | |
| GQ-17 | 8.15 | |
| GQ-18 | 6.95 | |
| GQ-19 | 8.2 | |
| GQ-20 | 8.5 | |
| GQ-21 | 8.1 | |
| GQ-22 | 6.55 | Cloud/DevOps readiness |
| GQ-23 | 7.4 | |
| GQ-24 | 7.15 | |
| GQ-25 | 7.85 | |
| GQ-26 | 8.45 | |
| GQ-27 | 8.35 | |
| GQ-28 | 7.85 | |
| GQ-29 | 6.85 | Python-only course retrieval |
| GQ-30 | 6.1 | Java-only jobs |

**Below 7 (good candidates if your image marks “wrong” or weak):** GQ-12, GQ-13, GQ-22, GQ-24, GQ-29, GQ-30 (plus GQ-03, GQ-06, GQ-10, GQ-18, GQ-23, GQ-25, GQ-28 if you use &lt;8 as the bar).

Re-run eval: `cd server && python tests/gold_questions.py` (overwrites `gold_results.md`).
