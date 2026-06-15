# Day 4 - CSV/JSON File Handling

## Muc tieu

Doc/ghi file du lieu co cau truc, chuan bi cho cac bai OCR/RAG phia sau.

## 1. File path

### Dinh nghia

File path la duong dan den file. Nen tach input va output ra thu muc rieng.

### Vi du

```python
from pathlib import Path

base_dir = Path(__file__).resolve().parent
input_path = base_dir / "data" / "students.csv"
output_path = base_dir / "output" / "students_report.json"

print(input_path)
print(output_path)
```

## 2. `open()`

### Dinh nghia

`open()` dung de doc/ghi file text. Nen dung encoding `utf-8`.

### Vi du

```python
with open("note.txt", "w", encoding="utf-8") as file:
    file.write("Hello file")

with open("note.txt", "r", encoding="utf-8") as file:
    content = file.read()

print(content)
```

## 3. CSV

### Dinh nghia

CSV la file bang dang text, moi row la mot dong, moi cot cach nhau bang dau phay. Khi doc CSV bang Python, gia tri thuong la string.

### Vi du doc CSV

```python
import csv

with open("data/students.csv", "r", encoding="utf-8", newline="") as file:
    reader = csv.DictReader(file)
    rows = list(reader)

print(rows)
```

### Vi du ghi CSV

```python
import csv

rows = [
    {"name": "An", "status": "pass"},
    {"name": "Binh", "status": "review"},
]

with open("output/report.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["name", "status"])
    writer.writeheader()
    writer.writerows(rows)
```

## 4. JSON

### Dinh nghia

JSON la dinh dang du lieu co cau truc, phu hop de luu list/dict nested va report doc bang code.

### Vi du

```python
import json

rows = [
    {"name": "An", "score": 8, "status": "pass"},
    {"name": "Binh", "score": 6, "status": "review"},
]

with open("output/report.json", "w", encoding="utf-8") as file:
    json.dump(rows, file, ensure_ascii=False, indent=2)
```

## 5. Convert type khi doc CSV

### Dinh nghia

CSV khong giu kieu `int`/`float`. Can convert truoc khi tinh toan hoac so sanh.

### Vi du

```python
row = {"name": "An", "hours": "2.5", "score": "8"}

hours = float(row["hours"])
score = int(row["score"])

print(hours >= 2)
print(score >= 7)
```

## Bai tap

Tao file:

```text
day4_file_handling.py
```

Input file:

```text
data/students.csv
```

Noi dung:

```csv
name,hours,score
An,2.5,8
Binh,1.5,6
Chi,3.0,9
```

Yeu cau:

- Doc `students.csv`.
- Convert `hours` sang `float`.
- Convert `score` sang `int`.
- Them field `status`.
- Export ket qua ra `output/students_report.json`.

## Vi du code

```python
import csv
import json
from pathlib import Path

base_dir = Path(__file__).resolve().parent
input_path = base_dir / "data" / "students.csv"
output_path = base_dir / "output" / "students_report.json"

def get_status(score):
    if score >= 7:
        return "pass"
    return "review"

with open(input_path, "r", encoding="utf-8", newline="") as file:
    reader = csv.DictReader(file)
    rows = []

    for row in reader:
        score = int(row["score"])
        rows.append({
            "name": row["name"],
            "hours": float(row["hours"]),
            "score": score,
            "status": get_status(score),
        })

output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, "w", encoding="utf-8") as file:
    json.dump(rows, file, ensure_ascii=False, indent=2)
```

## Checklist

- Doc duoc CSV.
- Convert dung kieu du lieu.
- Ghi duoc JSON.
- Xu ly file path ro rang.
- Khong ghi de nham file input.

