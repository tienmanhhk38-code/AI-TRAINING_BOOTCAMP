from io import BytesIO
from pathlib import Path
from shutil import which


DEFAULT_TESSERACT_PATHS = (
    Path.home() / "AppData" / "Local" / "Programs" / "Tesseract-OCR" / "tesseract.exe",
    Path("C:/Program Files/Tesseract-OCR/tesseract.exe"),
    Path("C:/Program Files (x86)/Tesseract-OCR/tesseract.exe"),
)


def extract_pdf_text(pdf_path):
    try:
        import fitz
    except ModuleNotFoundError as error:
        raise RuntimeError("PyMuPDF is required for PDF processing") from error

    doc = fitz.open(pdf_path)
    pages = []

    for page_index, page in enumerate(doc, start=1):
        text = page.get_text("text").strip()
        if not text:
            text = extract_scanned_page_text(page, fitz).strip()
        if text:
            pages.append(f"--- Page {page_index} ---\n{text}")

    return "\n\n".join(pages)


def extract_scanned_page_text(page, fitz):
    try:
        from PIL import Image
        import pytesseract
    except ModuleNotFoundError as error:
        raise RuntimeError("Pillow and pytesseract are required for scanned PDF OCR") from error

    configure_tesseract_command(pytesseract)
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
    image = Image.open(BytesIO(pix.tobytes("png")))
    return pytesseract.image_to_string(image, lang="eng")


def configure_tesseract_command(pytesseract, candidates=None):
    if which("tesseract"):
        return None

    for candidate in candidates or DEFAULT_TESSERACT_PATHS:
        candidate = Path(candidate)
        if candidate.is_file():
            tesseract_path = str(candidate)
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
            return tesseract_path

    return None


def render_first_page(pdf_path, output_path):
    try:
        import fitz
    except ModuleNotFoundError as error:
        raise RuntimeError("PyMuPDF is required for PDF rendering") from error

    doc = fitz.open(pdf_path)
    if doc.page_count == 0:
        raise ValueError("PDF has no pages")

    page = doc[0]
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pix.save(output_path)
    return output_path
