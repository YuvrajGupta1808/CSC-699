# Gold Question Evaluation Report

**Run date:** 2026-05-12 12:18
**Total questions:** 30
**System:** LangGraph advisor · Ollama (llama3.2) · Qdrant + Supabase

## Summary

| Metric | Value |
|---|---|
| Passed | 30/30 |
| Errors | 0 |
| Average score | 7.82/10 |
| Average time | 45.4s |
| Score legend | 🟢 ≥8 · 🟡 ≥6 · 🔴 <6 |

## Scores At a Glance

| ID | Category | Student | Intent | Rel | Sup | Util | **Total** | Time |
|---|---|---|---|---|---|---|---|---|
| GQ-01 | Specific Job Fit | Alex Chen | `jobs` | 8 | 6 | 3 | 🔴 **5.95** | 45.0s |
| GQ-02 | Specific Job Fit | Maria Gomez | `skill_gap` | 7 | 8 | 8 | 🟡 **7.65** | 54.5s |
| GQ-03 | Specific Job Fit | Sam Patel | `jobs` | 8 | 9 | 6 | 🟡 **7.9** | 35.1s |
| GQ-04 | Skill Gap Analysis | Alex Chen | `skill_gap` | 8 | 10 | 7 | 🟢 **8.55** | 32.0s |
| GQ-05 | Skill Gap Analysis | Maria Gomez | `skill_gap` | 7 | 8 | 8 | 🟡 **7.65** | 41.7s |
| GQ-06 | Skill Gap Analysis | Sam Patel | `skill_gap` | 10 | 8 | 8 | 🟢 **8.7** | 38.1s |
| GQ-07 | Course Recommendation | Alex Chen | `courses` | 10 | 8 | 9 | 🟢 **8.95** | 39.0s |
| GQ-08 | Course Recommendation | Sam Patel | `courses` | 10 | 8 | 6 | 🟢 **8.2** | 34.4s |
| GQ-09 | Course Recommendation | Maria Gomez | `courses` | 8 | 10 | 8 | 🟢 **8.8** | 33.9s |
| GQ-10 | Career Readiness | Alex Chen | `broad` | 3 | 9 | 6 | 🟡 **6.15** | 41.6s |
| GQ-11 | Career Readiness | Maria Gomez | `broad` | 10 | 4 | 10 | 🟡 **7.6** | 89.8s |
| GQ-12 | Career Readiness | Sam Patel | `broad` | 3 | 6 | 5 | 🔴 **4.7** | 47.8s |
| GQ-13 | Job Comparison | Alex Chen | `jobs` | 6 | 8 | 7 | 🟡 **7.05** | 34.2s |
| GQ-14 | Job Comparison | Maria Gomez | `skill_gap` | 8 | 10 | 8 | 🟢 **8.8** | 50.7s |
| GQ-15 | Action Plan | Alex Chen | `broad` | 10 | 8 | 10 | 🟢 **9.2** | 50.8s |
| GQ-16 | Action Plan | Sam Patel | `courses` | 6 | 10 | 8 | 🟢 **8.1** | 34.2s |
| GQ-17 | Domain Pivot | Alex Chen | `skill_gap` | 6 | 10 | 7 | 🟡 **7.85** | 44.7s |
| GQ-18 | Domain Pivot | Maria Gomez | `jobs` | 7 | 8 | 5 | 🟡 **6.9** | 49.5s |
| GQ-19 | Self-Assessment | Alex Chen | `skill_gap` | 9 | 8 | 10 | 🟢 **8.85** | 50.9s |
| GQ-20 | Self-Assessment | Maria Gomez | `broad` | 10 | 8 | 9 | 🟢 **8.95** | 54.4s |
| GQ-21 | Strong Fit | Jordan Kim | `jobs` | 9 | 5 | 10 | 🟡 **7.65** | 48.6s |
| GQ-22 | Strong Fit | Marcus Webb | `broad` | 10 | 8 | 10 | 🟢 **9.2** | 51.1s |
| GQ-23 | Strong Fit | Taylor Reyes | `jobs` | 8 | 6 | 7 | 🟡 **6.95** | 53.6s |
| GQ-24 | Cross-Disciplinary | Priya Sharma | `jobs` | 9 | 8 | 7 | 🟢 **8.1** | 40.6s |
| GQ-25 | Cross-Disciplinary | Priya Sharma | `courses` | 8 | 9 | 7 | 🟢 **8.15** | 46.1s |
| GQ-26 | Skill Gap with Job Context | Jordan Kim | `skill_gap` | 10 | 8 | 10 | 🟢 **9.2** | 38.5s |
| GQ-27 | Skill Gap with Job Context | Marcus Webb | `skill_gap` | 7 | 8 | 6 | 🟡 **7.15** | 56.3s |
| GQ-28 | Skill Gap with Job Context | Taylor Reyes | `skill_gap` | 8 | 9 | 8 | 🟢 **8.4** | 39.3s |
| GQ-29 | Retrieval Precision | Alex Chen | `courses` | 9 | 6 | 8 | 🟡 **7.55** | 36.7s |
| GQ-30 | Retrieval Precision | Sam Patel | `jobs` | 8 | 4 | 5 | 🔴 **5.65** | 47.8s |

---

## Question-by-Question Results

### Specific Job Fit

#### GQ-01 — Alex Chen

**Query:** _Am I a good fit for the Junior Software Engineer role at Leidos?_

**Rationale:** Tests whether the system retrieves a specific named job and computes Alex's exact gap for it.

**Expected:** Must reference Leidos by name, list Alex's covered and gap skills specifically.

| Field | Value |
|---|---|
| Intent | `jobs` (jobs=1, courses=0) |
| Planner reason | None |
| Relevance | 8/10 |
| Support | 6/10 |
| Utility | 3/10 |
| **Total** | 🔴 **5.95/10** |
| Time | 45.0s |

**Critique flags:**
- ⚠️ unsupported job titles: junior software engineer
- ⚠️ company references do not align with retrieved jobs

**Critique summary:** The response lacks specificity in identifying course codes or skills that directly address the evidence context. It merely states the gaps without providing clear, actionable recommendations.

**Response:**

