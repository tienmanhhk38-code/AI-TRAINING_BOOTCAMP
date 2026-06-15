# Day 7 - Mini Project: CSV -> Process -> API -> Report

## Muc tieu

Ghep toan bo ky nang Week 1 thanh mot automation project chay duoc.

## 1. Mo ta project

### Dinh nghia

Mini project la ung dung nho co input, xu ly, goi API va output. Day la ban tap duot cho cac pipeline OCR/RAG sau nay.

### Flow

```text
Input CSV -> Validate Email -> Call API -> Enrich Data -> Export CSV/JSON Report
```

## 2. Cau truc project

### Dinh nghia

Cau truc project giup tach code theo trach nhiem, de doc va de test.

### Vi du

```text
week1_data_api_report/
  .env
  .gitignore
  README.md
  requirements.txt
  data/
    input.csv
  output/
    report.csv
    report.json
  src/
    main.py
    processor.py
    api_client.py
    exporter.py
```

## 3. Input CSV

### Dinh nghia

Input CSV la du lieu nguon. Moi row can duoc validate truoc khi goi API.

### Vi du

File `data/input.csv`:

```csv
name,email,company_id
An,an@example.com,1
Binh,bad-email,2
Chi,chi@example.com,3
```

## 4. API

### Dinh nghia

API la service ben ngoai cung cap du lieu bo sung. Project nay dung `company_id` de goi endpoint user mau.

### Vi du

```text
https://jsonplaceholder.typicode.com/users/{company_id}
```

## 5. Output report

### Dinh nghia

Output report la ket qua sau khi validate, goi API va enrich du lieu.

| Column | Y nghia |
| --- | --- |
| `name` | Ten tu input CSV |
| `email` | Email tu input CSV |
| `company_id` | ID dung de goi API |
| `is_valid_email` | Ket qua validate email |
| `api_name` | Name tra ve tu API |
| `api_email` | Email tra ve tu API |
| `status` | `success`, `invalid_email` hoac `api_error` |

## 6. Function can co

### Dinh nghia

Moi function nen lam mot viec ro rang. Dieu nay giup debug nhanh va de thay doi.

### Vi du skeleton

```python
def load_rows(path):
    pass

def is_valid_email(email):
    pass

def fetch_user(api_base_url, user_id):
    pass

def build_report(input_rows, api_base_url):
    pass

def export_csv(rows, path):
    pass

def export_json(rows, path):
    pass
```

## 7. Vi du implementation rut gon

```python
import csv
import json
import os
import re
from pathlib import Path

import requests
from dotenv import load_dotenv

EMAIL_PATTERN = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

def load_rows(path):
    with open(path, "r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))

def is_valid_email(email):
    return bool(re.match(EMAIL_PATTERN, str(email)))

def fetch_user(api_base_url, user_id):
    response = requests.get(f"{api_base_url}/users/{user_id}", timeout=10)
    response.raise_for_status()
    return response.json()

def build_report(input_rows, api_base_url):
    report_rows = []

    for row in input_rows:
        valid_email = is_valid_email(row["email"])

        report_row = {
            "name": row["name"],
            "email": row["email"],
            "company_id": row["company_id"],
            "is_valid_email": valid_email,
            "api_name": "",
            "api_email": "",
            "status": "invalid_email",
        }

        if valid_email:
            try:
                user = fetch_user(api_base_url, row["company_id"])
            except requests.RequestException:
                report_row["status"] = "api_error"
            else:
                report_row["api_name"] = user.get("name", "")
                report_row["api_email"] = user.get("email", "")
                report_row["status"] = "success"

        report_rows.append(report_row)

    return report_rows

def export_csv(rows, path):
    if not rows:
        return

    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

def export_json(rows, path):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(rows, file, ensure_ascii=False, indent=2)

def main():
    load_dotenv()

    api_base_url = os.getenv("API_BASE_URL")
    if not api_base_url:
        raise RuntimeError("API_BASE_URL is missing")

    base_dir = Path(__file__).resolve().parent.parent
    input_path = base_dir / "data" / "input.csv"
    output_dir = base_dir / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    input_rows = load_rows(input_path)
    report_rows = build_report(input_rows, api_base_url)

    export_csv(report_rows, output_dir / "report.csv")
    export_json(report_rows, output_dir / "report.json")

if __name__ == "__main__":
    main()
```

## 8. README can co

### Dinh nghia

README giup nguoi khac setup va chay project dung cach.

### Vi du

````markdown
# Week 1 Data API Report

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Environment

Create `.env`:

```text
API_BASE_URL=https://jsonplaceholder.typicode.com
```

## Run

```powershell
python src/main.py
```
````

## Acceptance checklist

- Project chay bang mot command.
- Input CSV duoc doc dung.
- Email sai format duoc phat hien.
- API chi duoc goi cho row hop le.
- API loi khong lam crash toan bo script.
- CSV report duoc tao.
- JSON report duoc tao.
- `.env` duoc su dung.
- `requirements.txt` ton tai.
- README co huong dan setup va run command.
