# Gold Question Evaluation Report

**Run date:** 2026-05-12 14:22
**Total questions:** 30
**System:** LangGraph advisor · Ollama (llama3.2) · Qdrant + Supabase

## Summary

| Metric | Value |
|---|---|
| Passed | 30/30 |
| Errors | 0 |
| Average score | 7.93/10 |
| Average time | 48.2s |
| Score legend | 🟢 ≥8 · 🟡 ≥6 · 🔴 <6 |

## Scores At a Glance

| ID | Category | Student | Intent | Rel | Sup | Util | **Total** | Time |
|---|---|---|---|---|---|---|---|---|
| GQ-01 | Specific Job Fit | Alex Chen | `jobs` | 7 | 10 | 7 | 🟢 **8.2** | 42.2s |
| GQ-02 | Specific Job Fit | Maria Gomez | `skill_gap` | 10 | 8 | 10 | 🟢 **9.2** | 58.3s |
| GQ-03 | Specific Job Fit | Sam Patel | `jobs` | 8 | 6 | 7 | 🟡 **6.95** | 56.3s |
| GQ-04 | Skill Gap Analysis | Alex Chen | `skill_gap` | 10 | 8 | 9 | 🟢 **8.95** | 48.0s |
| GQ-05 | Skill Gap Analysis | Maria Gomez | `skill_gap` | 10 | 6 | 10 | 🟢 **8.4** | 41.0s |
| GQ-06 | Skill Gap Analysis | Sam Patel | `skill_gap` | 8 | 9 | 5 | 🟡 **7.65** | 42.7s |
| GQ-07 | Course Recommendation | Alex Chen | `courses` | 10 | 9 | 8 | 🟢 **9.1** | 50.8s |
| GQ-08 | Course Recommendation | Sam Patel | `courses` | 10 | 10 | 10 | 🟢 **10.0** | 42.7s |
| GQ-09 | Course Recommendation | Maria Gomez | `courses` | 7 | 10 | 7 | 🟢 **8.2** | 49.4s |
| GQ-10 | Career Readiness | Alex Chen | `broad` | 6 | 8 | 8 | 🟡 **7.3** | 72.5s |
| GQ-11 | Career Readiness | Maria Gomez | `broad` | 7 | 10 | 9 | 🟢 **8.7** | 63.3s |
| GQ-12 | Career Readiness | Sam Patel | `broad` | 6 | 6 | 3 | 🔴 **5.25** | 52.9s |
| GQ-13 | Job Comparison | Alex Chen | `jobs` | 7 | 5 | 7 | 🟡 **6.2** | 52.7s |
| GQ-14 | Job Comparison | Maria Gomez | `broad` | 10 | 8 | 10 | 🟢 **9.2** | 73.0s |
| GQ-15 | Action Plan | Alex Chen | `broad` | 10 | 8 | 9 | 🟢 **8.95** | 44.2s |
| GQ-16 | Action Plan | Sam Patel | `courses` | 9 | 10 | 8 | 🟢 **9.15** | 33.1s |
| GQ-17 | Domain Pivot | Alex Chen | `skill_gap` | 8 | 9 | 7 | 🟢 **8.15** | 44.1s |
| GQ-18 | Domain Pivot | Maria Gomez | `jobs` | 9 | 7 | 4 | 🟡 **6.95** | 41.8s |
| GQ-19 | Self-Assessment | Alex Chen | `skill_gap` | 10 | 8 | 6 | 🟢 **8.2** | 56.5s |
| GQ-20 | Self-Assessment | Maria Gomez | `broad` | 9 | 9 | 7 | 🟢 **8.5** | 47.0s |
| GQ-21 | Strong Fit | Jordan Kim | `jobs` | 9 | 8 | 7 | 🟢 **8.1** | 38.5s |
| GQ-22 | Strong Fit | Marcus Webb | `broad` | 6 | 8 | 5 | 🟡 **6.55** | 54.3s |
| GQ-23 | Strong Fit | Taylor Reyes | `jobs` | 7 | 8 | 7 | 🟡 **7.4** | 41.3s |
| GQ-24 | Cross-Disciplinary | Priya Sharma | `jobs` | 7 | 8 | 6 | 🟡 **7.15** | 49.4s |
| GQ-25 | Cross-Disciplinary | Priya Sharma | `courses` | 8 | 7 | 9 | 🟡 **7.85** | 41.8s |
| GQ-26 | Skill Gap with Job Context | Jordan Kim | `skill_gap` | 10 | 8 | 7 | 🟢 **8.45** | 41.2s |
| GQ-27 | Skill Gap with Job Context | Marcus Webb | `skill_gap` | 9 | 8 | 8 | 🟢 **8.35** | 42.1s |
| GQ-28 | Skill Gap with Job Context | Taylor Reyes | `skill_gap` | 6 | 10 | 7 | 🟡 **7.85** | 43.1s |
| GQ-29 | Retrieval Precision | Alex Chen | `courses` | 8 | 7 | 5 | 🟡 **6.85** | 40.5s |
| GQ-30 | Retrieval Precision | Sam Patel | `jobs` | 4 | 8 | 6 | 🟡 **6.1** | 40.2s |

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
| Planner reason | job-fit or role recommendation question |
| Relevance | 7/10 |
| Support | 10/10 |
| Utility | 7/10 |
| **Total** | 🟢 **8.2/10** |
| Time | 42.2s |

**Critique summary:** fallback critique

**Response:**

> No retrieved job posting for "Junior Software Engineer" or similar titles were found that directly matches your profile. However, the skills and gaps you have listed appear to be relevant to software engineering roles in general. You may need to look beyond this course catalog to find a better match.

---

#### GQ-02 — Maria Gomez

**Query:** _Which ML engineering jobs match my profile and what's missing?_

**Rationale:** Maria has ML/DL skills — tests whether the system retrieves ML-relevant roles and accurately identifies remaining gaps.

**Expected:** Should surface ML-relevant roles, use Maria's actual skill set, list specific gaps.

| Field | Value |
|---|---|
| Intent | `skill_gap` (jobs=6, courses=4) |
| Planner reason | skill-gap question requires job context |
| Relevance | 10/10 |
| Support | 8/10 |
| Utility | 10/10 |
| **Total** | 🟢 **9.2/10** |
| Time | 58.3s |

