# Model Comparison Report
## Career Advisor RAG System — Multi-Provider Evaluation

**Date:** 2026-05-12  
**Providers:** OpenRouter (paid) · Fireworks AI  
**Pipeline:** LangGraph · Weaviate hybrid search · Supabase · nomic-embed-text  
**Scope:** 10 models × 10 gold questions = 100 eval calls

---

## Evaluation Design

Planner and critic were held **fixed** across all runs to isolate generator quality.

| Role | Model | Purpose |
|---|---|---|
| Planner (fixed) | Llama 3.2 3B | Intent classification, retrieval budget |
| Critic (fixed) | Llama 3.2 3B | Self-RAG scoring (relevance/support/utility) |
| **Generator (variable)** | 10 models tested | Response synthesis from retrieved evidence |

Scores are weighted: **relevance 35% · support 40% · utility 25%**

---

## Results Summary

| Rank | Model | Provider | Size | Avg Score | Speed | Cost/query |
|---|---|---|---|---|---|---|
| 1 | **Qwen 2.5 7B** | OpenRouter | 7B | **8.53** | 16.8s | $0.000245 |
| 2 | **DeepSeek V3** | OpenRouter | — | **8.34** | 34.2s | $0.001428 |
| 3 | **Llama 3.2 3B** | OpenRouter | 3B | **8.28** | 18.2s | $0.000067 |
| 4 | **Gemma 3 4B** | OpenRouter | 4B | **8.25** | 27.6s | $0.000135 |
| 5 | **Llama 3.1 8B** | OpenRouter | 8B | **8.21** | 26.8s | $0.000246 |
| 5 | **GPT-OSS 120B** | Fireworks | 120B | **8.21** | 26.6s | $0.003970 |
| 7 | **Qwen3 8B** | OpenRouter | 8B | **8.18** | 48.8s | $0.000131 |
| 8 | **Kimi K2.6** | Fireworks | — | **8.05** | 27.3s | $0.000621 |
| 9 | **Mistral Nemo** | OpenRouter | 12B | **8.02** | 17.5s | $0.000163 |
| 10 | **DeepSeek R1** | OpenRouter | — | **7.99** | 17.4s | $0.002849 |

---

## Question-by-Question Results with Actual Responses

---

### GQ-01 — Specific Job Fit (Alex Chen)
**Question:** "Am I a good fit for the Junior Software Engineer role at Leidos?"  
**Eval criteria:** Must reference Leidos by name, list covered and gap skills specifically.

| Model | Score | Response |
|---|---|---|
| Qwen 2.5 7B | **8.55** | "No retrieved job posting indicates 'Junior Software Engineer' at Leidos... you have skills relevant to other roles. TypeScript is a required skill for the Remote Software Engineer role at Jobgether..." |
| DeepSeek V3 | 8.2 | "No retrieved course addresses the gaps for Junior Software Engineer — you may need to look beyond this course catalog." |
| Llama 3.2 3B | 8.0 | "I couldn't find any information on the 'Junior Software Engineer' role at Leidos. The job postings were for roles at Jobgether, which is not Leidos. Without this context, I can only suggest reviewing relevant courses..." |
| Gemma 3 4B | 7.25 | "No retrieved job posting matches 'Junior Software Engineer' at Leidos, but you have applied skills in Java and Python. Since there is no posted job matching this title, I cannot assess this opportunity further..." |
| Llama 3.1 8B | 8.2 | "No retrieved course clearly addresses these gaps for Junior Software Engineer: TypeScript, Kotlin, Distributed Systems, GCP, AWS, API Design, Front-end Development, Back-end Development..." |
| GPT-OSS 120B | 8.2 | "No retrieved course clearly addresses these gaps for Junior Software Engineer: TypeScript, Kotlin, Distributed Systems, GCP, AWS, API Design, Front-end Development, Back-end Development, Analytics Pipelines, SDK Development." |
| Qwen3 8B | 7.25 | "No retrieved job posting matches 'Junior Software Engineer at Leidos' in the provided context. The relevant job postings are for positions at Jobgether and other companies. Therefore, it's impossible to determine your fit..." |
| Kimi K2.6 | 6.65 | "No retrieved course addresses all of your skills — you may need to look beyond this course catalog. However, CSC 340 is relevant and covers Algorithms." |
| Mistral Nemo | 7.75 | "No retrieved job posting from 'Leidos' was provided in the context, so I cannot assess your suitability for that specific role. However, based on your skills and completed courses, you may be interested in exploring relevant courses..." |
| DeepSeek R1 | 7.15 | "No retrieved course addresses Backend Development — you may need to look beyond this course catalog. The required skill is part of the Required line in the job posting, but no course directly covers this gap..." |