> To assess your fit for the Junior Software Engineer role at Leidos, we'll examine the job requirements. The required skills are: Java, Agile Development, IT Service Management (ITSM), Cloud Computing, Problem Solving.
> 
> You have Python and Java as part of your current skill set, so you cover some of the required skills. However, the gaps in the job posting remain: Agile Development, IT Service Management (ITSM), Cloud Computing, and Problem Solving.
> 
> No retrieved course clearly addresses the gaps for Junior Software Engineer at Leidos — you may need to look beyond this course catalog to develop these skills.

---

#### GQ-02 — Maria Gomez

**Query:** _Which ML engineering jobs match my profile and what's missing?_

**Rationale:** Maria has ML/DL skills — tests whether the system retrieves ML-relevant roles and accurately identifies remaining gaps.

**Expected:** Should surface ML-relevant roles, use Maria's actual skill set, list specific gaps.

| Field | Value |
|---|---|
| Intent | `skill_gap` (jobs=3, courses=4) |
| Planner reason | None |
| Relevance | 7/10 |
| Support | 8/10 |
| Utility | 8/10 |
| **Total** | 🟡 **7.65/10** |
| Time | 54.5s |

**Critique flags:**
- ⚠️ unsupported job titles: enterprise genai

**Critique summary:** fallback critique

**Response:**

> Based on your current skills and completed courses, here are two relevant job postings that match your profile:
> 
> 1. Applied AI Engineer, Enterprise GenAI at Scale AI:
> You cover 2 out of 15 required skills: Machine Learning, Python.
> The gaps in this role are: Cloud Technology, Data-Driven Approach, Software Engineering, Generative AI, Technical Solutions, Cybersecurity, Collaboration, Debugging, Multimodal Functionality, Tool-Calling, Business Requirements, AI Applications, Model Performance, Research.
> 
> 2. No retrieved job posting matches your profile exactly.
> However, the gaps in your completed courses are addressed by CSC 306: An Interdisciplinary Approach to Computer Programming (addresses debugging skill), and CSC 803: Generative AI: Fundamentals and Applications (covers generative AI).

---

#### GQ-03 — Sam Patel

**Query:** _I only have basic programming skills. What entry-level jobs are realistic for me right now?_

**Rationale:** Sam has minimal skills — tests realistic expectation setting for an underprepared student.

**Expected:** Should not oversell Sam's readiness; should name specific achievable jobs and list actual gaps honestly.

| Field | Value |
|---|---|
| Intent | `jobs` (jobs=6, courses=2) |
| Planner reason | None |
| Relevance | 8/10 |
| Support | 9/10 |
| Utility | 6/10 |
| **Total** | 🟡 **7.9/10** |
| Time | 35.1s |

**Critique summary:** The response does not provide specific skill gaps or recommended courses for entry-level jobs beyond general problem-solving. It misses mentioning relevant job postings.

**Response:**

> Given your current skillset, it's essential to focus on entry-level positions that align with your strengths. Since you've completed CSC 215 (which implies some problem-solving skills), let's explore job openings that might be a good fit.
> 
> Considering your current skills in Programming Fundamentals, Computational Thinking, and Problem Solving, you may want to look into junior roles that require basic programming proficiency. Here are a few entry-level positions to consider:
> 
> 1. Junior Software Tester - You can leverage your problem-solving skills and test your knowledge of programming concepts.
> 2. Help Desk Technician - Your technical background will be valuable in troubleshooting hardware and software issues for clients or internal teams.
> 
> These jobs may not directly address the gaps in the Site Reliability Engineer job posting, but they're entry-level positions that don't require extensive programming expertise. However, to become competitive for more senior roles, you'll need to exp

---

### Skill Gap Analysis

#### GQ-04 — Alex Chen

**Query:** _What specific skills am I missing to qualify for a full stack engineering role?_

**Rationale:** Tests extraction of full-stack-specific gap skills from retrieved job evidence.

**Expected:** Must name concrete missing skills (e.g. JavaScript, React, SQL) grounded in job evidence.

| Field | Value |
|---|---|
| Intent | `skill_gap` (jobs=3, courses=4) |
| Planner reason | None |
| Relevance | 8/10 |
| Support | 10/10 |
| Utility | 7/10 |
| **Total** | 🟢 **8.55/10** |
| Time | 32.0s |

**Critique summary:** fallback critique

**Response:**

> Based on the job postings, you are missing React, Node.js, Tailwind CSS, HTML/CSS, FastAPI, WebSockets, Vector Databases, LLM APIs, UI/UX Design, Data Engineering, and Full Stack Development skills.

---

#### GQ-05 — Maria Gomez

**Query:** _I'm strong in ML and deep learning. What gaps are blocking me from cloud engineering roles?_

**Rationale:** Tests cross-domain gap detection — Maria's ML profile vs cloud requirements.

**Expected:** Should identify cloud-specific gaps (GCP, AWS, Terraform, etc.) not covered by Maria's ML background.

| Field | Value |
|---|---|
| Intent | `skill_gap` (jobs=3, courses=4) |
| Planner reason | None |
| Relevance | 7/10 |
| Support | 8/10 |
| Utility | 8/10 |
| **Total** | 🟡 **7.65/10** |
| Time | 41.7s |

**Critique flags:**
- ⚠️ unsupported skill mentions: csc

**Critique summary:** fallback critique

**Response:**

> Based on the job postings, you have gaps in Cloud Technology, Data-Driven Approach, Software Engineering, Generative AI, Technical Solutions, Cybersecurity, Collaboration, Debugging, Multimodal Functionality, Tool-Calling, Business Requirements, AI Applications, Model Performance, and Research. 
> 
> A course that addresses some of these gaps is CSC 603: Generative AI: Fundamentals and Applications, which covers Generative AI.

---

#### GQ-06 — Sam Patel

**Query:** _What is the single most important skill I should learn next to become more employable?_

**Rationale:** Tests prioritized advice — system should pick one concrete skill with justification from evidence.

**Expected:** Must name one specific skill with supporting job evidence, not a generic list.

| Field | Value |
|---|---|
| Intent | `skill_gap` (jobs=3, courses=4) |
| Planner reason | None |
| Relevance | 10/10 |
| Support | 8/10 |
| Utility | 8/10 |
| **Total** | 🟢 **8.7/10** |
| Time | 38.1s |

