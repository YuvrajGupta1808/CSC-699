# Eval Report: qwen2.5-7b

**Date:** 2026-05-12 19:02  
**Generator:** `qwen2.5-7b`  
**Planner:** `llama-3.2-3b`  **Critic:** `llama-3.2-3b`  
**Fireworks ID:** `qwen/qwen-2.5-7b-instruct`

**Pricing:** $0.05/M input · $0.15/M output

## Summary

| Metric | Value |
|---|---|
| Questions run | 5 |
| Errors | 0 |
| Avg Score | 8.53/10 |
| Avg Latency | 16.8s |
| Avg Cost/query | $0.000245 |
| Total Cost | $0.001225 |

## Score Overview

| ID | Category | Student | Score | Rel | Sup | Util | Time | Status |
|---|---|---|---|---|---|---|---|---|
| GQ-01 | Specific Job Fit | Alex Chen | **8.55** | 8 | 10 | 7 | 16.5s | ✅ |
| GQ-03 | Specific Job Fit | Sam Patel | **8.8** | 8 | 10 | 8 | 17.3s | ✅ |
| GQ-07 | Course Recommendation | Alex Chen | **8.8** | 8 | 10 | 8 | 17.1s | ✅ |
| GQ-12 | Career Readiness | Sam Patel | **8.45** | 7 | 10 | 8 | 14.1s | ✅ |
| GQ-21 | Strong Fit | Jordan Kim | **8.05** | 8 | 10 | 5 | 19.0s | ✅ |

## Per-Question Results

### GQ-01 — Specific Job Fit (Alex Chen)

**Question:** Am I a good fit for the Junior Software Engineer role at Leidos?

**Eval criteria:** _Must reference Leidos by name, list Alex's covered and gap skills specifically._

**Score:** 8.55/10 (rel=8, sup=10, util=7)  
**Intent:** `jobs` (keyword_fallback)  
**Time:** 16.5s
**Tokens:** 3795 in / 248 out  **Cost:** $0.000227

**Critic note:** _fallback critique_

**Pipeline:** Loaded student profile for `Alex Chen`. → Planner selected `6` jobs and `2` courses: job-fit or recommendation question. → Job search returned `6` hit(s). → Course search returned `2` hit(s). → Built evidence bundle with `6` jobs and `2` courses. → Built `3` candidate view(s): A — Specific Job, B — Job Cluster, C — Course Path. → Generated `3` candidate response(s). → Critiqued `3` candidate response(s). → Refinement skipped: support score sufficient. → Selected `B — Job Cluster` with total critique score `8.55`.

**Response:**

> No retrieved job posting indicates "Junior Software Engineer" at Leidos, so I cannot assess your
> qualifications based on this specific role.  However, you have skills and courses that might be
> relevant to other roles. Let's look at gaps in your skills:  TypeScript is a required skill for the
> Remote Software Engineer role at Jobgether, which you could potentially apply to.  Looking into
> other job postings may help identify better matches.

---

### GQ-03 — Specific Job Fit (Sam Patel)

**Question:** I only have basic programming skills. What entry-level jobs are realistic for me right now?

**Eval criteria:** _Should not oversell Sam's readiness; should name specific achievable jobs and list actual gaps honestly._

**Score:** 8.8/10 (rel=8, sup=10, util=8)  
**Intent:** `jobs` (keyword_fallback)  
**Time:** 17.3s
**Tokens:** 4380 in / 297 out  **Cost:** $0.000264

**Critic note:** _fallback critique_

**Pipeline:** Loaded student profile for `Sam Patel`. → Planner selected `6` jobs and `2` courses: job-fit or recommendation question. → Job search returned `6` hit(s). → Course search returned `2` hit(s). → Built evidence bundle with `6` jobs and `2` courses. → Built `3` candidate view(s): A — Specific Job, B — Job Cluster, C — Course Path. → Generated `3` candidate response(s). → Critiqued `3` candidate response(s). → Refinement skipped: support score sufficient. → Selected `C — Course Path` with total critique score `8.8`.

**Response:**

> Given your current skills and experience as a Computer Science student with completed courses CSC
> 101, CSC 110, and CSC 215, I can recommend some entry-level job opportunities that may be a good
> fit.  Considering the gaps in the Software Engineer roles you've posted, CSC 215 seems like a
> crucial stepping stone to address. This course covers Java programming fundamentals, which is one of
> your existing skills. If you complete this course, it will help bridge the gap for Object-Oriented
> Programming and other areas.  No retrieved course addresses JavaScript — you may need to look beyond
> this course catalog.

---

