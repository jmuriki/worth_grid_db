
<div>
    <h1 style="margin: 0;">Злоупотребление if-elif-else</h1>
    <p style="margin: 0;">Анти-паттерн</p>
</div>

***

Если при использовании if-elif-else данных много и они похожи, то лучше использовать циклы или словари. Это уменьшит количество кода, позволит править логику сразу для всех случаев и улучшит читаемость.

***

### Пример 1

**Плохо:**
```python
customer_type = ...

if customer_type == "bronze":
    discount = 5
elif customer_type == "silver":
    discount = 10
elif customer_type == "gold":
    discount = 15
elif customer_type == "platinum":
    discount = 20
else:
    discount = 0
```
**Хорошо:**
```python
customer_type = ...

discounts = {
    "bronze": 5,
    "silver": 10,
    "gold": 15,
    "platinum": 20,
}

discount = discounts.get(customer_type, 0)
```
***

### Пример 2

**Плохо:**
```python
def get_month(month_number):
    if month_number == 1:
        return 'Январь'
    elif month_number == 2:
        return 'Февраль'
    elif month_number == 3:
        return 'Март'
    ...
    else:
        return 'Неверный номер месяца'

month_name = get_month_name(3)
```
**Хорошо:**
```python
def get_month(month_number):
    months = {
        1: 'Январь',
        2: 'Февраль',
        3: 'Март',
        ...
    }
    return months.get(month_number, 'Неверный номер месяца')

month_name = get_month_name(3)
```