**Critique flags:**
- ⚠️ unsupported skill mentions: next to

**Critique summary:** The response provides actionable insights, but it could have been more concise.

**Response:**

> Based on the provided job posting, Python is the single most important skill you can learn next to become more employable. You are currently covering Java, but the job posting requires and highlights Python as a key skill for this role. Additionally, two courses (CSC 411: Intermediate Machine Learning for Interdisciplinary Data Scientists and CSC 871: Deep Learning) also address Python as a gap skill that you can fill by taking these courses.

---

### Course Recommendation

#### GQ-07 — Alex Chen

**Query:** _Which courses should I take to become competitive for web development jobs?_

**Rationale:** Tests course retrieval for a specific domain — web dev — with course code citation.

**Expected:** Must cite actual course codes (e.g. CSC 307, CSC 317) and explain which gap each addresses.

| Field | Value |
|---|---|
| Intent | `courses` (jobs=0, courses=6) |
| Planner reason | None |
| Relevance | 10/10 |
| Support | 8/10 |
| Utility | 9/10 |
| **Total** | 🟢 **8.95/10** |
| Time | 39.0s |

**Critique flags:**
- ⚠️ unsupported course titles: html and css

**Critique summary:** unsupported course titles: html and css

**Response:**

> To become competitive for web development jobs, you should consider taking CSC 317: Introduction to Web Software Development and CSC 307: An Interdisciplinary Approach to Web Programming, with a focus on CSC 317. 
> 
> CSC 317 addresses essential skills such as JavaScript, HTML5 and CSS3, Node.js, Express.js, SQL and MySQL, Client-Server Architecture, RESTful APIs, Form Validation and Sanitization, Session Management and Cookies, Git/GitHub, Responsive Web Design, and Web Security. 
> 
> CSC 307 also covers important topics like HTML and CSS, PHP, Python, SQL and MySQL, Database Design, Client-Server Architecture, Form Validation, Web Security, Web Debugging, and Database Querying.

---

#### GQ-08 — Sam Patel

**Query:** _What's the most valuable course I can take next semester to open up more job options?_

**Rationale:** Tests highest-impact course recommendation for a beginner student.

**Expected:** Must name a specific course code and explain which job gaps it closes.

| Field | Value |
|---|---|
| Intent | `courses` (jobs=0, courses=6) |
| Planner reason | None |
| Relevance | 10/10 |
| Support | 8/10 |
| Utility | 6/10 |
| **Total** | 🟢 **8.2/10** |
| Time | 34.4s |

**Critique flags:**
- ⚠️ citation source 'course code' not found in evidence

**Critique summary:** No evidence of explicitly citing skill names, only job titles and course codes where applicable.

**Response:**

> Based on your current skills and completed courses, CSC 306: An Interdisciplinary Approach to Computer Programming appears to be a relevant course that addresses several gaps in your skillset. It covers Python programming, procedural programming, scientific computing, data analysis, problem-solving, and control flow, which are valuable skills for a wide range of job options.
> 
> Additionally, this course may also enhance your computational thinking and problem-solving skills, which are essential for many roles in the computer science field.

---

#### GQ-09 — Maria Gomez

**Query:** _I've already taken CSC 415 and CSC 510. What advanced courses build on those for AI roles?_

**Rationale:** Tests awareness of completed courses and progression recommendations.

**Expected:** Should not recommend CSC 415/510 again; should suggest genuinely next-level courses for AI.

| Field | Value |
|---|---|
| Intent | `courses` (jobs=0, courses=6) |
| Planner reason | None |
| Relevance | 8/10 |
| Support | 10/10 |
| Utility | 8/10 |
| **Total** | 🟢 **8.8/10** |
| Time | 33.9s |

**Critique summary:** fallback critique

**Response:**

> Since you've completed CSC 415 (Operating System Principles) and CSC 510 (Analysis of Algorithms I), here are a few relevant advanced courses that can help build on your foundation for AI roles:
> 
> - CSC 865: Artificial Intelligence 
>   Teaches: AI Search Algorithms, Heuristic Search, Adversarial Search, Machine Learning Fundamentals, Neural Networks, Knowledge Representation, Bayesian Networks, Constraint Satisfaction, Evolutionary Algorithms, Reinforcement Learning, Python, Agent Architectures, Natural Language Processing

---

### Career Readiness

#### GQ-10 — Alex Chen

**Query:** _I'm graduating in 6 months. Give me an honest assessment of my job market readiness._

**Rationale:** Tests broad readiness analysis — should balance encouragement with honest gap identification.

**Expected:** Must be grounded in Alex's actual skills, name real jobs, not claim readiness for roles he can't fill.

| Field | Value |
|---|---|
| Intent | `broad` (jobs=6, courses=6) |
| Planner reason | None |
| Relevance | 3/10 |
| Support | 9/10 |
| Utility | 6/10 |
| **Total** | 🟡 **6.15/10** |
| Time | 41.6s |

**Critique summary:** The response inaccurately states that there are no gaps in the student

**Response:**

> Based on the provided information, it appears that you have a strong foundation in programming languages (Python, Java) and fundamental computer science concepts (Data Structures, Algorithms). However, your current skills list doesn't include any gaps in areas like Automation, Cloud Computing, or Data Science, which are increasingly in demand.
> 
> The job postings you've been matched with highlight the importance of skills in these areas. For example, the Senior Site Reliability Engineer role at iManage requires expertise in automation, cloud computing, and containerization. While your completed courses (CSC 101, CSC 220, CSC 315, CSC 340) are relevant to computer science, they may not directly address the gaps mentioned in the job postings.
> 
> Your current skills list only covers Java, Python, and some fundamental CS concepts, but it lacks a broad range of technologies and skills that would make you more competitive in the job market.

---

#### GQ-11 — Maria Gomez

**Query:** _Create a semester-by-semester plan to make me competitive for senior ML roles._

**Rationale:** Tests multi-step planning grounded in available courses and job requirements.

**Expected:** Must use real course codes, real job titles from evidence; should not invent steps or skills.