### GQ-07 — Course Recommendation (Alex Chen)

**Question:** Which courses should I take to become competitive for web development jobs?

**Eval criteria:** _Must cite actual course codes (e.g. CSC 307, CSC 317) and explain which gap each addresses._

**Score:** 8.8/10 (rel=8, sup=10, util=8)  
**Intent:** `broad` (keyword_fallback)  
**Time:** 17.1s
**Tokens:** 4421 in / 277 out  **Cost:** $0.000263

**Critic note:** _fallback critique_

**Pipeline:** Loaded student profile for `Alex Chen`. → Planner selected `6` jobs and `6` courses: broad readiness analysis. → Job search returned `6` hit(s). → Course search returned `6` hit(s). → Built evidence bundle with `6` jobs and `6` courses. → Built `3` candidate view(s): A — Specific Job, B — Job Cluster, C — Course Path. → Generated `3` candidate response(s). → Critiqued `3` candidate response(s). → Refinement skipped: support score sufficient. → Selected `A — Specific Job` with total critique score `8.8`.

**Response:**

> Based on the Relevant Courses provided, you should take CSC 317: Introduction to Web Software
> Development and CSC 867: Internet Application Design and Development.  CSC 317 addresses JavaScript,
> which is listed as a gap skill in the Glean job posting. While it only covers JavaScript, this
> course can provide a solid foundation for web development skills.  CSC 867 directly addresses
> JavaScript, Node.js, and other technologies commonly used in web development. It also covers RESTful
> APIs, HTML5/CSS3, and database connectivity, making it an essential course for becoming competitive
> in web development jobs.

---

### GQ-12 — Career Readiness (Sam Patel)

**Question:** Be honest — am I competitive for any real industry jobs right now?

**Eval criteria:** _Should not invent optimism — must reflect Sam's limited skill set accurately while pointing to a path forward._

**Score:** 8.45/10 (rel=7, sup=10, util=8)  
**Intent:** `jobs` (keyword_fallback)  
**Time:** 14.1s
**Tokens:** 3941 in / 217 out  **Cost:** $0.000230

**Critic note:** _fallback critique_

**Pipeline:** Loaded student profile for `Sam Patel`. → Planner selected `6` jobs and `2` courses: job-fit or recommendation question. → Job search returned `6` hit(s). → Course search returned `2` hit(s). → Built evidence bundle with `6` jobs and `2` courses. → Built `3` candidate view(s): A — Specific Job, B — Job Cluster, C — Course Path. → Generated `3` candidate response(s). → Critiqued `3` candidate response(s). → Refinement skipped: support score sufficient. → Selected `B — Job Cluster` with total critique score `8.45`.

**Response:**

> Based on the provided information, it seems that you cover none of the required skills for the top 6
> retrieved job postings. Your most recent completed courses are CSC 101, CSC 110, and CSC 215, but
> none of these directly address a gap in your listed skill gaps.  The only potential connection is
> CSC 221: Data Structure Lab, which addresses Debugging, one of your gaps. However, this course
> doesn't cover enough skills to make you competitive for the top jobs on your list.

---

### GQ-21 — Strong Fit (Jordan Kim)

**Question:** What full stack or web engineering roles am I competitive for right now?

**Eval criteria:** _Should show high skill coverage (≥50%), short gap list, and name specific web/full-stack roles._

**Score:** 8.05/10 (rel=8, sup=10, util=5)  
**Intent:** `jobs` (keyword_fallback)  
**Time:** 19.0s
**Tokens:** 3799 in / 347 out  **Cost:** $0.000242

**Critic note:** _fallback critique_

**Pipeline:** Loaded student profile for `Jordan Kim`. → Planner selected `6` jobs and `2` courses: job-fit or recommendation question. → Job search returned `6` hit(s). → Course search returned `2` hit(s). → Built evidence bundle with `6` jobs and `2` courses. → Built `3` candidate view(s): A — Specific Job, B — Job Cluster, C — Course Path. → Generated `3` candidate response(s). → Critiqued `3` candidate response(s). → Refinement skipped: support score sufficient. → Selected `B — Job Cluster` with total critique score `8.05`.

**Response:**

> Based on the job postings you've seen, it seems that you're more competitive for roles that don't
> require Java, Spring Boot, or other languages not listed in your current skill set.   Given your
> skills in Python, TypeScript, React, Node.js, SQL, and REST, you might be competitive for full stack
> roles at companies like Color, Fidelity Investments (for non-Java related positions), or possibly
> IXL Learning if they're open to JavaScript/React-based development. However, keep in mind that these
> are just educated guesses based on the available job postings.

---