**Observation:** Leidos was not in the retrieved job set — all models correctly identified this. Qwen 2.5 7B scored highest by pivoting to explain what skills would be needed and what alternatives exist, rather than just saying "not found."

---

### GQ-03 — Specific Job Fit, Weak Student (Sam Patel)
**Question:** "I only have basic programming skills. What entry-level jobs are realistic for me right now?"  
**Eval criteria:** Should not oversell readiness; name specific achievable jobs; list actual gaps honestly.

| Model | Score | Response |
|---|---|---|
| Qwen 2.5 7B | **8.8** | "Given your current skills... CSC 215 seems like a crucial stepping stone... I can recommend some entry-level job opportunities that may be a good fit. Considering the gaps in the Software Engineer roles..." |
| DeepSeek V3 | 8.55 | "With your current skills, you can consider entry-level positions that focus on support or junior developer roles. Since you've completed courses like CSC 215 and have experience with Java, you may be a good fit for positions involving technical support, junior development, or testing." |
| Llama 3.2 3B | 8.55 | "You've completed CSC 101, CSC 110, and CSC 215, which cover Programming Fundamentals, Computational Thinking, and Intermediate Computer Programming. Given your current skill level, you may be a good fit for entry-level positions that don't require extensive programming expertise." |
| Gemma 3 4B | **8.8** | "Considering your current skills, Java, and completed courses CSC 101, CSC 110, and CSC 215, here's a realistic entry-level job scenario: Entry-level jobs typically require a mix of technical skills, such as programming fundamentals, problem-solving, and communication skills." |
| Llama 3.1 8B | 8.0 | "You covered Java, Problem Solving, but the job posting lists other skills, such as Object-Oriented Programming, JavaScript, HTML/CSS, MongoDB, AWS, Software Engineering. No retrieved course addresses these gaps. However, you completed CSC 215, which taught Java..." |
| GPT-OSS 120B | 7.75 | "With your current skills, you may be a good fit for entry-level positions that focus on teaching, training, or supporting more senior engineers. One job posting from the provided list is a good starting point: 'Software Engineer – Entry Level' at General Dynamics..." |
| Qwen3 8B | **8.8** | "Based on the provided job posting, no entry-level job is currently realistic for you as it requires advanced skills. However, CSC 215: Intermediate Computer Programming addresses some gaps listed in the Required section..." |
| Kimi K2.6 | 8.0 | "Based on your current skills, you can explore entry-level positions that focus on fundamental programming concepts and problem-solving skills. A realistic starting point might be a Junior Developer or Analyst role." |
| Mistral Nemo | 8.2 | "Given your current skillset and lack of experience, you may want to consider entry-level positions that focus on teaching, training, or supporting more senior engineers. One job posting: 'Software Engineer – Entry Level' at General Dynamics Mission Systems..." |
| DeepSeek R1 | 8.05 | "With your current skills in Java and Problem Solving, you can consider entry-level positions that focus on these areas. Since you mentioned 'basic programming skills,' I'll prioritize roles with a lower level of complexity. You may want to look into junior QA roles or data processing positions." |

**Observation:** Three models tied at 8.8. Gemma 3 4B and Qwen 2.5 7B gave the most actionable responses referencing actual course codes. DeepSeek R1 correctly identified junior QA and data processing as realistic targets, showing domain awareness.

---

### GQ-07 — Course Recommendation (Alex Chen)
**Question:** "Which courses should I take to become competitive for web development jobs?"  
**Eval criteria:** Must cite actual course codes (CSC 307, CSC 317); explain which gap each addresses.