**Critique flags:**
- ⚠️ unsupported job titles: enterprise genai

**Critique summary:** unsupported job titles: enterprise genai

**Response:**

> Based on your profile, the following machine learning engineering jobs seem to be a good fit:
> 
> 1. Associate Data Scientist, New College Grad - 2026 at Jobs for Humanity
>    Required: SQL, Python, Machine Learning, Generative AI, Statistical Modeling, R, Apache Spark, Scikit-learn, Tableau, Power BI, Prompt Engineering, Data Mining, Exploratory Data Analysis, Feature Engineering, NLP, LLMs
>    Student covers: SQL, Python, Machine Learning
> 
> Gaps: Generative AI, Statistical Modeling, R, Apache Spark, Scikit-learn, Tableau, Power BI, Prompt Engineering, Data Mining, Exploratory Data Analysis, Feature Engineering, NLP, LLMs
> 
> 2. Applied AI Engineer, Enterprise GenAI at Scale AI
>    Required: Machine Learning, Python, Cloud Technology, Data-Driven Approach, Software Engineering, Generative AI, Technical Solutions, Cybersecurity, Collaboration, Debugging, Multimodal Functionality, Tool-Calling, Business Requirements, AI Applications, Model Performance, Research
> 
> Gaps: Cloud Technology, Data-Drive

---

#### GQ-03 — Sam Patel

**Query:** _I only have basic programming skills. What entry-level jobs are realistic for me right now?_

**Rationale:** Sam has minimal skills — tests realistic expectation setting for an underprepared student.

**Expected:** Should not oversell Sam's readiness; should name specific achievable jobs and list actual gaps honestly.

| Field | Value |
|---|---|
| Intent | `jobs` (jobs=6, courses=2) |
| Planner reason | job-fit or role recommendation question |
| Relevance | 8/10 |
| Support | 6/10 |
| Utility | 7/10 |
| **Total** | 🟡 **6.95/10** |
| Time | 56.3s |

**Critique flags:**
- ⚠️ unsupported job titles: junior developer or an assistant programmer.

the, software engineer
- ⚠️ unsupported course titles: object-oriented programming

**Critique summary:** fallback critique

**Response:**

> With your current skills in Java, Programming Fundamentals, Computational Thinking, and Problem Solving, you may find entry-level opportunities as a Junior Developer or an Assistant Programmer.
> 
> The job posting for Software Engineer at Dictionary.com requires Java, but also other skills like Object-Oriented Programming, JavaScript, HTML/CSS, and MongoDB. While your current skills don't fully cover all the gaps, it's essential to note that you do have Problem Solving covered.
> 
> The job posting for Software Engineer II (ONSITE) at RTX has a much broader set of required skills, including C++, Angular, GraphQL, and TypeScript, which are beyond your current skillset.

---

### Skill Gap Analysis

#### GQ-04 — Alex Chen

**Query:** _What specific skills am I missing to qualify for a full stack engineering role?_

**Rationale:** Tests extraction of full-stack-specific gap skills from retrieved job evidence.

**Expected:** Must name concrete missing skills (e.g. JavaScript, React, SQL) grounded in job evidence.

| Field | Value |
|---|---|
| Intent | `skill_gap` (jobs=3, courses=4) |
| Planner reason | ... |
| Relevance | 10/10 |
| Support | 8/10 |
| Utility | 9/10 |
| **Total** | 🟢 **8.95/10** |
| Time | 48.0s |

**Critique summary:** The response is highly relevant and provides a comprehensive list of skills needed to complete a full stack engineering role, including React, Django, SQL, AWS, LLMs, and Code Review. However, it could be more actionable by linking each missing skill directly to evidence from the student's courses and profile. This would enhance clarity and provide clear directions for specific course choices.

**Response:**

> You are missing React, Django, SQL, AWS, LLMs, and Code Review as gap skills.

---

#### GQ-05 — Maria Gomez

**Query:** _I'm strong in ML and deep learning. What gaps are blocking me from cloud engineering roles?_

**Rationale:** Tests cross-domain gap detection — Maria's ML profile vs cloud requirements.

**Expected:** Should identify cloud-specific gaps (GCP, AWS, Terraform, etc.) not covered by Maria's ML background.

| Field | Value |
|---|---|
| Intent | `skill_gap` (jobs=3, courses=4) |
| Planner reason | user references a prior topic (ML/Deep Learning) and asks about specific gaps for a role (Cloud Engineering) |
| Relevance | 10/10 |
| Support | 6/10 |
| Utility | 10/10 |
| **Total** | 🟢 **8.4/10** |
| Time | 41.0s |

**Critique flags:**
- ⚠️ unsupported job titles: applied ai engineer
- ⚠️ unsupported course titles: aws or gcp

**Critique summary:** unsupported job titles: applied ai engineer; unsupported course titles: aws or gcp

**Response:**

> Based on the job posting for Applied AI Engineer at Scale AI, you cover Machine Learning and Python. The gaps that appear to be blocking you from this role include Cloud Technology, Data-Driven Approach, Software Engineering, Generative AI, Technical Solutions, Cybersecurity, Collaboration, Debugging, Multimodal Functionality, Tool-Calling, Business Requirements, AI Applications, Model Performance, Research, and possibly a strong foundation in Cloud platforms such as AWS or GCP.

---

#### GQ-06 — Sam Patel

**Query:** _What is the single most important skill I should learn next to become more employable?_

**Rationale:** Tests prioritized advice — system should pick one concrete skill with justification from evidence.

**Expected:** Must name one specific skill with supporting job evidence, not a generic list.

| Field | Value |
|---|---|
| Intent | `skill_gap` (jobs=3, courses=4) |
| Planner reason | skill_gap intent due to specific skill inquiry and lack of job context. |
| Relevance | 8/10 |
| Support | 9/10 |
| Utility | 5/10 |
| **Total** | 🟡 **7.65/10** |
| Time | 42.7s |

**Critique summary:** The AI Career Advisor underlined the importance of Python's demand but failed to provide actionable steps, particularly for specific course recommendations tied directly to the evidence context.

**Response:**

> Python is a highly sought-after skill in the industry, and it's currently addressed as a gap by both job postings you've seen. Learning Python would be a valuable investment for your future career prospects.

---

### Course Recommendation

#### GQ-07 — Alex Chen

**Query:** _Which courses should I take to become competitive for web development jobs?_

