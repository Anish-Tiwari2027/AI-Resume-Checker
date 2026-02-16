def extract_jd_skills(jd_text, skills_list):
    jd_text = jd_text.lower()
    jd_skills = set()

    for skill in skills_list:
        if skill in jd_text:
            jd_skills.add(skill)

    return list(jd_skills)
