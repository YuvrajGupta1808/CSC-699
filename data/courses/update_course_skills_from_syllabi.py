"""
Update course skill metadata using the syllabi in ../syllabus as the source.

This script intentionally uses curated mappings derived from the available
syllabi so the resulting skills stay specific, job-relevant, and consistent
across paired undergraduate/graduate offerings.

Run:
  python server/update_course_skills_from_syllabi.py
"""

from __future__ import annotations

import csv
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
COURSES_CSV = REPO_ROOT / "data" / "sfsu_csc_courses_clean_skills.csv"


def skill_string(items: list[tuple[str, int]]) -> str:
    return "[" + ", ".join(f"({name}, {weight})" for name, weight in items) + "]"


UPDATED_SKILLS: dict[str, str] = {
    "CSC 101": skill_string([
        ("Java", 20),
        ("Programming Fundamentals", 18),
        ("Problem Solving", 16),
        ("Algorithms", 14),
        ("Computational Thinking", 12),
        ("Arrays", 10),
        ("Modular Programming", 10),
    ]),
    "CSC 215": skill_string([
        ("Java", 20),
        ("Object-Oriented Programming", 18),
        ("Algorithmic Problem Solving", 16),
        ("Testing and Debugging", 16),
        ("Software Documentation", 15),
        ("Software Development Tools", 15),
    ]),
    "CSC 220": skill_string([
        ("Data Structures", 20),
        ("Java", 16),
        ("Abstract Data Types", 16),
        ("Algorithms", 14),
        ("Recursion", 12),
        ("Sorting and Searching", 12),
        ("Hash Tables", 10),
    ]),
    "CSC 230": skill_string([
        ("Discrete Mathematics", 20),
        ("Logic", 16),
        ("Proof Techniques", 16),
        ("Set Theory", 14),
        ("Graph Theory", 12),
        ("Combinatorics", 12),
        ("Recursion", 10),
    ]),
    "CSC 256": skill_string([
        ("Computer Architecture", 18),
        ("Assembly Language", 18),
        ("Digital Logic", 16),
        ("MIPS", 14),
        ("Memory Hierarchy", 14),
        ("CPU Pipelines", 10),
        ("Interrupt Handling", 10),
    ]),
    "CSC 300GW": skill_string([
        ("Technical Communication", 18),
        ("Professional Ethics", 18),
        ("Privacy", 16),
        ("Cybersecurity", 14),
        ("Software Documentation", 12),
        ("Requirements Analysis", 12),
        ("Presentations", 10),
    ]),
    "CSC 317": skill_string([
        ("JavaScript", 18),
        ("HTML/CSS", 16),
        ("Node.js", 16),
        ("SQL", 14),
        ("Client-Server Architecture", 14),
        ("Git", 12),
        ("Linux/Unix", 10),
    ]),
    "CSC 340": skill_string([
        ("C++", 20),
        ("Object-Oriented Programming", 18),
        ("Algorithms", 16),
        ("Problem Solving", 14),
        ("Time Complexity Analysis", 12),
        ("Unit Testing", 10),
        ("Sorting and Searching", 10),
    ]),
    "CSC 413": skill_string([
        ("Object-Oriented Programming", 18),
        ("Java", 16),
        ("Design Patterns", 16),
        ("Software Design", 14),
        ("Testing and Debugging", 14),
        ("UI Design", 12),
        ("GitHub", 10),
    ]),
    "CSC 510": skill_string([
        ("Algorithms", 20),
        ("Dynamic Programming", 16),
        ("Divide and Conquer", 16),
        ("Greedy Algorithms", 14),
        ("Complexity Analysis", 14),
        ("Backtracking", 10),
        ("Correctness Proofs", 10),
    ]),
    "CSC 600": skill_string([
        ("Programming Languages", 20),
        ("Functional Programming", 16),
        ("Logic Programming", 16),
        ("Object-Oriented Programming", 14),
        ("Procedural Programming", 14),
        ("Language Syntax and Semantics", 10),
        ("Program Performance", 10),
    ]),
    "CSC 620": skill_string([
        ("Natural Language Processing", 20),
        ("Python", 16),
        ("Text Processing", 16),
        ("Language Modeling", 14),
        ("Text Classification", 12),
        ("Vector Semantics", 12),
        ("Neural Language Models", 10),
    ]),
    "CSC 820": skill_string([
        ("Natural Language Processing", 20),
        ("Python", 16),
        ("Text Processing", 16),
        ("Language Modeling", 14),
        ("Text Classification", 12),
        ("Vector Semantics", 12),
        ("Neural Language Models", 10),
    ]),
    "CSC 621": skill_string([
        ("Biomedical Imaging", 18),
        ("Image Processing", 18),
        ("Image Segmentation", 16),
        ("Image Registration", 14),
        ("Image Filtering", 14),
        ("Medical Image Analysis", 10),
        ("Image Visualization", 10),
    ]),
    "CSC 821": skill_string([
        ("Biomedical Imaging", 18),
        ("Image Processing", 18),
        ("Image Segmentation", 16),
        ("Image Registration", 14),
        ("Image Filtering", 14),
        ("Medical Image Analysis", 10),
        ("Image Visualization", 10),
    ]),
    "CSC 630": skill_string([
        ("Computer Graphics", 20),
        ("OpenGL", 16),
        ("GPU Programming", 16),
        ("3D Rendering", 14),
        ("Shading", 12),
        ("Linear Algebra", 12),
        ("Animation", 10),
    ]),
    "CSC 830": skill_string([
        ("Computer Graphics", 20),
        ("OpenGL", 16),
        ("GPU Programming", 16),
        ("3D Rendering", 14),
        ("Shading", 12),
        ("Linear Algebra", 12),
        ("Animation", 10),
    ]),
    "CSC 631": skill_string([
        ("Game Development", 18),
        ("Unity", 18),
        ("Network Programming", 16),
        ("Client-Server Architecture", 14),
        ("Computer Graphics", 12),
        ("Software Engineering", 12),
        ("Integration Testing", 10),
    ]),
    "CSC 831": skill_string([
        ("Game Development", 18),
        ("Unity", 18),
        ("Network Programming", 16),
        ("Client-Server Architecture", 14),
        ("Computer Graphics", 12),
        ("Software Engineering", 12),
        ("Integration Testing", 10),
    ]),
    "CSC 641": skill_string([
        ("Performance Modeling", 18),
        ("Benchmarking", 16),
        ("Queueing Theory", 16),
        ("Simulation", 14),
        ("Capacity Planning", 14),
        ("Performance Tuning", 12),
        ("Workload Analysis", 10),
    ]),
    "CSC 841": skill_string([
        ("Performance Modeling", 18),
        ("Benchmarking", 16),
        ("Queueing Theory", 16),
        ("Simulation", 14),
        ("Capacity Planning", 14),
        ("Performance Tuning", 12),
        ("Workload Analysis", 10),
    ]),
    "CSC 642": skill_string([
        ("Human-Computer Interaction", 18),
        ("User Research", 16),
        ("User-Centered Design", 16),
        ("Prototyping", 14),
        ("Usability Testing", 14),
        ("Personas and User Stories", 12),
        ("Design Evaluation", 10),
    ]),
    "CSC 842": skill_string([
        ("Human-Computer Interaction", 18),
        ("User Research", 16),
        ("User-Centered Design", 16),
        ("Prototyping", 14),
        ("Usability Testing", 14),
        ("Personas and User Stories", 12),
        ("Design Evaluation", 10),
    ]),
    "CSC 645": skill_string([
        ("Computer Networks", 18),
        ("TCP/IP", 16),
        ("Network Programming", 16),
        ("Routing", 14),
        ("Socket Programming", 14),
        ("HTTP", 12),
        ("Network Troubleshooting", 10),
    ]),
    "CSC 647": skill_string([
        ("Quantum Computing", 20),
        ("Quantum Algorithms", 16),
        ("Quantum Circuits", 16),
        ("Qiskit", 14),
        ("Quantum Information", 14),
        ("Quantum Hardware", 10),
        ("Hybrid Quantum-Classical Systems", 10),
    ]),
    "CSC 747": skill_string([
        ("Quantum Computing", 20),
        ("Quantum Algorithms", 16),
        ("Quantum Circuits", 16),
        ("Qiskit", 14),
        ("Quantum Information", 14),
        ("Quantum Hardware", 10),
        ("Hybrid Quantum-Classical Systems", 10),
    ]),
    "CSC 648": skill_string([
        ("Software Engineering", 18),
        ("Agile Development", 16),
        ("Requirements Analysis", 16),
        ("Software Testing", 14),
        ("Project Management", 14),
        ("User-Centered Design", 12),
        ("Cloud Deployment", 10),
    ]),
    "CSC 848": skill_string([
        ("Software Engineering", 18),
        ("Agile Development", 16),
        ("Requirements Analysis", 16),
        ("Software Testing", 14),
        ("Project Management", 14),
        ("User-Centered Design", 12),
        ("Cloud Deployment", 10),
    ]),
    "CSC 652": skill_string([
        ("Cybersecurity", 18),
        ("Cryptography", 18),
        ("Differential Privacy", 18),
        ("Data Privacy", 16),
        ("Privacy-Preserving Data Analysis", 16),
        ("Security Algorithms", 14),
    ]),
    "CSC 852": skill_string([
        ("Cybersecurity", 18),
        ("Cryptography", 18),
        ("Differential Privacy", 18),
        ("Data Privacy", 16),
        ("Privacy-Preserving Data Analysis", 16),
        ("Security Algorithms", 14),
    ]),
    "CSC 656": skill_string([
        ("Computer Architecture", 18),
        ("Instruction Set Design", 16),
        ("Pipelining", 16),
        ("Cache Design", 14),
        ("Memory Systems", 14),
        ("Parallel Processing", 12),
        ("MIPS", 10),
    ]),
    "CSC 659": skill_string([
        ("Explainable AI", 18),
        ("AI Ethics", 18),
        ("Prompt Engineering", 16),
        ("Model Evaluation", 16),
        ("Trustworthy AI", 14),
        ("Retrieval-Augmented Generation", 10),
        ("Fine-Tuning", 8),
    ]),
    "CSC 859": skill_string([
        ("Explainable AI", 18),
        ("AI Ethics", 18),
        ("Prompt Engineering", 16),
        ("Model Evaluation", 16),
        ("Trustworthy AI", 14),
        ("Retrieval-Augmented Generation", 10),
        ("Fine-Tuning", 8),
    ]),
    "CSC 665": skill_string([
        ("Artificial Intelligence", 20),
        ("Search Algorithms", 16),
        ("Knowledge Representation", 16),
        ("Machine Learning", 14),
        ("Game Playing", 12),
        ("Intelligent Agents", 12),
        ("Neural Networks", 10),
    ]),
    "CSC 865": skill_string([
        ("Artificial Intelligence", 20),
        ("Search Algorithms", 16),
        ("Knowledge Representation", 16),
        ("Machine Learning", 14),
        ("Game Playing", 12),
        ("Intelligent Agents", 12),
        ("Neural Networks", 10),
    ]),
    "CSC 667": skill_string([
        ("HTTP APIs", 18),
        ("Node.js", 16),
        ("JavaScript", 16),
        ("HTML/CSS", 14),
        ("PostgreSQL", 14),
        ("Client-Server Architecture", 12),
        ("Express", 10),
    ]),
    "CSC 867": skill_string([
        ("HTTP APIs", 18),
        ("Node.js", 16),
        ("JavaScript", 16),
        ("HTML/CSS", 14),
        ("PostgreSQL", 14),
        ("Client-Server Architecture", 12),
        ("Express", 10),
    ]),
    "CSC 671": skill_string([
        ("Deep Learning", 20),
        ("PyTorch", 16),
        ("Neural Networks", 16),
        ("Convolutional Neural Networks", 14),
        ("Transformers", 14),
        ("Recurrent Neural Networks", 10),
        ("Model Training", 10),
    ]),
    "CSC 871": skill_string([
        ("Deep Learning", 20),
        ("PyTorch", 16),
        ("Neural Networks", 16),
        ("Convolutional Neural Networks", 14),
        ("Transformers", 14),
        ("Recurrent Neural Networks", 10),
        ("Model Training", 10),
    ]),
    "CSC 676": skill_string([
        ("Soft Computing", 18),
        ("Fuzzy Logic", 18),
        ("Decision Support Systems", 16),
        ("Computational Intelligence", 16),
        ("Approximate Reasoning", 12),
        ("Information Fusion", 10),
        ("Neural Networks", 10),
    ]),
    "CSC 876": skill_string([
        ("Soft Computing", 18),
        ("Fuzzy Logic", 18),
        ("Decision Support Systems", 16),
        ("Computational Intelligence", 16),
        ("Approximate Reasoning", 12),
        ("Information Fusion", 10),
        ("Neural Networks", 10),
    ]),
    "CSC 746": skill_string([
        ("High-Performance Computing", 18),
        ("Parallel Programming", 16),
        ("MPI", 16),
        ("Shared Memory Programming", 14),
        ("GPU Computing", 14),
        ("Clusters", 12),
        ("Cloud Computing", 10),
    ]),
    "CSC 810": skill_string([
        ("Advanced Algorithms", 20),
        ("Graph Algorithms", 16),
        ("NP-Completeness", 16),
        ("Approximation Algorithms", 14),
        ("Randomized Algorithms", 14),
        ("Lower Bounds", 10),
        ("Correctness Proofs", 10),
    ]),
    "CSC 845": skill_string([
        ("Advanced Computer Networks", 18),
        ("Wireless Networks", 16),
        ("Mobile Networks", 16),
        ("Software-Defined Networking", 14),
        ("Network Security", 14),
        ("Multimedia Networking", 12),
        ("Network Protocols", 10),
    ]),
    "CSC 849": skill_string([
        ("Search Engines", 20),
        ("Information Retrieval", 18),
        ("Text Processing", 16),
        ("Indexing and Compression", 14),
        ("Ranking Models", 12),
        ("Web Search", 10),
        ("Text Classification", 10),
    ]),
    "CSC 872": skill_string([
        ("Pattern Recognition", 18),
        ("Machine Learning", 16),
        ("Statistical Modeling", 16),
        ("Bayesian Methods", 14),
        ("Classification", 12),
        ("Dimensionality Reduction", 12),
        ("Neural Networks", 12),
    ]),
}


NEW_ROWS = [
    {
        "course_code": "CSC 849",
        "title": "Search Engines",
        "description": (
            "Fundamental concepts of text processing and information retrieval, "
            "including indexing, ranking, web search, and applications of search "
            "technology through research-oriented projects."
        ),
        "skills": UPDATED_SKILLS["CSC 849"],
    }
]


def sort_key(row: dict[str, str]) -> tuple[int, str]:
    code = row["course_code"]
    digits = "".join(ch for ch in code if ch.isdigit())
    return (int(digits) if digits else 9999, code)


def main() -> None:
    with COURSES_CSV.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    by_code = {row["course_code"]: row for row in rows}

    for code, skills in UPDATED_SKILLS.items():
        if code in by_code:
            by_code[code]["skills"] = skills

    for row in NEW_ROWS:
        if row["course_code"] not in by_code:
            rows.append(row)

    rows = sorted(rows, key=sort_key)

    with COURSES_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["course_code", "title", "description", "skills"],
            quoting=csv.QUOTE_ALL,
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Updated {len(UPDATED_SKILLS)} course rows from syllabus-derived mappings.")
    print("Added:", ", ".join(row["course_code"] for row in NEW_ROWS))


if __name__ == "__main__":
    main()
