import streamlit as st
import tempfile
import base64

from parser.resume_parser import extract_text_from_pdf
from matcher.skill_extractor import load_skills, extract_skills
from matcher.jd_parser import extract_jd_skills
from scorer.score_calculator import calculate_match_score
from scorer.tfidf_similarity import compute_tfidf_similarity
from scorer.resume_feedback import generate_resume_feedback


# Page configuration
st.set_page_config(
    page_title="AI Resume Checker",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* App background with subtle gradient */
    .stApp {
        background: linear-gradient(180deg, #0A0E1A 0%, #0F172A 100%);
        color: #F1F5F9;
    }
    
    .main {
        background: transparent;
    }
    
    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    
    /* Header with glow effect */
    .header-container {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        padding: 3.5rem 2.5rem;
        border-radius: 24px;
        margin-bottom: 2.5rem;
        text-align: center;
        box-shadow: 0 20px 60px rgba(0,0,0,0.7), 0 0 80px rgba(56,189,248,0.08);
        border: 1px solid rgba(56,189,248,0.15);
    }
    
    .header-title {
        color: #FFFFFF;
        font-size: 3.5rem;
        font-weight: 900;
        letter-spacing: -0.02em;
        text-shadow: 0 4px 20px rgba(56,189,248,0.3);
        margin-bottom: 0.5rem;
    }
    
    .header-subtitle {
        color: #CBD5E1;
        font-size: 1.15rem;
        font-weight: 500;
        letter-spacing: 0.01em;
    }
    
    /* Enhanced cards with borders */
    .upload-card,
    .results-section,
    .metric-card,
    .instruction-card {
        background: linear-gradient(135deg, #1E293B 0%, #151E2E 100%);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(56,189,248,0.2);
        box-shadow: 0 10px 40px rgba(0,0,0,0.6);
        transition: all 0.3s ease;
    }
    
    .upload-card:hover,
    .results-section:hover,
    .metric-card:hover,
    .instruction-card:hover {
        border-color: rgba(56,189,248,0.4);
        box-shadow: 0 15px 50px rgba(0,0,0,0.7), 0 0 40px rgba(56,189,248,0.1);
    }
    
    .card-title,
    .section-title {
        color: #F8FAFC;
        font-weight: 800;
        font-size: 1.5rem;
        margin-bottom: 1rem;
        letter-spacing: -0.01em;
    }
    
    /* Enhanced inputs */
    .stFileUploader,
    .stTextArea textarea,
    .stTextInput input {
        background: #0A0E1A !important;
        border: 2px solid #334155 !important;
        color: #F1F5F9 !important;
        border-radius: 14px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea textarea::placeholder,
    .stTextInput input::placeholder {
        color: #64748B !important;
    }
    
    .stTextArea textarea:focus,
    .stTextInput input:focus {
        border-color: #38BDF8 !important;
        box-shadow: 0 0 0 4px rgba(56,189,248,0.15) !important;
        background: #0F172A !important;
    }
    
    /* Premium button design */
    .stButton button {
        background: linear-gradient(135deg, #0EA5E9 0%, #38BDF8 50%, #0EA5E9 100%) !important;
        background-size: 200% 100% !important;
        color: #020617 !important;
        font-weight: 800 !important;
        border-radius: 14px !important;
        padding: 1rem 2.5rem !important;
        border: none !important;
        box-shadow: 0 10px 30px rgba(14,165,233,0.5) !important;
        transition: all 0.4s ease !important;
        letter-spacing: 0.02em !important;
        text-transform: uppercase !important;
        font-size: 0.9rem !important;
    }
    
    .stButton button:hover {
        background-position: 100% 0 !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 40px rgba(14,165,233,0.7) !important;
    }
    
    .stButton button:active {
        transform: translateY(-1px) !important;
    }
    
    /* Glowing metrics */
    [data-testid="stMetricValue"] {
        color: #38BDF8 !important;
        font-size: 2.8rem !important;
        font-weight: 900 !important;
        text-shadow: 0 0 20px rgba(56,189,248,0.5) !important;
    }
    
    .stMetric label {
        color: #94A3B8 !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        font-size: 0.85rem !important;
    }
    
    /* Enhanced skill tags */
    .skill-tag {
        background: linear-gradient(135deg, #064E3B 0%, #065F46 100%);
        color: #D1FAE5;
        border: 2px solid #10B981;
        border-radius: 12px;
        padding: 0.5rem 1.1rem;
        margin: 0.4rem;
        font-weight: 700;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(16,185,129,0.3);
        transition: all 0.3s ease;
    }
    
    .skill-tag:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(16,185,129,0.5);
    }
    
    .missing-skill-tag {
        background: linear-gradient(135deg, #7F1D1D 0%, #991B1B 100%);
        color: #FEE2E2;
        border: 2px solid #EF4444;
        border-radius: 12px;
        padding: 0.5rem 1.1rem;
        margin: 0.4rem;
        font-weight: 700;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(239,68,68,0.3);
        transition: all 0.3s ease;
    }
    
    .missing-skill-tag:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(239,68,68,0.5);
    }
    
    /* Enhanced feedback items */
    .feedback-item {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        border-left: 5px solid #38BDF8;
        color: #F1F5F9;
        border-radius: 12px;
        padding: 1.3rem 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        transition: all 0.3s ease;
    }
    
    .feedback-item:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 20px rgba(56,189,248,0.3);
    }
    
    /* Modern alerts */
    .alert-success {
        background: linear-gradient(135deg, #022C22 0%, #064E3B 100%);
        color: #D1FAE5;
        border-left: 5px solid #10B981;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 4px 15px rgba(16,185,129,0.2);
    }
    
    .alert-info {
        background: linear-gradient(135deg, #0C1E33 0%, #0F172A 100%);
        color: #DBEAFE;
        border-left: 5px solid #38BDF8;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 4px 15px rgba(56,189,248,0.2);
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #451A03 0%, #78350F 100%);
        color: #FEF3C7;
        border-left: 5px solid #F59E0B;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 4px 15px rgba(245,158,11,0.2);
    }
    
    /* Enhanced scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0A0E1A;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #38BDF8 0%, #0EA5E9 100%);
        border-radius: 6px;
        border: 2px solid #0A0E1A;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #0EA5E9 0%, #0284C7 100%);
    }
    
    /* Footer */
    .footer {
        color: #64748B;
        text-align: center;
        margin-top: 4rem;
        border-top: 1px solid rgba(56,189,248,0.2);
        padding-top: 2rem;
        font-weight: 500;
    }
    
    /* Selection styling */
    ::selection {
        background: rgba(56,189,248,0.3);
        color: #FFFFFF;
    }
    
    /* Smooth transitions for all interactive elements */
    button, a, input, textarea, select {
        transition: all 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)


# Header section
st.markdown("""
<div class="header-container">
    <div class="icon-xl">📄</div>
    <h1 class="header-title">AI Resume Checker</h1>
    <p class="header-subtitle">Upload your resume and job description to get instant AI-powered matching analysis</p>
</div>
""", unsafe_allow_html=True)

# Create two columns for upload section
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("""
    <div class="upload-card">
        <span class="card-icon">📤</span>
        <h3 class="card-title">Upload Resume</h3>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose your resume file",
        type=["pdf"],
        help="Upload your resume in PDF format for analysis",
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        st.markdown(
            '<div class="alert-success">✅ <strong>Resume uploaded successfully!</strong> Ready for analysis.</div>',
            unsafe_allow_html=True
        )

with col2:
    st.markdown("""
    <div class="upload-card">
        <span class="card-icon">📋</span>
        <h3 class="card-title">Job Description</h3>
    </div>
    """, unsafe_allow_html=True)
    
    job_description = st.text_area(
        "Paste job description",
        height=180,
        placeholder="Paste the complete job description here including requirements, responsibilities, qualifications, and desired skills...",
        label_visibility="collapsed"
    )

# Analysis button and results
if uploaded_file and job_description:
    
    if st.button("🚀 Analyze Resume Match"):
        with st.spinner("🔍 Analyzing your resume against job requirements... This may take a moment"):
            # Save uploaded PDF temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                resume_path = tmp.name

            # Extract resume text
            resume_text = extract_text_from_pdf(resume_path)

            # Load skills
            skills_list = load_skills("data/skills_list.txt")

            # Extract skills
            resume_skills = extract_skills(resume_text, skills_list)
            jd_skills = extract_jd_skills(job_description, skills_list)

            # Scores
            skill_score, matched, missing = calculate_match_score(
                resume_skills, jd_skills
            )
            tfidf_score = compute_tfidf_similarity(resume_text, job_description)

            final_score = round((0.6 * skill_score) + (0.4 * tfidf_score), 2)

            # Feedback
            feedback = generate_resume_feedback(
                resume_text,
                resume_skills,
                jd_skills,
                skill_score,
                tfidf_score
            )

        # Results section
        st.markdown('<div class="results-section">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">📊 Match Analysis Results</h2>', unsafe_allow_html=True)
        
        # Score interpretation with visual badge
        if final_score >= 75:
            st.markdown(
                '<div class="alert-success">🎉 <strong>Excellent Match!</strong> Your resume aligns very well with this job description. You\'re a strong candidate for this position.<span class="score-badge score-excellent">EXCELLENT FIT</span></div>',
                unsafe_allow_html=True
            )
        elif final_score >= 50:
            st.markdown(
                '<div class="alert-info">💡 <strong>Good Match!</strong> Your resume shows promise with room for optimization. Consider highlighting more relevant skills.<span class="score-badge score-good">GOOD FIT</span></div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div class="alert-warning">⚠️ <strong>Needs Improvement</strong> Your resume could better align with the job requirements. Review the missing skills below.<span class="score-badge score-fair">FAIR FIT</span></div>',
                unsafe_allow_html=True
            )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Score metrics
        st.markdown('<div style="margin: 2rem 0;">', unsafe_allow_html=True)
        metric_col1, metric_col2, metric_col3 = st.columns(3, gap="large")
        
        with metric_col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="icon-xl">🎯</div>', unsafe_allow_html=True)
            st.metric(
                label="Skill Match Score",
                value=f"{skill_score}%"
            )
            st.markdown("</div>", unsafe_allow_html=True)
        
        with metric_col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="icon-xl">📈</div>', unsafe_allow_html=True)
            st.metric(
                label="Content Similarity",
                value=f"{tfidf_score}%"
            )
            st.markdown("</div>", unsafe_allow_html=True)
        
        with metric_col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="icon-xl">⭐</div>', unsafe_allow_html=True)
            st.metric(
                label="Overall Match",
                value=f"{final_score}%"
            )
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Skills section
        st.markdown('<div class="results-section">', unsafe_allow_html=True)
        
        skill_col1, skill_col2 = st.columns(2, gap="large")
        
        with skill_col1:
            st.markdown('<h3 class="section-title">✅ Matched Skills</h3>', unsafe_allow_html=True)
            st.markdown('<p style="color: #475569; margin-bottom: 1rem; font-weight: 500;">These skills from the job description were found in your resume</p>', unsafe_allow_html=True)
            if matched:
                skills_html = "".join([f'<span class="skill-tag">{skill}</span>' for skill in matched])
                st.markdown(f'<div style="margin-top: 1rem;">{skills_html}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="alert-warning">No matched skills found. Consider adding relevant keywords.</div>', unsafe_allow_html=True)
        
        with skill_col2:
            st.markdown('<h3 class="section-title">⚠️ Missing Skills</h3>', unsafe_allow_html=True)
            st.markdown('<p style="color: #475569; margin-bottom: 1rem; font-weight: 500;">These required skills are not evident in your resume</p>', unsafe_allow_html=True)
            if missing:
                skills_html = "".join([f'<span class="missing-skill-tag">{skill}</span>' for skill in missing])
                st.markdown(f'<div style="margin-top: 1rem;">{skills_html}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="alert-success">🎉 All required skills are present in your resume!</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Feedback section
        st.markdown('<div class="results-section">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-title">💬 AI-Powered Recommendations</h3>', unsafe_allow_html=True)
        st.markdown('<p style="color: #475569; margin-bottom: 1.5rem; font-weight: 500;">Personalized suggestions to improve your resume match</p>', unsafe_allow_html=True)
        
        if feedback:
            for item in feedback:
                st.markdown(f'<div class="feedback-item">💡 {item}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="alert-info">Your resume looks good! No specific improvements needed at this time.</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Next steps
        st.markdown("""
        <div class="alert-info" style="margin-top: 2rem;">
            <strong>📌 Next Steps:</strong><br><br>
            1. Review the feedback and missing skills above<br>
            2. Update your resume to include relevant keywords and experiences<br>
            3. Re-upload and analyze again to track your improvements<br>
            4. Tailor your resume for each job application for best results
        </div>
        """, unsafe_allow_html=True)

else:
    # Instructions when inputs are missing
    st.markdown("""
    <div class="instruction-card">
        <h3 style="color: #1E293B; font-size: 1.5rem; font-weight: 700; margin-bottom: 1.5rem; text-align: center;">
            🚀 How It Works
        </h3>
        
        <div class="instruction-step">
            <div class="step-number">1</div>
            <div>
                <strong style="color: #1E293B;">Upload Your Resume</strong><br>
                <span style="color: #475569;">Choose a PDF file containing your latest resume or CV</span>
            </div>
        </div>
        
        <div class="instruction-step">
            <div class="step-number">2</div>
            <div>
                <strong style="color: #1E293B;">Paste Job Description</strong><br>
                <span style="color: #475569;">Copy and paste the complete job posting including requirements</span>
            </div>
        </div>
        
        <div class="instruction-step">
            <div class="step-number">3</div>
            <div>
                <strong style="color: #1E293B;">Get Instant Analysis</strong><br>
                <span style="color: #475569;">Receive AI-powered matching scores and personalized recommendations</span>
            </div>
        </div>
        
        <div class="instruction-step">
            <div class="step-number">4</div>
            <div>
                <strong style="color: #1E293B;">Improve & Resubmit</strong><br>
                <span style="color: #475569;">Update your resume based on feedback and analyze again</span>
            </div>
        </div>
    </div>
    
    <div class="alert-info">
        <strong>💡 Pro Tip:</strong> For best results, ensure your resume includes specific skills, accomplishments, 
        and keywords that match the job description. Our AI analyzes both hard skills and content similarity.
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p style="font-size: 1rem; margin-bottom: 0.5rem;">
        <strong>AI Resume Checker</strong>
    </p>
    <p>
        Powered by Advanced AI Technology • Built with ❤️ using Streamlit<br>
        © 2024 All Rights Reserved
    </p>
</div>
""", unsafe_allow_html=True)
