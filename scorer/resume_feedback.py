import re


def generate_resume_feedback(
    resume_text,
    resume_skills,
    jd_skills,
    skill_score,
    tfidf_score
):
    feedback = []

    # 1. Skill gap feedback
    missing_skills = set(jd_skills) - set(resume_skills)
    if missing_skills:
        for skill in missing_skills:
            feedback.append(
                f"Consider adding or highlighting experience with '{skill}'."
            )
    else:
        feedback.append(
            "All required skills from the job description are present."
        )

    # 2. Low semantic similarity feedback
    if tfidf_score < 20:
        feedback.append(
            "Resume wording is not closely aligned with the job description. "
            "Consider tailoring your resume language to match the JD."
        )

    # 3. Skill balance feedback
    if skill_score < 50:
        feedback.append(
            "Low overall skill match. Resume may not be suitable for this role."
        )
    elif skill_score >= 80:
        feedback.append(
            "Strong skill match for the given job role."
        )

    # 4. Resume quality checks
    if "project" not in resume_text:
        feedback.append(
            "No projects detected. Adding relevant projects can significantly improve the resume."
        )

    if not re.search(r"\d+%", resume_text):
        feedback.append(
            "No measurable metrics found (e.g., accuracy %, improvement %). "
            "Adding metrics can strengthen impact."
        )

    if "machine learning" in jd_skills and "machine learning" not in resume_skills:
        feedback.append(
            "Job requires Machine Learning, but it is not clearly highlighted in the resume."
        )

    return feedback