| Field | Value |
|---|---|
| Intent | `broad` (jobs=6, courses=6) |
| Planner reason | None |
| Relevance | 10/10 |
| Support | 4/10 |
| Utility | 10/10 |
| **Total** | 🟡 **7.6/10** |
| Time | 89.8s |

**Critique flags:**
- ⚠️ unsupported course codes: CSC 720, CSC 725, CSC 730
- ⚠️ unsupported course titles: coursera or
- ⚠️ response suggests non-retrieved learning resources

**Critique summary:** unsupported course codes: CSC 720, CSC 725, CSC 730; unsupported course titles: coursera or

**Response:**

> To create a comprehensive plan, let's focus on the gaps you have in your skillset. You need to develop skills in:
> 
> React, Django, AWS, LLMs, and Code Review.
> 
> Here is a suggested plan to help you build these skills over two semesters:
> 
> Semester 1:
> - Take CSC 720: Data Science with Deep Learning — this course covers LLMs.
> - Enroll in an online React bootcamp or take CSC 725: Frontend Development with React — address the React gap skill.
> - Complete a bootcamp or enroll in CSC 730: Django for Web Development — this addresses Django's gap skill.
> - Begin learning AWS fundamentals through online resources like Coursera or edX (since no retrieved course directly covers AWS).
> 
> Semester 2:
> - Take CSC 750: Cloud Computing with AWS — directly addresses the AWS gap skill.
> - Enroll in an online bootcamp or take CSC 740: Code Review and Version Control — this addresses Code Review's gap skill.
> - Continue learning React, Django, and AWS through self-study or additional courses.
> 
> By following this pla

---

#### GQ-12 — Sam Patel

**Query:** _Be honest — am I competitive for any real industry jobs right now?_

**Rationale:** Tests candid honest assessment for a weak profile without being discouraging.

**Expected:** Should not invent optimism — must reflect Sam's limited skill set accurately while pointing to a path forward.

| Field | Value |
|---|---|
| Intent | `broad` (jobs=6, courses=6) |
| Planner reason | None |
| Relevance | 3/10 |
| Support | 6/10 |
| Utility | 5/10 |
| **Total** | 🔴 **4.7/10** |
| Time | 47.8s |

**Critique flags:**
- ⚠️ unsupported job titles: senior software engineer, voltai. the

**Critique summary:** The AI Career Advisor

**Response:**

> Based on the provided job posting and course catalog, it appears that you may not be directly competitive for the Senior Software Engineer role at Voltai. The job posting lists a wide range of technical skills as Required, many of which are not currently covered in your completed courses or listed as gaps in your skillset.
> 
> However, it's worth noting that CSC 859 and CSC 803 cover some of the key areas mentioned in the job posting (Explainable AI, Retrieval-Augmented Generation). While these courses are a good starting point, they may not provide comprehensive coverage of all required skills.

---

### Job Comparison

#### GQ-13 — Alex Chen

**Query:** _Between a software engineering role at Microsoft and one at a startup like Giga, which is a better fit for where I am now?_

**Rationale:** Tests comparative multi-job reasoning — system must assess Alex against two different role profiles.

**Expected:** Must compare both companies using evidence; should not fabricate requirements not in retrieved data.

| Field | Value |
|---|---|
| Intent | `jobs` (jobs=2, courses=0) |
| Planner reason | None |
| Relevance | 6/10 |
| Support | 8/10 |
| Utility | 7/10 |
| **Total** | 🟡 **7.05/10** |
| Time | 34.2s |

**Critique flags:**
- ⚠️ unsupported job titles: university grad

**Critique summary:** fallback critique

**Response:**

> Considering your current skills and completed courses, neither option directly aligns with the gaps in the job posting for Software Engineer, University Grad at Glean. No retrieved course clearly addresses these gaps: JavaScript, Natural Language Processing, Distributed Systems.

---

#### GQ-14 — Maria Gomez

**Query:** _Which pays off more for my career — taking more ML courses or pivoting to cloud/DevOps?_

**Rationale:** Tests strategic advice grounded in job evidence — system must compare both paths using retrieved data.

**Expected:** Must use retrieved job and course evidence; must not speculate beyond the evidence.

| Field | Value |
|---|---|
| Intent | `skill_gap` (jobs=3, courses=4) |
| Planner reason | None |
| Relevance | 8/10 |
| Support | 10/10 |
| Utility | 8/10 |
| **Total** | 🟢 **8.8/10** |
| Time | 50.7s |

**Critique summary:** fallback critique

**Response:**

> Based on the job postings, Site Reliability Engineer at Qlik requires a broader range of skills that cover not just programming languages like Python but also infrastructure management and security. The salary implications suggest that this role tends to be higher paying.
> 
> In contrast, AI Engineer at HAVI focuses more on Artificial Intelligence, Machine Learning, and Deep Learning-specific technologies. While the job posting does mention Azure Databricks and Apache Spark, which are cloud-based platforms, they are not necessarily considered a primary skillset for the role.
> 
> Pivoting to cloud/DevOps would require taking courses that cover Kubernetes, Terraform, AWS, or Azure, among others. These skills can be valuable across various industries, including IT and software development.
> 
> Considering your current skill set includes Machine Learning, Python, Databases, Operating Systems, Deep Learning, and SQL, there is a moderate gap in the cloud/DevOps domain that could benefit from courses 

---

### Action Plan

#### GQ-15 — Alex Chen

**Query:** _What are the top 3 most impactful things I can do this semester to improve my job prospects?_

**Rationale:** Tests synthesis into concrete action items — courses + skill targets grounded in evidence.

**Expected:** Must produce exactly 3 items; each item must map to real evidence (course codes or specific job gaps).

| Field | Value |
|---|---|
| Intent | `broad` (jobs=6, courses=6) |
| Planner reason | None |
| Relevance | 10/10 |
| Support | 8/10 |
| Utility | 10/10 |
| **Total** | 🟢 **9.2/10** |
| Time | 50.8s |

**Critique flags:**
- ⚠️ unsupported skill mentions: these topics

**Critique summary:** unsupported skill mentions: these topics

**Response:**