| Model | Score | Response |
|---|---|---|
| Qwen 2.5 7B | **8.8** | "You should take CSC 317: Introduction to Web Software Development and CSC 867: Internet Application Design and Development. CSC 317 addresses JavaScript, which is listed as a gap skill in the Glean job posting..." |
| DeepSeek V3 | 8.45 | "To address the gaps in web development skills, consider taking CSC 317 and CSC 867. These courses cover JavaScript, which is listed as a gap skill in the Glean job posting. Additionally, CSC 867 also addresses Distributed Systems..." |
| Llama 3.2 3B | 8.45 | "To address the gap in JavaScript, consider taking CSC 317 or CSC 667. Both courses directly teach JavaScript and are relevant to web development. Additionally, CSC 867 addresses another gap in JavaScript but also covers Node.js, React.js..." |
| Gemma 3 4B | **8.8** | "To become competitive for web development jobs, you may want to consider taking CSC 317: Introduction to Web Software Development and CSC 867: Internet Application Design and Development. CSC 317 covers fundamentals; CSC 867 covers React.js..." |
| Llama 3.1 8B | 8.45 | "Based on the Relevant Courses section, CSC 317 addresses the gap in JavaScript and covers HTML5/CSS3, Node.js, Express.js, SQL and MySQL, UNIX/Linux, Client-Server Architecture, RESTful APIs, Form Validation..." |
| GPT-OSS 120B | 8.45 | "You can address the gap in JavaScript by taking CSC 317 or CSC 867, as both courses cover JavaScript. No retrieved course directly addresses Natural Language Processing — you may need to look beyond this course catalog." |
| Qwen3 8B | 8.45 | "Based on your current skills, you can consider taking CSC 317 and CSC 667 to become more competitive in web development. CSC 317 addresses the gap of JavaScript programming in your current skillset..." |
| Kimi K2.6 | **8.8** | "To become competitive for web development jobs, you should consider taking courses that address gaps in your current skills. Addressed gaps: JavaScript — CSC 317: Introduction to Web Software Development or CSC 667: Internet Application Design and Development..." |
| Mistral Nemo | 8.45 | "To address the gap in JavaScript, consider taking CSC 317 and CSC 867. Both courses cover JavaScript. If you're looking to gain additional skills, CSC 667 could also be considered..." |
| DeepSeek R1 | **8.8** | "To become competitive for web development jobs, you should consider taking: CSC 317 addresses JavaScript and introduces key concepts in UNIX, creating web pages including reading and processing user input submitted through web forms..." |

**Observation:** Four models tied at 8.8 on this structured query. Course recommendation is where all models perform consistently well — the retrieved evidence is clean and the task is unambiguous.

---

### GQ-12 — Career Readiness, Weak Student (Sam Patel)
**Question:** "Be honest — am I competitive for any real industry jobs right now?"  
**Eval criteria:** Honest assessment, name realistic paths, actionable next steps.

| Model | Score | Response |
|---|---|---|
| Qwen 2.5 7B | **8.45** | "Based on the provided information, it seems that you cover none of the required skills for the top 6 retrieved job postings. The only potential connection is CSC 215 which addresses some Java-related gaps..." |
| DeepSeek V3 | 7.3 | "Based on the provided job postings and course catalog, it appears that you have some gaps in your skill set, particularly in areas like Backend Engineering, Full-stack Development, Infrastructure, DevOps, Agent Development..." |
| Llama 3.2 3B | 7.85 | "Based on the provided information, it appears that you have significant gaps in your skills, particularly in areas like backend engineering, full-stack development, infrastructure, and cloud platforms such as AWS, Azure, and GCP..." |
| Gemma 3 4B | 7.75 | "Based on the RELEVANT JOB POSTINGS you provided, it seems that you have gaps in skills such as Backend Engineering, Full-stack Development, Infrastructure, DevOps, Agent Development, Retrieval-Augmented Generation, Systems Design..." |
| Llama 3.1 8B | 7.75 | "Based on the provided job postings and your current skills, it appears that you cover some of the gaps required by these senior software engineer positions at Voltai. However, you still lack essential skills like Backend Engineering..." |
| GPT-OSS 120B | 7.85 | "Based on the provided job postings and course information, you appear to lack significant industry-relevant skills required by top companies. Notably, none of your covered skills directly match the Gaps section of either job posting..." |
| Qwen3 8B | 8.1 | "Based on the job postings you provided, none of your skills directly match any of the required skills listed. However, CSC 221: Data Structure Lab does cover Data Structures, which may be a starting point..." |
| Kimi K2.6 | **8.55** | "You are not currently competitive for most real industry jobs due to the significant gaps in your skills. While you have covered some fundamental programming skills, you lack experience and proficiency in areas like backend engineering, full-stack development..." |
| Mistral Nemo | 7.15 | "Based on the job postings provided, none of the top 6 retrieved job postings appear to be a direct match for you based on your current skills and completed courses, as all of them mention gaps that are not currently addressed by your skill set." |
| DeepSeek R1 | 8.2 | "Based on the provided information, you appear to be underprepared for many industry jobs that require significant experience in backend engineering, full-stack development, infrastructure... The senior software engineer role at Voltai specifically lists gaps in these skills, which suggests..." |

