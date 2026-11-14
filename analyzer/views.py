from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from .models import Analysis
from .services import extract_pdf_text, analyze_resume

MAX_FILE_SIZE = 5 * 1024 * 1024

@require_http_methods(["GET", "POST"])
def home(request):
    error = ""
    if request.method == "POST":
        uploaded = request.FILES.get("resume")
        job_description = request.POST.get("job_description", "").strip()
        job_title = request.POST.get("job_title", "").strip()[:150]

        if not uploaded:
            error = "Please choose a PDF resume."
        elif not uploaded.name.lower().endswith(".pdf"):
            error = "Only PDF files are supported."
        elif uploaded.size > MAX_FILE_SIZE:
            error = "File is too large. Maximum size is 5 MB."
        elif len(job_description) < 50:
            error = "Please paste a job description with at least 50 characters."
        elif len(job_description) > 20000:
            error = "Job description is too long. Maximum is 20,000 characters."
        else:
            try:
                resume_text = extract_pdf_text(uploaded)
                result = analyze_resume(resume_text, job_description)
                analysis = Analysis.objects.create(
                    resume_name=uploaded.name[:255],
                    job_title=job_title,
                    match_score=result["score"],
                    matched_skills=result["matched_skills"],
                    missing_skills=result["missing_skills"],
                )
                request.session["latest_analysis"] = {
                    "id": analysis.id,
                    "score": result["score"],
                    "matched": result["matched_skills"],
                    "missing": result["missing_skills"],
                }
                return redirect("result", analysis_id=analysis.id)
            except (ValueError, RuntimeError) as exc:
                error = str(exc)
            except Exception:
                error = "We could not read this PDF. Please try another text-based PDF."

    recent = Analysis.objects.all()[:5]
    return render(request, "analyzer/home.html", {"error": error, "recent": recent})

def result(request, analysis_id):
    analysis = get_object_or_404(Analysis, pk=analysis_id)
    return render(request, "analyzer/result.html", {"analysis": analysis})

def history(request):
    paginator = Paginator(Analysis.objects.all(), 10)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "analyzer/history.html", {"page_obj": page_obj})

def delete_history(request, analysis_id):
    if request.method == "POST":
        get_object_or_404(Analysis, pk=analysis_id).delete()
    return redirect("history")
