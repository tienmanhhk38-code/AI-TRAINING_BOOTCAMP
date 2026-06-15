# Day 2 - Lists, Dictionaries, Functions, Loops, Lambda

## Muc tieu

Dung data structure va function de xu ly nhieu dong du lieu.

## 1. List

### Dinh nghia

List la tap hop nhieu gia tri theo thu tu. List phu hop khi can luu danh sach hoc vien, danh sach file, danh sach row.

### Vi du

```python
names = ["An", "Binh", "Chi"]

print(names[0])
names.append("Dung")

for name in names:
    print(name)
```

## 2. Dictionary

### Dinh nghia

Dictionary luu du lieu dang key-value. Dictionary phu hop de bieu dien mot object hoac mot row du lieu.

### Vi du

```python
student = {
    "name": "An",
    "hours": 2.5,
    "score": 8,
}

print(student["name"])
print(student.get("email", "no-email"))

student["status"] = "pass"
print(student)
```

## 3. List of dict

### Dinh nghia

List of dict la danh sach cac dictionary. Dang nay rat gan voi du lieu bang CSV/API.

### Vi du

```python
students = [
    {"name": "An", "hours": 2.5, "score": 8},
    {"name": "Binh", "hours": 1.5, "score": 6},
    {"name": "Chi", "hours": 3.0, "score": 9},
]

for student in students:
    print(student["name"], student["score"])
```

## 4. Loop

### Dinh nghia

Loop dung de lap qua tung item trong danh sach. `for` dung nhieu nhat khi xu ly data.

### Vi du

```python
students = [
    {"name": "An", "hours": 2.5},
    {"name": "Binh", "hours": 1.5},
]

for student in students:
    if student["hours"] >= 2:
        print(f'{student["name"]}: committed')
```

## 5. Function

### Dinh nghia

Function gom mot khoi logic co ten, co input va output. Function giup tranh lap code.

### Vi du

```python
def get_status(score):
    if score >= 7:
        return "pass"
    return "review"

print(get_status(8))
print(get_status(6))
```

## 6. Lambda

### Dinh nghia

Lambda la function ngan, thuong dung cho transform hoac sort don gian.

### Vi du

```python
students = [
    {"name": "An", "score": 8},
    {"name": "Binh", "score": 6},
    {"name": "Chi", "score": 9},
]

sorted_students = sorted(students, key=lambda item: item["score"], reverse=True)
print(sorted_students)
```

## 7. List comprehension

### Dinh nghia

List comprehension la cach tao list moi tu list cu ngan gon hon loop thong thuong.

### Vi du

```python
scores = [8, 6, 9]
passed_scores = [score for score in scores if score >= 7]

print(passed_scores)
```

## Bai tap

Tao file:

```text
day2_collections.py
```

Dung du lieu mau:

```python
students = [
    {"name": "An", "hours": 2.5, "score": 8},
    {"name": "Binh", "hours": 1.5, "score": 6},
    {"name": "Chi", "hours": 3.0, "score": 9},
]
```

Yeu cau:

- In ten tat ca hoc vien.
- Loc hoc vien hoc it nhat 2 gio/ngay.
- Tinh diem trung binh.
- Sort hoc vien theo `score` giam dan.
- Them field `status`: `"pass"` neu score >= 7, nguoc lai `"review"`.

## Loi giai goi y

```python
students = [
    {"name": "An", "hours": 2.5, "score": 8},
    {"name": "Binh", "hours": 1.5, "score": 6},
    {"name": "Chi", "hours": 3.0, "score": 9},
]

def get_status(score):
    if score >= 7:
        return "pass"
    return "review"

for student in students:
    student["status"] = get_status(student["score"])

committed_students = [student for student in students if student["hours"] >= 2]
average_score = sum(student["score"] for student in students) / len(students)
sorted_students = sorted(students, key=lambda item: item["score"], reverse=True)

print(committed_students)
print(average_score)
print(sorted_students)
```

## Checklist

- Duyet duoc list of dict.
- Viet duoc function co input/output ro rang.
- Dung duoc loop va condition cung nhau.
- Filter/sort duoc du lieu.
- Biet khi nao nen tach logic thanh function.

