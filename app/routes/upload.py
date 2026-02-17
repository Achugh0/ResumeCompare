from flask import Blueprint, request, render_template, current_app, flash, redirect, url_for
from ..utils.helpers import save_uploaded_file
from ..parsers.pdf_parser import PDFParser
from ..parsers.docx_parser import DOCXParser
from .analysis import run_analysis
from ..generators.pdf_generator import PDFReportGenerator
from ..analyzers.improvement_engine import ImprovementEngine

upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/", methods=["GET"])
def index():
    # Render home with no analysis yet
    return render_template("index.html", analysis=None, matrix=None, error=None, suggestions=None)

@upload_bp.route("/compare", methods=["POST"])
def compare():
    cfg = current_app.config
    allowed = cfg["ALLOWED_EXTENSIONS"]
    upload_folder = cfg["UPLOAD_FOLDER"]

    resume_file = request.files.get("resume")
    jd_file = request.files.get("job_description")

    if not resume_file or not jd_file:
        error = "Both resume and job description files are required."
        return render_template("index.html", analysis=None, matrix=None, error=error, suggestions=None)

    try:
        # Save files
        resume_path = save_uploaded_file(resume_file, upload_folder, allowed)
        jd_path = save_uploaded_file(jd_file, upload_folder, allowed)

        # Extract text
        def extract(path):
            ext = path.rsplit(".", 1)[1].lower()
            if ext == "pdf":
                return PDFParser.extract_text(path)
            return DOCXParser.extract_text(path)

        resume_text = extract(resume_path)
        jd_text = extract(jd_path)

        # Run analysis
        analysis, matrix = run_analysis(resume_text, jd_text)

        # Generate PDF report
        pdf_gen = PDFReportGenerator(cfg)
        pdf_filename = pdf_gen.generate_report(analysis, matrix)

        # NEW: Generate improvement suggestions (non-intrusive addition)
        suggestions = None
        try:
            print("[UPLOAD] Generating improvement suggestions...")
            improvement_engine = ImprovementEngine(cfg)
            suggestions = improvement_engine.generate_suggestions(analysis, resume_text, jd_text)
            print(f"[UPLOAD] Suggestions generated. Is demo: {suggestions.get('_is_demo', 'unknown') if suggestions else 'None'}")
        except Exception as e:
            print(f"[UPLOAD] Could not generate suggestions: {e}")
            import traceback
            traceback.print_exc()
            # Continue without suggestions - not critical
        
        # Store text for resume generation
        analysis["_resume_text"] = resume_text
        analysis["_jd_text"] = jd_text
        
        return render_template("index.html", analysis=analysis, matrix=matrix, pdf_report=pdf_filename, suggestions=suggestions)

    except Exception as e:
        flash(f"An unexpected error occurred: {str(e)}")
        return redirect(url_for("upload.index"))