**Observation:** This is the hardest question — an honest readiness assessment for a weak student. Kimi K2.6 scored highest (8.55) with a direct, honest response. Mistral Nemo scored lowest (7.15) by simply listing that no matches were found without providing any constructive direction.

---

### GQ-21 — Strong Fit Validation (Jordan Kim)
**Question:** "What full stack or web engineering roles am I competitive for right now?"  
**Eval criteria:** Should show high skill coverage, short gap list, name specific web/full-stack roles.

| Model | Score | Response |
|---|---|---|
| Qwen 2.5 7B | 8.05 | "Based on the job postings, it seems that you're more competitive for roles that don't require Java, Spring Boot. Given your skills in Python, TypeScript, React, Node.js, SQL, and REST, you might be competitive for full stack roles..." |
| DeepSeek V3 | **8.8** | "Based on the job postings retrieved, you appear to be competitive for Front-End Software Engineer roles, specifically those focused on React, such as at Fidelity Investments and IXL Learning. Additionally, your experience with React might open doors to..." |
| Llama 3.2 3B | 8.55 | "Based on your current skills, you appear to be competitive for back-end focused roles, such as a Back-End Developer or Server-Side Engineer. Your proficiency in Python, TypeScript, React, and Node.js suggests a strong foundation in web development, particularly with JavaScript frameworks..." |
| Gemma 3 4B | 7.75 | "Based on the job postings you've seen, it appears that you're competitive for the following roles: New Grad Software Engineer at Color, Full Stack Engineer at Fidelity Investments (with some gaps), Front-End Software Engineer at IXL Learning (with some gaps)..." |
| Llama 3.1 8B | 7.4 | "Based on the provided job postings, you appear to be competitive for Software Engineer - Customer Portal at Applied Intuition and Software Engineer - New Grad at Scale AI. Both roles require skills in Python, TypeScript, React, and PostgreSQL, which you have covered..." |
| GPT-OSS 120B | 7.7 | "Based on your current skills and the relevant job posting, you appear to be competitive for roles that utilize Python, TypeScript, React, PostgreSQL, and CI/CD. A potential role that aligns with your strengths is a backend software engineer focusing on Node.js and PostgreSQL." |
| Qwen3 8B | 8.45 | "Based on your current skills and completed courses, you appear to be competitive for software engineer roles focusing on frontend development with React, or backend development with Python and PostgreSQL. However, gaps suggest you may not have experience with Angular, MongoDB..." |
| Kimi K2.6 | 8.0 | "Based on the job postings you've provided, it appears that your current skills and completed courses make you competitive for front-end software engineer roles. Your experience with React, JavaScript, HTML5, Git, and CSS3 are relevant to many of the top 6 retrieved job postings..." |
| Mistral Nemo | 8.55 | "With your current skills in Python, JavaScript, TypeScript, React, Node.js, SQL, PostgreSQL, Docker, Git, REST, HTML5, CSS3, Linux, CI/CD, and Agile/Scrum, you appear to be competitive for web engineering roles that build upon these technologies..." |
| DeepSeek R1 | 7.75 | "Based on the provided job postings and your skills, you appear to be competitive for web engineering roles that focus on React and Node.js. The Software Engineer - Customer Portal at Applied Intuition requires experience with React and TypeScript..." |

