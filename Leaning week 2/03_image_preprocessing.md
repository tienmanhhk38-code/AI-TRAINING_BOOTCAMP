# Day 4 - Image Preprocessing

## Muc tieu

Biet tien xu ly anh de tang do chinh xac OCR: grayscale, threshold, deskew, denoise.

## 1. Image Preprocessing

### Dinh nghia

Image preprocessing la buoc chinh sua anh truoc OCR de chu ro hon va bot nhieu hon.

### Vi du flow

```text
raw image -> grayscale -> denoise -> threshold -> OCR
```

## 2. Grayscale

### Dinh nghia

Grayscale chuyen anh mau thanh anh xam. OCR thuong khong can mau, chi can text ro.

### Vi du Pillow

```python
from PIL import Image

image = Image.open("input/sample_image.png")
gray = image.convert("L")
gray.save("output/sample_gray.png")
```

## 3. Threshold

### Dinh nghia

Threshold chuyen anh xam thanh trang/den dua tren nguong. Chu ro hon nen OCR de doc hon.

### Vi du Pillow

```python
from PIL import Image

image = Image.open("input/sample_image.png").convert("L")
threshold = 180
binary = image.point(lambda pixel: 255 if pixel > threshold else 0)
binary.save("output/sample_threshold.png")
```

## 4. Denoise

### Dinh nghia

Denoise la giam nhieu trong anh. Anh scan co cham den, bong, noise nen OCR de nhan sai.

### Vi du OpenCV

```python
import cv2

image = cv2.imread("input/sample_image.png", cv2.IMREAD_GRAYSCALE)
denoised = cv2.medianBlur(image, 3)
cv2.imwrite("output/sample_denoised.png", denoised)
```

## 5. Deskew

### Dinh nghia

Deskew la xoay thang anh bi nghieng. OCR doc tot hon khi dong chu nam ngang.

### Vi du y tuong

```text
detect text angle -> rotate image opposite angle -> OCR
```

Deskew day du can OpenCV va xu ly contour/angle. Trong Week 2 chi can hieu muc tieu va thu voi anh don gian.

## 6. Khi nao preprocessing co ich?

| Van de anh | Buoc nen thu |
| --- | --- |
| Anh mau, nen phuc tap | Grayscale |
| Chu mo, nen xam | Threshold |
| Nhieu hat/cham | Denoise |
| Anh bi nghieng | Deskew |
| Chu nho | Resize upscale |

## Bai tap

Tao file:

```text
day4_image_preprocessing.py
```

Yeu cau:

- Doc `input/sample_image.png`.
- Tao anh grayscale.
- Tao anh threshold.
- Neu co OpenCV, tao anh denoised.
- So sanh OCR output truoc va sau preprocessing.

## Checklist

- Hieu preprocessing vi sao can cho OCR.
- Tao duoc anh grayscale.
- Tao duoc anh threshold.
- Biet khi nao can denoise.
- Biet deskew la gi.

