# Eval Report: llama-3.2-3b

**Date:** 2026-05-12 19:00  
**Generator:** `llama-3.2-3b`  
**Planner:** `llama-3.2-3b`  **Critic:** `llama-3.2-3b`  
**Fireworks ID:** `meta-llama/llama-3.2-3b-instruct`

**Pricing:** $0.015/M input · $0.025/M output

## Summary

| Metric | Value |
|---|---|
| Questions run | 5 |
| Errors | 0 |
| Avg Score | 8.28/10 |
| Avg Latency | 18.2s |
| Avg Cost/query | $0.000067 |
| Total Cost | $0.000337 |

## Score Overview

| ID | Category | Student | Score | Rel | Sup | Util | Time | Status |
|---|---|---|---|---|---|---|---|---|
| GQ-01 | Specific Job Fit | Alex Chen | **8.0** | 8 | 8 | 8 | 17.7s | ✅ |
| GQ-03 | Specific Job Fit | Sam Patel | **8.55** | 8 | 10 | 7 | 18.6s | ✅ |
| GQ-07 | Course Recommendation | Alex Chen | **8.45** | 7 | 10 | 8 | 19.4s | ✅ |
| GQ-12 | Career Readiness | Sam Patel | **7.85** | 6 | 10 | 7 | 18.2s | ✅ |
| GQ-21 | Strong Fit | Jordan Kim | **8.55** | 8 | 10 | 7 | 17.1s | ✅ |

## Per-Question Results

### GQ-01 — Specific Job Fit (Alex Chen)

**Question:** Am I a good fit for the Junior Software Engineer role at Leidos?

**Eval criteria:** _Must reference Leidos by name, list Alex's covered and gap skills specifically._

**Score:** 8.0/10 (rel=8, sup=8, util=8)  
**Intent:** `jobs` (keyword_fallback)  
**Time:** 17.7s
**Tokens:** 3730 in / 218 out  **Cost:** $0.000061

**Critic note:** _fallback critique | course recommendation lacks gap support for CSC 688_

**Pipeline:** Loaded student profile for `Alex Chen`. → Planner selected `6` jobs and `2` courses: job-fit or recommendation question. → Job search returned `6` hit(s). → Course search returned `2` hit(s). → Built evidence bundle with `6` jobs and `2` courses. → Built `3` candidate view(s): A — Specific Job, B — Job Cluster, C — Course Path. → Generated `3` candidate response(s). → Critiqued `3` candidate response(s). → Refinement skipped: support score sufficient. → Selected `C — Course Path` with total critique score `8.0`.

**Response:**

> I couldn't find any information on the "Junior Software Engineer" role at "Leidos". The job postings
> you provided were for roles at Jobgether, which is not Leidos. Without this context, I can only
> suggest that you review relevant courses that may address gaps in your skills, such as CSC 688: AI
> Entrepreneurship (covers cross-functional communication) or CSC 694: Cooperative Education: Computer
> Science (covers team collaboration and code review).

---

### GQ-03 — Specific Job Fit (Sam Patel)

**Question:** I only have basic programming skills. What entry-level jobs are realistic for me right now?

**Eval criteria:** _Should not oversell Sam's readiness; should name specific achievable jobs and list actual gaps honestly._

**Score:** 8.55/10 (rel=8, sup=10, util=7)  
**Intent:** `jobs` (keyword_fallback)  
**Time:** 18.6s
**Tokens:** 4348 in / 272 out  **Cost:** $0.000072

**Critic note:** _fallback critique_

**Pipeline:** Loaded student profile for `Sam Patel`. → Planner selected `6` jobs and `2` courses: job-fit or recommendation question. → Job search returned `6` hit(s). → Course search returned `2` hit(s). → Built evidence bundle with `6` jobs and `2` courses. → Built `3` candidate view(s): A — Specific Job, B — Job Cluster, C — Course Path. → Generated `3` candidate response(s). → Critiqued `3` candidate response(s). → Refinement skipped: support score sufficient. → Selected `A — Specific Job` with total critique score `8.55`.

**Response:**

> You've completed CSC 101, CSC 110, and CSC 215, which cover Programming Fundamentals, Computational
> Thinking, and Intermediate Computer Programming, respectively. Given your current skill level, you
> may be a good fit for entry-level positions that don't require extensive programming expertise.
> Some realistic entry-level job options might include Junior Data Analyst or Junior Quality Assurance
> (QA) Tester roles in various industries.

---

### GQ-07 — Course Recommendation (Alex Chen)

