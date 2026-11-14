# SmartResume — AI Resume Analyzer

A one-day, beginner-friendly Django project that compares a PDF resume with a job description.

## What it does
- Upload a PDF resume (max 5 MB)
- Paste a job description
- Extract PDF text using PyMuPDF
- Calculate a TF-IDF cosine-similarity score with scikit-learn
- Detect matched and missing skills from a small editable skill dictionary
- Save analysis history in SQLite
- Show a clean dashboard and individual result page

## Important project limitation
The displayed percentage is a **text similarity score**, not an official ATS score and not a prediction of hiring success. Skill detection is keyword-based. It can miss synonyms and context (for example, "JS" versus "JavaScript"). Explain this honestly in interviews.

## Requirements
- Python 3.10+
- pip
- VS Code (recommended)

## Windows setup
Open PowerShell or Command Prompt in this folder:

```bash
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/

## Try the sample
1. Open `sample_data/sample_job_description.txt`.
2. Copy its contents into the Job Description box.
3. For a sample PDF, create a PDF from `sample_data/sample_resume.txt` using Word/Google Docs (Save as PDF), then upload it.
   - Or use your own PDF resume.
4. Click **Analyze Resume**.

## Project structure
```text
smartresume_project/
├── manage.py
├── requirements.txt
├── smartresume/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── analyzer/
│   ├── migrations/
│   ├── services.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── templates/analyzer/
│   └── static/analyzer/
└── sample_data/
```

## How the matching works
1. PyMuPDF extracts text from the uploaded PDF.
2. The service cleans whitespace and checks for a minimum amount of text.
3. `TfidfVectorizer` converts the resume and job description into weighted word features.
4. `cosine_similarity` compares the two vectors.
5. A curated skill list is searched in both texts to show matched and missing skills.
6. Django stores the result in SQLite and renders it.

## Interview explanation
"SmartResume is a Django-based resume analysis web application. A user uploads a PDF resume and pastes a job description. I extract text from the PDF using PyMuPDF, convert the resume and job description into TF-IDF vectors using Scikit-learn, and calculate cosine similarity. I also compare a predefined skill dictionary to show matched and missing skills. Django handles the upload, validation, database storage and result pages."

## Suggested one-day build plan
- Hour 1: create virtual environment and install dependencies
- Hours 2–3: build templates and CSS
- Hour 4: implement PDF text extraction
- Hours 5–6: implement TF-IDF similarity and skill matching
- Hour 7: connect Django views and SQLite history
- Hour 8: test with multiple resumes and polish

## Production improvements (not included in this one-day version)
Add authentication, malware scanning, stronger file storage controls, OCR for scanned PDFs, synonym/semantic embeddings, comprehensive skill taxonomy, tests, deployment configuration, and privacy/retention controls.
