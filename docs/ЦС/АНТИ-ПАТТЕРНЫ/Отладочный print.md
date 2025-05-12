# Анти-паттерн: "Отладочный print"

***

Отладочных print вообще не должно быть в рабочем коде. Если что-то нужно выводить в консоль, используйте logging.

***

### Пример 1

**Плохо:**
```python
def do_something(value):
    print(value)
    ...
```
**Хорошо:**
```python
def do_something(value):
    ...
```
***

### Пример 2

**Плохо:**
```python
try:
    do_something()
except AnyException as err:
    print(err)
```
**Хорошо:**
```python
try:
    do_something()
except AnyException as err:
    logging.error(err)
```

