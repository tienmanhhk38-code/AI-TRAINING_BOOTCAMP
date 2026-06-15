# Day 6 - API, Environment, pip, venv

## Muc tieu

Setup project Python sach va goi duoc API ben ngoai.

## 1. Virtual environment

### Dinh nghia

Virtual environment la moi truong Python rieng cho tung project. No giup dependency cua cac project khong lan vao nhau.

### Vi du

Tao venv:

```powershell
python -m venv .venv
```

Activate tren PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

## 2. pip

### Dinh nghia

`pip` la tool cai package Python.

### Vi du

```powershell
pip install requests python-dotenv
```

Luu dependency:

```powershell
pip freeze > requirements.txt
```

Cai lai dependency tu file:

```powershell
pip install -r requirements.txt
```

## 3. `.env`

### Dinh nghia

`.env` la file luu config local nhu API base URL hoac API key. Khong nen hardcode config trong code.

### Vi du `.env`

```text
API_BASE_URL=https://jsonplaceholder.typicode.com
```

### Vi du doc `.env`

```python
import os
from dotenv import load_dotenv

load_dotenv()

api_base_url = os.getenv("API_BASE_URL")
print(api_base_url)
```

## 4. requests

### Dinh nghia

`requests` la thu vien dung de goi HTTP API.

### Vi du

```python
import requests

response = requests.get(
    "https://jsonplaceholder.typicode.com/users",
    timeout=10,
)

response.raise_for_status()
users = response.json()

for user in users:
    print(user["name"], user["email"])
```

## 5. API error handling

### Dinh nghia

API co the loi do timeout, mat mang, status 4xx/5xx, hoac response khong dung format. Code can bat loi de script khong crash vo nghia.

### Vi du

```python
import requests

try:
    response = requests.get(
        "https://jsonplaceholder.typicode.com/users",
        timeout=10,
    )
    response.raise_for_status()
except requests.Timeout:
    print("API timeout")
except requests.HTTPError as error:
    print(f"API returned bad status: {error}")
except requests.RequestException as error:
    print(f"API request failed: {error}")
else:
    print(response.json())
```

## Bai tap

Tao file:

```text
day6_api_environment.py
```

Public API:

```text
https://jsonplaceholder.typicode.com/users
```

File `.env`:

```text
API_BASE_URL=https://jsonplaceholder.typicode.com
```

Yeu cau:

- Load `API_BASE_URL` tu `.env`.
- Call endpoint `/users`.
- In ra name va email cua users.
- Handle request timeout.
- Handle response status loi.

## Vi du code

```python
import os

import requests
from dotenv import load_dotenv

load_dotenv()

api_base_url = os.getenv("API_BASE_URL")

if not api_base_url:
    raise RuntimeError("API_BASE_URL is missing")

try:
    response = requests.get(f"{api_base_url}/users", timeout=10)
    response.raise_for_status()
except requests.Timeout:
    print("API timeout")
except requests.HTTPError as error:
    print(f"API returned bad status: {error}")
except requests.RequestException as error:
    print(f"API request failed: {error}")
else:
    users = response.json()
    for user in users:
        print(f'{user["name"]} - {user["email"]}')
```

## Checklist

- Tao va activate duoc virtual environment.
- Cai duoc package bang `pip`.
- Tao duoc `requirements.txt`.
- Goi API bang `requests`.
- Doc duoc `.env`.
- Co timeout khi goi API.
- Co xu ly loi API co ban.

