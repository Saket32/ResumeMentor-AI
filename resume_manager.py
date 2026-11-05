
import os
import uuid

from document_chat import extract_text_from_pdf
from database import save_resume_profile, get_resume_profile

RESUME_FOLDER = os.path.join("uploads", "resumes")


def upload_resume(pdf_file):
    """Save a PDF resume and store its extracted text in the profile."""

    if not pdf_file.name.lower().endswith(".pdf"):
        raise ValueError("Please upload a PDF file.")

    os.makedirs(RESUME_FOLDER, exist_ok=True)

    extracted_text = extract_text_from_pdf(pdf_file)

    if not extracted_text.strip():
        raise ValueError(
            "No readable text found in this PDF. "
            "It may be scanned or image-based."
        )

    # Generate a unique filename to avoid accidental overwrites
    unique_filename = f"{uuid.uuid4().hex}_{os.path.basename(pdf_file.name)}"
    file_path = os.path.join(RESUME_FOLDER, unique_filename)

    # Save the original PDF
    pdf_file.seek(0)

    with open(file_path, "wb") as file:
        file.write(pdf_file.getvalue())

    try:
        # Save resume information in SQLite
        save_resume_profile(
            filename=pdf_file.name,
            file_path=file_path,
            extracted_text=extracted_text
        )
    except Exception:
        # Remove the newly saved file if database saving fails
        if os.path.exists(file_path):
            os.remove(file_path)
        raise

    return {
        "filename": pdf_file.name,
        "file_path": file_path,
        "character_count": len(extracted_text),
        "extracted_text": extracted_text
    }


def get_current_resume():
    """Retrieve the user's saved resume profile."""

    return get_resume_profile()
