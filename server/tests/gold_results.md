# Gold Question Evaluation Report

**Run date:** 2026-05-11 20:00
**Total questions:** 30
**System:** LangGraph advisor · Ollama (llama3.2) · Qdrant + Supabase

## Summary

| Metric | Value |
|---|---|
| Passed | 30/30 |
| Errors | 0 |
| Average score | 7.98/10 |
| Average time | 48.6s |
| Score legend | 🟢 ≥8 · 🟡 ≥6 · 🔴 <6 |

## Scores At a Glance

| ID | Category | Student | Intent | Rel | Sup | Util | **Total** | Time |
|---|---|---|---|---|---|---|---|---|
| GQ-01 | Specific Job Fit | Alex Chen | `jobs` | 9 | 7 | 8 | 🟡 **7.95** | 38.4s |
| GQ-02 | Specific Job Fit | Maria Gomez | `skill_gap` | 9 | 8 | 9 | 🟢 **8.6** | 46.4s |
| GQ-03 | Specific Job Fit | Sam Patel | `jobs` | 8 | 8 | 8 | 🟢 **8.0** | 46.9s |
| GQ-04 | Skill Gap Analysis | Alex Chen | `skill_gap` | 8 | 10 | 8 | 🟢 **8.8** | 35.9s |
| GQ-05 | Skill Gap Analysis | Maria Gomez | `skill_gap` | 8 | 6 | 8 | 🟡 **7.2** | 60.9s |
| GQ-06 | Skill Gap Analysis | Sam Patel | `skill_gap` | 10 | 6 | 10 | 🟢 **8.4** | 38.9s |
| GQ-07 | Course Recommendation | Alex Chen | `courses` | 9 | 8 | 9 | 🟢 **8.6** | 44.6s |
| GQ-08 | Course Recommendation | Sam Patel | `courses` | 6 | 10 | 8 | 🟢 **8.1** | 43.6s |
| GQ-09 | Course Recommendation | Maria Gomez | `courses` | 10 | 8 | 9 | 🟢 **8.95** | 38.7s |
| GQ-10 | Career Readiness | Alex Chen | `broad` | 8 | 6 | 8 | 🟡 **7.2** | 55.4s |
| GQ-11 | Career Readiness | Maria Gomez | `broad` | 6 | 10 | 7 | 🟡 **7.85** | 61.8s |
| GQ-12 | Career Readiness | Sam Patel | `broad` | 7 | 4 | 8 | 🟡 **6.05** | 75.0s |
| GQ-13 | Job Comparison | Alex Chen | `jobs` | 6 | 8 | 7 | 🟡 **7.05** | 22.0s |
| GQ-14 | Job Comparison | Maria Gomez | `jobs` | 8 | 10 | 8 | 🟢 **8.8** | 61.0s |
| GQ-15 | Action Plan | Alex Chen | `skill_gap` | 8 | 7 | 6 | 🟡 **7.1** | 59.3s |
| GQ-16 | Action Plan | Sam Patel | `courses` | 10 | 8 | 9 | 🟢 **8.95** | 45.4s |
| GQ-17 | Domain Pivot | Alex Chen | `skill_gap` | 10 | 4 | 8 | 🟡 **7.1** | 66.5s |
| GQ-18 | Domain Pivot | Maria Gomez | `jobs` | 7 | 8 | 7 | 🟡 **7.4** | 42.8s |
| GQ-19 | Self-Assessment | Alex Chen | `skill_gap` | 4 | 8 | 7 | 🟡 **6.35** | 31.7s |
| GQ-20 | Self-Assessment | Maria Gomez | `broad` | 7 | 8 | 8 | 🟡 **7.65** | 59.1s |
| GQ-21 | Strong Fit | Jordan Kim | `jobs` | 8 | 6 | 8 | 🟡 **7.2** | 42.4s |
| GQ-22 | Strong Fit | Marcus Webb | `skill_gap` | 7 | 6 | 8 | 🟡 **6.85** | 52.1s |
| GQ-23 | Strong Fit | Taylor Reyes | `jobs` | 6 | 10 | 7 | 🟡 **7.85** | 41.1s |
| GQ-24 | Cross-Disciplinary | Priya Sharma | `jobs` | 10 | 6 | 10 | 🟢 **8.4** | 38.8s |
| GQ-25 | Cross-Disciplinary | Priya Sharma | `courses` | 10 | 10 | 10 | 🟢 **10.0** | 47.7s |
| GQ-26 | Skill Gap with Job Context | Jordan Kim | `skill_gap` | 8 | 6 | 9 | 🟡 **7.45** | 54.1s |
| GQ-27 | Skill Gap with Job Context | Marcus Webb | `skill_gap` | 10 | 10 | 10 | 🟢 **10.0** | 53.0s |
| GQ-28 | Skill Gap with Job Context | Taylor Reyes | `skill_gap` | 10 | 9 | 10 | 🟢 **9.6** | 63.8s |
| GQ-29 | Retrieval Precision | Alex Chen | `courses` | 8 | 8 | 8 | 🟢 **8.0** | 44.2s |
| GQ-30 | Retrieval Precision | Sam Patel | `jobs` | 8 | 8 | 8 | 🟢 **8.0** | 45.2s |

---

## Question-by-Question Results

### Specific Job Fit

#### GQ-01 — Alex Chen

**Query:** _Am I a good fit for the Junior Software Engineer role at Leidos?_

**Rationale:** Tests whether the system retrieves a specific named job and computes Alex's exact gap for it.

**Expected:** Must reference Leidos by name, list Alex's covered and gap skills specifically.

| Field | Value |
|---|---|
| Intent | `jobs` (jobs=6, courses=2) |
| Planner reason | None |
| Relevance | 9/10 |
| Support | 7/10 |
| Utility | 8/10 |
| **Total** | 🟡 **7.95/10** |
| Time | 38.4s |

**Critique flags:**
- ⚠️ citation source "no course or skill from leidos's job postings aligns with these gaps in the evidence context." not found in evidence

**Critique summary:** The AI advisor focused on relevance, support, and utility without addressing the weakest axis. The student is a good fit but lacks specific skills like Computer Vision, Deep Learning, etc., which are highlighted in the response.

**Response:**

> Based on the retrieved evidence, Applied Computer Vision Engineer (TS/SCI) at Vantor is the clearest fit in this view. You already cover: Python. Your main gaps are: Computer Vision, Deep Learning, Geospatial Intelligence, Data Engineering, Docker, Kubernetes, Linux, YOLO, Image Processing, Generative AI, Cloud Computing, Technical Writing, Data Science, Remote Sensing. No retrieved courses clearly address these gaps for Applied Computer Vision Engineer (TS/SCI): Computer Vision, Deep Learning, Geospatial Intelligence, Data Engineering, Docker, Kubernetes, Linux, YOLO, Image Processing, Generative AI, Cloud Computing, Technical Writing, Data Science, Remote Sensing. I cannot make a supported course recommendation for those gaps from the retrieved courses, so the reliable next step is to target those skill areas directly and retrieve a broader matching course set.