> You should focus on improving your skills in AWS and Infrastructure as Code, which are significant gaps mentioned in the Site Reliability Engineer job posting. You could take advantage of CSC 847: Cloud and Distributed Computing: Concepts and Applications to learn these topics comprehensively. Additionally, reviewing and practicing Terraform would help bridge another gap.

---

#### GQ-16 — Sam Patel

**Query:** _If I can only take one more course, which one gives me the best shot at getting hired?_

**Rationale:** Tests forced single-best-choice recommendation with full justification.

**Expected:** Must name one specific course code and explain concretely why that course beats the alternatives.

| Field | Value |
|---|---|
| Intent | `courses` (jobs=0, courses=6) |
| Planner reason | None |
| Relevance | 6/10 |
| Support | 10/10 |
| Utility | 8/10 |
| **Total** | 🟢 **8.1/10** |
| Time | 34.2s |

**Critique summary:** fallback critique

**Response:**

> Considering your current skills and completed courses, CSC 306: An Interdisciplinary Approach to Computer Programming would give you a strong foundation in programming and problem-solving. As it teaches Python, procedural programming, and scientific computing, this course addresses the gap for "Procedural Programming" and introduces relevant problem-solving approaches.

---

### Domain Pivot

#### GQ-17 — Alex Chen

**Query:** _I want to pivot into data science. What's the gap between where I am and data science jobs?_

**Rationale:** Tests gap analysis for a domain pivot — Alex's current profile vs data science requirements.

**Expected:** Must identify specific data science skills (ML, SQL, stats, etc.) missing from Alex's profile.

| Field | Value |
|---|---|
| Intent | `skill_gap` (jobs=3, courses=4) |
| Planner reason | None |
| Relevance | 6/10 |
| Support | 10/10 |
| Utility | 7/10 |
| **Total** | 🟡 **7.85/10** |
| Time | 44.7s |

**Critique summary:** fallback critique

**Response:**

> You have a solid foundation in programming languages like Python, Java, and experience with data structures and algorithms. However, several gaps need to be addressed to align with typical data scientist job requirements. The key gaps include SQL, PowerBI/Tableau, Data Visualization, Statistical Analysis, Data Cleaning, Feature Engineering, and HIPAA Compliance.

---

#### GQ-18 — Maria Gomez

**Query:** _I'm thinking of moving into systems or embedded software. Is my background relevant at all?_

**Rationale:** Tests cross-domain relevance check — ML background vs systems engineering requirements.

**Expected:** Must assess Maria's actual skills against systems requirements; should not fabricate overlap.

| Field | Value |
|---|---|
| Intent | `jobs` (jobs=6, courses=2) |
| Planner reason | None |
| Relevance | 7/10 |
| Support | 8/10 |
| Utility | 5/10 |
| **Total** | 🟡 **6.9/10** |
| Time | 49.5s |

**Critique flags:**
- ⚠️ unsupported course titles: c or c++

**Critique summary:** fallback critique

**Response:**

> You have a strong foundation in computer science with experience in machine learning, Python, databases, and operating systems. While your current skills might not be directly applicable to systems or embedded software, they can still provide a solid base for exploration. Your experience with Python could help you adapt to languages like C or C++, which are commonly used in embedded systems development.

---

### Self-Assessment

#### GQ-19 — Alex Chen

**Query:** _What are my strongest marketable skills and which job category do they point toward?_

**Rationale:** Tests skill-to-job-category mapping for the student's actual skills.

**Expected:** Must reference Alex's real skills (Python, Java, DS, Algorithms); must point to specific job categories from evidence.

| Field | Value |
|---|---|
| Intent | `skill_gap` (jobs=3, courses=4) |
| Planner reason | None |
| Relevance | 9/10 |
| Support | 8/10 |
| Utility | 10/10 |
| **Total** | 🟢 **8.85/10** |
| Time | 50.9s |

**Critique summary:** The response mentions Python but does not explicitly cite any course codes or skill names beyond what is in the evidence context. While it connects Data Structures to generative AI, which might be an oversight if no specific source is given, all other points are supported by evidence.

**Response:**

> Based on the provided job postings, your strongest marketable skills are Python, Data Structures, Algorithms, and Object-Oriented Programming. These skills are present in both job postings and can be directly related to the roles of AI Engineer at Doosan Corp and Senior Backend Engineer (AdTech) ID52365 at AgileEngine.
> 
> Both jobs require strong programming skills, with a focus on developing and deploying sophisticated software systems. Your proficiency in Python, Data Structures, Algorithms, and Object-Oriented Programming demonstrates your ability to design, develop, and maintain complex software applications, which is highly valued in both roles.

---

#### GQ-20 — Maria Gomez

**Query:** _Given everything I've learned, what kind of engineer am I becoming and what should I double down on?_

**Rationale:** Tests identity/trajectory synthesis from profile data — Maria's ML-heavy background.

**Expected:** Should identify Maria's ML/data trajectory explicitly, recommend courses or job directions that deepen it.

| Field | Value |
|---|---|
| Intent | `broad` (jobs=6, courses=6) |
| Planner reason | None |
| Relevance | 10/10 |
| Support | 8/10 |
| Utility | 9/10 |
| **Total** | 🟢 **8.95/10** |
| Time | 54.4s |

**Critique summary:** Focus on React, Node.js, WebSockets; data engineering; full stack development; UI/UX design. Use courses like CSC 867, 667, and 317 to strengthen your profile for AI positions.

**Response:**

> Based on the job posting for Full Stack AI Engineer (Front-End Learning) at Inception Point AI, it appears that you are becoming a Full Stack Developer with expertise in machine learning. You have already covered some key skills like Python, but there are significant gaps in your skillset.
> 
> To double down on, I recommend focusing on the following areas:
> 
> React, Node.js, and WebSockets: These skills appear to be critical for the job posting and are currently unaddressed in your skillset.
> Data Engineering and Full Stack Development: The job posting mentions "Data Engineering" as a required skill, indicating that you need more depth in this area. Additionally, being proficient in full stack development will help you integrate machine learning with front-end development.
> UI/UX Design: Although not directly listed as a gap, UI/UX design is mentioned as part of the role, suggesting that you should consider developing your skills in this area to complement your machine learning expertise.
> 
> By

