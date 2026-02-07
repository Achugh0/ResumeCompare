from flask import Blueprint, request, render_template, current_app, redirect, url_for, flash
from ..utils.helpers import save_uploaded_file
from ..parsers.pdf_parser import PDFParser
from ..parsers.docx_parser import DOCXParser
from .analysis import run_analysis

upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@upload_bp.route("/compare", methods=["POST"])
def compare():
    cfg = current_app.config
    allowed = cfg["ALLOWED_EXTENSIONS"]
    upload_folder = cfg["UPLOAD_FOLDER"]

    resume_file = request.files.get("resume")
    jd_file = request.files.get("job_description")

    if not resume_file or not jd_file:
        flash("Both files are required.")
        return redirect(url_for("upload.index"))

    try:
        resume_path = save_uploaded_file(resume_file, upload_folder, allowed)
        jd_path = save_uploaded_file(jd_file, upload_folder, allowed)

        def extract(path):
            ext = path.rsplit(".", 1)[1].lower()
            if ext == "pdf":
                return PDFParser.extract_text(path)
            return DOCXParser.extract_text(path)

        resume_text = extract(resume_path)
        jd_text = extract(jd_path)

        return run_analysis(resume_text, jd_text)

    except Exception as e:
        flash(f"Error: {e}")
        return redirect(url_for("upload.index"))
