from parser.resume_parser import extract_text_from_pdf
from matcher.skill_extractor import load_skills, extract_skills
from matcher.jd_parser import extract_jd_skills
from scorer.score_calculator import calculate_match_score
from scorer.tfidf_similarity import compute_tfidf_similarity

resume_text = extract_text_from_pdf("sample_resume.pdf")

job_description = """
Looking for an AI intern with strong Python, Machine Learning,
scikit-learn, SQL, and FastAPI experience.
"""

skills_list = load_skills("data/skills_list.txt")

resume_skills = extract_skills(resume_text, skills_list)
jd_skills = extract_jd_skills(job_description, skills_list)

skill_score, matched, missing = calculate_match_score(
    resume_skills, jd_skills
)

tfidf_score = compute_tfidf_similarity(resume_text, job_description)

# Weighted final score
final_score = round((0.6 * skill_score) + (0.4 * tfidf_score), 2)

print("\nResume Skills:", resume_skills)
print("JD Skills:", jd_skills)
print("\nSkill Match Score:", skill_score, "%")
print("TF-IDF Similarity Score:", tfidf_score, "%")
print("FINAL SCORE:", final_score, "%")
print("\nMatched Skills:", matched)
print("Missing Skills:", missing)

from scorer.resume_feedback import generate_resume_feedback

feedback = generate_resume_feedback(
    resume_text,
    resume_skills,
    jd_skills,
    skill_score,
    tfidf_score
)

print("\nResume Feedback:")
for item in feedback:
    print("-", item)