**Rationale:** Tests course retrieval for a specific domain — web dev — with course code citation.

**Expected:** Must cite actual course codes (e.g. CSC 307, CSC 317) and explain which gap each addresses.

| Field | Value |
|---|---|
| Intent | `courses` (jobs=0, courses=6) |
| Planner reason | learning or upskill question |
| Relevance | 10/10 |
| Support | 9/10 |
| Utility | 8/10 |
| **Total** | 🟢 **9.1/10** |
| Time | 50.8s |

**Critique summary:** The AI career advisor provided relevant course suggestions, but they lack specificity about which skills and courses are best for different web development roles. This makes it unclear how to prioritize certain courses over others without additional context from job requirements or industry specifics.

**Response:**

> Based on the job requirements, you may need courses that cover HTML, CSS, JavaScript, Node.js, Express.js, SQL and MySQL, Client-Server Architecture, RESTful APIs, Web Security, and Database Design. 
> 
> For example, CSC 307: An Interdisciplinary Approach to Web Programming covers topics such as HTML, PHP, Python, SQL, and MySQL database, which could be relevant to web development jobs. However, it may not be the best fit since it focuses on a broader interdisciplinary approach.
> 
> CSC 317: Introduction to Web Software Development seems more directly applicable, covering topics like JavaScript, Node.js, Express.js, and RESTful APIs.

---

#### GQ-08 — Sam Patel

**Query:** _What's the most valuable course I can take next semester to open up more job options?_

**Rationale:** Tests highest-impact course recommendation for a beginner student.

**Expected:** Must name a specific course code and explain which job gaps it closes.

| Field | Value |
|---|---|
| Intent | `courses` (jobs=0, courses=6) |
| Planner reason | learning or upskill question |
| Relevance | 10/10 |
| Support | 10/10 |
| Utility | 10/10 |
| **Total** | 🟢 **10.0/10** |
| Time | 42.7s |

**Response:**

> Considering your current skills and major, CSC 306: An Interdisciplinary Approach to Computer Programming would be a valuable addition to your skillset. It covers Python programming, procedural programming, scientific computing, and problem-solving approaches relevant to interdisciplinary problems, which could complement your existing Java expertise. Additionally, this course addresses the gap in "Procedural Programming," making it a strong candidate to enhance job prospects.

---

#### GQ-09 — Maria Gomez

**Query:** _I've already taken CSC 415 and CSC 510. What advanced courses build on those for AI roles?_

**Rationale:** Tests awareness of completed courses and progression recommendations.

**Expected:** Should not recommend CSC 415/510 again; should suggest genuinely next-level courses for AI.

| Field | Value |
|---|---|
| Intent | `courses` (jobs=0, courses=6) |
| Planner reason | learning or upskill question |
| Relevance | 7/10 |
| Support | 10/10 |
| Utility | 7/10 |
| **Total** | 🟢 **8.2/10** |
| Time | 49.4s |

**Critique summary:** fallback critique

**Response:**

> You have already completed CSC 415 (Operating System Principles) and CSC 510 (Analysis of Algorithms I). Based on the course descriptions, a relevant advanced course that builds upon your foundation would be CSC 865: Artificial Intelligence.
> 
> This course teaches fundamental concepts needed to attain human-level intelligence in computer systems, covering topics such as machine learning fundamentals, neural networks, knowledge representation, Bayesian networks, and more. This is an excellent choice for AI roles, considering its comprehensive coverage of key areas.

---

### Career Readiness

#### GQ-10 — Alex Chen

**Query:** _I'm graduating in 6 months. Give me an honest assessment of my job market readiness._

**Rationale:** Tests broad readiness analysis — should balance encouragement with honest gap identification.

**Expected:** Must be grounded in Alex's actual skills, name real jobs, not claim readiness for roles he can't fill.

| Field | Value |
|---|---|
| Intent | `broad` (jobs=6, courses=6) |
| Planner reason | broad readiness or roadmap question |
| Relevance | 6/10 |
| Support | 8/10 |
| Utility | 8/10 |
| **Total** | 🟡 **7.3/10** |
| Time | 72.5s |

**Critique flags:**
- ⚠️ unsupported course titles: distributed systems

**Critique summary:** fallback critique

**Response:**

> Based on the provided information, your current skill set covers some but not all required skills for both jobs posted. You have strengths in Python and Java, which are two of the required languages. However, you lack proficiency in JavaScript, TypeScript, Rust, Kotlin, Swift, React, Next.js, Operating Systems, and React Native.
> 
> You also have gaps in other areas such as Distributed Systems, GCP, AWS, API Design, Front-end Development, Back-end Development, Analytics Pipelines, SDK Development, Cloud Deployment, Agile Development, Technical Documentation, and Research and Technical Writing. These skills are either required or closely related to the job requirements.
> 
> Given that you're graduating soon, it's essential to prioritize courses that address these gaps. Focusing on Relevant Courses like CSC 667 (Internet Application Design and Development) which covers JavaScript, React.js, and some additional areas may help bridge some of the gaps.

---

#### GQ-11 — Maria Gomez

**Query:** _Create a semester-by-semester plan to make me competitive for senior ML roles._

**Rationale:** Tests multi-step planning grounded in available courses and job requirements.

**Expected:** Must use real course codes, real job titles from evidence; should not invent steps or skills.

| Field | Value |
|---|---|
| Intent | `broad` (jobs=6, courses=6) |
| Planner reason | broad readiness or roadmap question |
| Relevance | 7/10 |
| Support | 10/10 |
| Utility | 9/10 |
| **Total** | 🟢 **8.7/10** |
| Time | 63.3s |

**Critique summary:** The response fails to address the gap in Python proficiency for more complex ML tasks such as image processing or natural language understanding, which are identified in the job postings. Additionally, while it provides actionable steps for courses, some coding names like 'MMO' might be less common.

**Response:**

> To make you competitive for senior ML roles, I recommend the following plan:
> 
> Year 2 (Sophomore): 
> Focus on building strong fundamentals in Machine Learning by taking CSC 510: Introduction to Deep Learning and focusing on deep learning projects.
> 
> Year 3 (Junior):
> Take CSC 667: Advanced Topics in Deep Learning to expand your knowledge of deep learning techniques. Additionally, work on a capstone project involving computer vision or natural language processing tasks that require deep learning.
> 
> Year 4 (Senior):
> CSC 600 is recommended for its broad coverage of Machine Learning topics. After completing this course, focus on projects that demonstrate expertise in multiple areas of machine learning and build your professional network through attending industry events, meetups, and contributing to open-source ML projects.

