# Week 2 Project - OCR Pipeline

Project dau ra Week 2: doc document, extract text, clean text, chunk text, va ghi output cho Week 3 RAG.

Project mau chay duoc voi file text, PDF co text layer, PDF scan, va image:

```text
input/*
```

PDF scan va image OCR can cai Python dependencies trong `requirements.txt` va Tesseract engine tren may.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
winget install --id UB-Mannheim.TesseractOCR --exact --accept-package-agreements --accept-source-agreements
```

Neu Windows chua nhan PATH moi, code se tu tim Tesseract tai user-local va Program Files paths pho bien.

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
input/*.pdf -> extract text layer first, OCR blank/scanned pages with pytesseract
input/*.png/*.jpg -> OCR with pytesseract
```
