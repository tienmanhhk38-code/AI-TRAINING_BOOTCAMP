import csv
import json
import re


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def load_customers(path):
    with open(path, "r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def is_valid_email(email):
    return bool(EMAIL_PATTERN.match(str(email or "").strip()))


def is_valid_customer_id(customer_id):
    return str(customer_id or "").isdigit()


def validate_customer(row):
    errors = []

    name = str(row.get("name", "")).strip()
    email = str(row.get("email", "")).strip()
    customer_id = str(row.get("customer_id", "")).strip()

    if not name:
        errors.append("missing_name")
    if not is_valid_email(email):
        errors.append("invalid_email")
    if not is_valid_customer_id(customer_id):
        errors.append("invalid_customer_id")

    return {
        "name": name,
        "email": email,
        "customer_id": customer_id,
        "is_valid": not errors,
        "errors": ";".join(errors),
    }


def build_report(customers, api_client):
    report_rows = []

    for raw_customer in customers:
        customer = validate_customer(raw_customer)
        report_row = {
            "name": customer["name"],
            "email": customer["email"],
            "customer_id": customer["customer_id"],
            "is_valid": customer["is_valid"],
            "errors": customer["errors"],
            "api_name": "",
            "api_email": "",
            "api_company": "",
            "status": "invalid_data",
        }

        if customer["is_valid"]:
            try:
                api_customer = api_client.get_customer(customer["customer_id"])
            except Exception as error:
                report_row["errors"] = type(error).__name__
                report_row["status"] = "api_error"
            else:
                report_row["api_name"] = api_customer.get("name", "")
                report_row["api_email"] = api_customer.get("email", "")
                report_row["api_company"] = api_customer.get("company", {}).get("name", "")
                report_row["status"] = "success"

        report_rows.append(report_row)

    return report_rows


def export_csv(rows, path):
    if not rows:
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def export_json(rows, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(rows, file, ensure_ascii=False, indent=2)
