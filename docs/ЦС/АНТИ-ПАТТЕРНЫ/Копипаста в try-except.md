
<div>
    <h1 style="margin: 0;">Копипаста в try-except</h1>
    <p style="margin: 0;">Анти-паттерн</p>
</div>

***

Избегайте использования нескольких `except` блоков для идентичной обработки разных исключений.
Если ошибки похожи, то лучше обрабатывать их в одном блоке except - такой подход позволяет уменьшить кол-во кода и улучшить читаемость.

***

### Пример 

**Плохо:**
```python
try:
    do_something()
except ValueError:
    logging.error('Value error')
except IndexError:
    logging.error('Index error')
```
**Хорошо:**
```python
try:
    do_something()
except (ValueError, IndexError) as e:
    logging.error(f'Error: {e}')
```

