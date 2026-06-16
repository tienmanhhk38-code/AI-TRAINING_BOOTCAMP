# Week 2 Project - OCR Pipeline

Project dau ra Week 2: doc document, extract text, clean text, chunk text, va ghi output cho Week 3 RAG.

Project mau chay duoc ngay voi file text:

```text
input/sample_document.txt
```

PDF/image OCR la phan mo rong sau khi cai dependencies nhu PyMuPDF, Pillow, pytesseract va Tesseract engine.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run

```powershell
python src/main.py
```

## Output

```text
output/extracted_text.txt
output/chunks.json
```

## Input flow

```text
input/*.txt -> read text directly
input/*.pdf -> extract text with PyMuPDF if installed
input/*.png/*.jpg -> OCR with pytesseract if installed
```

