import re
import fitz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Simple editable keyword catalogue for this demo.
SKILLS = [
    "Python", "Java", "JavaScript", "TypeScript", "React", "Django",
    "Flask", "FastAPI", "HTML", "CSS", "SQL", "MySQL", "PostgreSQL",
    "MongoDB", "SQLite", "REST API", "Git", "GitHub", "Docker",
    "AWS", "Linux", "Pandas", "NumPy", "Scikit-learn", "Machine Learning",
    "NLP", "TensorFlow", "PyTorch", "Data Analysis", "Excel",
    "Communication", "Problem Solving", "OOP", "Data Structures",
]

def extract_pdf_text(uploaded_file):
    """Extract selectable text from a PDF. Scanned-image OCR is not included."""
    text_parts = []
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as pdf:
        if pdf.is_encrypted:
            raise ValueError("This PDF is password-protected. Upload an unlocked PDF.")
        for page in pdf:
            text_parts.append(page.get_text("text"))
    text = "\n".join(text_parts).strip()
    if len(text) < 40:
        raise ValueError(
            "Not enough selectable text was found. If this is a scanned PDF, "
            "export a text-based PDF or add OCR support."
        )
    return text

def normalize(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def find_skills(text):
    normalized = normalize(text)
    found = []
    for skill in SKILLS:
        pattern = r"(?<![a-z0-9])" + re.escape(skill.lower()) + r"(?![a-z0-9])"
        if re.search(pattern, normalized):
            found.append(skill)
    return found

def analyze_resume(resume_text, job_description):
    resume_clean = normalize(resume_text)
    job_clean = normalize(job_description)
    if not resume_clean or not job_clean:
        raise ValueError("Resume and job description must both contain text.")

    # Fit on this pair only: this is similarity matching, not a trained classifier.
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
    vectors = vectorizer.fit_transform([resume_clean, job_clean])
    score = float(cosine_similarity(vectors[0:1], vectors[1:2])[0][0] * 100)

    resume_skills = find_skills(resume_text)
    job_skills = find_skills(job_description)
    matched = [skill for skill in job_skills if skill in resume_skills]
    missing = [skill for skill in job_skills if skill not in resume_skills]

    return {
        "score": round(score, 1),
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched,
        "missing_skills": missing,
        "resume_word_count": len(resume_clean.split()),
        "job_word_count": len(job_clean.split()),
    }
