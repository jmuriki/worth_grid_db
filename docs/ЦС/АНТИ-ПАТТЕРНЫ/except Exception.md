
<div>
    <h1 style="margin: 0;">except Exception</h1>
    <p style="margin: 0;">Анти-паттерн</p>
</div>

***

Не рекомендуется использовать базовое исключение `Exception` вместо того, чтобы избирательно и целенаправленно отлавливать и обрабатывать ошибки.
Как максимум, оно может быть использовано в дополнение к ожидаемым исключениям.
Бывают ситуации, когда могут возникнуть неожиданные исключения, и тогда в завершающем `except` можно ловить `Exception`.

***

### Пример 

Если ловятся исключения, не связанные с основной идеей защищаемого участка кода, непредвиденные ситуации могут случайно быть подавлены, а программа продолжит работу в некорректном состоянии.

**Плохо:**
```python
try:
    do_something()
except Exception:
    logging.error('Произошла ошибка')
```
**Допустимо:**
```python
try:
    do_something()
except FileNotFoundError:
    logging.error('Файл не найден!')
except PermissionError:
    logging.error('Нет прав доступа к файлу!')
except Exception as e:
    logging.error(f'Произошла ошибка: {e}.')
```
**Хорошо:**
```python
try:
    do_something()
except FileNotFoundError:
    logging.error('Файл не найден!')
except PermissionError:
    logging.error('Нет прав доступа к файлу!')
```

