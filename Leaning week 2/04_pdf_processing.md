# Day 5-6 - PDF Processing

## Muc tieu

Biet xu ly PDF theo 2 truong hop: PDF co text layer va PDF scan can OCR.

## 1. PDF text layer

### Dinh nghia

PDF co text layer la PDF ma text co the copy/select duoc. Truong hop nay khong can OCR, chi can extract text.

### Vi du PyMuPDF

```python
import fitz

doc = fitz.open("input/sample.pdf")

for page in doc:
    text = page.get_text("text")
    print(text)
```

## 2. Scanned PDF

### Dinh nghia

Scanned PDF la PDF gom anh scan. Text khong copy duoc. Can render page thanh image roi OCR.

### Vi du flow

```text
PDF page -> image -> preprocessing -> OCR -> text
```

## 3. PyMuPDF render page

### Dinh nghia

PyMuPDF co the render page PDF thanh anh PNG. Anh nay dua vao OCR engine.

### Vi du

```python
import fitz

doc = fitz.open("input/sample.pdf")
page = doc[0]
pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
pix.save("output/page_1.png")
```

## 4. pdfplumber

### Dinh nghia

`pdfplumber` phu hop de extract text va table tu PDF co text layer.

### Vi du

```python
import pdfplumber

with pdfplumber.open("input/sample.pdf") as pdf:
    for page in pdf.pages:
        print(page.extract_text())
        print(page.extract_tables())
```

## 5. Table extraction

### Dinh nghia

Table extraction la lay du lieu bang tu PDF. Ket qua thuong can clean vi cot/dong co the bi lech.

### Vi du output mong muon

```python
[
    ["Product", "Quantity", "Price"],
    ["Keyboard", "2", "500000"],
]
```

## 6. Chon tool nao?

| Truong hop | Tool goi y |
| --- | --- |
| PDF co text layer | PyMuPDF, pdfplumber |
| PDF scan | PyMuPDF render image + OCR |
| PDF co table | pdfplumber |
| PDF can tach page thanh anh | PyMuPDF |

## Bai tap

Tao file:

```text
day5_pdf_processing.py
```

Yeu cau:

- Doc `input/sample.pdf`.
- Thu extract text bang PyMuPDF.
- Neu text rong, render page thanh PNG.
- Ghi text ra `output/pdf_text.txt`.
- Ghi page image ra `output/page_1.png` neu can OCR.

## Checklist

- Phan biet PDF text layer va scanned PDF.
- Extract text duoc tu PDF co text layer.
- Render duoc PDF page thanh image.
- Biet khi nao can OCR.
- Biet pdfplumber dung khi nao.

