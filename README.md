
# AI Resume Checker

AI Resume Checker is an NLP-powered web application that evaluates how well a candidate’s resume matches a given job description. It extracts skills, measures semantic similarity, computes a match score, and generates personalized feedback to help users optimize their resumes for specific roles.

The system combines skill-based matching with TF-IDF content similarity to provide both quantitative evaluation and actionable improvement suggestions through an interactive Streamlit interface.

---

## Features

* Resume text extraction from PDF files
* Automated skill extraction from resumes and job descriptions
* Skill overlap analysis with matched and missing skills
* TF-IDF based semantic similarity scoring
* Weighted overall compatibility score
* AI-generated resume improvement recommendations
* Interactive Streamlit dashboard for real-time analysis

---

## How It Works

1. Extracts text from uploaded resume (PDF)
2. Loads predefined skill database
3. Identifies skills in resume and job description
4. Computes skill match score and semantic similarity
5. Generates improvement feedback
6. Displays detailed analysis and recommendations

---

## Tech Stack

* Python
* Streamlit
* Natural Language Processing (NLP)
* TF-IDF Similarity
* Modular Machine Learning Pipeline

---

## Project Structure

```
AI_Resume_Checker/
│
├── data/
│   └── skills_list.txt
│
├── parser/
│   └── resume_parser.py
│
├── matcher/
│   ├── skill_extractor.py
│   └── jd_parser.py
│
├── scorer/
│   ├── score_calculator.py
│   ├── tfidf_similarity.py
│   └── resume_feedback.py
│
├── streamlit_app.py
├── app.py
└── sample_resume.pdf
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Anish-Tiwari2027/AI-Resume-Checker.git
cd AI-Resume-Checker
```

### 2. Create virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

```bash
streamlit run streamlit_app.py
```

Then open the local URL shown in the terminal.

---

## Usage

1. Upload resume in PDF format
2. Paste job description
3. Click **Analyze Resume Match**
4. View scores, matched skills, missing skills, and feedback
5. Improve resume and re-analyze

---

## Use Cases

* Resume optimization for specific job roles
* ATS keyword alignment
* Skill gap identification
* Job application preparation

---

## Future Improvements

* Advanced semantic embeddings (BERT / transformers)
* Resume section-level analysis
* Multi-format resume support (DOCX, TXT)
* Model deployment via API
* Recruiter dashboard

---

## License

This project is for educational and portfolio purposes.

---

## Author

Anish Tiwari
AI / Machine Learning Projects
