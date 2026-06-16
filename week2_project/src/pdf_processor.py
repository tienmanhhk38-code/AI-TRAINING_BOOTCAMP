def extract_pdf_text(pdf_path):
    try:
        import fitz
    except ModuleNotFoundError as error:
        raise RuntimeError("PyMuPDF is required for PDF processing") from error

    doc = fitz.open(pdf_path)
    pages = []

    for page_index, page in enumerate(doc, start=1):
        text = page.get_text("text").strip()
        if text:
            pages.append(f"--- Page {page_index} ---\n{text}")

    return "\n\n".join(pages)


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
