# Day 1 - Python Syntax & Basic Data Types

## Muc tieu

Hieu cu phap Python va cac kieu du lieu co ban de viet duoc script nho.

## 1. File Python

### Dinh nghia

File Python la file co duoi `.py`. Python chay code tu tren xuong duoi, tung dong mot.

### Vi du

```python
print("Hello Python")
print("Week 1 - Python Foundation")
```

Chay file:

```powershell
python day1_basics.py
```

## 2. Bien

### Dinh nghia

Bien la ten dung de luu gia tri. Python khong can khai bao kieu du lieu truoc.

### Vi du

```python
name = "An"
age = 25
daily_hours = 2.5
is_active = True

print(name)
print(age)
print(daily_hours)
print(is_active)
```

## 3. Kieu du lieu co ban

### Dinh nghia

Kieu du lieu cho Python biet gia tri dang la chuoi, so, logic hay rong.

| Kieu | Y nghia | Vi du |
| --- | --- | --- |
| `str` | Chuoi ky tu | `"An"` |
| `int` | So nguyen | `25` |
| `float` | So thuc | `2.5` |
| `bool` | Dung/sai | `True`, `False` |
| `None` | Khong co gia tri | `None` |

### Vi du

```python
student_name = "An"
score = 8
hours = 2.5
passed = True
note = None

print(type(student_name))
print(type(score))
print(type(hours))
print(type(passed))
print(type(note))
```

## 4. Convert kieu du lieu

### Dinh nghia

Convert kieu du lieu la chuyen gia tri tu kieu nay sang kieu khac. Du lieu doc tu CSV/API thuong la string, can convert truoc khi tinh toan.

### Vi du

```python
raw_hours = "2.5"
raw_score = "8"

hours = float(raw_hours)
score = int(raw_score)

print(hours + 1)
print(score + 2)
```

## 5. Operator

### Dinh nghia

Operator la toan tu dung de tinh toan, so sanh hoac ket hop dieu kien.

| Nhom | Operator | Vi du |
| --- | --- | --- |
| So hoc | `+`, `-`, `*`, `/` | `2 + 3` |
| So sanh | `==`, `!=`, `>`, `>=`, `<`, `<=` | `score >= 7` |
| Logic | `and`, `or`, `not` | `hours >= 2 and score >= 7` |

### Vi du

```python
hours = 2.5
score = 8

meets_time = hours >= 2
passed = score >= 7
ready = meets_time and passed

print(meets_time)
print(passed)
print(ready)
```

## 6. F-string

### Dinh nghia

F-string la cach format chuoi de chen bien vao text.

### Vi du

```python
name = "An"
hours = 2.5

message = f"Learner {name} studies {hours} hours/day"
print(message)
```

## 7. Condition

### Dinh nghia

Condition dung `if`, `elif`, `else` de re nhanh logic theo dieu kien.

### Vi du

```python
daily_hours = 1.5

if daily_hours >= 2:
    print("Meets commitment")
else:
    print("Needs more study time")
```

## Bai tap

Tao file:

```text
day1_basics.py
```

Yeu cau:

- Khai bao thong tin hoc vien: ten, tuoi, vai tro, so gio hoc moi ngay.
- In summary bang f-string.
- Tinh tong so gio hoc trong 7 ngay.
- Kiem tra hoc vien co dat cam ket toi thieu 2 gio/ngay khong.

Output goi y:

```text
Learner: An
Role: Backend Developer
Daily hours: 2.5
Weekly hours: 17.5
Meets commitment: True
```

## Checklist

- Chay duoc file `.py`.
- Dung duoc bien va kieu du lieu co ban.
- Convert duoc `str`, `int`, `float`.
- Dung duoc f-string.
- Viet duoc dieu kien don gian.

