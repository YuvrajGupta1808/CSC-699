# Model Comparison Report

**Run date:** 2026-05-12 01:35
**RAGAS judge:** OpenAI gpt-4o-mini  
**Advisor pipeline:** 100% local (Ollama + Weaviate)  
**Models compared:** `llama3.2`, `deepseek-r1:1.5b`
**Questions:** 10

---

## Summary

| Model | Faithfulness ↑ | Resp. Relevancy ↑ | Ctx Precision | RAGAS Avg ↑ | Internal /10 | Avg Time |
|---|---|---|---|---|---|---|
| `llama3.2` | 🟡0.78 | 🔴0.55 | 0.86 | **—** | 7.9 | 64.3s |
| `deepseek-r1:1.5b` | 🟡0.68 | 🔴0.52 | 0.93 | **—** | 8.1 | 64.1s |

> **Faithfulness** and **Response Relevancy** are the primary model comparison metrics.  
> **Context Precision** reflects retrieval quality — slight variance per model is expected.

---

## Per-Question Breakdown

### GQ-01 — Specific Job Fit (Alex Chen)
**Query:** _Am I a good fit for the Junior Software Engineer role at Leidos?_

| Model | Faith | Rel | CtxP | RAGAS | Internal | Time |
|---|---|---|---|---|---|---|
| `llama3.2` | 🟡0.62 | 🔴0.00 | 0.50 | **0.38** | 7.8 | 55.5s |
| `deepseek-r1:1.5b` | 🟡0.62 | 🔴0.00 | 0.50 | **0.38** | 5.8 | 51.1s |

<details><summary><code>llama3.2</code></summary>

> Based on the retrieved evidence, Applied Computer Vision Engineer (TS/SCI) at Vantor is the clearest fit in this view. You already cover: Python. Your main gaps are: Computer Vision, Deep Learning, Geospatial Intelligence, Data Engineering, Docker, Kubernetes, Linux, YOLO, Image Processing, Generative AI, Cloud Computing, Technical Writing, Data Science, Remote Sensing. No retrieved courses clearly address these gaps for Applied Computer Vision Engineer (TS/SCI): Computer Vision, Deep Learning, Geospatial Intelligence, Data Engineering, Docker, Kubernetes, Linux, YOLO, Image Processing, Generative AI, Cloud Computing, Technical Writing, Data Science, Remote Sensing. I cannot make a supported course recommendation for those gaps from the retrieved courses, so the reliable next step is to target those skill areas directly and retrieve a broader matching course set.

</details>

<details><summary><code>deepseek-r1:1.5b</code></summary>

> Based on the retrieved evidence, Applied Computer Vision Engineer (TS/SCI) at Vantor is the clearest fit in this view. You already cover: Python. Your main gaps are: Computer Vision, Deep Learning, Geospatial Intelligence, Data Engineering, Docker, Kubernetes, Linux, YOLO, Image Processing, Generative AI, Cloud Computing, Technical Writing, Data Science, Remote Sensing. No retrieved courses clearly address these gaps for Applied Computer Vision Engineer (TS/SCI): Computer Vision, Deep Learning, Geospatial Intelligence, Data Engineering, Docker, Kubernetes, Linux, YOLO, Image Processing, Generative AI, Cloud Computing, Technical Writing, Data Science, Remote Sensing. I cannot make a supported course recommendation for those gaps from the retrieved courses, so the reliable next step is to target those skill areas directly and retrieve a broader matching course set.

</details>

---

### GoQ-04 — Skill Gap Analysis (Alex Chen)
**Query:** _What specific skills am I missing to qualify for a full stack engineering role?_

| Model | Faith | Rel | CtxP | RAGAS | Internal | Time |
|---|---|---|---|---|---|---|
| `llama3.2` | 🟢1.00 | 🟢0.92 | 1.00 | **0.97** | 8.0 | 51.5s |
| `deepseek-r1:1.5b` | — | 🟢0.93 | 1.00 | **0.97** | 7.0 | 74.1s |

