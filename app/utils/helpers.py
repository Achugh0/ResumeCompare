import os
from werkzeug.utils import secure_filename

def allowed_file(filename, allowed_exts):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_exts

def save_uploaded_file(file_obj, upload_folder, allowed_exts):
    if not file_obj or file_obj.filename == "":
        raise ValueError("No file selected")

    if not allowed_file(file_obj.filename, allowed_exts):
        raise ValueError("Unsupported file type")

    filename = secure_filename(file_obj.filename)
    os.makedirs(upload_folder, exist_ok=True)
    path = os.path.join(upload_folder, filename)
    file_obj.save(path)
    return path
