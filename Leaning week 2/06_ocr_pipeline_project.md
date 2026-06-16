# Week 2 Project - OCR Pipeline

## Muc tieu

Xay mot OCR pipeline nho co the doc document, trich xuat text, clean text, chunk text, va ghi output.

## 1. Input

### Dinh nghia

Input la file document/image can trich xuat text. Project mau chay san voi file text, va co cau truc de mo rong sang PDF/image khi cai them OCR dependencies.

### Vi du

```text
week2_project/input/sample_document.txt
```

## 2. Output

### Dinh nghia

Output gom text da extract va chunks JSON dung cho RAG Week 3.

### Vi du

```text
week2_project/output/extracted_text.txt
week2_project/output/chunks.json
```

## 3. Kien truc module

| File | Trach nhiem |
| --- | --- |
| `main.py` | Dieu phoi pipeline |
| `ocr_engine.py` | Extract text tu text/pdf/image |
| `pdf_processor.py` | Xu ly PDF text layer hoac render page |
| `image_preprocessor.py` | Preprocess image neu co Pillow |
| `chunker.py` | Clean text va chunk text |

## 4. Flow

```text
main.py
  -> find input files
  -> extract text
  -> clean text
  -> chunk text
  -> export extracted_text.txt
  -> export chunks.json
```

## 5. Acceptance checklist

- Chay bang mot lenh: `python src/main.py`.
- Tao `output/extracted_text.txt`.
- Tao `output/chunks.json`.
- Chunk co `chunk_id`, `source`, `index`, `text`.
- Code khong crash neu chua cai OCR dependency.
- README co huong dan chay.

## 6. Mo rong sau bai hoc

Sau khi cai Tesseract/PyMuPDF/Pillow, co the them:

- OCR image bang `pytesseract`.
- Extract PDF text layer bang PyMuPDF.
- Render scanned PDF thanh image.
- Preprocess image truoc OCR.

