# Анти-паттерн: "try-except вместо suppress"

***

Иногда требуется игнорировать исключение.
Вместо блока try except игнорировать ошибку лучше с помощью контекстного менеджера suppress.

***

### Пример 

**Плохо:**
```python
try:
    do_something()
except NotImportantError:
    pass
```
**Плохо:**
```python
try:
    do_something()
except NotImportantError:
    continue
```
**Хорошо:**
```python
from contextlib import suppress

with suppress(NotImportantError):
    do_something()
```

