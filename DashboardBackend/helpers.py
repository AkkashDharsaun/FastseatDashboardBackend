import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file, upload_folder, prefix=""):
    if file and allowed_file(file.filename):
        safe = secure_filename(file.filename)
        new_filename = f"{prefix}_{safe}"
        file.save(os.path.join(upload_folder, new_filename))
        return new_filename
    return None