---

#### GQ-12 — Sam Patel

**Query:** _Be honest — am I competitive for any real industry jobs right now?_

**Rationale:** Tests candid honest assessment for a weak profile without being discouraging.

**Expected:** Should not invent optimism — must reflect Sam's limited skill set accurately while pointing to a path forward.

| Field | Value |
|---|---|
| Intent | `broad` (jobs=6, courses=6) |
| Planner reason | broad readiness or roadmap question |
| Relevance | 6/10 |
| Support | 6/10 |
| Utility | 3/10 |
| **Total** | 🔴 **5.25/10** |
| Time | 52.9s |

**Critique flags:**
- ⚠️ unsupported job titles: senior software engineer
- ⚠️ unsupported course titles: backend engineering

**Critique summary:** The response provides a reasonable claim about skill gaps but only addresses one relevant course (CSC 215) and mentions other areas like cloud platforms. It does not cover all required skills in the evidence context, which is noted with unsupported claims. The utility is low because while specific recommendations are given, they lack completeness.

**Response:**

> Based on the provided job posting and your current skills, it appears that you are not competitive for this specific Senior Software Engineer role at Voltai. You lack experience in the required fields such as Backend Engineering, Full-stack Development, Infrastructure, DevOps, Agent Development, Systems Design, and various cloud platforms like AWS, Azure, GCP.
> 
> While you have some relevant completed courses like CSC 215 (which addresses a gap skill), your overall skills set does not align with the job requirements.

---

### Job Comparison

#### GQ-13 — Alex Chen

**Query:** _Between a software engineering role at Microsoft and one at a startup like Giga, which is a better fit for where I am now?_

**Rationale:** Tests comparative multi-job reasoning — system must assess Alex against two different role profiles.

**Expected:** Must compare both companies using evidence; should not fabricate requirements not in retrieved data.

| Field | Value |
|---|---|
| Intent | `jobs` (jobs=2, courses=0) |
| Planner reason | job-fit or role recommendation question |
| Relevance | 7/10 |
| Support | 5/10 |
| Utility | 7/10 |
| **Total** | 🟡 **6.2/10** |
| Time | 52.7s |

**Critique summary:** The advisor doesn

**Response:**

> Considering the job posting at Glean, it's clear that they're looking for recent university graduates with experience in software engineering roles. Although you've completed your CS degree, there is no direct correspondence between your completed courses and the gaps listed by the job posting.
> 
> However, CSC 620: Natural Language Technologies covers Natural Language Processing, which is one of the unfulfilled skills required by Glean's job posting. Taking this course may bridge some gap in the requirements for a more suitable fit at Microsoft or other similar companies.

---

#### GQ-14 — Maria Gomez

**Query:** _Which pays off more for my career — taking more ML courses or pivoting to cloud/DevOps?_

**Rationale:** Tests strategic advice grounded in job evidence — system must compare both paths using retrieved data.

**Expected:** Must use retrieved job and course evidence; must not speculate beyond the evidence.

| Field | Value |
|---|---|
| Intent | `broad` (jobs=6, courses=6) |
| Planner reason | broad readiness analysis |
| Relevance | 10/10 |
| Support | 8/10 |
| Utility | 10/10 |
| **Total** | 🟢 **9.2/10** |
| Time | 73.0s |

**Critique flags:**
- ⚠️ unsupported job titles: ai engineers
- ⚠️ citation source 'course descriptions focus on these areas.' not found in evidence
- ⚠️ citation source 'job postings highlight cloud-based infrastructure.' not found in evidence

**Critique summary:** unsupported job titles: ai engineers; citation source 'course descriptions focus on these areas.' not found in evidence

**Response:**

> Based on the provided job postings, it appears that AI Engineers at HAVI require strong skills in Machine Learning, Deep Learning, and Cloud technologies. The company's emphasis on supply chain management and logistics suggests a need for automation and data-driven decision-making.
> 
> While both options can be beneficial, I would recommend pivoting to cloud/DevOps as the more lucrative option in the long run. The job posting highlights Azure Data Factory, ADLS Gen2, and Terraform as required skills, indicating a strong demand for professionals with expertise in cloud-based infrastructure and development.
> 
> In contrast, while Machine Learning is essential, the HAVI job posting does not specify a particular ML framework or toolset (e.g., TensorFlow, PyTorch). This suggests that while ML skills are valuable, they may be more generalizable to other roles or industries.
> 
> Pivoting to cloud/DevOps can lead to a broader range of job opportunities and higher earning potential, as the demand for cl

---

### Action Plan

#### GQ-15 — Alex Chen

**Query:** _What are the top 3 most impactful things I can do this semester to improve my job prospects?_

**Rationale:** Tests synthesis into concrete action items — courses + skill targets grounded in evidence.

**Expected:** Must produce exactly 3 items; each item must map to real evidence (course codes or specific job gaps).

| Field | Value |
|---|---|
| Intent | `broad` (jobs=6, courses=6) |
| Planner reason | broad readiness or roadmap question |
| Relevance | 10/10 |
| Support | 8/10 |
| Utility | 9/10 |
| **Total** | 🟢 **8.95/10** |
| Time | 44.2s |

**Critique summary:** The critique is weak as it doesn't address any specific axis. The response meets all three criteria and cites evidence properly.

**Response:**

> Based on your skill gaps and relevant coursework, here are three actionable steps you can take this semester to enhance your job prospects:
> 
> 1. Take CSC 847: Cloud and Distributed Computing: Concepts and Applications to address the gaps in Kubernetes, NoSQL Databases, and Infrastructure as Code.
> 2. Enroll in CSC 317: Introduction to Web Software Development or CSC 667/867: Internet Application Design and Development to reinforce your JavaScript and Node.js skills, specifically focusing on RESTful APIs and web development fundamentals.
> 3. Pursue the Cooperative Education course (CSC 694) to develop technical communication skills, which are essential for software engineers in various industries.
> 
> By taking these steps, you'll be able to address key gaps in your skillset and make yourself a more competitive candidate for software engineer positions.

---

#### GQ-16 — Sam Patel

