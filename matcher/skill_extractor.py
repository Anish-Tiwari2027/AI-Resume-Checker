# matcher/skill_extractor.py

def load_skills(skill_file):
    """
    Load skills from a text file.
    Each skill should be on a new line.
    """
    skills = []
    with open(skill_file, "r", encoding="utf-8") as f:
        for line in f:
            skill = line.strip().lower()
            if skill:
                skills.append(skill)
    return skills


# Canonical skill name -> possible variations in resumes
SKILL_ALIASES = {
    "python": ["python"],
    "java": ["java"],
    "c++": ["c++", "cpp"],
    "c": ["c language", "c"],
    "javascript": ["javascript", "js"],
    "node.js": ["node.js", "nodejs"],
    "express.js": ["express.js", "express"],
    "react": ["react", "reactjs", "react.js"],
    "sql": ["sql", "mysql", "postgresql"],
    "mongodb": ["mongodb", "mongo"],
    "firebase": ["firebase"],
    "git": ["git"],
    "github": ["github", "git hub"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "matplotlib": ["matplotlib"],
    "flask": ["flask"],
    "fastapi": ["fastapi"],
    "streamlit": ["streamlit"],
    "docker": ["docker"],
    "linux": ["linux"],
    "solidity": ["solidity"],
    "hardhat": ["hardhat"],
    "ganache": ["ganache"],
    "metamask": ["metamask"]
}


def extract_skills(resume_text, skills_list):
    """
    Extract skills from resume text using:
    1. Exact matching from skills list
    2. Alias-based normalization
    """
    resume_text = resume_text.lower()
    found_skills = set()

    # Exact match from skills list
    for skill in skills_list:
        if skill in resume_text:
            found_skills.add(skill)

    # Alias-based matching
    for canonical_skill, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            if alias in resume_text:
                found_skills.add(canonical_skill)
                break  # stop checking other aliases for this skill

    return sorted(found_skills)
