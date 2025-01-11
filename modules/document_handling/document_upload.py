# This module is there to upload the pdf file and validate it

import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "static/uploads/"
ALLOWED_EXTENSIONS = {"pdf"}

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_pdf(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        return filepath
    return None