**Query:** _If I can only take one more course, which one gives me the best shot at getting hired?_

**Rationale:** Tests forced single-best-choice recommendation with full justification.

**Expected:** Must name one specific course code and explain concretely why that course beats the alternatives.

| Field | Value |
|---|---|
| Intent | `courses` (jobs=0, courses=6) |
| Planner reason | learning or upskill question |
| Relevance | 9/10 |
| Support | 10/10 |
| Utility | 8/10 |
| **Total** | 🟢 **9.15/10** |
| Time | 33.1s |

**Response:**

> Based on your current skills and completed courses, CSC 306: An Interdisciplinary Approach to Computer Programming addresses Python programming and problem-solving skills that are highly relevant to many job openings. This course may provide you with a competitive edge in the hiring process for positions involving data analysis, scientific computing, or software development.

---

### Domain Pivot

#### GQ-17 — Alex Chen

**Query:** _I want to pivot into data science. What's the gap between where I am and data science jobs?_

**Rationale:** Tests gap analysis for a domain pivot — Alex's current profile vs data science requirements.

**Expected:** Must identify specific data science skills (ML, SQL, stats, etc.) missing from Alex's profile.

| Field | Value |
|---|---|
| Intent | `skill_gap` (jobs=3, courses=4) |
| Planner reason | skill-gap question requires job context |
| Relevance | 8/10 |
| Support | 9/10 |
| Utility | 7/10 |
| **Total** | 🟢 **8.15/10** |
| Time | 44.1s |

**Critique summary:** The advisor cited specific skills but did not reference evidence context properly.

**Response:**

> You need skills in ETL Tools, APIs, Data Modeling, Kafka, Kinesis, AWS GovCloud, FHIR, Docker, Cloud-native Data Services, and Data Governance.

---

#### GQ-18 — Maria Gomez

**Query:** _I'm thinking of moving into systems or embedded software. Is my background relevant at all?_

**Rationale:** Tests cross-domain relevance check — ML background vs systems engineering requirements.

**Expected:** Must assess Maria's actual skills against systems requirements; should not fabricate overlap.

| Field | Value |
|---|---|
| Intent | `jobs` (jobs=6, courses=2) |
| Planner reason | job-fit or role recommendation question |
| Relevance | 9/10 |
| Support | 7/10 |
| Utility | 4/10 |
| **Total** | 🟡 **6.95/10** |
| Time | 41.8s |

**Critique summary:** The response lacks specific, actionable course references from the evidence context. It doesn't detail skill gaps or recommend courses by code, making it vague.

**Response:**

> Your background in machine learning and deep learning might not be directly applicable to the systems/embedded software field, as those areas are more focused on data-driven approaches. However, your experience with Python and Operating Systems could be transferable, especially if you've gained hands-on experience working with embedded systems or operating systems during your courses.

---

### Self-Assessment

#### GQ-19 — Alex Chen

**Query:** _What are my strongest marketable skills and which job category do they point toward?_

**Rationale:** Tests skill-to-job-category mapping for the student's actual skills.

**Expected:** Must reference Alex's real skills (Python, Java, DS, Algorithms); must point to specific job categories from evidence.

| Field | Value |
|---|---|
| Intent | `skill_gap` (jobs=3, courses=4) |
| Planner reason | role context provided |
| Relevance | 10/10 |
| Support | 8/10 |
| Utility | 6/10 |
| **Total** | 🟢 **8.2/10** |
| Time | 56.5s |

**Critique flags:**
- ⚠️ unsupported job titles: senior backend engineer
- ⚠️ citation source 'evidence_citations' not found in evidence

**Critique summary:** The career advisor did not explicitly state that all required skills from their courses are covered, leading to uncertainty about their proficiency in some areas.

**Response:**

> Your strongest marketable skills appear to be Python, Data Structures, Algorithms, and Object-Oriented Programming. These skills suggest that you have a strong foundation in programming and software development, particularly in the areas of data management and object-oriented design.
> 
> Given your current skill set, it seems that job categories in finance, data analysis, or software development could be a good fit for you. The Senior Backend Engineer role at AgileEngine, which requires skills like Python, Java, and Distributed Systems, appears to be a potential match, although there are still gaps in your coverage of other technologies and concepts.

---

#### GQ-20 — Maria Gomez

**Query:** _Given everything I've learned, what kind of engineer am I becoming and what should I double down on?_

**Rationale:** Tests identity/trajectory synthesis from profile data — Maria's ML-heavy background.

**Expected:** Should identify Maria's ML/data trajectory explicitly, recommend courses or job directions that deepen it.

| Field | Value |
|---|---|
| Intent | `broad` (jobs=6, courses=6) |
| Planner reason | broad readiness or roadmap question |
| Relevance | 9/10 |
| Support | 9/10 |
| Utility | 7/10 |
| **Total** | 🟢 **8.5/10** |
| Time | 47.0s |

**Response:**

> Based on the job posting and your completed courses, it appears that you are becoming interested in Data Engineering. You have skills in SQL and Python, but there is a gap in Java, Azure, ETL/ELT, Data Warehousing, Apache Spark, Databricks, Apache Airflow, Medallion Architecture, NoSQL, CI/CD, Terraform, Data Lakehouse, Data Governance, and Query Optimization.
> 
> You should double down on courses that address these gaps, such as CSC 878: Big Data Platforms and Systems (addresses gap in Apache Spark) or another course that covers Java. Additionally, consider taking courses that introduce you to cloud platforms like Azure, which is mentioned in the job posting.

---

### Strong Fit

#### GQ-21 — Jordan Kim

**Query:** _What full stack or web engineering roles am I competitive for right now?_

**Rationale:** Jordan has 15 web-relevant skills — tests whether the system recognizes a strong fit and shrinks the gap list accordingly.

**Expected:** Should show high skill coverage (≥50%), short gap list, and name specific web/full-stack roles.

| Field | Value |
|---|---|
| Intent | `jobs` (jobs=6, courses=2) |
| Planner reason | job-fit or role recommendation question |
| Relevance | 9/10 |
| Support | 8/10 |
| Utility | 7/10 |
| **Total** | 🟢 **8.1/10** |
| Time | 38.5s |

**Critique flags:**
- ⚠️ unsupported job titles: customer portal

**Critique summary:** The advisor missed specific skill gaps, such as the lack of knowledge in Retrieval-Augmented Generation, which should have been included.