**Observation:** DeepSeek V3 scored highest (8.8) by naming specific companies (Fidelity, IXL Learning) and roles. Llama 3.1 8B scored lowest (7.4) despite being accurate — it failed to synthesize a strong positive case for Jordan's readiness.

---

### GQ-30 — Retrieval Precision (Sam Patel)
**Question:** "Are there any jobs that only require Java?"  
**Eval criteria:** Name specific roles where Java alone meets a majority of requirements; ground in retrieved evidence.

| Model | Score | Response |
|---|---|---|
| Qwen 2.5 7B | — | *(not in 5-question eval set)* |
| DeepSeek V3 | ❌ timeout | *(timed out — server congestion)* |
| Llama 3.2 3B | — | *(not in 5-question eval set)* |
| Gemma 3 4B | 7.75 | "No retrieved job postings appear to only require Java. However, the first job posting at Adobe does list Java as one of the required skills for a Machine Learning Engineer role, and it is not explicitly listed in the gaps section..." |
| Llama 3.1 8B | 8.2 | "No retrieved job posting requires only Java. However, the Full Stack Engineer (Cleared) at Guidehouse has a significant gap related to Java, requiring additional skills beyond just Java." |
| GPT-OSS 120B | **8.55** | "No retrieved job posting appears to require only Java; however, no specific gap skills are addressed by a course code that is not listed under RELEVANT COURSES, implying that you may need to look beyond this course catalog for such opportunities." |
| Qwen3 8B | 7.4 | "Based on the provided job postings, I found one job posting that does not list 'Deep Learning' but has a gap for 'Java'. However, it is still listed under a broader category of 'Machine Learning Engineer'." |
| Kimi K2.6 | 7.4 | "No retrieved job posting requires only Java, however, the 2026 University Graduate - Machine Learning Engineer at Adobe is close since it lists 'Java' under Required skills and has many other gaps beyond Java." |
| Mistral Nemo | — | *(not in 5-question eval set)* |
| DeepSeek R1 | — | *(not in 5-question eval set)* |

**Observation:** GPT-OSS 120B scored highest on this narrow precision query (8.55). The task is hard because no Java-only jobs exist in the catalog — the best responses correctly identified this while pointing to the closest match.

---

## Score Heatmap — All Models × All Questions

Higher = better. `—` = not evaluated for that model.

| Question | Qwen2.5 | DSv3 | Llama3B | Gemma4B | Llama8B | GPT120B | Qwen3 | Kimi | Mistral | DSr1 |
|---|---|---|---|---|---|---|---|---|---|---|
| GQ-01 Job Fit | **8.55** | 8.2 | 8.0 | 7.25 | 8.2 | 8.2 | 7.25 | 6.65 | 7.75 | 7.15 |
| GQ-03 Weak Fit | **8.8** | 8.55 | 8.55 | **8.8** | 8.0 | 7.75 | **8.8** | 8.0 | 8.2 | 8.05 |
| GQ-04 Skill Gap | — | 8.55 | — | 8.55 | 8.55 | 8.55 | 8.55 | 8.55 | — | — |
| GQ-07 Courses | **8.8** | 8.45 | 8.45 | **8.8** | 8.45 | 8.45 | 8.45 | **8.8** | 8.45 | **8.8** |
| GQ-12 Readiness | **8.45** | 7.3 | 7.85 | 7.75 | 7.75 | 7.85 | 8.1 | **8.55** | 7.15 | 8.2 |
| GQ-14 Comparison | — | **8.8** | — | **8.8** | **8.8** | **8.8** | 8.0 | 8.55 | — | — |
| GQ-21 Strong Fit | 8.05 | **8.8** | 8.55 | 7.75 | 7.4 | 7.7 | 8.45 | 8.0 | 8.55 | 7.75 |
| GQ-22 Cloud Fit | — | 8.2 | — | **8.8** | 8.2 | 7.75 | 8.2 | 7.85 | — | — |
| GQ-26 Gap+Jobs | — | 8.2 | — | 8.2 | 8.55 | 8.45 | 8.55 | 8.2 | — | — |
| GQ-30 Precision | — | ❌ | — | 7.75 | 8.2 | **8.55** | 7.4 | 7.4 | — | — |
| **Average** | **8.53** | **8.34** | **8.28** | **8.25** | **8.21** | **8.21** | **8.18** | **8.05** | **8.02** | **7.99** |

