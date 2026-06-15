# Week 1 Project - CSV to API Report

Project dau ra Week 1: doc CSV, validate du lieu, goi API bang `requests`, va ghi report ra CSV/JSON.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Environment

File `.env`:

```text
API_BASE_URL=https://jsonplaceholder.typicode.com
API_KEY=
```

`API_KEY` de trong vi API demo khong can key. Neu dung API that, dien key vao `.env`, khong hardcode trong code.

## Run

```powershell
python src/main.py
```

## Output

```text
output/report.csv
output/report.json
```