**Response:**

> Based on the provided job postings and your current skills, you appear to be most competitive for web-related roles that leverage your expertise in React, Node.js, PostgreSQL, and HTML/CSS. You may also have opportunities in customer-facing software engineering roles where Python, TypeScript, and React are required.
> 
> Your lack of experience with Angular might make you less competitive for the Software Engineer - Customer Portal role at Applied Intuition, but you can consider other web-related job postings that don't require this specific skillset. 
> 
> You should focus on building more projects that demonstrate your proficiency in React, Node.js, PostgreSQL, and CI/CD pipelines to increase your chances of landing a full-stack or web engineering role.

---

#### GQ-22 — Marcus Webb

**Query:** _Am I ready for a cloud or DevOps engineering role?_

**Rationale:** Marcus has 14 cloud/DevOps skills — tests whether the system correctly identifies near-readiness and gives a precise, short gap list.

**Expected:** Should show high coverage for cloud roles, list specific remaining gaps (e.g. Azure, GCP), not generic advice.

| Field | Value |
|---|---|
| Intent | `broad` (jobs=6, courses=6) |
| Planner reason | broad readiness or roadmap question |
| Relevance | 6/10 |
| Support | 8/10 |
| Utility | 5/10 |
| **Total** | 🟡 **6.55/10** |
| Time | 54.3s |

**Critique summary:** The AI response accurately identifies the student's current skills but fails to specify the specific technical deficiencies in Azure-related roles, particularly Jenkins, JFrog Artifactory, SonarQube, Grafana, Container Security, semantic versioning, public Trust Clearance, Cloud Automation, and Observability. These gaps are significant for preparing for cloud or DevOps roles.

**Response:**

> Based on your current skills and completed courses, you appear to have some relevant skills for both roles. For cloud engineering, you cover Azure, Terraform, Ansible, Kubernetes, Docker, and Infrastructure as Code, which is good. However, you lack experience with Azure, DevSecOps, Windows Server, Network Administration, IAM, Bicep, ARM Templates, Root Cause Analysis, Cloud Scaling, Hybrid Cloud Infrastructure, Monitoring Tools, and Compliance Auditing.
> 
> For DevOps engineering, your skills in CI/CD, Docker, Terraform, Ansible, Kubernetes, Python, Git, and Infrastructure as Code are well-covered. Nevertheless, you have gaps in areas such as Jenkins, JFrog Artifactory, SonarQube, Grafana, Container Security, Semantic Versioning, Public Trust Clearance, Cloud Automation, and Observability.
> 
> Given your current profile, it's unclear whether you're fully prepared for either a cloud or DevOps engineering role. You may want to focus on filling the gaps mentioned above before applying for these

---

#### GQ-23 — Taylor Reyes

**Query:** _Which ML or AI research engineering positions am I closest to qualifying for?_

**Rationale:** Taylor has 16 ML/AI skills — tests whether the system identifies near-qualified ML roles and produces a tight gap list.

**Expected:** Should name ML/AI specific roles, show strong coverage, list only a few remaining gaps.

| Field | Value |
|---|---|
| Intent | `jobs` (jobs=6, courses=2) |
| Planner reason | job-fit or role recommendation question |
| Relevance | 7/10 |
| Support | 8/10 |
| Utility | 7/10 |
| **Total** | 🟡 **7.4/10** |
| Time | 41.3s |

**Critique flags:**
- ⚠️ unsupported course titles: prompt engineering and bias detection and mitigation. while csc

**Critique summary:** The advisor's critique misses citing evidence context phrases like 'student profile' or 'evidence context,' and only refers to course codes and job titles. They also didn't list specific courses with exact skill addresses.

**Response:**

> Based on your skills, you are closest to qualifying for Research Engineer positions that focus on Explainable AI and LLMs. Your completed course CSC 859 addresses the gap in Retrieval-Augmented Generation and covers relevant topics such as Prompt Engineering and Bias Detection and Mitigation. While CSC 659 also touches upon this topic, it is not directly listed under RELEVANT COURSES with the exact gap skill addressed.

---

### Cross-Disciplinary

#### GQ-24 — Priya Sharma

**Query:** _Given my biology and CS background, what unique job opportunities exist for me?_

**Rationale:** Priya is a CS/Biology double major — tests whether the system surfaces bioinformatics/biotech roles and treats her interdisciplinary background as an advantage.

**Expected:** Should reference bioinformatics or biotech-adjacent roles; must not treat her as a generic CS student.

| Field | Value |
|---|---|
| Intent | `jobs` (jobs=6, courses=2) |
| Planner reason | job-fit or role recommendation question |
| Relevance | 7/10 |
| Support | 8/10 |
| Utility | 6/10 |
| **Total** | 🟡 **7.15/10** |
| Time | 49.4s |

**Critique summary:** The response effectively addresses the relevance by highlighting how student skills can apply to various roles and provides some job titles. However, it could improve by more specifically linking each recommendation to course codes or skills, especially for those without explicit ties.

**Response:**

> With your combined biology and Computer Science background, you have a versatile set of skills that can be applied to various fields. Your strengths in bioinformatics, machine learning, statistical modeling, data analysis, and programming languages like Python, R, and MATLAB make you an attractive candidate for roles at the intersection of biology and technology.
> 
> In particular, your background may lead to opportunities in research institutions, biotechnology companies, or pharmaceutical firms that focus on analyzing genomic data, developing predictive models, or creating personalized treatment plans. Some examples of job titles that might be a good fit include bioinformatics scientist, computational biologist, data analyst in genomics, or machine learning engineer for medical imaging.
> 
> Keep in mind that your biology major may not have been directly related to your current skills, but your CS education has given you a solid foundation in programming and analytical thinking. This combin

---

#### GQ-25 — Priya Sharma

**Query:** _Which courses would strengthen my data science skills specifically for biomedical research?_

**Rationale:** Tests domain-specific course recommendations for a niche interdisciplinary student.

**Expected:** Should recommend courses relevant to biomedical data (CSC 509, 511, 621, 657 etc.); must cite course codes.

| Field | Value |
|---|---|
| Intent | `courses` (jobs=0, courses=6) |
| Planner reason | learning or upskill question |
| Relevance | 8/10 |
| Support | 7/10 |
| Utility | 9/10 |
| **Total** | 🟡 **7.85/10** |
| Time | 41.8s |

