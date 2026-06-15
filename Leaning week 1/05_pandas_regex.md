# Day 5 - Pandas Basics & Regex

## Muc tieu

Dung Pandas va Regex de clean, validate, transform du lieu dang bang.

## 1. Pandas

### Dinh nghia

Pandas la thu vien Python dung de xu ly du lieu dang bang. Object quan trong nhat la `DataFrame`.

### Vi du

```python
import pandas as pd

df = pd.DataFrame([
    {"name": "An", "hours": 2.5, "score": 8},
    {"name": "Binh", "hours": 1.5, "score": 6},
])

print(df)
```

## 2. DataFrame

### Dinh nghia

DataFrame la bang co hang va cot, gan giong Excel/CSV.

### Vi du

```python
print(df["name"])
print(df[["name", "score"]])
```

## 3. `read_csv()`

### Dinh nghia

`read_csv()` doc file CSV thanh DataFrame.

### Vi du

```python
import pandas as pd

df = pd.read_csv("data/contacts.csv")
print(df.head())
print(df.shape)
```

## 4. Filter row

### Dinh nghia

Filter row la chon cac dong thoa dieu kien.

### Vi du

```python
committed = df[df["hours"] >= 2]
print(committed)
```

## 5. Tao cot moi

### Dinh nghia

Tao cot moi giup bo sung ket qua tinh toan, validation hoac status.

### Vi du

```python
df["status"] = df["score"].apply(lambda score: "pass" if score >= 7 else "review")
print(df)
```

## 6. Regex

### Dinh nghia

Regex la cach mo ta pattern cua chuoi. Regex thuong dung de validate email, phone, ma ho so, hoac clean text.

### Vi du validate email

```python
import re

pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

print(bool(re.match(pattern, "an@example.com")))
print(bool(re.match(pattern, "bad-email")))
```

### Vi du normalize phone

```python
import re

phone = "090-123 4567"
normalized = re.sub(r"[\s-]", "", phone)

print(normalized)
```

## Bai tap

Tao file:

```text
day5_pandas_regex.py
```

Input file:

```text
data/contacts.csv
```

Noi dung:

```csv
name,email,phone,hours
An,an@example.com,090-123-4567,2.5
Binh,bad-email,091 222 3333,1.5
Chi,chi@example.com,invalid-phone,3.0
```

Yeu cau:

- Load CSV bang Pandas.
- Them cot `is_valid_email`.
- Them cot `is_valid_phone`.
- Normalize phone number bang cach xoa space va hyphen.
- Filter cac dong hop le.
- Export ra `output/valid_contacts.csv`.

## Vi du code

```python
import re
from pathlib import Path

import pandas as pd

base_dir = Path(__file__).resolve().parent
input_path = base_dir / "data" / "contacts.csv"
output_path = base_dir / "output" / "valid_contacts.csv"

email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
phone_pattern = r"^0\d{9}$"

def is_valid_email(email):
    return bool(re.match(email_pattern, str(email)))

def normalize_phone(phone):
    return re.sub(r"[\s-]", "", str(phone))

def is_valid_phone(phone):
    return bool(re.match(phone_pattern, phone))

df = pd.read_csv(input_path)
df["normalized_phone"] = df["phone"].apply(normalize_phone)
df["is_valid_email"] = df["email"].apply(is_valid_email)
df["is_valid_phone"] = df["normalized_phone"].apply(is_valid_phone)

valid_df = df[df["is_valid_email"] & df["is_valid_phone"]]

output_path.parent.mkdir(parents=True, exist_ok=True)
valid_df.to_csv(output_path, index=False)

print(f"Input rows: {len(df)}")
print(f"Valid rows: {len(valid_df)}")
```

## Checklist

- Load duoc du lieu bang Pandas.
- Tao duoc computed column.
- Validate duoc email/phone bang Regex.
- Export duoc cleaned CSV.
- Biet kiem tra so dong truoc/sau khi filter.

