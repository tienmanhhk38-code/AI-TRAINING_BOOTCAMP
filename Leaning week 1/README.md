# Week 1 - Python Foundation

Nguon lo trinh: `../Week_1_Python_Foundation_Learning.md`

Muc tieu Week 1: viet duoc Python automation script theo flow:

```text
Input CSV -> Validate/Clean Data -> Call API -> Enrich Data -> Export Report
```

## Danh sach bai hoc

| Ngay | File | Noi dung |
| --- | --- | --- |
| Day 1 | [01_python_syntax_data_types.md](01_python_syntax_data_types.md) | Python syntax, bien, kieu du lieu, operator, f-string, condition |
| Day 2 | [02_lists_dicts_functions_loops_lambda.md](02_lists_dicts_functions_loops_lambda.md) | List, dictionary, loop, function, lambda, list comprehension |
| Day 3 | [03_oop_modules_error_handling.md](03_oop_modules_error_handling.md) | Module, class, object, inheritance, error handling |
| Day 4 | [04_csv_json_file_handling.md](04_csv_json_file_handling.md) | File path, open, CSV, JSON, encoding |
| Day 5 | [05_pandas_regex.md](05_pandas_regex.md) | Pandas, DataFrame, clean data, Regex validation |
| Day 6 | [06_api_environment_pip_venv.md](06_api_environment_pip_venv.md) | venv, pip, requirements, requests, dotenv, API error handling |
| Day 7 | [07_mini_project_csv_process_api_report.md](07_mini_project_csv_process_api_report.md) | Mini project tong hop Week 1 |

## Cach hoc moi ngay

1. Doc phan dinh nghia.
2. Chay tung vi du code.
3. Tu sua input va quan sat output.
4. Lam bai tap cuoi file.
5. Tick checklist truoc khi sang ngay tiep theo.

## Deliverable cuoi tuan

Project dau ra da tao o `../week1_project/`.

```text
week1_project/
  .env
  requirements.txt
  input/
    customers.csv
  output/
    report.csv
    report.json
  src/
    main.py
    api_client.py
    processor.py
```

Chay project:

```powershell
cd ../week1_project
python src/main.py
```

Tieu chi dat:

- Chay bang mot lenh: `python src/main.py`.
- Doc CSV that tu `input/customers.csv`.
- Validate du lieu loi: email sai, `customer_id` sai, API loi.
- Goi API bang `requests`.
- Ghi report ra CSV/JSON:
  - `output/report.csv`
  - `output/report.json`
- Khong hardcode API key, doc config tu `.env`.
- Co README ngan huong dan chay.

Project mau cu trong bai hoc:

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
