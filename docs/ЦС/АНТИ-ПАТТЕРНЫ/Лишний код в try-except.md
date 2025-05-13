
<div>
    <h1 style="margin: 0;">Лишний код в try-except</h1>
    <p style="margin: 0;">Анти-паттерн</p>
</div>

***

Когда в блоке `try-except` оказывается слишком много кода, помимо тех операций, которые действительно могут выбросить исключение, или когда в `try-except` оборачивает участок кода, в котором исключения не ожидаются вовсе, возникает целый ряд проблем.

***

### Пример 1

Если операторы не предполагают возможного возникновения исключений, то их оборачивание в  `try-except` является избыточным.

**Плохо:**
```python
def get_percent(payload):
    try:
        number = float(payload)  # Преобразование данных (может вызвать ValueError)
        logger.info("Обработка числа:", number) # Логирование обычно не вызывает исключений
        result = number * 100 # Дополнительная логика, не связанная напрямую с преобразованием
    except ValueError as err:
        logger.error("Произошла ошибка:", err)
        result = None
    return result
```
**Хорошо:**
```python
def get_percent(payload):
    try:
        number = float(payload)
    except ValueError as err:
        logger.error("Произошла ошибка:", err)
        return

    logger.info("Обработка числа:", number)
    return number * 100
```
***

### Пример 2

Операции, которые не предполагают возникновения исключений, не нуждаются в подстраховке.

**Плохо:**
```python
try:
    first_word = "Привет"
    second_word = "мир"
    whole_phrase = f"{first_word}, {second_word}!"
    print(whole_phrase)
except Exception as err:
    print("Произошло исключение:", err)
```
**Хорошо:**
```python
first_word = "Привет"
second_word = "мир"
whole_phrase = f"{first_word}, {second_word}!"
print(whole_phrase)
```

