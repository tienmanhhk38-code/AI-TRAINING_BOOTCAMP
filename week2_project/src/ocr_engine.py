from pathlib import Path

from pdf_processor import configure_tesseract_command, extract_pdf_text


TEXT_EXTENSIONS = {".txt", ".md"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff"}


def extract_text_from_text_file(path):
    return path.read_text(encoding="utf-8")


def extract_text_from_image(path):
    try:
        from PIL import Image
        import pytesseract
    except ModuleNotFoundError as error:
        raise RuntimeError("Pillow and pytesseract are required for image OCR") from error

    image = Image.open(path)
    configure_tesseract_command(pytesseract)
    return pytesseract.image_to_string(image, lang="eng")


def extract_text(path):
    path = Path(path)
    suffix = path.suffix.lower()

    if suffix in TEXT_EXTENSIONS:
        return extract_text_from_text_file(path)
    if suffix == ".pdf":
        return extract_pdf_text(path)
    if suffix in IMAGE_EXTENSIONS:
        return extract_text_from_image(path)

    raise ValueError(f"Unsupported input file type: {path.name}")
