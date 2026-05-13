# Eval Report: llama-3.1-8b

**Date:** 2026-05-12 20:09  
**Generator:** `llama-3.1-8b`  
**Planner:** `llama-3.2-3b`  **Critic:** `llama-3.2-3b`  
**Provider:** `openrouter`  **Model ID:** `meta-llama/llama-3.1-8b-instruct`

**Pricing:** $0.055/M input · $0.055/M output

## Summary

| Metric | Value |
|---|---|
| Questions run | 10 |
| Errors | 0 |
| Avg Score | 8.21/10 |
| Avg Latency | 26.8s |
| Avg Cost/query | $0.000246 |
| Total Cost | $0.002457 |

## Score Overview

| ID | Category | Student | Score | Rel | Sup | Util | Time | Status |
|---|---|---|---|---|---|---|---|---|
| GQ-01 | Specific Job Fit | Alex Chen | **8.2** | 7 | 10 | 7 | 20.5s | ✅ |
| GQ-03 | Specific Job Fit | Sam Patel | **8.0** | 8 | 8 | 8 | 21.5s | ✅ |
| GQ-04 | Skill Gap Analysis | Alex Chen | **8.55** | 8 | 10 | 7 | 22.9s | ✅ |
| GQ-07 | Course Recommendation | Alex Chen | **8.45** | 7 | 10 | 8 | 25.9s | ✅ |
| GQ-12 | Career Readiness | Sam Patel | **7.75** | 8 | 8 | 7 | 26.9s | ✅ |
| GQ-14 | Job Comparison | Maria Gomez | **8.8** | 8 | 10 | 8 | 45.1s | ✅ |
| GQ-21 | Strong Fit | Jordan Kim | **7.4** | 7 | 8 | 7 | 35.9s | ✅ |
| GQ-22 | Strong Fit | Marcus Webb | **8.2** | 7 | 10 | 7 | 29.9s | ✅ |
| GQ-26 | Skill Gap with Job Context | Jordan Kim | **8.55** | 8 | 10 | 7 | 21.4s | ✅ |
| GQ-30 | Retrieval Precision | Sam Patel | **8.2** | 7 | 10 | 7 | 17.5s | ✅ |

## Per-Question Results

### GQ-01 — Specific Job Fit (Alex Chen)

**Question:** Am I a good fit for the Junior Software Engineer role at Leidos?

**Eval criteria:** _Must reference Leidos by name, list Alex's covered and gap skills specifically._

**Score:** 8.2/10 (rel=7, sup=10, util=7)  
**Intent:** `jobs` (keyword_fallback)  
**Time:** 20.5s
**Tokens:** 3739 in / 260 out  **Cost:** $0.000220

**Critic note:** _fallback critique_

**Pipeline:** Loaded student profile for `Alex Chen`. → Planner selected `6` jobs and `2` courses: job-fit or recommendation question. → Job search returned `6` hit(s). → Course search returned `2` hit(s). → Built evidence bundle with `6` jobs and `2` courses. → Built `3` candidate view(s): A — Specific Job, B — Job Cluster, C — Course Path. → Generated `3` candidate response(s). → Critiqued `3` candidate response(s). → Refinement skipped: support score sufficient. → Selected `A — Specific Job` with total critique score `8.2`.

**Response:**

> No retrieved course clearly addresses these gaps for Junior Software Engineer: TypeScript, Kotlin,
> Distributed Systems, GCP, AWS, API Design, Front-end Development, Back-end Development, Analytics
> Pipelines, SDK Development.

---

### GQ-03 — Specific Job Fit (Sam Patel)

**Question:** I only have basic programming skills. What entry-level jobs are realistic for me right now?

**Eval criteria:** _Should not oversell Sam's readiness; should name specific achievable jobs and list actual gaps honestly._

**Score:** 8.0/10 (rel=8, sup=8, util=8)  
**Intent:** `jobs` (keyword_fallback)  
**Time:** 21.5s
**Tokens:** 4491 in / 273 out  **Cost:** $0.000262

**Critic note:** _fallback critique | unsupported course titles: object-oriented programming_

**Pipeline:** Loaded student profile for `Sam Patel`. → Planner selected `6` jobs and `2` courses: job-fit or recommendation question. → Job search returned `6` hit(s). → Course search returned `2` hit(s). → Built evidence bundle with `6` jobs and `2` courses. → Built `3` candidate view(s): A — Specific Job, B — Job Cluster, C — Course Path. → Generated `3` candidate response(s). → Critiqued `3` candidate response(s). → Refinement skipped: support score sufficient. → Selected `A — Specific Job` with total critique score `8.0`.

