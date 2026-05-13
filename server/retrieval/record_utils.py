def first_present(row: dict, *keys: str):
    for key in keys:
        if key in row and row.get(key) is not None:
            return row.get(key)
    return None


def job_skills_value(row: dict) -> list:
    return first_present(row, "skills_jobs", "skills_jobs_json") or []


def course_skills_value(row: dict) -> list:
    return first_present(row, "skills_courses", "skills_courses_json") or []


def student_skill_profile_value(row: dict) -> list:
    return first_present(row, "skill_profile", "skill_profile_json") or []


def student_completed_courses_value(row: dict) -> list:
    return first_present(row, "completed_courses", "completed_courses_json") or []


def student_last_recommendations_value(row: dict):
    return first_present(row, "last_recommendations", "last_recommendations_json")