**Critique summary:** The advisor only supported all claims by evidence context, but the course code in CSC 621 does not directly tie into data science skills for biomedical research. The advisor overclaimed with weak claim support from that course,

**Response:**

> CSC 408, CSC 621 would strengthen your data science skills specifically for biomedical research, as they both teach Python, Genomics, Data Preprocessing, Data Visualization, and Bioinformatics Concepts. CSC 408 covers Machine Learning and Data Science in the context of personalized medicine, while CSC 621 focuses on Medical Imaging Analysis, which is also relevant to biomedical research.

---

### Skill Gap with Job Context

#### GQ-26 — Jordan Kim

**Query:** _What skills am I missing to land a senior software engineer role?_

**Rationale:** Targets the new skill_gap intent which must retrieve ≥3 jobs alongside courses — tests the invariant that gap analysis is grounded in job evidence, not just general learning advice.

**Expected:** Must reference specific retrieved job roles, list Jordan's actual gaps (e.g. system design, cloud), and recommend courses by code.

| Field | Value |
|---|---|
| Intent | `skill_gap` (jobs=3, courses=4) |
| Planner reason | skill-gap question requires job context |
| Relevance | 10/10 |
| Support | 8/10 |
| Utility | 7/10 |
| **Total** | 🟢 **8.45/10** |
| Time | 41.2s |

**Critique flags:**
- ⚠️ unsupported skill mentions: skills related

**Critique summary:** The response focuses on relevant gaps but lacks specific course recommendations tied to machine learning and cloud platforms. It doesn't tie these gaps directly to courses like CSC 620 or others mentioned.

**Response:**

> Based on the Relevant Job Postings you provided, it appears that you are missing skills related to machine learning, cloud platforms, and technical communication. Additionally, your gaps in Gaps include LLMs (Large Language Models), AWS (Amazon Web Services), Java, Rust, Testing, Technical Communication.
> 
> Considering this information, CSC 620: Natural Language Technologies may help address the gap in Natural Language Processing, but it might not directly cover all required skills for a senior software engineer role. A more comprehensive course covering machine learning and LLMs would be beneficial.

---

#### GQ-27 — Marcus Webb

**Query:** _I want to move into ML engineering — what's the gap between my DevOps background and those roles?_

**Rationale:** Cross-domain gap test: Marcus has cloud/DevOps skills; asking about ML engineering should retrieve ML-specific job evidence and identify missing ML skills.

**Expected:** Must identify ML-specific gaps from retrieved job evidence (PyTorch, TF, model training, etc.); should not conflate DevOps overlap with ML readiness.

| Field | Value |
|---|---|
| Intent | `skill_gap` (jobs=3, courses=4) |
| Planner reason | skill-gap question requires job context |
| Relevance | 9/10 |
| Support | 8/10 |
| Utility | 8/10 |
| **Total** | 🟢 **8.35/10** |
| Time | 42.1s |

**Critique flags:**
- ⚠️ unsupported skill mentions: hands on experience, machine learning

**Critique summary:** The response identifies gaps but could better connect course codes to practical ML application in DevOps roles.

**Response:**

> The main gaps are Machine Learning, Deep Learning, TensorFlow/Keras, PyTorch, Natural Language Processing (NLP), and Computer Vision. You're missing hands-on experience with these technologies, as well as a strong understanding of ML fundamentals like supervised/unsupervised learning, regression, classification, clustering, etc.

---

#### GQ-28 — Taylor Reyes

**Query:** _What skills do I still need to qualify for production ML engineering at a top tech company?_

**Rationale:** Taylor has deep research ML skills — tests whether the system identifies the research-to-production gap (MLOps, deployment, distributed training, system design).

**Expected:** Must surface production/MLOps gaps (e.g. Kubernetes, MLflow, distributed training) grounded in job evidence; should not suggest research courses Taylor already has.

| Field | Value |
|---|---|
| Intent | `skill_gap` (jobs=3, courses=4) |
| Planner reason | skill-gap question requires job context |
| Relevance | 6/10 |
| Support | 10/10 |
| Utility | 7/10 |
| **Total** | 🟡 **7.85/10** |
| Time | 43.1s |

**Critique summary:** fallback critique

**Response:**

> You cover Machine Learning, Python, SQL, TensorFlow, PyTorch, NLP, and Git. You have gaps in GCP, Vertex AI, BigQuery, CI/CD, REST API Design, Data Engineering, Model Deployment, Applied Statistics, Linux.

---

### Retrieval Precision

#### GQ-29 — Alex Chen

**Query:** _What Python-specific courses do I still need?_

**Rationale:** Narrow query — should retrieve Python-teaching courses specifically, not generic CS courses. Tests whether the course query is tightly scoped to user intent.

**Expected:** Must recommend only courses that teach Python or Python-adjacent skills; must cite course codes; should not recommend unrelated courses.

| Field | Value |
|---|---|
| Intent | `courses` (jobs=0, courses=6) |
| Planner reason | learning or upskill question |
| Relevance | 8/10 |
| Support | 7/10 |
| Utility | 5/10 |
| **Total** | 🟡 **6.85/10** |
| Time | 40.5s |

**Critique flags:**
- ⚠️ unsupported course codes: CSC 309, CSC 320, CSC 610

**Critique summary:** The AI career advisor's response is somewhat actionable and provides specific course recommendations, but it lacks explicit evidence from the provided context. The student could benefit from a more detailed breakdown of how each course can contribute to their Python-specific skills.

**Response:**

> You already have knowledge in Python from CSC 310: Computer Programming Lab, but to further expand your skills, you might want to consider CSC 220 doesn't cover advanced topics of python however CSC 309 was not mentioned as an option. CSC 320 or 340 are not listed as relevant courses, therefore the next most likely course would be CSC 610 (not present) or 620: Natural Language Technologies is not a Python-specific course.

---

#### GQ-30 — Sam Patel

**Query:** _Are there any jobs that only require Java?_

**Rationale:** Tests whether the system can identify a narrow requirement filter — jobs whose coverage is achievable with just Java skills. Tests precision over recall.

**Expected:** Should name specific roles where Java alone (or with basic skills Sam has) meets a majority of requirements; must ground in retrieved job evidence.

