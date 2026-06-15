# Day 3 - OOP, Modules, Error Handling

## Muc tieu

Biet to chuc code thanh module va class don gian de project khong bi don vao mot file.

## 1. Module

### Dinh nghia

Module la mot file Python co the duoc import vao file khac. Module giup chia code theo trach nhiem.

### Vi du

File `report.py`:

```python
def get_status(score):
    if score >= 7:
        return "pass"
    return "review"
```

File `main.py`:

```python
from report import get_status

print(get_status(8))
```

## 2. Class va object

### Dinh nghia

Class la ban thiet ke. Object la mot instance duoc tao tu class. Class phu hop khi du lieu va hanh vi di chung voi nhau.

### Vi du

```python
class Student:
    def __init__(self, name, hours, score):
        self.name = name
        self.hours = hours
        self.score = score

    def is_committed(self):
        return self.hours >= 2

    def status(self):
        if self.score >= 7:
            return "pass"
        return "review"

student = Student("An", 2.5, 8)
print(student.name)
print(student.is_committed())
print(student.status())
```

## 3. `__init__`

### Dinh nghia

`__init__` la method khoi tao, chay khi tao object moi.

### Vi du

```python
class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url

client = ApiClient("https://jsonplaceholder.typicode.com")
print(client.base_url)
```

## 4. Inheritance

### Dinh nghia

Inheritance cho phep class con ke thua attribute/method tu class cha. Chi nen dung khi quan he "is-a" ro rang.

### Vi du

```python
class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, score):
        super().__init__(name)
        self.score = score

student = Student("An", 8)
print(student.name)
print(student.score)
```

## 5. Error handling

### Dinh nghia

Error handling dung `try`, `except`, `raise` de xu ly loi co kiem soat. Script tot can bao loi ro rang thay vi crash kho hieu.

### Vi du

```python
def validate_score(score):
    if score < 0 or score > 10:
        raise ValueError("score must be between 0 and 10")
    return score

try:
    validate_score(12)
except ValueError as error:
    print(f"Invalid data: {error}")
```

## Bai tap

Tao cau truc:

```text
day3_oop_modules/
  main.py
  student.py
  report.py
```

Yeu cau:

- `student.py`: tao class `Student` co `name`, `hours`, `score`.
- `Student.is_committed()` tra ve `True` neu `hours >= 2`.
- `Student.status()` tra ve `"pass"` neu `score >= 7`, nguoc lai `"review"`.
- `report.py`: tao function `build_summary(students)`.
- `main.py`: tao danh sach student, build summary, print ket qua.
- Raise `ValueError` neu score nam ngoai khoang 0-10.

## Vi du code

File `student.py`:

```python
class Student:
    def __init__(self, name, hours, score):
        if score < 0 or score > 10:
            raise ValueError("score must be between 0 and 10")

        self.name = name
        self.hours = hours
        self.score = score

    def is_committed(self):
        return self.hours >= 2

    def status(self):
        if self.score >= 7:
            return "pass"
        return "review"
```

File `report.py`:

```python
def build_summary(students):
    rows = []

    for student in students:
        rows.append({
            "name": student.name,
            "committed": student.is_committed(),
            "status": student.status(),
        })

    return rows
```

File `main.py`:

```python
from student import Student
from report import build_summary

students = [
    Student("An", 2.5, 8),
    Student("Binh", 1.5, 6),
]

summary = build_summary(students)
print(summary)
```

## Checklist

- Import duoc code tu file khac.
- Tao va dung duoc class.
- Biet raise/catch error.
- Tach code thanh module nho.
- Hieu khac biet co ban giua function va class.

