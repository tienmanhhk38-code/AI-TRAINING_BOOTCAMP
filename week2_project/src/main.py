from pathlib import Path

from chunker import chunk_text, clean_text, export_chunks
from ocr_engine import extract_text


SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf", ".png", ".jpg", ".jpeg", ".bmp", ".tiff"}


def find_input_files(input_dir):
    return [
        path
        for path in sorted(input_dir.iterdir())
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]


def write_text(text, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main():
    project_dir = Path(__file__).resolve().parent.parent
    input_dir = project_dir / "input"
    output_dir = project_dir / "output"

    input_files = find_input_files(input_dir)
    if not input_files:
        raise RuntimeError("No supported input files found")

    extracted_sections = []
    all_chunks = []

    for input_file in input_files:
        try:
            raw_text = extract_text(input_file)
        except Exception as error:
            cleaned = f"ERROR extracting {input_file.name}: {type(error).__name__}: {error}"
        else:
            cleaned = clean_text(raw_text)

        extracted_sections.append(f"## Source: {input_file.name}\n\n{cleaned}")
        all_chunks.extend(chunk_text(cleaned, source=input_file.name, chunk_size=500, overlap=50))

    extracted_text = "\n\n".join(extracted_sections)

    write_text(extracted_text, output_dir / "extracted_text.txt")
    export_chunks(all_chunks, output_dir / "chunks.json")

    print(f"Read {len(input_files)} input files")
    print(f"Wrote {output_dir / 'extracted_text.txt'}")
    print(f"Wrote {output_dir / 'chunks.json'}")
    print(f"Chunks: {len(all_chunks)}")


if __name__ == "__main__":
    main()