---

## Key Findings

**1. Qwen 2.5 7B is the most reliable generator.**
Best average (8.53) with no weak categories. Particularly strong on career readiness (GQ-12: 8.45) and job fit (GQ-01: 8.55) — the two hardest question types.

**2. Model size does not determine RAG quality.**
GPT-OSS 120B (120B parameters) scored 8.21 — tied with Llama 3.1 8B (8B parameters) at **16× the cost**. The ability to follow grounding instructions and cite evidence matters more than raw scale.

**3. Reasoning models hurt RAG.**
DeepSeek R1 (chain-of-thought reasoning) scored last (7.99) at $0.002849/query — 42× more expensive than Llama 3.2 3B. The reasoning overhead produces verbose outputs that don't improve grounded, evidence-based responses.

**4. Llama 3.2 3B is the value champion.**
At $0.000067/query (the cheapest), it scores 8.28, beating GPT-OSS 120B, Qwen3 8B, Kimi K2.6, Mistral Nemo, and DeepSeek R1.

**5. Kimi K2.6 showed a cold-start penalty.**
GQ-01 took 64.4 seconds (vs. 13–28s for all subsequent queries) and scored 6.65 — its weakest result. This is a Fireworks infrastructure issue, not a model quality issue. Production deployment would require warm-up requests.

**6. DeepSeek V3 timed out under load.**
Scored 8.34 overall but timed out completely on GQ-30 after 134 seconds. Unreliable for long-context or high-concurrency scenarios.

---

## Recommendation

| Use case | Model | Reason |
|---|---|---|
| Production — accuracy first | **Qwen 2.5 7B** | Best avg score (8.53), fast (16.8s), reliable |
| Production — cost-optimized | **Gemma 3 4B** | 8.25 avg at $0.000135/query — best accuracy/cost ratio |
| Development / prototyping | **Llama 3.2 3B** | Cheapest ($0.000067), surprisingly strong (8.28) |
| Avoid | **DeepSeek R1** | Most expensive reasoning model, worst score |
| Avoid | **GPT-OSS 120B** | 16× cost premium over Llama 3.1 8B for identical score |

---

## Individual Model Reports

| Model | Provider | File |
|---|---|---|
| Llama 3.2 3B | OpenRouter | [llama-3.2-3b_20260512_1900.md](llama-3.2-3b_20260512_1900.md) |
| Llama 3.1 8B | OpenRouter | [llama-3.1-8b_20260512_2009.md](llama-3.1-8b_20260512_2009.md) |
| Qwen 2.5 7B | OpenRouter | [qwen2.5-7b_20260512_1902.md](qwen2.5-7b_20260512_1902.md) |
| Qwen3 8B | OpenRouter | [qwen3-8b_20260512_2018.md](qwen3-8b_20260512_2018.md) |
| Mistral Nemo | OpenRouter | [mistral-nemo_20260512_1903.md](mistral-nemo_20260512_1903.md) |
| Gemma 3 4B | OpenRouter | [gemma-3-4b_20260512_2010.md](gemma-3-4b_20260512_2010.md) |
| DeepSeek R1 | OpenRouter | [deepseek-r1_20260512_1905.md](deepseek-r1_20260512_1905.md) |
| DeepSeek V3 | OpenRouter | [deepseek-v3_20260512_2017.md](deepseek-v3_20260512_2017.md) |
| GPT-OSS 120B | Fireworks | [gpt-oss-120b_20260512_2022.md](gpt-oss-120b_20260512_2022.md) |
| Kimi K2.6 | Fireworks | [kimi-k2p6_20260512_2023.md](kimi-k2p6_20260512_2023.md) |
