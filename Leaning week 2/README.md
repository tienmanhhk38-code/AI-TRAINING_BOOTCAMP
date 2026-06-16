# Week 2 - AI Architecture + OCR

Nguon lo trinh: `../README.md`

Muc tieu Week 2: hieu kien truc AI Chatbot tong the va xay duoc OCR pipeline xu ly tai lieu that.

Flow can nam:

```text
Document/Image -> OCR -> Clean Text -> Chunk Text -> Save Output
```

## Danh sach bai hoc

| Ngay | File | Noi dung |
| --- | --- | --- |
| Day 1 | [01_ai_system_architecture.md](01_ai_system_architecture.md) | SA session, C4 container model, pipeline AI Chatbot |
| Day 2-3 | [02_basic_ocr_tesseract_easyocr.md](02_basic_ocr_tesseract_easyocr.md) | OCR co ban, Tesseract, pytesseract, EasyOCR |
| Day 4 | [03_image_preprocessing.md](03_image_preprocessing.md) | Grayscale, threshold, deskew, denoise |
| Day 5-6 | [04_pdf_processing.md](04_pdf_processing.md) | PDF text layer, PDF to image, PyMuPDF, pdfplumber |
| Day 7 | [05_cloud_ocr_chunking.md](05_cloud_ocr_chunking.md) | Cloud OCR, text cleaning, chunking |
| Project | [06_ocr_pipeline_project.md](06_ocr_pipeline_project.md) | Mini project tong hop Week 2 |

## Cach hoc moi ngay

1. Doc dinh nghia.
2. Chay vi du nho.
3. So sanh input va output.
4. Lam bai tap.
5. Tick checklist.

## Deliverable cuoi tuan

Project dau ra da tao o `../week2_project/`.

```text
week2_project/
  input/
    sample_document.txt
  output/
    extracted_text.txt
    chunks.json
  src/
    main.py
    ocr_engine.py
    pdf_processor.py
    image_preprocessor.py
    chunker.py
```

Chay project:

```powershell
cd ../week2_project
python src/main.py
```

Tieu chi dat:

- Doc duoc input document.
- Trich xuat text ra `output/extracted_text.txt`.
- Clean text co ban.
- Chunk text ra `output/chunks.json`.
- Code tach theo module.
- Co README ngan huong dan chay.