**Response:**

> You covered Java, Problem Solving, but the job posting lists other skills, such as Object-Oriented
> Programming, JavaScript, HTML/CSS, MongoDB, AWS, Software Engineering, and Analytical Reasoning. No
> retrieved course addresses these gaps.   However, you completed CSC 215, which taught Java, Object-
> Oriented Programming, among other topics. Given your current skillset, entry-level jobs may be more
> suitable.

---

### GQ-04 — Skill Gap Analysis (Alex Chen)

**Question:** What specific skills am I missing to qualify for a full stack engineering role?

**Eval criteria:** _Must name concrete missing skills (e.g. JavaScript, React, SQL) grounded in job evidence._

**Score:** 8.55/10 (rel=8, sup=10, util=7)  
**Intent:** `jobs` (keyword_fallback)  
**Time:** 22.9s
**Tokens:** 3820 in / 277 out  **Cost:** $0.000225

**Critic note:** _fallback critique_

**Pipeline:** Loaded student profile for `Alex Chen`. → Planner selected `6` jobs and `2` courses: job-oriented skill requirements question. → Job search returned `6` hit(s). → Course search returned `2` hit(s). → Built evidence bundle with `6` jobs and `2` courses. → Built `3` candidate view(s): A — Specific Job, B — Job Cluster, C — Course Path. → Generated `3` candidate response(s). → Critiqued `3` candidate response(s). → Refinement skipped: support score sufficient. → Selected `A — Specific Job` with total critique score `8.55`.

**Response:**

> Based on the job posting, you are missing TypeScript, React, MongoDB, Retrieval-Augmented
> Generation, Statistical Modeling, and Human-AI Interaction skills to qualify for a full stack
> engineering role.

---

### GQ-07 — Course Recommendation (Alex Chen)

**Question:** Which courses should I take to become competitive for web development jobs?

**Eval criteria:** _Must cite actual course codes (e.g. CSC 307, CSC 317) and explain which gap each addresses._

**Score:** 8.45/10 (rel=7, sup=10, util=8)  
**Intent:** `broad` (keyword_fallback)  
**Time:** 25.9s
**Tokens:** 4598 in / 211 out  **Cost:** $0.000264

**Critic note:** _fallback critique_

**Pipeline:** Loaded student profile for `Alex Chen`. → Planner selected `6` jobs and `6` courses: broad readiness analysis. → Job search returned `6` hit(s). → Course search returned `6` hit(s). → Built evidence bundle with `6` jobs and `6` courses. → Built `3` candidate view(s): A — Specific Job, B — Job Cluster, C — Course Path. → Generated `3` candidate response(s). → Critiqued `3` candidate response(s). → Refinement skipped: support score sufficient. → Selected `A — Specific Job` with total critique score `8.45`.

**Response:**

> Based on the Relevant Courses section, CSC 317: Introduction to Web Software Development addresses
> the gap in JavaScript and covers topics such as HTML5/CSS3, Node.js, Express.js, SQL and MySQL,
> UNIX/Linux, Client-Server Architecture, RESTful APIs, Form Validation and Sanitization, Session
> Management and Cookies, Git/GitHub, Responsive Web Design, Web Security, Database Connectivity,
> E-Commerce Application Development, and Deployment Basics.   Additionally, CSC 867: Internet
> Application Design and Development addresses the gap in JavaScript and covers topics such as
> React.js, PostgreSQL, RESTful API Design, Docker Containerization, and Git/GitHub CI/CD.

---

### GQ-12 — Career Readiness (Sam Patel)

**Question:** Be honest — am I competitive for any real industry jobs right now?

**Eval criteria:** _Should not invent optimism — must reflect Sam's limited skill set accurately while pointing to a path forward._

**Score:** 7.75/10 (rel=8, sup=8, util=7)  
**Intent:** `jobs` (keyword_fallback)  
**Time:** 26.9s
**Tokens:** 4055 in / 217 out  **Cost:** $0.000235

**Critic note:** _fallback critique | unsupported course titles: backend engineering_

**Pipeline:** Loaded student profile for `Sam Patel`. → Planner selected `6` jobs and `2` courses: job-fit or recommendation question. → Job search returned `6` hit(s). → Course search returned `2` hit(s). → Built evidence bundle with `6` jobs and `2` courses. → Built `3` candidate view(s): A — Specific Job, B — Job Cluster, C — Course Path. → Generated `3` candidate response(s). → Critiqued `3` candidate response(s). → Refinement skipped: support score sufficient. → Selected `B — Job Cluster` with total critique score `7.75`.