<details><summary><code>llama3.2</code></summary>

> Based on the relevant job posting and course, it appears that you are missing the following skills:
> 
> * TypeScript
> * React
> * Angular
> * HTML/CSS
> * PostgreSQL
> * Operating Systems
> * Technical Communication
> 
> Additionally, having experience with these technologies will likely be beneficial for a full stack engineering role.
> 
> However, considering your completed courses, I recommend taking CSC 694: Cooperative Education: Computer Science to address the gap in Technical Communication. This course addresses one of the gaps you have in the job posting.
> 
> If you'd like to explore other options, you could also consider taking additional courses that focus on these missing skills, such as learning more about front-end development with React and Angular, or gaining experience with database management using PostgreSQL.

</details>

<details><summary><code>deepseek-r1:1.5b</code></summary>

> To qualify for a full stack engineering role, Alex Chen needs to develop specific technical skills. Here's a structured plan based on the identified gaps:
> 
> ### Required Skills for a Full Stack Engineering Role:
> 1. **HTML/CSS/UX Development**: Strong foundational skills in creating responsive and user-friendly interfaces.
> 2. **React/Django/PHP/Node.js/Python/TypeScript**: Proficiency in front-end development using key frameworks and languages.
> 3. **SQL/Django/Python/Agile/Cloud Computing (AWS)/ML/NLP**: Expertise in database management, cloud technologies, and machine learning integration.
> 4. **Web Development with PHP/PHP-Numbers**: Strong background in backend systems and tools for web operations.
> 5. **Domain Knowledge in AI, NLP, etc.**: Specialization in areas relevant to current engineering roles.
> 
> ### Courses Alex Should Complete:
> 1. **Web Development with PHP/PHP-Numbers** (CSC 220

</details>

---

### GQ-06 — Skill Gap Analysis (Sam Patel)
**Query:** _What is the single most important skill I should learn next to become more employable?_

| Model | Faith | Rel | CtxP | RAGAS | Internal | Time |
|---|---|---|---|---|---|---|
| `llama3.2` | 🟢0.88 | 🟡0.69 | 1.00 | **0.85** | 9.0 | 48.3s |
| `deepseek-r1:1.5b` | 🟢1.00 | 🟡0.69 | 1.00 | **0.90** | 8.0 | 62.4s |

<details><summary><code>llama3.2</code></summary>

> Based on the provided information, it appears that learning Python would be a crucial step in addressing your gaps. You are currently proficient in Java, but none of the relevant job postings require Java as a required skill. However, all of them list Python as a required or desirable skill.
> 
> Among the courses you've completed and retrieved, CSC 411: Intermediate Machine Learning for Interdisciplinary Data Scientists and CSC 871: Deep Learning both teach Python. Additionally, CSC 306: An Interdisciplinary Approach to Computer Programming also covers Python. 
> 
> Learning Python would address your gaps in Python and provide a valuable skillset that aligns with the requirements of the job postings you've seen.

</details>

<details><summary><code>deepseek-r1:1.5b</code></summary>

> To address the skill gaps highlighted in the job postings, your next step should focus on expanding your knowledge of deep learning frameworks and improving your programming skills to apply them more effectively. Additionally, you may want to strengthen your computational thinking by taking courses that cover algorithms and data structures.
> 
> 1. **Deep Learning Frameworks**: Deepen your understanding of deep learning frameworks beyond the scope covered in Csc 871 (Deep Learning). If available, learn how to use TensorFlow or Keras for building more complex models.
> 2. **Algorithm and Data Structure Refresher**: Enhance your programming skills by taking a refresher course on algorithm design and data structures, which will be useful in both the Product Engineer and AI Engineer roles.
> 3. **Reinforcement of Java Skills**: If applicable, take a Java refresher to solidify your knowledge of more 

</details>

---

### GQ-07 — Course Recommendation (Alex Chen)
**Query:** _Which courses should I take to become competitive for web development jobs?_

| Model | Faith | Rel | CtxP | RAGAS | Internal | Time |
|---|---|---|---|---|---|---|
| `llama3.2` | 🟡0.73 | 🟢0.89 | 0.50 | **0.71** | 7.8 | 65.6s |
| `deepseek-r1:1.5b` | 🔴0.57 | 🟢0.91 | 0.83 | **0.77** | 8.6 | 72.7s |

<details><summary><code>llama3.2</code></summary>

> To be competitive for web development jobs, I recommend taking CSC 317: Introduction to Web Software Development and CSC 867/667: Internet Application Design and Development.
> 
> These two courses cover essential topics in web software development, including client-side and server-side programming, database integration, RESTful APIs, form validation and sanitization, session management and cookies, and cloud deployment. Additionally, they introduce popular front-end frameworks (HTML5/CSS3, JavaScript, React.js) and back-end technologies (Node.js, Express.js).
> 
> CSC 317 provides a solid foundation in web development basics, while CSC 867/667 offers more advanced topics, including RESTful API design, database ORM, and agile development. Taking both courses will give you a comprehensive understanding of the web development field.
> 
> Note that I'm not recommending CSC 307: An Interdisciplinary App

</details>

<details><summary><code>deepseek-r1:1.5b</code></summary>

> Alex Chen should take both **CSC 667** and **CSC 317** for a well-rounded approach to web development.
> 
> - **CSC 667**: Teaches essential JavaScript, Node.js, React, Express, PostgreSQL, and web security. This course will enhance his skills in frontend components, server-side technologies, databases, and testing.
>   
> - **CSC 317**: Provides a comprehensive foundation in HTML/CSS, Node.js, Express, SQL/MySQL, UNIX/Linux, RESTful APIs, form validation, cookies, security, and database connectivity. This course will cover the broader scope of front-end and back-end development.
> 
> These courses together offer foundational knowledge in both front-end and back-end development, preparing Alex for competitive web development roles.

</details>

---

### GQ-10 — Career Readiness (Alex Chen)
**Query:** _I'm graduating in 6 months. Give me an honest assessment of my job market readiness._

| Model | Faith | Rel | CtxP | RAGAS | Internal | Time |
|---|---|---|---|---|---|---|
| `llama3.2` | — | 🔴0.00 | 1.00 | **0.50** | 6.8 | 74.9s |
| `deepseek-r1:1.5b` | 🟡0.67 | 🟡0.61 | 1.00 | **0.76** | 7.6 | 54.6s |

<details><summary><code>llama3.2</code></summary>

> Based on the information provided, I'd say you're not entirely ready for the job market just yet.
> 
> You've completed some relevant courses, such as CSC 101, CSC 220, and CSC 315, but there are significant gaps in your skill set that need to be addressed. Specifically, you lack experience with:
> 
> 1. Automation
> 2. Kubernetes
> 3. Azure
> 4. AKS (Azure Kubernetes Service)
> 5. Terraform
> 6. Chef
> 7. Docker
> 8. Prometheus
> 9. Grafana
> 10. ELK/EFK
> 11. CI/CD
> 12. Go
> 13. Bash
> 14. PowerShell
> 
> Additionally, the job posting for the Senior Site Reliability Engineer at iManage highlights the importance of a broader range of skills, including:
> 
> * Cloud and distributed computing concepts (not directly addressed in your current courses)
> * Serverless Computing
> * MapReduce
> * NoSQL Databases
> * Apache Kafka
> * Distributed Consensus
> * CAP Theorem and Consistency Models
> * Infrastructure as Code
> 
> While you have experience w

</details>

<details><summary><code>deepseek-r1:1.5b</code></summary>

> **Alex Chen Job Market Assessment**
> 
> **Current Skills and Courses:**
> - **Python, Java, Data Structures, Algorithms, Object-Oriented Programming**
> - Completed Courses:
>   - CSC 847: Cloud and Distributed Computing (Teaches AWS/GCP/Azure Docker/Kubernetes, etc.)
> 
> **Job Requirements:**
> - Automation, Kubernetes, Azure, AKS, Terraform, Chef, Docker, Prometheus, Grafana, ELK/EFK, CI/CD, Go, Bash, PowerShell.
> 
> **Gap Analysis:**
> 
> Alex's skills cover most job requirements except for specific cloud technologies beyond the scope of their current course. Specifically:
> - **Gap in Job Postings:** Kubernetes and related cloud platforms (e.g., AWS, Azure) are missing.
> - **Additional Skills Needed:** Advanced roles may require expertise in these cloud technologies.
> 
> **Recommendations:**
> 1. **CSC 847** is a strong candidate for the gap in **Kubernetes**, providing foundational knowledge essential for iMana

</details>

---

### GQ-13 — Job Comparison (Alex Chen)
**Query:** _Between a software engineering role at Microsoft and one at a startup like Giga, which is a better fit for where I am now?_

| Model | Faith | Rel | CtxP | RAGAS | Internal | Time |
|---|---|---|---|---|---|---|
| `llama3.2` | 🔴0.50 | 🟡0.67 | 0.58 | **0.59** | 7.2 | 61.2s |
| `deepseek-r1:1.5b` | 🔴0.40 | 🟡0.62 | 1.00 | **0.67** | 8.6 | 76.3s |

<details><summary><code>llama3.2</code></summary>

> Based on the job posting excerpt for Software Engineer, University Grad at Glean, it appears that both Microsoft and Giga require additional skills beyond what you've already completed. 
> 
> Glean requires JavaScript, Natural Language Processing, Distributed Systems, in addition to the skills you've covered. It seems more aligned with your current skill set.
> 
> Microsoft's requirements don't have any gaps directly addressed by the courses you've completed (CSC 101, CSC 220, CSC 315, and CSC 340). However, CSC 867: Internet Application Design and Development does cover JavaScript, which addresses one of Glean's gap requirements.

</details>

<details><summary><code>deepseek-r1:1.5b</code></summary>

> Based on the information provided, the conclusion is that Giga offers a job opportunity focused on web software development skills, which aligns with the courses taken by the student. While Microsoft also provides opportunities in various roles, Giga's emphasis on hands-on experience and specific technical competencies makes it a suitable fit for candidates comfortable with Python, Java, JavaScript, RESTful APIs, API Testing, Session Management, Cloud Deployment, Agile Development, and Technical Documentation.
> 
> **Recommendation:** If confident in the specific courses and having some gaps covered, Giga may offer a fitting job opportunity due to its focus on web software development skills.

</details>

---

### GQ-15 — Action Plan (Alex Chen)
**Query:** _What are the top 3 most impactful things I can do this semester to improve my job prospects?_

| Model | Faith | Rel | CtxP | RAGAS | Internal | Time |
|---|---|---|---|---|---|---|
| `llama3.2` | 🟢0.92 | 🟡0.78 | 1.00 | **0.90** | 9.2 | 80.0s |
| `deepseek-r1:1.5b` | 🟡0.70 | 🟡0.62 | 1.00 | **0.77** | 9.2 | 66.6s |

<details><summary><code>llama3.2</code></summary>

> Based on your current skills and the gaps identified from the relevant job postings, I recommend the following top 3 most impactful things you can do this semester to improve your job prospects:
> 
> 1. **Take CSC 847: Cloud and Distributed Computing: Concepts and Applications**. This course addresses several key gaps in your skillset, including Kubernetes, NoSQL Databases, and Infrastructure as Code. By taking this course, you'll gain a deeper understanding of cloud computing concepts and how to apply them in a real-world setting.
> 2. **Take CSC 317: Introduction to Web Software Development** or **CSC 667/867: Internet Application Design and Development**, whichever is available. These courses cover essential skills for web development, including JavaScript, Node.js, RESTful APIs, and database management. By taking one of these courses, you'll gain hands-on experience with modern web technol

</details>

<details><summary><code>deepseek-r1:1.5b</code></summary>

> Based on your profile and the job postings, I recommend completing the following CS-related courses that align with the technical skills required for many of the positions listed:
> 
> 1. **CSC 317: Introduction to Web Software Development**  
>    This course focuses on building modern web applications using JavaScript, HTML5/CSS3, React.js, and Express.js, which are essential for roles requiring web-based solutions.
> 
> 2. **CSC 667/867: Internet Application Design and Development**  
>    These advanced courses cover topics such as RESTful API design, WebSockets, JWT and OAuth2, which are critical for roles that require modern application architectures.
> 
> 3. **CSC 867: Internet Application Design and Development**  
>    This course delves deeper into advanced technologies like database ORM, API testing, session management, and cloud deployment, preparing you for roles in mission-critical environme

</details>

---

### GQ-17 — Domain Pivot (Alex Chen)
**Query:** _I want to pivot into data science. What's the gap between where I am and data science jobs?_

| Model | Faith | Rel | CtxP | RAGAS | Internal | Time |
|---|---|---|---|---|---|---|
| `llama3.2` | 🟢1.00 | 🟡0.60 | 1.00 | **0.87** | 7.6 | 79.2s |
| `deepseek-r1:1.5b` | 🔴0.56 | 🟡0.79 | 1.00 | **0.78** | 10.0 | 69.6s |

<details><summary><code>llama3.2</code></summary>

> Based on the job posting for Clinical Data Scientist at RedSail Technologies, it seems that you have a good foundation in programming languages like Python, but there are several gaps in your skills.
> 
> You're missing SQL, PowerBI, Tableau, Go, Data Visualization, Statistical Analysis, Data Cleaning, Exploratory Data Analysis, Feature Engineering, HIPAA Compliance, and Data Collection. 
> 
> The CSC 311: Data Structures for Data Science Application Development course seems like a good starting point to address some of these gaps, particularly in Exploratory Data Analysis.
> 
> Additionally, the CSC 869: Data Mining course covers many of the other missing skills, such as Feature Engineering and Data Visualization.

</details>

<details><summary><code>deepseek-r1:1.5b</code></summary>

> Alex Chen is transitioning into data science and needs courses that address his skill gaps. Here's a structured summary of the required courses:
> 
> 1. **RedSails Technologies (Clinical Data Scientist Role)**
>    - **Gaps**: ETL/ELT, Data Modeling, SQL, Cloud Platforms, CI/CD, etc.
>    - **Courses Needed**:
>      - CSC 874: Big Data Analysis covers ETL/ELT and cloud platforms.
> 
> 2. **Lakeview Loan Servicing (Data Engineer/Mortgage Servicing Role)**
>    - **Gaps**: ETL/ELT, Data Modeling, Cloud Platforms (AWS), CI/CD, etc.
>    - **Courses Needed**:
>      - CSC 874: Big Data Analysis covers ETL/ELT and cloud platforms.
> 
> 3. **Network Designs Inc. (Data Engineer/Integration Specialist #1768469)**
>    - **Gaps**: ETL Tools, APIs, Microservices, Data Modeling, Data Governance, etc.
>    - **Courses Needed**:
>      - CSC 869: Data Mining covers feature engineering and data visualization.
> 
> Each course address

</details>

---

### GQ-22 — Strong Fit (Marcus Webb)
**Query:** _Am I ready for a cloud or DevOps engineering role?_

| Model | Faith | Rel | CtxP | RAGAS | Internal | Time |
|---|---|---|---|---|---|---|
| `llama3.2` | 🟢0.83 | 🔴0.00 | 1.00 | **0.61** | 7.2 | 79.9s |
| `deepseek-r1:1.5b` | 🟢0.83 | 🔴0.00 | 1.00 | **0.61** | 7.7 | 54.8s |

<details><summary><code>llama3.2</code></summary>

> Based on your current skills and completed courses, it appears that you have a solid foundation in many areas relevant to cloud engineering. You've taken courses like CSC 647: Cloud Security and Compliance (not directly listed, but likely covered similar topics as CSC 746), which suggests some knowledge of security considerations in the cloud.
> 
> However, there are still some gaps in your skill set and expertise that you'll need to address for a role in either cloud engineering or DevOps. Specifically:
> 
> 1. Azure: While you've taken courses on AWS and have experience with other cloud providers (Docker, Kubernetes, Terraform), it seems you lack hands-on experience with Microsoft Azure.
> 2. DevSecOps: You've covered some aspects of DevOps (CI/CD, Infrastructure as Code) but not specifically the security component.
> 3. Virtualization: Although you have a course on virtualization in CSC 847, revi

</details>

<details><summary><code>deepseek-r1:1.5b</code></summary>

> Marcus Webb's preparation for a cloud engineering role at Leidos is strong in foundational topics like infrastructure as code, containerization, microservices architecture, and security. However, he may need further training or courses on Azure, DevSecOps, Windows Server, and Identity Management to fully prepare for the role.
> 
> **Recommendation:**
> - Marcus should complete additional courses on Azure technology and DevSecOps principles.
> - He might also benefit from courses that cover Windows server management and identity management systems.

</details>

---

### GQ-25 — Cross-Disciplinary (Priya Sharma)
**Query:** _Which courses would strengthen my data science skills specifically for biomedical research?_

| Model | Faith | Rel | CtxP | RAGAS | Internal | Time |
|---|---|---|---|---|---|---|
| `llama3.2` | 🔴0.55 | 🟢0.97 | 1.00 | **0.84** | 8.1 | 47.4s |
| `deepseek-r1:1.5b` | 🟡0.75 | 🔴0.00 | 1.00 | **0.58** | 8.2 | 59.2s |

<details><summary><code>llama3.2</code></summary>

> Based on your current skillset and completed courses, I recommend the following courses to strengthen your data science skills specifically for biomedical research:
> 
> 1. CSC 408: Machine Learning and Data Science for Personalized Medicine
> 	* This course covers machine learning and data science concepts applied to genomic datasets, which is highly relevant to biomedical research.
> 2. CSC 821 (or CSC 621): Biomedical Imaging and Analysis
> 	* Although there's a minor discrepancy in course titles, both versions cover medical image processing, analysis, and visualization, which are essential skills for working with biomedical data.
> 
> These courses will help you develop the necessary skills in machine learning, data science, and biomedical imaging to tackle common challenges in biomedical research.

</details>

<details><summary><code>deepseek-r1:1.5b</code></summary>

> Based on the retrieved evidence, Bioinformatics Scientist at Axle is the clearest fit in this view. You already cover: Bioinformatics, Statistical Modeling, Python, R, Genomics, Data analysis. Your main gaps are: NGS analysis, C++, Bash, Docker, Snakemake, Nextflow, Transcriptomics, Proteomics, HPC infrastructure, Experimental design. No retrieved courses clearly address these gaps for Bioinformatics Scientist: NGS analysis, C++, Bash, Docker, Snakemake, Nextflow, Transcriptomics, Proteomics, HPC infrastructure, Experimental design. I cannot make a supported course recommendation for those gaps from the retrieved courses, so the reliable next step is to target those skill areas directly and retrieve a broader matching course set.

</details>

---

## Key Findings

- **Fastest model:** `deepseek-r1:1.5b`
- **Slowest model:** `llama3.2`
