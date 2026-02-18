from flask import Blueprint, send_from_directory, current_app

templates_bp = Blueprint("templates_bp", __name__, url_prefix="/templates")

@templates_bp.route("/resume")
def download_resume_template():
    folder = current_app.config["DOWNLOADS_FOLDER"]
    return send_from_directory(folder, "resume_template.docx", as_attachment=True)

@templates_bp.route("/job-description")
def download_jd_template():
    folder = current_app.config["DOWNLOADS_FOLDER"]
    return send_from_directory(folder, "job_description_template.docx", as_attachment=True)
@templates_bp.route("/download/<filename>")
def download_file(filename):
    folder = current_app.config["DOWNLOADS_FOLDER"]
    return send_from_directory(folder, filename, as_attachment=True)