| Field | Value |
|---|---|
| Intent | `jobs` (jobs=6, courses=2) |
| Planner reason | job-fit or role recommendation question |
| Relevance | 4/10 |
| Support | 8/10 |
| Utility | 6/10 |
| **Total** | 🟡 **6.1/10** |
| Time | 40.2s |

**Critique flags:**
- ⚠️ unsupported job titles: machine learning engineer

**Critique summary:** The critique is weak as it only partially addresses the student

**Response:**

> No retrieved job posting requires only Java; however, the Machine Learning Engineer role at Adobe requires Java but covers a broader set of skills.

---

## Key Findings

### Top Performers (score ≥ 8)
- **GQ-08** (Course Recommendation, Sam Patel): 10.0/10 — _What's the most valuable course I can take next semester to open up more job opt_
- **GQ-02** (Specific Job Fit, Maria Gomez): 9.2/10 — _Which ML engineering jobs match my profile and what's missing?_
- **GQ-14** (Job Comparison, Maria Gomez): 9.2/10 — _Which pays off more for my career — taking more ML courses or pivoting to cloud/_
- **GQ-16** (Action Plan, Sam Patel): 9.15/10 — _If I can only take one more course, which one gives me the best shot at getting _
- **GQ-07** (Course Recommendation, Alex Chen): 9.1/10 — _Which courses should I take to become competitive for web development jobs?_
- **GQ-04** (Skill Gap Analysis, Alex Chen): 8.95/10 — _What specific skills am I missing to qualify for a full stack engineering role?_
- **GQ-15** (Action Plan, Alex Chen): 8.95/10 — _What are the top 3 most impactful things I can do this semester to improve my jo_
- **GQ-11** (Career Readiness, Maria Gomez): 8.7/10 — _Create a semester-by-semester plan to make me competitive for senior ML roles._
- **GQ-20** (Self-Assessment, Maria Gomez): 8.5/10 — _Given everything I've learned, what kind of engineer am I becoming and what shou_
- **GQ-26** (Skill Gap with Job Context, Jordan Kim): 8.45/10 — _What skills am I missing to land a senior software engineer role?_
- **GQ-05** (Skill Gap Analysis, Maria Gomez): 8.4/10 — _I'm strong in ML and deep learning. What gaps are blocking me from cloud enginee_
- **GQ-27** (Skill Gap with Job Context, Marcus Webb): 8.35/10 — _I want to move into ML engineering — what's the gap between my DevOps background_
- **GQ-01** (Specific Job Fit, Alex Chen): 8.2/10 — _Am I a good fit for the Junior Software Engineer role at Leidos?_
- **GQ-09** (Course Recommendation, Maria Gomez): 8.2/10 — _I've already taken CSC 415 and CSC 510. What advanced courses build on those for_
- **GQ-19** (Self-Assessment, Alex Chen): 8.2/10 — _What are my strongest marketable skills and which job category do they point tow_
- **GQ-17** (Domain Pivot, Alex Chen): 8.15/10 — _I want to pivot into data science. What's the gap between where I am and data sc_
- **GQ-21** (Strong Fit, Jordan Kim): 8.1/10 — _What full stack or web engineering roles am I competitive for right now?_

### Needs Work (score < 6)
- **GQ-12** (Career Readiness, Sam Patel): 5.25/10 — _Be honest — am I competitive for any real industry jobs right now?_

### Recurring Critique Flags
- `unsupported job titles` — appeared 8×
- `unsupported course titles` — appeared 5×
- `unsupported skill mentions` — appeared 2×
- `citation source 'course descriptions focus on these areas.' not found in evidence` — appeared 1×
- `citation source 'job postings highlight cloud-based infrastructure.' not found in evidence` — appeared 1×
- `citation source 'evidence_citations' not found in evidence` — appeared 1×
- `unsupported course codes` — appeared 1×

### Slow Queries (> 40s)
- **GQ-01**: 42.2s — Am I a good fit for the Junior Software Engineer role at Leidos?
- **GQ-02**: 58.3s — Which ML engineering jobs match my profile and what's missing?
- **GQ-03**: 56.3s — I only have basic programming skills. What entry-level jobs are realis
- **GQ-04**: 48.0s — What specific skills am I missing to qualify for a full stack engineer
- **GQ-05**: 41.0s — I'm strong in ML and deep learning. What gaps are blocking me from clo
- **GQ-06**: 42.7s — What is the single most important skill I should learn next to become 
- **GQ-07**: 50.8s — Which courses should I take to become competitive for web development 
- **GQ-08**: 42.7s — What's the most valuable course I can take next semester to open up mo
- **GQ-09**: 49.4s — I've already taken CSC 415 and CSC 510. What advanced courses build on
- **GQ-10**: 72.5s — I'm graduating in 6 months. Give me an honest assessment of my job mar
- **GQ-11**: 63.3s — Create a semester-by-semester plan to make me competitive for senior M
- **GQ-12**: 52.9s — Be honest — am I competitive for any real industry jobs right now?
- **GQ-13**: 52.7s — Between a software engineering role at Microsoft and one at a startup 
- **GQ-14**: 73.0s — Which pays off more for my career — taking more ML courses or pivoting
- **GQ-15**: 44.2s — What are the top 3 most impactful things I can do this semester to imp
- **GQ-17**: 44.1s — I want to pivot into data science. What's the gap between where I am a
- **GQ-18**: 41.8s — I'm thinking of moving into systems or embedded software. Is my backgr
- **GQ-19**: 56.5s — What are my strongest marketable skills and which job category do they
- **GQ-20**: 47.0s — Given everything I've learned, what kind of engineer am I becoming and
- **GQ-22**: 54.3s — Am I ready for a cloud or DevOps engineering role?
- **GQ-23**: 41.3s — Which ML or AI research engineering positions am I closest to qualifyi
- **GQ-24**: 49.4s — Given my biology and CS background, what unique job opportunities exis
- **GQ-25**: 41.8s — Which courses would strengthen my data science skills specifically for
- **GQ-26**: 41.2s — What skills am I missing to land a senior software engineer role?
- **GQ-27**: 42.1s — I want to move into ML engineering — what's the gap between my DevOps 
- **GQ-28**: 43.1s — What skills do I still need to qualify for production ML engineering a
- **GQ-29**: 40.5s — What Python-specific courses do I still need?
- **GQ-30**: 40.2s — Are there any jobs that only require Java?