---

#### GQ-02 — Maria Gomez

**Query:** _Which ML engineering jobs match my profile and what's missing?_

**Rationale:** Maria has ML/DL skills — tests whether the system retrieves ML-relevant roles and accurately identifies remaining gaps.

**Expected:** Should surface ML-relevant roles, use Maria's actual skill set, list specific gaps.

| Field | Value |
|---|---|
| Intent | `skill_gap` (jobs=3, courses=4) |
| Planner reason | None |
| Relevance | 9/10 |
| Support | 8/10 |
| Utility | 9/10 |
| **Total** | 🟢 **8.6/10** |
| Time | 46.4s |

**Critique flags:**
- ⚠️ unsupported job titles: applied ai engineer, based on the
- ⚠️ citation source 'csc 306 course description' not found in evidence
- ⚠️ citation source 'csc 803 course description' not found in evidence

**Critique summary:** The response addresses the student's profile by identifying skill gaps and provides actionable recommendations. While it covers necessary gaps (e.g., debugging, generative AI), it also introduces additional skills that might be beyond the initial requirement.

**Response:**

> Based on the job postings you provided, the Applied AI Engineer role at Scale AI is a good match for your profile. However, it appears that there are several gaps in your skills.
> 
> The Applied AI Engineer job posting requires expertise in Cloud Technology, Data-Driven Approach, Software Engineering, Generative AI, Technical Solutions, Cybersecurity, Collaboration, Debugging, Multimodal Functionality, Tool-Calling, Business Requirements, AI Applications, Model Performance, and Research. 
> 
> You are already proficient in Machine Learning and Python, but the other required skills are not covered by your current profile.
> 
> To address these gaps, I recommend taking the following courses:
> 
> 1. CSC 306: An Interdisciplinary Approach to Computer Programming - This course addresses the gap for Debugging.
> 2. CSC 803: Generative AI: Fundamentals and Applications - This course addresses the gap for Generative AI expertise.
> While it covers some of the necessary gaps, it also introduces additional topics

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
| Support | 8/10 |
| Utility | 8/10 |
| **Total** | 🟢 **8.0/10** |
| Time | 46.9s |

**Critique flags:**
- ⚠️ unsupported course titles: go

**Critique summary:** fallback critique

**Response:**

> Based on the provided information, it appears that you're looking for entry-level positions that don't require advanced technical skills like Go, JavaScript, or Kubernetes.
> 
> Considering your completed courses and current skills, I'd recommend exploring roles in fields where Python is a common language. Here are two relevant courses that could help bridge gaps and prepare you for entry-level positions:
> 
> 1. CSC 310: Computer Programming Lab
> 	* Addresses gap: Debugging
> 	* This course covers debugging techniques, which will be helpful in identifying and resolving issues in your future roles.
> 2. CSC 306: An Interdisciplinary Approach to Computer Programming (not directly addressing gaps, but a good starting point)
> 	* Teaches: Python, Procedural Programming, Control Flow, File I/O, Problem Solving
> 	* While this course doesn't cover all the gaps, it will help you build your foundation in programming with Python and problem-solving skills, which can be applied to various entry-level positions.

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
| Utility | 8/10 |
| **Total** | 🟢 **8.8/10** |
| Time | 35.9s |

**Critique summary:** fallback critique

**Response:**

