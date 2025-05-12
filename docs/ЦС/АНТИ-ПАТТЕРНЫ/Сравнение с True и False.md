# Анти-паттерн: "Сравнение с True и False"

***

Зачем сравнивать bool-переменную с True или False, когда Python позволяет писать лаконичный код? Следует пользоваться данной возможностью.

***

### Пример 

Сравнивать с `True` имеет смысл только если есть вероятность, что переменная содержит ненулевое значение, отличное от `True`. Сравнивать с `False` имеет смысл только если есть вероятность, что переменная содержит пустую коллекцию или `None`.

**Плохо:**
```python
is_active = True
...

if is_active == True:
    do_something()
```
**Плохо:**
```python
is_active = False
...

if is_active == False:
    do_something()
```
**Хорошо:**
```python
is_active = True

if is_active:
    do_something()
```
**Хорошо:**
```python
is_active = False

if not is_active:
    do_something()
```