---

### Strong Fit

#### GQ-21 — Jordan Kim

**Query:** _What full stack or web engineering roles am I competitive for right now?_

**Rationale:** Jordan has 15 web-relevant skills — tests whether the system recognizes a strong fit and shrinks the gap list accordingly.

**Expected:** Should show high skill coverage (≥50%), short gap list, and name specific web/full-stack roles.

| Field | Value |
|---|---|
| Intent | `jobs` (jobs=6, courses=2) |
| Planner reason | None |
| Relevance | 9/10 |
| Support | 5/10 |
| Utility | 10/10 |
| **Total** | 🟡 **7.65/10** |
| Time | 48.6s |

**Critique flags:**
- ⚠️ unsupported job titles: customer portal
- ⚠️ course recommendation lacks gap support for CSC 307

**Critique summary:** The AI career advisor

**Response:**

> Based on the job posting of Software Engineer - Customer Portal at Applied Intuition, you appear to be competitive for this role due to your proficiency in Python, TypeScript, React, and PostgreSQL. However, considering the top combined gaps mentioned in the job posting, it seems that full stack development skills are a notable gap. 
> 
> You may want to explore courses that address web infrastructure, software architecture, and system design as these seem to be areas where you have some gaps. CSC 307 and CSC 317 cover more general topics but do not directly address the specific skills required for this role.

---

#### GQ-22 — Marcus Webb

**Query:** _Am I ready for a cloud or DevOps engineering role?_

**Rationale:** Marcus has 14 cloud/DevOps skills — tests whether the system correctly identifies near-readiness and gives a precise, short gap list.

**Expected:** Should show high coverage for cloud roles, list specific remaining gaps (e.g. Azure, GCP), not generic advice.

| Field | Value |
|---|---|
| Intent | `broad` (jobs=6, courses=6) |
| Planner reason | None |
| Relevance | 10/10 |
| Support | 8/10 |
| Utility | 10/10 |
| **Total** | 🟢 **9.2/10** |
| Time | 51.1s |

**Critique summary:** The response is good in relevance, utility, and support but lacks direct evidence for Azure expertise beyond Docker and Kubernetes,

**Response:**

> Based on the provided job posting and your current skills, you have some gaps in Azure expertise, DevSecOps knowledge, Virtualization understanding, Network Security awareness, Identity and Access Management skill, Root Cause Analysis expertise, Cloud Scaling experience, Hybrid Cloud Infrastructure knowledge, Monitoring Tools application, and Compliance Auditing practices. While you're proficient in many relevant areas like Terraform, Ansible, Kubernetes, Docker, and CI/CD, the gaps suggest that further education and hands-on experience are necessary to be a competitive candidate for these roles.

---

#### GQ-23 — Taylor Reyes

**Query:** _Which ML or AI research engineering positions am I closest to qualifying for?_

**Rationale:** Taylor has 16 ML/AI skills — tests whether the system identifies near-qualified ML roles and produces a tight gap list.

**Expected:** Should name ML/AI specific roles, show strong coverage, list only a few remaining gaps.

| Field | Value |
|---|---|
| Intent | `jobs` (jobs=6, courses=2) |
| Planner reason | None |
| Relevance | 8/10 |
| Support | 6/10 |
| Utility | 7/10 |
| **Total** | 🟡 **6.95/10** |
| Time | 53.6s |

**Critique summary:** The AI career advisor's response focuses on Taylor's strengths and gaps, suggesting she should take additional courses in R, Java, etc. However, the evidence context doesn't provide these course codes or skill names from job postings.

**Response:**

> Based on your skills, you are closest to qualifying for Research and Development Computer Vision Engineer at Penn State University, considering your experience in Computer Vision (covered) and Machine Learning (covered). Additionally, you have a strong foundation in Python, which is also required by the job. Your gap in Geospatial data might be addressed with further study or project work, but it does not appear to be directly related to this specific job posting.

---

### Cross-Disciplinary

#### GQ-24 — Priya Sharma

**Query:** _Given my biology and CS background, what unique job opportunities exist for me?_

**Rationale:** Priya is a CS/Biology double major — tests whether the system surfaces bioinformatics/biotech roles and treats her interdisciplinary background as an advantage.

**Expected:** Should reference bioinformatics or biotech-adjacent roles; must not treat her as a generic CS student.

| Field | Value |
|---|---|
| Intent | `jobs` (jobs=6, courses=2) |
| Planner reason | None |
| Relevance | 9/10 |
| Support | 8/10 |
| Utility | 7/10 |
| **Total** | 🟢 **8.1/10** |
| Time | 40.6s |

**Critique flags:**
- ⚠️ unsupported job titles: computational biologist. this
- ⚠️ citation source 'csp1982' not found in evidence

**Critique summary:** The AI career advisor provides a comprehensive response that clearly connects both the student's background and skills to specific job opportunities. The advice is actionable and offers clear connections between course codes and job requirements.

**Response:**

> With your background in both Biology and Computer Science, you may be interested in jobs that combine these fields. A unique opportunity is a Data Analyst in the Pharmaceutical or Biotechnology industry. You can leverage your Statistical Modeling and Data Analysis skills to analyze data related to drug development and disease research.
> 
> Another potential opportunity is as a Computational Biologist. This role involves applying computational techniques, such as machine learning and bioinformatics, to analyze biological systems and develop new insights into disease mechanisms. Your Genomics, Bioinformatics, and Python skills can be valuable in this field.

---

#### GQ-25 — Priya Sharma

**Query:** _Which courses would strengthen my data science skills specifically for biomedical research?_

**Rationale:** Tests domain-specific course recommendations for a niche interdisciplinary student.

**Expected:** Should recommend courses relevant to biomedical data (CSC 509, 511, 621, 657 etc.); must cite course codes.

| Field | Value |
|---|---|
| Intent | `courses` (jobs=0, courses=6) |
| Planner reason | None |
| Relevance | 8/10 |
| Support | 9/10 |
| Utility | 7/10 |
| **Total** | 🟢 **8.15/10** |
| Time | 46.1s |

**Critique summary:** No mention of course sources for data visualization.

**Response:**

