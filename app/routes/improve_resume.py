from flask import Blueprint, request, send_file, jsonify, current_app
from ..generators.resume_generator import ATSResumeGenerator
import os
import json
from datetime import datetime

improve_resume_bp = Blueprint("improve_resume", __name__)

@improve_resume_bp.route("/api/generate-improved-resume", methods=["POST"])
def generate_improved_resume():
    """
    Generate an improved ATS-friendly resume based on suggestions.
    
    Expected JSON payload:
    {
        "resume_text": "original resume text",
        "suggestions": {...},
        "analysis": {...},
        "jd_text": "job description text",
        "format": "docx" or "pdf"
    }
    """
    try:
        data = request.get_json()
        
        print(f"[IMPROVE RESUME] Received request for format: {data.get('format', 'docx')}")
        
        resume_text = data.get("resume_text")
        suggestions = data.get("suggestions")
        analysis = data.get("analysis")
        jd_text = data.get("jd_text")
        output_format = data.get("format", "docx")
        
        print(f"[IMPROVE RESUME] Resume text length: {len(resume_text) if resume_text else 0}")
        print(f"[IMPROVE RESUME] Suggestions: {suggestions.get('_is_demo', 'unknown') if suggestions else 'None'}")
        
        if not all([resume_text, suggestions, jd_text]):
            return jsonify({"error": "Missing required fields"}), 400
        
        cfg = current_app.config
        generator = ATSResumeGenerator(cfg)
        
        # Generate improved resume content
        print(f"[IMPROVE RESUME] Calling generator.generate_improved_resume...")
        resume_data = generator.generate_improved_resume(
            resume_text, 
            suggestions, 
            analysis or {},
            jd_text
        )
        
        print(f"[IMPROVE RESUME] Resume data generated. Is demo: {resume_data.get('_is_demo', False)}")
        
        # Create output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Generate file - always create .docx
        docx_filename = f"improved_resume_{timestamp}.docx"
        docx_path = os.path.join(cfg["DOWNLOADS_FOLDER"], docx_filename)
        
        print(f"[IMPROVE RESUME] Creating .docx file at: {docx_path}")
        file_path = generator.create_docx(resume_data, docx_path)
        
        # Determine correct mimetype and download name
        if output_format == "pdf":
            # User requested PDF but we're giving them .docx
            # Change the download name to .docx and use correct mimetype
            download_name = f"improved_resume_{timestamp}.docx"
            mimetype = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            print(f"[IMPROVE RESUME] PDF requested but returning .docx (PDF conversion not implemented)")
        else:
            download_name = os.path.basename(file_path)
            mimetype = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        
        print(f"[IMPROVE RESUME] Sending file: {file_path}")
        
        # Return file for download
        return send_file(
            file_path,
            as_attachment=True,
            download_name=download_name,
            mimetype=mimetype
        )
    
    except Exception as e:
        print(f"[IMPROVE RESUME] Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