> To qualify for a full-stack engineering role, you are currently lacking:
> 
> 1. TypeScript
> 2. React
> 3. Angular
> 4. HTML/CSS
> 5. PostgreSQL
> 6. Operating Systems
> 7. Technical Communication (this course can help bridge the gap, but it's not directly applicable to this specific list of gaps)
> 
> Note that CSC 694 addresses a broader skill set, including Technical Communication, which is relevant to some of the gaps listed above. However, for full-stack engineering specifically, the other six skills are more critical.

---

#### GQ-05 — Maria Gomez

**Query:** _I'm strong in ML and deep learning. What gaps are blocking me from cloud engineering roles?_

**Rationale:** Tests cross-domain gap detection — Maria's ML profile vs cloud requirements.

**Expected:** Should identify cloud-specific gaps (GCP, AWS, Terraform, etc.) not covered by Maria's ML background.

| Field | Value |
|---|---|
| Intent | `skill_gap` (jobs=3, courses=4) |
| Planner reason | None |
| Relevance | 8/10 |
| Support | 6/10 |
| Utility | 8/10 |
| **Total** | 🟡 **7.2/10** |
| Time | 60.9s |

**Critique flags:**
- ⚠️ unsupported course codes: CSC 800
- ⚠️ course recommendation lacks gap support for CSC 220

**Critique summary:** fallback critique

**Response:**

> Based on the relevant job posting and courses you've completed, it appears that Cloud Technology is a significant gap for you to address in order to pursue Cloud Engineering roles.
> 
> While you have a solid foundation in Machine Learning (CSC 220, CSC 415, CSC 510, CSC 667) and Deep Learning (CSC 415, CSC 510, CSC 667), the job posting highlights Cloud Technology as a required skill for this role. 
> 
> Considering your current skills and completed courses, I recommend adding:
> 
> - CSC 603: Generative AI: Fundamentals and Applications
>   This course covers Generative AI, which is not directly relevant to cloud engineering. However, it might help you understand some of the concepts that could be applicable in other fields like data science or applications development, but not particularly cloud.
> 
> As for gaps related to Cloud Technology specifically, I couldn't find any courses that cover it from your list of completed courses, and there isn't a course called "CSC 800: Cloud Computing" in the pro

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
| Support | 6/10 |
| Utility | 10/10 |
| **Total** | 🟢 **8.4/10** |
| Time | 38.9s |

**Critique flags:**
- ⚠️ unsupported job titles: based on the
- ⚠️ unsupported skill mentions: next is
- ⚠️ citation source 'student_profile: product engineer 1 - customization and framework at esri (required: python, java, javascript, rust, testing, agile/scrum, technical communication; gaps: python, javascript, rust, testing, agile/scrum, technical communication)' not found in evidence
- ⚠️ citation source 'evidence context used: csu 1348250097575 - csu 671: deep learning. teaching: python, pytorch, deep neural networks, convolutional neural networks, rnns, transformer architecture...' not found in evidence

**Critique summary:** unsupported job titles: based on the; unsupported skill mentions: next is

**Response:**

> Based on the job postings, the single most important skill you should learn next is **Python**.
> 
> Two of the top job postings (Product Engineer and AI Engineer) specifically require Python as a core skill. Additionally, two relevant courses (CSC 411: Intermediate Machine Learning for Interdisciplinary Data Scientists and CSC 671: Deep Learning) teach Python as a fundamental skill.
> 
> Learning Python will help you bridge the gaps in your current skills and make yourself more competitive for these roles.

---

### Course Recommendation

#### GQ-07 — Alex Chen

**Query:** _Which courses should I take to become competitive for web development jobs?_

**Rationale:** Tests course retrieval for a specific domain — web dev — with course code citation.

**Expected:** Must cite actual course codes (e.g. CSC 307, CSC 317) and explain which gap each addresses.

| Field | Value |
|---|---|
| Intent | `courses` (jobs=6, courses=2) |
| Planner reason | None |
| Relevance | 9/10 |
| Support | 8/10 |
| Utility | 9/10 |
| **Total** | 🟢 **8.6/10** |
| Time | 44.6s |

**Critique flags:**
- ⚠️ unsupported job titles: based on the
- ⚠️ citation source 'csc 317: introduction to web software development' not found in evidence

**Critique summary:** The AI correctly identified the missing skills in the evidence context while addressing the relevance of the claim. However, it should have more precisely connected the skill gap to the specific evidence context from the job postings.

**Response:**

> Based on the job posting you provided, it appears that JavaScript is required, but only partially covered by CSC 317.
> 
> To address this gap and gain more expertise in web development, I recommend taking CSC 412: Advanced Software Lab. It covers JavaScript/Node.js Basics, which will help fill in your skills gap.
> 
> Additionally, while not explicitly stated as a requirement, gaining experience with REST API Development, Web Technologies, and Database Integration would be beneficial for any web development role. These topics are covered in CSC 412, so taking this course would address these gaps and provide you with more well-rounded knowledge in the field.
> 
> Note that while CSC 317 covers JavaScript, it's only a partial match to the requirements listed in the job posting. Taking CSC 412 will help fill in your skills gap and make you more competitive for web development jobs.

---

#### GQ-08 — Sam Patel

**Query:** _What's the most valuable course I can take next semester to open up more job options?_

**Rationale:** Tests highest-impact course recommendation for a beginner student.

**Expected:** Must name a specific course code and explain which job gaps it closes.

| Field | Value |
|---|---|
| Intent | `courses` (jobs=0, courses=6) |
| Planner reason | None |
| Relevance | 6/10 |
| Support | 10/10 |
| Utility | 8/10 |
| **Total** | 🟢 **8.1/10** |
| Time | 43.6s |

**Critique summary:** fallback critique

**Response:**

> Based on your current skills and completed courses, CSC 694: Cooperative Education: Computer Science appears to be a highly relevant course that addresses multiple gaps in your profile.
> 
> This course covers Industry Development, Project Management, Technical Communication, Agile Practices, Team Collaboration and Code Review, Problem Solving in Business Context, Career Development, Industry Tools, Technical Report Writing, Self-Direction and Initiative, Quality Assurance in Industry, and Time Management. These skills are highly valued by employers across various industries.
> 
> By taking this course, you can gain practical experience working in an industry position, develop essential soft skills, and expand your professional network. This course also addresses the gap between theoretical knowledge and real-world applications.
> 
> While CSC 310: Computer Programming Lab focuses on Python programming and lab work, it does not cover business context or industry development, which are addressed in

---

#### GQ-09 — Maria Gomez

**Query:** _I've already taken CSC 415 and CSC 510. What advanced courses build on those for AI roles?_

**Rationale:** Tests awareness of completed courses and progression recommendations.

**Expected:** Should not recommend CSC 415/510 again; should suggest genuinely next-level courses for AI.

| Field | Value |
|---|---|
| Intent | `courses` (jobs=0, courses=6) |
| Planner reason | None |
| Relevance | 10/10 |
| Support | 8/10 |
| Utility | 9/10 |
| **Total** | 🟢 **8.95/10** |
| Time | 38.7s |

**Critique summary:** The critique should note that while the AI advisor effectively highlights how CSC 865 builds on CSC 415 and 510, additional evidence of practical application would reinforce utility. However, all claims are supported by specific course sources.

**Response:**

> Since you've already completed CSC 415 (Operating System Principles) and CSC 510 (Analysis of Algorithms I), I recommend the following advanced course that builds upon these foundations:
> 
> CSC 865: Artificial Intelligence
> 
> This course covers fundamental concepts in artificial intelligence, including machine learning fundamentals, neural networks, and AI search algorithms. It provides hands-on experience with programming exercises and assignments to gain a deeper understanding of these concepts.
> 
> By taking CSC 865 after CSC 510, you'll be well-prepared for roles involving advanced AI techniques, as it builds upon the algorithm design principles learned in Analysis of Algorithms I.

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
| Relevance | 8/10 |
| Support | 6/10 |
| Utility | 8/10 |
| **Total** | 🟡 **7.2/10** |
| Time | 55.4s |

**Critique flags:**
- ⚠️ unsupported course titles: python
- ⚠️ course recommendation lacks gap support for CSC 101

**Critique summary:** fallback critique

**Response:**

> Based on the information provided, I can give you an honest assessment of your job market readiness.
> 
> You've completed four relevant courses in Computer Science: CSC 101, CSC 220, CSC 315, and CSC 340. However, none of these courses cover the specific gaps mentioned in the job postings that you're interested in. For example, the Senior Site Reliability Engineer role at iManage requires Automation, Kubernetes, Azure, AKS, Terraform, Chef, Docker, Prometheus, Grafana, ELK/EFK, CI/CD, and Go, but your course list doesn't include any courses on these topics.
> 
> Additionally, you've taken a Cloud and Distributed Computing course (CSC 847), which addresses one of the gaps mentioned in the job postings. However, it's not sufficient to fill all the gaps.
> 
> You also have some relevant skills, such as Python, Java, Data Structures, Algorithms, Object-Oriented Programming, but they're not specifically tailored to the required technologies and tools mentioned in the job postings.
> 
> Overall, I would sa

---

#### GQ-11 — Maria Gomez

**Query:** _Create a semester-by-semester plan to make me competitive for senior ML roles._

**Rationale:** Tests multi-step planning grounded in available courses and job requirements.

**Expected:** Must use real course codes, real job titles from evidence; should not invent steps or skills.

| Field | Value |
|---|---|
| Intent | `broad` (jobs=6, courses=6) |
| Planner reason | None |
| Relevance | 6/10 |
| Support | 10/10 |
| Utility | 7/10 |
| **Total** | 🟡 **7.85/10** |
| Time | 61.8s |

**Critique summary:** fallback critique

**Response:**

> Based on the retrieved evidence, New Grad Software Engineer at Color is the clearest fit in this view. You already cover: Python, SQL. Your main gaps are: React, Django, AWS, LLMs, Code Review. No retrieved courses clearly address these gaps for New Grad Software Engineer: React, Django, AWS, LLMs, Code Review. I cannot make a supported course recommendation for those gaps from the retrieved courses, so the reliable next step is to target those skill areas directly and retrieve a broader matching course set.

---

#### GQ-12 — Sam Patel

**Query:** _Be honest — am I competitive for any real industry jobs right now?_

**Rationale:** Tests candid honest assessment for a weak profile without being discouraging.

**Expected:** Should not invent optimism — must reflect Sam's limited skill set accurately while pointing to a path forward.

| Field | Value |
|---|---|
| Intent | `broad` (jobs=6, courses=6) |
| Planner reason | None |
| Relevance | 7/10 |
| Support | 4/10 |
| Utility | 8/10 |
| **Total** | 🟡 **6.05/10** |
| Time | 75.0s |

**Critique flags:**
- ⚠️ unsupported job titles: senior software engineer
- ⚠️ unsupported course titles: backend engineering, csc
- ⚠️ unsupported skill mentions: particularly concerning

**Critique summary:** fallback critique

**Response:**

> Based on the provided information, it's challenging to make a definitive assessment of your competitiveness for industry jobs. However, there are several gaps in your skills that suggest you may need additional training or experience.
> 
> Your current skill set includes Java and Programming Fundamentals, which is a good foundation for many computer science roles. However, none of the top 2 retrieved job postings (Senior Software Engineer at Voltai and Sr. Embedded Systems Engineer at Trane Technologies) require or mention Java as a required skill. This could indicate that your skills are not directly aligned with the most in-demand technologies in these industries.
> 
> Additionally, you have significant gaps in areas such as:
> 
> 1. Backend Engineering
> 2. Full-stack Development
> 3. Infrastructure
> 4. DevOps
> 5. Agent Development
> 6. Retrieval-Augmented Generation
> 7. Systems Design
> 8. Debugging
> 9. Docker
> 10. AWS
> 11. Azure
> 12. GCP
> 13. IaC
> 14. On-prem Deployment
> 15. Field Engineering
> 16. Solutions Eng

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
| Time | 22.0s |

**Critique flags:**
- ⚠️ unsupported job titles: university grad

**Critique summary:** fallback critique

**Response:**

> Based on the retrieved evidence, Software Engineer, University Grad at Glean is the clearest fit in this view. You already cover: Python, Java, Data Structures, Algorithms. Your main gaps are: JavaScript, Natural Language Processing, Distributed Systems. No retrieved courses clearly address these gaps for Software Engineer, University Grad: JavaScript, Natural Language Processing, Distributed Systems. I cannot make a supported course recommendation for those gaps from the retrieved courses, so the reliable next step is to target those skill areas directly and retrieve a broader matching course set.

---

#### GQ-14 — Maria Gomez

**Query:** _Which pays off more for my career — taking more ML courses or pivoting to cloud/DevOps?_

**Rationale:** Tests strategic advice grounded in job evidence — system must compare both paths using retrieved data.

**Expected:** Must use retrieved job and course evidence; must not speculate beyond the evidence.

| Field | Value |
|---|---|
| Intent | `jobs` (jobs=6, courses=2) |
| Planner reason | None |
| Relevance | 8/10 |
| Support | 10/10 |
| Utility | 8/10 |
| **Total** | 🟢 **8.8/10** |
| Time | 61.0s |

**Critique summary:** fallback critique

**Response:**

> Based on the provided job posting, it appears that both options are relevant to the role of AI Engineer at HAVI. However, the gaps in your current skills suggest a potential need for training in certain areas.
> 
> Given the skills you already possess (Machine Learning and Deep Learning), taking more ML courses might not directly address the gap in Artificial Intelligence, which is also listed as a required skill for this job. Therefore, while ML courses can help enhance your existing capabilities, it's uncertain whether they would directly contribute to filling the broader AI-related gaps.
> 
> On the other hand, pivoting towards cloud/DevOps skills seems more likely to address some of the gaps in your current skills set, particularly Azure Databricks, Apache Spark, Scala, and DevOps. Since both CSC 874 and CSC 878 cover aspects of Big Data Platforms and Systems, which is closely related to cloud and DevOps, taking one or both of these courses could help bridge this gap.
> 
> Considering the prov

---

### Action Plan

#### GQ-15 — Alex Chen

**Query:** _What are the top 3 most impactful things I can do this semester to improve my job prospects?_

**Rationale:** Tests synthesis into concrete action items — courses + skill targets grounded in evidence.

**Expected:** Must produce exactly 3 items; each item must map to real evidence (course codes or specific job gaps).

| Field | Value |
|---|---|
| Intent | `skill_gap` (jobs=3, courses=6) |
| Planner reason | None |
| Relevance | 8/10 |
| Support | 7/10 |
| Utility | 6/10 |
| **Total** | 🟡 **7.1/10** |
| Time | 59.3s |

**Critique flags:**
- ⚠️ unsupported course titles: csc, react.js
- ⚠️ citation source "equifax's job posting on site reliability engineering" not found in evidence
- ⚠️ citation source 'the course description mentions aws, gcp, etc.' not found in evidence
- ⚠️ citation source "alex chen's resume shows these skills" not found in evidence

**Critique summary:** The AI response identifies three courses that address relevant skills and provide actionable steps, but it could better tie in the courses to specific industry needs or job roles. For example, while CSC 317 covers JavaScript and Node.js, it might not directly address cloud infrastructure gaps, which are critical for reliability engineering roles.

**Response:**

> Based on the retrieved course and job postings, here are the top 3 most impactful things you can do this semester to improve your job prospects:
> 
> 1. **Take CSC 847: Cloud and Distributed Computing: Concepts and Applications**.
> 
> This course addresses a significant gap in your skill set, specifically in Kubernetes and Infrastructure as Code. By taking this course, you will gain hands-on experience with cloud computing concepts, containerization, and infrastructure management, which are highly sought after skills in the industry. This course will not only help you fill the gap but also provide valuable knowledge that can enhance your chances of landing a Site Reliability Engineer role at Equifax or other similar positions.
> 
> 2. **Take CSC 317: Introduction to Web Software Development** or **CSC 667/867: Internet Application Design and Development** (choose one).
> 
> Both of these courses cover JavaScript, Node.js, and related skills that are essential for web development. By taking one of the

---

#### GQ-16 — Sam Patel

**Query:** _If I can only take one more course, which one gives me the best shot at getting hired?_

**Rationale:** Tests forced single-best-choice recommendation with full justification.

**Expected:** Must name one specific course code and explain concretely why that course beats the alternatives.

| Field | Value |
|---|---|
| Intent | `courses` (jobs=0, courses=6) |
| Planner reason | None |
| Relevance | 10/10 |
| Support | 8/10 |
| Utility | 9/10 |
| **Total** | 🟢 **8.95/10** |
| Time | 45.4s |

**Critique flags:**
- ⚠️ unsupported course titles: project management
- ⚠️ citation source "csc 694's source excerpt mentions project management in a business context." not found in evidence

**Critique summary:** The AI advisor provides excellent relevance by emphasizing industry-specific skills, but offers support by noting that foundational Python skills from CSC 310 and project management experience from CSC 694 are more directly applicable. Utility is good as both courses offer valuable skills, with the focus on project management being key for job prospects.

**Response:**

> Based on your current skills and completed courses, I would recommend taking CSC 694: Cooperative Education: Computer Science.
> 
> This course covers various industry-specific topics such as Project Management, Technical Communication, Agile Practices, Team Collaboration, and Problem Solving in Business Context. These skills are highly valued by employers, especially in the field of computer science.
> 
> Additionally, this course provides hands-on experience with projects in a business, government, or industrial position, which can give you an edge when it comes to getting hired.
> 
> While CSC 310: Computer Programming Lab is also relevant, it focuses more on Python programming and software development tools. While these skills are essential for a computer science career, they might not be as directly applicable to the job market as the industry-specific topics covered in CSC 694.
> 
> CSC 686: Experiences in Computer Science Teaching is unlikely to have an immediate impact on your job prospects, a

---

### Domain Pivot

#### GQ-17 — Alex Chen

**Query:** _I want to pivot into data science. What's the gap between where I am and data science jobs?_

**Rationale:** Tests gap analysis for a domain pivot — Alex's current profile vs data science requirements.

**Expected:** Must identify specific data science skills (ML, SQL, stats, etc.) missing from Alex's profile.

| Field | Value |
|---|---|
| Intent | `skill_gap` (jobs=6, courses=4) |
| Planner reason | None |
| Relevance | 10/10 |
| Support | 4/10 |
| Utility | 8/10 |
| **Total** | 🟡 **7.1/10** |
| Time | 66.5s |

**Critique flags:**
- ⚠️ unsupported course titles: apache spark, aws or azure
- ⚠️ unsupported skill mentions: 1, about big, about data
- ⚠️ course recommendation lacks gap support for CSC 101

**Critique summary:** There's no mention of specific evidence for cloud platforms or big data technologies in the AI advisor's response. They address SQL and statistical analysis but lack courses on cloud platforms, ETL/ELT tools, and big data technologies like Apache Spark or Hadoop,

**Response:**

> You're currently proficient in Python, Data Structures, Algorithms, Object-Oriented Programming, and have completed courses CSC 101, CSC 220, CSC 315, and CSC 340.
> 
> To bridge the gap to data science jobs, you'll need to address the following skills:
> 
> 1. **SQL**: You don't have proficiency in SQL, which is a fundamental skill for data scientists.
> 2. **Data Visualization**: You're missing data visualization skills, which are essential for communicating insights effectively.
> 3. **Statistical Analysis**: While you have Data Structures and Algorithms, you lack statistical analysis expertise.
> 4. **Machine Learning**: As a future data scientist, it's crucial to have basic machine learning knowledge.
> 5. **Cloud Platforms**: Data science often involves working with cloud-based tools; you don't have exposure to cloud platforms like AWS or Azure.
> 6. **Data Engineering**: Data scientists need to understand data engineering concepts, such as ETL/ELT, data modeling, and data warehousing.
> 7. **Big Da

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
| Utility | 7/10 |
| **Total** | 🟡 **7.4/10** |
| Time | 42.8s |

**Critique flags:**
- ⚠️ unsupported job titles: embedded systems engineer

**Critique summary:** fallback critique

**Response:**

> Based on the retrieved evidence, Associate Staff - Embedded Systems Engineer at MIT Lincoln Laboratory is the clearest fit in this view. You already cover: Python, Operating Systems. Your main gaps are: MATLAB, Linux, Cybersecurity. No retrieved courses clearly address these gaps for Associate Staff - Embedded Systems Engineer: MATLAB, Linux, Cybersecurity. I cannot make a supported course recommendation for those gaps from the retrieved courses, so the reliable next step is to target those skill areas directly and retrieve a broader matching course set.

---

### Self-Assessment

#### GQ-19 — Alex Chen

**Query:** _What are my strongest marketable skills and which job category do they point toward?_

**Rationale:** Tests skill-to-job-category mapping for the student's actual skills.

**Expected:** Must reference Alex's real skills (Python, Java, DS, Algorithms); must point to specific job categories from evidence.

| Field | Value |
|---|---|
| Intent | `skill_gap` (jobs=6, courses=0) |
| Planner reason | None |
| Relevance | 4/10 |
| Support | 8/10 |
| Utility | 7/10 |
| **Total** | 🟡 **6.35/10** |
| Time | 31.7s |

**Critique flags:**
- ⚠️ unsupported job titles: id52365

**Critique summary:** fallback critique

**Response:**

> Based on the retrieved evidence, Senior Backend Engineer (AdTech) ID52365 at AgileEngine is the clearest fit in this view. You already cover: Python, Java. Your main gaps are: Django, Kubernetes, PostgreSQL, AWS, AdTech, Distributed Systems, API Design, OpenRTB, Data Pipelines, System Architecture, .NET, Node.js, Google Ad Manager, Prebid. No retrieved courses clearly address these gaps for Senior Backend Engineer (AdTech) ID52365: Django, Kubernetes, PostgreSQL, AWS, AdTech, Distributed Systems, API Design, OpenRTB, Data Pipelines, System Architecture, .NET, Node.js, Google Ad Manager, Prebid. I cannot make a supported course recommendation for those gaps from the retrieved courses, so the reliable next step is to target those skill areas directly and retrieve a broader matching course set.

---

#### GQ-20 — Maria Gomez

**Query:** _Given everything I've learned, what kind of engineer am I becoming and what should I double down on?_

**Rationale:** Tests identity/trajectory synthesis from profile data — Maria's ML-heavy background.

**Expected:** Should identify Maria's ML/data trajectory explicitly, recommend courses or job directions that deepen it.

| Field | Value |
|---|---|
| Intent | `broad` (jobs=6, courses=6) |
| Planner reason | None |
| Relevance | 7/10 |
| Support | 8/10 |
| Utility | 8/10 |
| **Total** | 🟡 **7.65/10** |
| Time | 59.1s |

**Critique flags:**
- ⚠️ unsupported course titles: csc, react and node.js. additionally

**Critique summary:** fallback critique

**Response:**

> Based on the information provided, it appears that you are becoming a Full Stack developer with a focus on Front-End development, particularly in the context of AI and Machine Learning applications. This is evident from the job postings where React, Node.js, Python, and other related technologies are required.
> 
> However, there are some gaps in your skillset:
> 
> * Java: You don't have sufficient experience in Java, which is a critical language for many Full Stack roles.
> * TypeScript: Although you're familiar with JavaScript, you don't have specific experience with TypeScript, which is widely used in modern web development.
> * React Native: This is another technology you don't cover, and it's essential for mobile app development.
> * Prisma: While you have a solid grasp of SQL and Python, Prisma is a popular ORM solution that can help you work more efficiently with databases.
> 
> Considering your interests and strengths, I would recommend doubleing down on Full Stack Development, focusing on Fron

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
| Relevance | 8/10 |
| Support | 6/10 |
| Utility | 8/10 |
| **Total** | 🟡 **7.2/10** |
| Time | 42.4s |

**Critique flags:**
- ⚠️ unsupported job titles: based on the, for the front-end software engineer
- ⚠️ unsupported course titles: angular and ember, javascript

**Critique summary:** fallback critique

**Response:**

> Based on the job postings you provided and your current skills, here are some full stack or web engineering roles where you may be competitive:
> 
> 1. **Full Stack Engineer at Fidelity Investments**: This role is a good fit since it covers many of your skills, such as JavaScript, HTML5, Git, REST, SQL, and Tomcat.
> 2. **Front-End Software Engineer at IXL Product**: Although this role requires additional skills like Angular and Ember, you already have experience with React and JavaScript, which are essential for this position.
> 3. **Full Stack AI Engineer (Front-End Learning) at Inception Point AI**: As a full stack engineer in this role, you will need to develop UI/UX design skills, but your proficiency in React, Node.js, Python is a good foundation.
> 
> To become more competitive for these roles, consider addressing the gaps mentioned in the job postings:
> 
> * For the Full Stack Engineer at Fidelity Investments, focus on learning Java, Spring Boot, and Oracle.
> * For the Front-End Software Engin

---

#### GQ-22 — Marcus Webb

**Query:** _Am I ready for a cloud or DevOps engineering role?_

**Rationale:** Marcus has 14 cloud/DevOps skills — tests whether the system correctly identifies near-readiness and gives a precise, short gap list.

**Expected:** Should show high coverage for cloud roles, list specific remaining gaps (e.g. Azure, GCP), not generic advice.

| Field | Value |
|---|---|
| Intent | `skill_gap` (jobs=6, courses=4) |
| Planner reason | None |
| Relevance | 7/10 |
| Support | 6/10 |
| Utility | 8/10 |
| **Total** | 🟡 **6.85/10** |
| Time | 52.1s |

**Critique flags:**
- ⚠️ unsupported job titles: from the cloud engineer, leidos
- ⚠️ unsupported skill mentions: azure experience, azure expertise

**Critique summary:** fallback critique

**Response:**

> Based on your current skills and completed courses, you appear to have a solid foundation in cloud and DevOps concepts. However, a more thorough analysis of the job postings reveals some gaps that might impact your readiness for these roles.
> 
> From the Cloud Engineer at Leidos posting, you're missing Azure expertise, DevSecOps knowledge, virtualization experience, network security understanding, identity and access management skills, root cause analysis expertise, cloud scaling capabilities, hybrid cloud infrastructure familiarity, monitoring tools proficiency, and compliance auditing knowledge. Addressing these gaps would be essential to fill.
> 
> The Site Reliability Engineer at Qlik posting also presents some challenges. You're missing Azure experience, Prometheus expertise, Open Telemetry knowledge, Helm proficiency, MongoDB understanding, microservices awareness, networking security skills, and observability expertise. Some of these gaps may overlap with those from the Leidos role, bu

---

#### GQ-23 — Taylor Reyes

**Query:** _Which ML or AI research engineering positions am I closest to qualifying for?_

**Rationale:** Taylor has 16 ML/AI skills — tests whether the system identifies near-qualified ML roles and produces a tight gap list.

**Expected:** Should name ML/AI specific roles, show strong coverage, list only a few remaining gaps.

| Field | Value |
|---|---|
| Intent | `jobs` (jobs=6, courses=2) |
| Planner reason | None |
| Relevance | 6/10 |
| Support | 10/10 |
| Utility | 7/10 |
| **Total** | 🟡 **7.85/10** |
| Time | 41.1s |

**Critique summary:** fallback critique

**Response:**

> Based on the retrieved evidence, Research and Development Computer Vision Engineer at Penn State University is the clearest fit in this view. You already cover: Computer Vision, Python, Machine Learning, Data analysis. Your main gaps are: R, Java, C++, MATLAB, Object detection, Tracking, Recognition, Scene understanding, Geospatial data, High performance computing, Algorithm development. No retrieved courses clearly address these gaps for Research and Development Computer Vision Engineer: R, Java, C++, MATLAB, Object detection, Tracking, Recognition, Scene understanding, Geospatial data, High performance computing, Algorithm development. I cannot make a supported course recommendation for those gaps from the retrieved courses, so the reliable next step is to target those skill areas directly and retrieve a broader matching course set.

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
| Relevance | 10/10 |
| Support | 6/10 |
| Utility | 10/10 |
| **Total** | 🟢 **8.4/10** |
| Time | 38.8s |

**Critique flags:**
- ⚠️ unsupported course titles: csc
- ⚠️ course recommendation lacks gap support for CSC 657
- ⚠️ citation source 'the course description mentions a broad range of computational biology topics, including protein modeling and gene expression analysis.' not found in evidence
- ⚠️ citation source 'the course includes phylogenetic analysis and research literature review, which are relevant to job postings.' not found in evidence

**Critique summary:** unsupported course titles: csc; course recommendation lacks gap support for CSC 657

**Response:**

> Based on your background in Computer Science and Biology, you have a strong foundation in both fields. However, the job postings provided highlight some gaps that need to be addressed.
> 
> You can consider taking courses like CSC 857: Bioinformatics Computing or CSC 657: Bioinformatics Computing to fill these gaps. These courses will help you develop a broad range of topics in computational biology as practiced in the life science industry and leading research organizations.
> 
> CSC 857 may provide additional coverage on topics such as:
> 
> * Protein Modeling
> * Gene Expression Analysis
> 
> CSC 657 covers similar topics but also includes:
> * Phylogenetic Analysis
> * Research Literature Review

---

#### GQ-25 — Priya Sharma

**Query:** _Which courses would strengthen my data science skills specifically for biomedical research?_

**Rationale:** Tests domain-specific course recommendations for a niche interdisciplinary student.

**Expected:** Should recommend courses relevant to biomedical data (CSC 509, 511, 621, 657 etc.); must cite course codes.

| Field | Value |
|---|---|
| Intent | `courses` (jobs=0, courses=6) |
| Planner reason | None |
| Relevance | 10/10 |
| Support | 10/10 |
| Utility | 10/10 |
| **Total** | 🟢 **10.0/10** |
| Time | 47.7s |

**Critique flags:**
- ⚠️ citation source 'student profile, relevant courses (top 4 retrieved)' not found in evidence
- ⚠️ citation source 'relevant courses (top 4 retrieved)' not found in evidence
- ⚠️ citation source 'relevant courses (top 4 retrieved)' not found in evidence

**Critique summary:** citation source 'student profile, relevant courses (top 4 retrieved)' not found in evidence; citation source 'relevant courses (top 4 retrieved)' not found in evidence

**Response:**

> Based on the provided course information, I recommend taking CSC 408: Machine Learning and Data Science for Personalized Medicine.
> 
> This course teaches you about machine learning, genomic data analysis, bioinformatics concepts, and statistical analysis using Python, which are essential skills for working in biomedical research. Additionally, it provides domain knowledge in healthcare and covers topics such as model evaluation, research literature review, scientific writing, and data visualization, all of which are relevant to biomedical research.
> 
> By taking this course, you will gain a solid foundation in machine learning and data science concepts applied to genomic datasets, making you more competitive for roles in biomedical research.

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
| Relevance | 8/10 |
| Support | 6/10 |
| Utility | 9/10 |
| **Total** | 🟡 **7.45/10** |
| Time | 54.1s |

**Critique flags:**
- ⚠️ unsupported job titles: university grad
- ⚠️ unsupported skill mentions: 1 django this is required in the new grad software engineer role at color 2 aws this is required in the new grad software engineer role at color 3 llms, the following
- ⚠️ citation source 'evidence context: job description mentions django as required.' not found in evidence
- ⚠️ citation source 'evidence context: job description mentions aws as required.' not found in evidence
- ⚠️ citation source 'evidence context: job description mentions llms as required.' not found in evidence

**Critique summary:** The AI addressed most of the skill gaps identified by the student but missed specifying that Code Review should be at an intermediate level rather than advanced. The AI appropriately connected all relevant evidence, which is a strong point.

**Response:**

> Based on the relevant job postings, it appears that you are missing the following skills:
> 
> 1. Django - This is required in the New Grad Software Engineer role at Color.
> 2. AWS - This is required in the New Grad Software Engineer role at Color.
> 3. LLMs (Large Language Models) - This is required in the New Grad Software Engineer role at Color.
> 4. Code Review - You have completed CSC 215 and CSC 412, but it seems like a more advanced level of code review is needed for senior software engineer roles.
> 5. Java - This is required in the University Grad role at Glean.
> 
> It's also worth noting that having experience with Natural Language Processing (NLP) could be beneficial for certain types of roles or companies, as mentioned in the CSC 620 course description.

---

#### GQ-27 — Marcus Webb

**Query:** _I want to move into ML engineering — what's the gap between my DevOps background and those roles?_

**Rationale:** Cross-domain gap test: Marcus has cloud/DevOps skills; asking about ML engineering should retrieve ML-specific job evidence and identify missing ML skills.

**Expected:** Must identify ML-specific gaps from retrieved job evidence (PyTorch, TF, model training, etc.); should not conflate DevOps overlap with ML readiness.

| Field | Value |
|---|---|
| Intent | `skill_gap` (jobs=6, courses=4) |
| Planner reason | None |
| Relevance | 10/10 |
| Support | 10/10 |
| Utility | 10/10 |
| **Total** | 🟢 **10.0/10** |
| Time | 53.0s |

**Critique summary:** The AI advisor has effectively addressed Marcus by identifying gaps in his skills and providing actionable recommendations for course selection and skill development. The response is highly relevant, supported by credible evidence, and provides clear utility through specific actionable steps.

**Response:**

> Based on the retrieved evidence, Senior DevOps Engineer I at Spring Health is the clearest fit in this view. You already cover: AWS, Infrastructure as Code, Kubernetes, Observability. Your main gaps are: DevOps, Azure, GCP, EKS, Automation, Telemetry, Cloud infrastructure, System reliability, Containerization, Cybersecurity, Compliance. No retrieved courses clearly address these gaps for Senior DevOps Engineer I: DevOps, Azure, GCP, EKS, Automation, Telemetry, Cloud infrastructure, System reliability, Containerization, Cybersecurity, Compliance. I cannot make a supported course recommendation for those gaps from the retrieved courses, so the reliable next step is to target those skill areas directly and retrieve a broader matching course set.

---

#### GQ-28 — Taylor Reyes

**Query:** _What skills do I still need to qualify for production ML engineering at a top tech company?_

**Rationale:** Taylor has deep research ML skills — tests whether the system identifies the research-to-production gap (MLOps, deployment, distributed training, system design).

**Expected:** Must surface production/MLOps gaps (e.g. Kubernetes, MLflow, distributed training) grounded in job evidence; should not suggest research courses Taylor already has.

| Field | Value |
|---|---|
| Intent | `skill_gap` (jobs=3, courses=4) |
| Planner reason | None |
| Relevance | 10/10 |
| Support | 9/10 |
| Utility | 10/10 |
| **Total** | 🟢 **9.6/10** |
| Time | 63.8s |

**Critique flags:**
- ⚠️ citation source 'student profile' not found in evidence
- ⚠️ citation source 'relevant job postings' not found in evidence

**Critique summary:** The AI response addresses relevance by providing specific skills and courses that are directly relevant to ML engineering. It also accurately traces evidence, but the utility section could be stronger.

**Response:**

> Based on the retrieved evidence, Staff Machine Learning Engineer (Remote) at The Home Depot is the clearest fit in this view. You already cover: Machine Learning, Python, SQL, TensorFlow, PyTorch, NLP, Git. Your main gaps are: GCP, Vertex AI, BigQuery, CI/CD, REST API Design, Data Engineering, Model Deployment, Applied Statistics, Linux. No retrieved courses clearly address these gaps for Staff Machine Learning Engineer (Remote): GCP, Vertex AI, BigQuery, CI/CD, REST API Design, Data Engineering, Model Deployment, Applied Statistics, Linux. I cannot make a supported course recommendation for those gaps from the retrieved courses, so the reliable next step is to target those skill areas directly and retrieve a broader matching course set.

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
| Relevance | 8/10 |
| Support | 8/10 |
| Utility | 8/10 |
| **Total** | 🟢 **8.0/10** |
| Time | 44.2s |

**Critique flags:**
- ⚠️ course recommendation lacks gap support for CSC 220

**Critique summary:** fallback critique

**Response:**

> Based on the provided evidence, it appears that you have some foundation in Python programming from CSC 310 (Computer Programming Lab) and possibly other labs or activities within this course.
> 
> However, to address any gaps, here are two potential Python-specific courses:
> 
> 1. **CSC 810: Analysis of Algorithms II**: While not exclusively a Python course, this class covers algorithms that often involve Python implementation, such as approximation algorithms, online algorithms, and advanced graph algorithms.
> 
> 2. **CSC 220: Data Structures**: This course could cover additional Python-related topics such as data structures, which are fundamental in computer science and programming. Since you already completed CSC 101 and have a foundation in other areas, this might not fill the biggest gap, but still worth exploring if available.
> 
> Please note that these courses may require additional prerequisites or may be more focused on theory than practical Python implementation.

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
| Support | 8/10 |
| Utility | 8/10 |
| **Total** | 🟢 **8.0/10** |
| Time | 45.2s |

**Critique flags:**
- ⚠️ unsupported course titles: sql and

**Critique summary:** fallback critique

**Response:**

> No, there are no job postings you've retrieved that only require Java.
> 
> However, CSC 869: Data Mining covers a gap by requiring Python, which is one of the student's existing skills. This course can help address this gap and provide additional exposure to other relevant skills such as SQL and data visualization.

---

## Key Findings

### Top Performers (score ≥ 8)
- **GQ-25** (Cross-Disciplinary, Priya Sharma): 10.0/10 — _Which courses would strengthen my data science skills specifically for biomedica_
- **GQ-27** (Skill Gap with Job Context, Marcus Webb): 10.0/10 — _I want to move into ML engineering — what's the gap between my DevOps background_
- **GQ-28** (Skill Gap with Job Context, Taylor Reyes): 9.6/10 — _What skills do I still need to qualify for production ML engineering at a top te_
- **GQ-09** (Course Recommendation, Maria Gomez): 8.95/10 — _I've already taken CSC 415 and CSC 510. What advanced courses build on those for_
- **GQ-16** (Action Plan, Sam Patel): 8.95/10 — _If I can only take one more course, which one gives me the best shot at getting _
- **GQ-04** (Skill Gap Analysis, Alex Chen): 8.8/10 — _What specific skills am I missing to qualify for a full stack engineering role?_
- **GQ-14** (Job Comparison, Maria Gomez): 8.8/10 — _Which pays off more for my career — taking more ML courses or pivoting to cloud/_
- **GQ-02** (Specific Job Fit, Maria Gomez): 8.6/10 — _Which ML engineering jobs match my profile and what's missing?_
- **GQ-07** (Course Recommendation, Alex Chen): 8.6/10 — _Which courses should I take to become competitive for web development jobs?_
- **GQ-06** (Skill Gap Analysis, Sam Patel): 8.4/10 — _What is the single most important skill I should learn next to become more emplo_
- **GQ-24** (Cross-Disciplinary, Priya Sharma): 8.4/10 — _Given my biology and CS background, what unique job opportunities exist for me?_
- **GQ-08** (Course Recommendation, Sam Patel): 8.1/10 — _What's the most valuable course I can take next semester to open up more job opt_
- **GQ-03** (Specific Job Fit, Sam Patel): 8.0/10 — _I only have basic programming skills. What entry-level jobs are realistic for me_
- **GQ-29** (Retrieval Precision, Alex Chen): 8.0/10 — _What Python-specific courses do I still need?_
- **GQ-30** (Retrieval Precision, Sam Patel): 8.0/10 — _Are there any jobs that only require Java?_

### Needs Work (score < 6)
- All questions scored ≥ 6.

### Recurring Critique Flags
- `unsupported job titles` — appeared 10×
- `unsupported course titles` — appeared 10×
- `unsupported skill mentions` — appeared 5×
- `citation source 'evidence context` — appeared 3×
- `course recommendation lacks gap support for CSC 220` — appeared 2×
- `course recommendation lacks gap support for CSC 101` — appeared 2×
- `citation source 'relevant courses (top 4 retrieved)' not found in evidence` — appeared 2×
- `citation source "no course or skill from leidos's job postings aligns with these gaps in the evidence context." not found in evidence` — appeared 1×
- `citation source 'csc 306 course description' not found in evidence` — appeared 1×
- `citation source 'csc 803 course description' not found in evidence` — appeared 1×
- `unsupported course codes` — appeared 1×
- `citation source 'student_profile` — appeared 1×
- `citation source 'evidence context used` — appeared 1×
- `citation source 'csc 317` — appeared 1×
- `citation source "equifax's job posting on site reliability engineering" not found in evidence` — appeared 1×
- `citation source 'the course description mentions aws, gcp, etc.' not found in evidence` — appeared 1×
- `citation source "alex chen's resume shows these skills" not found in evidence` — appeared 1×
- `citation source "csc 694's source excerpt mentions project management in a business context." not found in evidence` — appeared 1×
- `course recommendation lacks gap support for CSC 657` — appeared 1×
- `citation source 'the course description mentions a broad range of computational biology topics, including protein modeling and gene expression analysis.' not found in evidence` — appeared 1×
- `citation source 'the course includes phylogenetic analysis and research literature review, which are relevant to job postings.' not found in evidence` — appeared 1×
- `citation source 'student profile, relevant courses (top 4 retrieved)' not found in evidence` — appeared 1×
- `citation source 'student profile' not found in evidence` — appeared 1×
- `citation source 'relevant job postings' not found in evidence` — appeared 1×

### Slow Queries (> 40s)
- **GQ-02**: 46.4s — Which ML engineering jobs match my profile and what's missing?
- **GQ-03**: 46.9s — I only have basic programming skills. What entry-level jobs are realis
- **GQ-05**: 60.9s — I'm strong in ML and deep learning. What gaps are blocking me from clo
- **GQ-07**: 44.6s — Which courses should I take to become competitive for web development 
- **GQ-08**: 43.6s — What's the most valuable course I can take next semester to open up mo
- **GQ-10**: 55.4s — I'm graduating in 6 months. Give me an honest assessment of my job mar
- **GQ-11**: 61.8s — Create a semester-by-semester plan to make me competitive for senior M
- **GQ-12**: 75.0s — Be honest — am I competitive for any real industry jobs right now?
- **GQ-14**: 61.0s — Which pays off more for my career — taking more ML courses or pivoting
- **GQ-15**: 59.3s — What are the top 3 most impactful things I can do this semester to imp
- **GQ-16**: 45.4s — If I can only take one more course, which one gives me the best shot a
- **GQ-17**: 66.5s — I want to pivot into data science. What's the gap between where I am a
- **GQ-18**: 42.8s — I'm thinking of moving into systems or embedded software. Is my backgr
- **GQ-20**: 59.1s — Given everything I've learned, what kind of engineer am I becoming and
- **GQ-21**: 42.4s — What full stack or web engineering roles am I competitive for right no
- **GQ-22**: 52.1s — Am I ready for a cloud or DevOps engineering role?
- **GQ-23**: 41.1s — Which ML or AI research engineering positions am I closest to qualifyi
- **GQ-25**: 47.7s — Which courses would strengthen my data science skills specifically for
- **GQ-26**: 54.1s — What skills am I missing to land a senior software engineer role?
- **GQ-27**: 53.0s — I want to move into ML engineering — what's the gap between my DevOps 
- **GQ-28**: 63.8s — What skills do I still need to qualify for production ML engineering a
- **GQ-29**: 44.2s — What Python-specific courses do I still need?
- **GQ-30**: 45.2s — Are there any jobs that only require Java?