> Based on the provided course catalog, CSC 408: Machine Learning and Data Science for Personalized Medicine and CSC 869: Data Mining could be relevant to strengthening your data science skills specifically for biomedical research.
> 
> CSC 408 directly addresses gaps in bioinformatics concepts, genomic data analysis, machine learning, and statistical analysis, which are essential for biomedical research. 
> 
> CSC 869 covers key mining algorithms, dimensionality reduction, feature engineering, and data visualization, all of which are critical skills for analyzing large datasets in biomedical research.
> 
> Additionally, CSC 311: Data Structures for Data Science Application Development and CSC 408 have a strong connection to each other; CSC 408 builds upon the foundation laid by CSC 311.

---

### Skill Gap with Job Context

#### GQ-26 — Jordan Kim

**Query:** _What skills am I missing to land a senior software engineer role?_

**Rationale:** Targets the new skill_gap intent which must retrieve ≥3 jobs alongside courses — tests the invariant that gap analysis is grounded in job evidence, not just general learning advice.

**Expected:** Must reference specific retrieved job roles, list Jordan's actual gaps (e.g. system design, cloud), and recommend courses by code.

| Field | Value |
|---|---|
| Intent | `skill_gap` (jobs=3, courses=4) |
| Planner reason | None |
| Relevance | 10/10 |
| Support | 8/10 |
| Utility | 10/10 |
| **Total** | 🟢 **9.2/10** |
| Time | 38.5s |

**Critique flags:**
- ⚠️ course recommendation overclaims support for CSC 412: django

**Critique summary:** course recommendation overclaims support for CSC 412: django

**Response:**

> Based on the job posting for New Grad Software Engineer at Color, you are missing Django, AWS, LLMs, and Code Review. 
> 
> Consider taking CSC 412: Advanced Software Lab or CSC 215: Intermediate Computer Programming to address some of these gaps, as they cover code review. However, no retrieved course directly addresses all the gaps; you may need to look beyond this course catalog.

---

#### GQ-27 — Marcus Webb

**Query:** _I want to move into ML engineering — what's the gap between my DevOps background and those roles?_

**Rationale:** Cross-domain gap test: Marcus has cloud/DevOps skills; asking about ML engineering should retrieve ML-specific job evidence and identify missing ML skills.

**Expected:** Must identify ML-specific gaps from retrieved job evidence (PyTorch, TF, model training, etc.); should not conflate DevOps overlap with ML readiness.

| Field | Value |
|---|---|
| Intent | `skill_gap` (jobs=3, courses=4) |
| Planner reason | None |
| Relevance | 7/10 |
| Support | 8/10 |
| Utility | 6/10 |
| **Total** | 🟡 **7.15/10** |
| Time | 56.3s |

**Critique summary:** The response does not explicitly name specific skill gaps (e.g., Cloud infrastructure or automation) that are directly applicable to students transitioning into ML Engineering roles based on their existing DevOps background,

**Response:**

> Your experience in DevOps provides a strong foundation for transitioning into ML Engineering. The main gaps are: Cloud infrastructure, System reliability, Containerization, Cybersecurity, Compliance, Azure, GCP, EKS, Automation, Telemetry. You have experience with Infrastructure as Code and Observability, which is relevant to some aspects of ML Engineering.

---

#### GQ-28 — Taylor Reyes

**Query:** _What skills do I still need to qualify for production ML engineering at a top tech company?_

**Rationale:** Taylor has deep research ML skills — tests whether the system identifies the research-to-production gap (MLOps, deployment, distributed training, system design).

**Expected:** Must surface production/MLOps gaps (e.g. Kubernetes, MLflow, distributed training) grounded in job evidence; should not suggest research courses Taylor already has.

| Field | Value |
|---|---|
| Intent | `skill_gap` (jobs=6, courses=4) |
| Planner reason | None |
| Relevance | 8/10 |
| Support | 9/10 |
| Utility | 8/10 |
| **Total** | 🟢 **8.4/10** |
| Time | 39.3s |

**Critique flags:**
- ⚠️ citation source 'csc 610' not found in evidence

**Critique summary:** The advisor should specify course references for unsupported skills like 'Data Engineering' to avoid vague claims.

**Response:**

> You still need to address the gaps: GCP, Vertex AI, BigQuery, CI/CD, REST API Design, Data Engineering, Model Deployment, Applied Statistics, and Linux.

---

### Retrieval Precision

#### GQ-29 — Alex Chen

**Query:** _What Python-specific courses do I still need?_

**Rationale:** Narrow query — should retrieve Python-teaching courses specifically, not generic CS courses. Tests whether the course query is tightly scoped to user intent.

**Expected:** Must recommend only courses that teach Python or Python-adjacent skills; must cite course codes; should not recommend unrelated courses.

| Field | Value |
|---|---|
| Intent | `courses` (jobs=0, courses=6) |
| Planner reason | None |
| Relevance | 9/10 |
| Support | 6/10 |
| Utility | 8/10 |
| **Total** | 🟡 **7.55/10** |
| Time | 36.7s |

**Critique flags:**
- ⚠️ unsupported course titles: ide and tooling

**Critique summary:** The response only cites course codes but doesn’t provide evidence for skills not covered in completed courses, making it unsupported.

**Response:**

> Based on your current skills and completed courses, it appears that you have a solid foundation in Python programming. However, CSC 310: Computer Programming Lab covers additional topics such as IDE and Tooling, Debugging, Virtual Environments, Version Control, Unit Testing, Scientific Python Stack, Code Style, Shell Scripting Basics, Problem Solving, and Lab Documentation.
> 
> As for other Python-specific courses, there is no direct evidence of any other courses covering specific gaps in your skills.

---

#### GQ-30 — Sam Patel

**Query:** _Are there any jobs that only require Java?_

**Rationale:** Tests whether the system can identify a narrow requirement filter — jobs whose coverage is achievable with just Java skills. Tests precision over recall.

**Expected:** Should name specific roles where Java alone (or with basic skills Sam has) meets a majority of requirements; must ground in retrieved job evidence.

| Field | Value |
|---|---|
| Intent | `jobs` (jobs=6, courses=2) |
| Planner reason | None |
| Relevance | 8/10 |
| Support | 4/10 |
| Utility | 5/10 |
| **Total** | 🔴 **5.65/10** |
| Time | 47.8s |

