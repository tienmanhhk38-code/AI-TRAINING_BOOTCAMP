import os
from pathlib import Path

from api_client import ApiClient
from processor import build_report, export_csv, export_json, load_customers


def load_env_file(path):
    try:
        from dotenv import load_dotenv
    except ModuleNotFoundError:
        if not path.exists():
            return

        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())
    else:
        load_dotenv(path)


def main():
    project_dir = Path(__file__).resolve().parent.parent
    load_env_file(project_dir / ".env")

    api_base_url = os.getenv("API_BASE_URL")
    api_key = os.getenv("API_KEY", "")

    if not api_base_url:
        raise RuntimeError("API_BASE_URL is missing in .env")

    input_path = project_dir / "input" / "customers.csv"
    output_dir = project_dir / "output"

    api_client = ApiClient(base_url=api_base_url, api_key=api_key)
    customers = load_customers(input_path)
    report_rows = build_report(customers, api_client)

    export_csv(report_rows, output_dir / "report.csv")
    export_json(report_rows, output_dir / "report.json")

    print(f"Read {len(customers)} customers")
    print(f"Wrote {output_dir / 'report.csv'}")
    print(f"Wrote {output_dir / 'report.json'}")


if __name__ == "__main__":
    main()