**Response:**

> Based on the provided job postings and your current skills, it appears that you cover some of the
> gaps required by these senior software engineer positions at Voltai. However, you still lack
> essential skills like Backend Engineering, Full-stack Development, Infrastructure, DevOps, Agent
> Development, Retrieval-Augmented Generation, Systems Design, Debugging, Docker, AWS, Azure, GCP,
> IaC, On-prem Deployment, Embedded Systems, C++, Telematics, IoT, Firmware, Real-Time Applications,
> Connectivity Technologies, Cloud Integration, Agile Development, Embedded Linux, RTOS, Hardware
> Debugging, Version Control, CI/CD, Cybersecurity, and Analytical Skills.  It is unlikely that you
> are competitive for any real industry jobs with these positions.

---

### GQ-14 — Job Comparison (Maria Gomez)

**Question:** Which pays off more for my career — taking more ML courses or pivoting to cloud/DevOps?

**Eval criteria:** _Must use retrieved job and course evidence; must not speculate beyond the evidence._

**Score:** 8.8/10 (rel=8, sup=10, util=8)  
**Intent:** `broad` (keyword_fallback)  
**Time:** 45.1s
**Tokens:** 5219 in / 293 out  **Cost:** $0.000303

**Critic note:** _fallback critique_

**Pipeline:** Loaded student profile for `Maria Gomez`. → Planner selected `6` jobs and `6` courses: broad readiness analysis. → Job search returned `6` hit(s). → Course search returned `6` hit(s). → Built evidence bundle with `6` jobs and `6` courses. → Built `3` candidate view(s): A — Specific Job, B — Job Cluster, C — Course Path. → Generated `3` candidate response(s). → Critiqued `3` candidate response(s). → Refinement skipped: support score sufficient. → Selected `A — Specific Job` with total critique score `8.8`.

**Response:**

> Based on the provided information, it's difficult to determine which path will pay off more for your
> career. However, I can provide some context and insights.  The job posting for AI Engineer at HAVI
> lists several gaps in Machine Learning skills that you already possess (Machine Learning, Deep
> Learning). This suggests that having a strong foundation in ML may be beneficial in this role.  On
> the other hand, cloud/DevOps skills are also relevant to the job posting, but they are listed as
> separate gaps (DevOps and Terraform). It's possible that gaining expertise in these areas could make
> you more competitive for AI Engineer roles or other opportunities at HAVI.  That being said, a
> course like CSC 878: Big Data Platforms and Systems addresses both Apache Spark and some cloud-
> related concepts. This course might provide a foundation for understanding big data technologies,
> which can be relevant to both ML and cloud/DevOps skills.  Considering your existing skillset in
> Machine Learning, taking additional ML courses might seem like the more direct way to address gaps.
> However, pivoting to cloud/DevOps could also benefit you if you're interested in transitioning into
> a role that focuses on big data technologies or infrastructure management.   To make a more informed
> decision, I recommend exploring the job market and networking with professionals in your desired
> field to gain a better understanding of the skills required for AI Engineer roles at HAVI.

---

### GQ-21 — Strong Fit (Jordan Kim)

**Question:** What full stack or web engineering roles am I competitive for right now?

**Eval criteria:** _Should show high skill coverage (≥50%), short gap list, and name specific web/full-stack roles._

**Score:** 7.4/10 (rel=7, sup=8, util=7)  
**Intent:** `jobs` (keyword_fallback)  
**Time:** 35.9s
**Tokens:** 3735 in / 255 out  **Cost:** $0.000219

**Critic note:** _fallback critique | unsupported job titles: customer portal, new grad_

**Pipeline:** Loaded student profile for `Jordan Kim`. → Planner selected `6` jobs and `2` courses: job-fit or recommendation question. → Job search returned `6` hit(s). → Course search returned `2` hit(s). → Built evidence bundle with `6` jobs and `2` courses. → Built `3` candidate view(s): A — Specific Job, B — Job Cluster, C — Course Path. → Generated `3` candidate response(s). → Critiqued `3` candidate response(s). → Refinement skipped: support score sufficient. → Selected `C — Course Path` with total critique score `7.4`.

**Response:**