**Question:** Which courses should I take to become competitive for web development jobs?

**Eval criteria:** _Must cite actual course codes (e.g. CSC 307, CSC 317) and explain which gap each addresses._

**Score:** 8.45/10 (rel=7, sup=10, util=8)  
**Intent:** `broad` (keyword_fallback)  
**Time:** 19.4s
**Tokens:** 4526 in / 246 out  **Cost:** $0.000074

**Critic note:** _fallback critique_

**Pipeline:** Loaded student profile for `Alex Chen`. → Planner selected `6` jobs and `6` courses: broad readiness analysis. → Job search returned `6` hit(s). → Course search returned `6` hit(s). → Built evidence bundle with `6` jobs and `6` courses. → Built `3` candidate view(s): A — Specific Job, B — Job Cluster, C — Course Path. → Generated `3` candidate response(s). → Critiqued `3` candidate response(s). → Refinement skipped: support score sufficient. → Selected `A — Specific Job` with total critique score `8.45`.

**Response:**

> To address the gap in JavaScript, consider taking CSC 317 or CSC 667. Both courses directly teach
> JavaScript and are relevant to web development. Additionally, CSC 867 addresses another gap in
> JavaScript but also covers other topics that may be valuable for web development, such as Node.js,
> React.js, and Express.js.

---

### GQ-12 — Career Readiness (Sam Patel)

**Question:** Be honest — am I competitive for any real industry jobs right now?

**Eval criteria:** _Should not invent optimism — must reflect Sam's limited skill set accurately while pointing to a path forward._

**Score:** 7.85/10 (rel=6, sup=10, util=7)  
**Intent:** `jobs` (keyword_fallback)  
**Time:** 18.2s
**Tokens:** 4071 in / 199 out  **Cost:** $0.000066

**Critic note:** _fallback critique_

**Pipeline:** Loaded student profile for `Sam Patel`. → Planner selected `6` jobs and `2` courses: job-fit or recommendation question. → Job search returned `6` hit(s). → Course search returned `2` hit(s). → Built evidence bundle with `6` jobs and `2` courses. → Built `3` candidate view(s): A — Specific Job, B — Job Cluster, C — Course Path. → Generated `3` candidate response(s). → Critiqued `3` candidate response(s). → Refinement skipped: support score sufficient. → Selected `A — Specific Job` with total critique score `7.85`.

**Response:**

> Based on the provided information, it appears that you have significant gaps in your skills,
> particularly in areas like backend engineering, full-stack development, infrastructure, and cloud
> platforms such as AWS, Azure, and GCP. Additionally, you lack experience in specific areas mentioned
> by Voltai, such as retrieval-augmented generation, agent development, and field engineering.  Your
> current skills only cover a few fundamental programming concepts, and while you've completed some
> courses, they don't appear to directly address the gaps present in the job posting. Therefore, it
> seems unlikely that you would be competitive for this particular role at Voltai without significant
> additional education or training.

---

### GQ-21 — Strong Fit (Jordan Kim)

**Question:** What full stack or web engineering roles am I competitive for right now?

**Eval criteria:** _Should show high skill coverage (≥50%), short gap list, and name specific web/full-stack roles._

**Score:** 8.55/10 (rel=8, sup=10, util=7)  
**Intent:** `jobs` (keyword_fallback)  
**Time:** 17.1s
**Tokens:** 3842 in / 240 out  **Cost:** $0.000064

**Critic note:** _fallback critique_

**Pipeline:** Loaded student profile for `Jordan Kim`. → Planner selected `6` jobs and `2` courses: job-fit or recommendation question. → Job search returned `6` hit(s). → Course search returned `2` hit(s). → Built evidence bundle with `6` jobs and `2` courses. → Built `3` candidate view(s): A — Specific Job, B — Job Cluster, C — Course Path. → Generated `3` candidate response(s). → Critiqued `3` candidate response(s). → Refinement skipped: support score sufficient. → Selected `A — Specific Job` with total critique score `8.55`.

**Response:**

> Based on your current skills, you appear to be competitive for back-end focused roles, such as a
> Back-End Developer or a Server-Side Engineer. Your proficiency in Python, TypeScript, React, and
> Node.js suggests that you have a strong foundation in web development, particularly with JavaScript
> frameworks. However, keep in mind that no retrieved course clearly addresses the gaps of HTML/CSS,
> Operating Systems, and Technical Communication, which may make it challenging to compete for full-
> stack or frontend-focused roles without additional training or experience.

---