**Critique flags:**
- ⚠️ unsupported job titles: full stack engineer, machine learning engineer
- ⚠️ unsupported course titles: python and scala
- ⚠️ citation source 'top 2 retrieved job postings' not found in evidence

**Critique summary:** The response inaccurately generalizes by stating that no job requires only Java, even though other skills are covered, indicating lack of specificity. Utility is weak as it doesn't pinpoint specific skill gaps related to Java.

**Response:**

> There are no retrieved job postings that only require Java, but a Full Stack Engineer role at Guidehouse does not explicitly mention that it's the only required skill, although Java is listed as covered. However, it lists many other skills that are required.
> 
> A 2026 University Graduate - Machine Learning Engineer role at Adobe requires Java, but covers most of its requirements in other areas such as Python and Scala.

---

## Key Findings

### Top Performers (score ≥ 8)
- **GQ-15** (Action Plan, Alex Chen): 9.2/10 — _What are the top 3 most impactful things I can do this semester to improve my jo_
- **GQ-22** (Strong Fit, Marcus Webb): 9.2/10 — _Am I ready for a cloud or DevOps engineering role?_
- **GQ-26** (Skill Gap with Job Context, Jordan Kim): 9.2/10 — _What skills am I missing to land a senior software engineer role?_
- **GQ-07** (Course Recommendation, Alex Chen): 8.95/10 — _Which courses should I take to become competitive for web development jobs?_
- **GQ-20** (Self-Assessment, Maria Gomez): 8.95/10 — _Given everything I've learned, what kind of engineer am I becoming and what shou_
- **GQ-19** (Self-Assessment, Alex Chen): 8.85/10 — _What are my strongest marketable skills and which job category do they point tow_
- **GQ-09** (Course Recommendation, Maria Gomez): 8.8/10 — _I've already taken CSC 415 and CSC 510. What advanced courses build on those for_
- **GQ-14** (Job Comparison, Maria Gomez): 8.8/10 — _Which pays off more for my career — taking more ML courses or pivoting to cloud/_
- **GQ-06** (Skill Gap Analysis, Sam Patel): 8.7/10 — _What is the single most important skill I should learn next to become more emplo_
- **GQ-04** (Skill Gap Analysis, Alex Chen): 8.55/10 — _What specific skills am I missing to qualify for a full stack engineering role?_
- **GQ-28** (Skill Gap with Job Context, Taylor Reyes): 8.4/10 — _What skills do I still need to qualify for production ML engineering at a top te_
- **GQ-08** (Course Recommendation, Sam Patel): 8.2/10 — _What's the most valuable course I can take next semester to open up more job opt_
- **GQ-25** (Cross-Disciplinary, Priya Sharma): 8.15/10 — _Which courses would strengthen my data science skills specifically for biomedica_
- **GQ-16** (Action Plan, Sam Patel): 8.1/10 — _If I can only take one more course, which one gives me the best shot at getting _
- **GQ-24** (Cross-Disciplinary, Priya Sharma): 8.1/10 — _Given my biology and CS background, what unique job opportunities exist for me?_

### Needs Work (score < 6)
- **GQ-12** (Career Readiness, Sam Patel): 4.7/10 — _Be honest — am I competitive for any real industry jobs right now?_
- **GQ-30** (Retrieval Precision, Sam Patel): 5.65/10 — _Are there any jobs that only require Java?_
- **GQ-01** (Specific Job Fit, Alex Chen): 5.95/10 — _Am I a good fit for the Junior Software Engineer role at Leidos?_

### Recurring Critique Flags
- `unsupported job titles` — appeared 7×
- `unsupported course titles` — appeared 5×
- `unsupported skill mentions` — appeared 3×
- `company references do not align with retrieved jobs` — appeared 1×
- `citation source 'course code' not found in evidence` — appeared 1×
- `unsupported course codes` — appeared 1×
- `response suggests non-retrieved learning resources` — appeared 1×
- `course recommendation lacks gap support for CSC 307` — appeared 1×
- `citation source 'csp1982' not found in evidence` — appeared 1×
- `course recommendation overclaims support for CSC 412` — appeared 1×
- `citation source 'csc 610' not found in evidence` — appeared 1×
- `citation source 'top 2 retrieved job postings' not found in evidence` — appeared 1×

### Slow Queries (> 40s)
- **GQ-01**: 45.0s — Am I a good fit for the Junior Software Engineer role at Leidos?
- **GQ-02**: 54.5s — Which ML engineering jobs match my profile and what's missing?
- **GQ-05**: 41.7s — I'm strong in ML and deep learning. What gaps are blocking me from clo
- **GQ-10**: 41.6s — I'm graduating in 6 months. Give me an honest assessment of my job mar
- **GQ-11**: 89.8s — Create a semester-by-semester plan to make me competitive for senior M
- **GQ-12**: 47.8s — Be honest — am I competitive for any real industry jobs right now?
- **GQ-14**: 50.7s — Which pays off more for my career — taking more ML courses or pivoting
- **GQ-15**: 50.8s — What are the top 3 most impactful things I can do this semester to imp
- **GQ-17**: 44.7s — I want to pivot into data science. What's the gap between where I am a
- **GQ-18**: 49.5s — I'm thinking of moving into systems or embedded software. Is my backgr
- **GQ-19**: 50.9s — What are my strongest marketable skills and which job category do they
- **GQ-20**: 54.4s — Given everything I've learned, what kind of engineer am I becoming and
- **GQ-21**: 48.6s — What full stack or web engineering roles am I competitive for right no
- **GQ-22**: 51.1s — Am I ready for a cloud or DevOps engineering role?
- **GQ-23**: 53.6s — Which ML or AI research engineering positions am I closest to qualifyi
- **GQ-24**: 40.6s — Given my biology and CS background, what unique job opportunities exis
- **GQ-25**: 46.1s — Which courses would strengthen my data science skills specifically for
- **GQ-27**: 56.3s — I want to move into ML engineering — what's the gap between my DevOps 
- **GQ-30**: 47.8s — Are there any jobs that only require Java?
