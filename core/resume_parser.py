import io
import re

from pypdf import PdfReader
from docx import Document


# =========================================
# EXTRACT TEXT FROM PDF
# =========================================

def extract_pdf_text(uploaded_file):

    pdf_bytes = uploaded_file.read()

    reader = PdfReader(
        io.BytesIO(pdf_bytes)
    )

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# =========================================
# EXTRACT TEXT FROM DOCX
# =========================================

def extract_docx_text(uploaded_file):

    docx_bytes = uploaded_file.read()

    document = Document(
        io.BytesIO(docx_bytes)
    )

    text = ""

    for paragraph in document.paragraphs:

        text += paragraph.text + "\n"

    return text


# =========================================
# EXTRACT TEXT FROM TXT
# =========================================

def extract_txt_text(uploaded_file):

    text_bytes = uploaded_file.read()

    return text_bytes.decode(
        "utf-8",
        errors="ignore"
    )


# =========================================
# MAIN TEXT EXTRACTION FUNCTION
# =========================================

def extract_resume_text(uploaded_file):

    file_name = uploaded_file.name.lower()

    # Reset file position
    uploaded_file.seek(0)

    if file_name.endswith(".pdf"):

        return extract_pdf_text(
            uploaded_file
        )

    elif file_name.endswith(".docx"):

        return extract_docx_text(
            uploaded_file
        )

    elif file_name.endswith(".txt"):

        return extract_txt_text(
            uploaded_file
        )

    else:

        return ""


# =========================================
# SKILL DETECTION
# =========================================

def detect_skills(text):

    skills = [
        "Python",
        "Machine Learning",
        "Statistics",
        "SQL",
        "Deep Learning",
        "NLP",
        "Git",
        "Docker",
        "FastAPI",
        "AWS",
        "Computer Vision",
        "Data Science",
        "Generative AI",
        "Pandas",
        "NumPy",
        "TensorFlow",
        "PyTorch",
        "Scikit-learn",
        "Power BI",
        "Excel"
    ]

    detected_skills = []

    text_lower = text.lower()

    for skill in skills:

        skill_lower = skill.lower()

        # Escape special characters
        pattern = re.escape(
            skill_lower
        )

        if re.search(
            pattern,
            text_lower
        ):

            detected_skills.append(skill)

    return detected_skills