> Based on the provided job postings, you appear to be competitive for Software Engineer - Customer
> Portal at Applied Intuition and Software Engineer - New Grad at Scale AI. Both roles require skills
> in Python, TypeScript, React, and PostgreSQL, which you have covered. However, neither of these
> roles specifically address the gaps mentioned, such as Angular, HTML/CSS, Operating Systems,
> Technical Communication.

---

### GQ-22 — Strong Fit (Marcus Webb)

**Question:** Am I ready for a cloud or DevOps engineering role?

**Eval criteria:** _Should show high coverage for cloud roles, list specific remaining gaps (e.g. Azure, GCP), not generic advice._

**Score:** 8.2/10 (rel=7, sup=10, util=7)  
**Intent:** `jobs` (keyword_fallback)  
**Time:** 29.9s
**Tokens:** 4446 in / 297 out  **Cost:** $0.000261

**Critic note:** _fallback critique_

**Pipeline:** Loaded student profile for `Marcus Webb`. → Planner selected `6` jobs and `2` courses: job-fit or recommendation question. → Job search returned `6` hit(s). → Course search returned `2` hit(s). → Built evidence bundle with `6` jobs and `2` courses. → Built `3` candidate view(s): A — Specific Job, B — Job Cluster, C — Course Path. → Generated `3` candidate response(s). → Critiqued `3` candidate response(s). → Refinement skipped: support score sufficient. → Selected `A — Specific Job` with total critique score `8.2`.

**Response:**

> You have a good foundation in AWS and Docker/Kubernetes. However, the job posting for Site
> Reliability Engineer at Qlik highlights gaps in areas like Azure, Prometheus, Open Telemetry, Helm,
> MongoDB, Microservices, and Networking Security that are not directly addressed by your current
> skills. Additionally, Terraform is listed as one of the required tools, but you also have
> Infrastructure as Code covered. You may want to consider further developing your skills in these
> areas before being fully competitive for cloud or DevOps engineering roles.

---

### GQ-26 — Skill Gap with Job Context (Jordan Kim)

**Question:** What skills am I missing to land a senior software engineer role?

**Eval criteria:** _Must reference specific retrieved job roles, list Jordan's actual gaps (e.g. system design, cloud), and recommend courses by code._

**Score:** 8.55/10 (rel=8, sup=10, util=7)  
**Intent:** `jobs` (keyword_fallback)  
**Time:** 21.4s
**Tokens:** 3855 in / 299 out  **Cost:** $0.000228

**Critic note:** _fallback critique_

**Pipeline:** Loaded student profile for `Jordan Kim`. → Planner selected `6` jobs and `2` courses: job-oriented skill requirements question. → Job search returned `6` hit(s). → Course search returned `2` hit(s). → Built evidence bundle with `6` jobs and `2` courses. → Built `3` candidate view(s): A — Specific Job, B — Job Cluster, C — Course Path. → Generated `3` candidate response(s). → Critiqued `3` candidate response(s). → Refinement skipped: support score sufficient. → Selected `A — Specific Job` with total critique score `8.55`.

**Response:**

> Based on the provided job posting, you appear to be missing Django, AWS, LLMs, and Code Review
> skills to land a senior software engineer role at Color. These skills are listed under the Gaps
> section of the job description.

---

### GQ-30 — Retrieval Precision (Sam Patel)

**Question:** Are there any jobs that only require Java?

**Eval criteria:** _Should name specific roles where Java alone (or with basic skills Sam has) meets a majority of requirements; must ground in retrieved job evidence._

**Score:** 8.2/10 (rel=7, sup=10, util=7)  
**Intent:** `jobs` (keyword_fallback)  
**Time:** 17.5s
**Tokens:** 4104 in / 230 out  **Cost:** $0.000238

**Critic note:** _fallback critique_

**Pipeline:** Loaded student profile for `Sam Patel`. → Planner selected `6` jobs and `2` courses: job-fit or recommendation question. → Job search returned `6` hit(s). → Course search returned `2` hit(s). → Built evidence bundle with `6` jobs and `2` courses. → Built `3` candidate view(s): A — Specific Job, B — Job Cluster, C — Course Path. → Generated `3` candidate response(s). → Critiqued `3` candidate response(s). → Refinement skipped: support score sufficient. → Selected `C — Course Path` with total critique score `8.2`.

**Response:**

> No retrieved job posting requires only Java. However, the Full Stack Engineer (Cleared) at
> Guidehouse has a significant gap related to Java, requiring additional skills beyond just Java.

---
