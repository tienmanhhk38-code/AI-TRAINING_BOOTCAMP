# Day 2-3 - Basic OCR: Tesseract, pytesseract, EasyOCR

## Muc tieu

Hieu OCR la gi va biet cach trich xuat text tu image bang Tesseract/pytesseract hoac EasyOCR.

## 1. OCR

### Dinh nghia

OCR la Optical Character Recognition. No chuyen chu trong anh hoac scan PDF thanh text may doc duoc.

### Vi du

```text
Input image: anh hoa don
Output text: "Invoice No: INV-001 Total: 120000"
```

## 2. Tesseract

### Dinh nghia

Tesseract la OCR engine open-source. `pytesseract` la Python wrapper goi Tesseract tu Python.

### Cai dat package Python

```powershell
python -m pip install pytesseract pillow
```

Tesseract engine can cai rieng tren may. Neu chua cai engine, `pytesseract` se import duoc nhung khong OCR duoc.

### Vi du code

```python
from PIL import Image
import pytesseract

image = Image.open("input/sample_image.png")
text = pytesseract.image_to_string(image, lang="eng")

print(text)
```

## 3. EasyOCR

### Dinh nghia

EasyOCR la OCR library Python co san model OCR cho nhieu ngon ngu. Cai dat de hon ve API, nhung package nang hon.

### Cai dat

```powershell
python -m pip install easyocr
```

### Vi du code

```python
import easyocr

reader = easyocr.Reader(["en"])
results = reader.readtext("input/sample_image.png")

for bbox, text, confidence in results:
    print(text, confidence)
```

## 4. Multi-language OCR

### Dinh nghia

Multi-language OCR la nhan dien nhieu ngon ngu trong mot anh, vi du tieng Anh + tieng Viet.

### Vi du EasyOCR

```python
import easyocr

reader = easyocr.Reader(["en", "vi"])
results = reader.readtext("input/vietnamese_invoice.png")

text_lines = [item[1] for item in results]
print("\n".join(text_lines))
```

## 5. OCR Output Quality

### Dinh nghia

OCR output thuong co loi: sai ky tu, mat dau, xuong dong sai, thua space. Can clean text truoc khi dua vao RAG.

### Vi du clean nho

```python
def clean_ocr_text(text):
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    return "\n".join(lines)

raw_text = " Invoice No: 001 \\n\\n Total: 120000   "
print(clean_ocr_text(raw_text))
```

## Bai tap

Tao file:

```text
day2_basic_ocr.py
```

Yeu cau:

- Doc 1 image tu folder `input/`.
- OCR bang Tesseract hoac EasyOCR.
- In raw text.
- Clean text co ban.
- Ghi ket qua ra `output/ocr_text.txt`.

## Checklist

- Giai thich duoc OCR la gi.
- Biet Tesseract va pytesseract khac nhau the nao.
- Biet EasyOCR phu hop khi nao.
- OCR duoc 1 image don gian.
- Clean duoc text sau OCR.

