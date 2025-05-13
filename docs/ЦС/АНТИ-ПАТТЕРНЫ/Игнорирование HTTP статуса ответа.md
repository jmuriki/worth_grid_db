
<div>
    <h1 style="margin: 0;">Игнорирование HTTP статуса ответа</h1>
    <p style="margin: 0;">Анти-паттерн</p>
</div>

***

HTTP статус позволяет гарантировать, что запрос был выполнен успешно и сервер вернул ожидаемый ответ. Не проверив HTTP статус ответа, вы рискуете получить неожиданные данные, которые обязательно сломают программу, но уже в другом месте.

***

### Пример 

**Плохо:**
```python
def do_something(url, params):
    response = requests.get(url, params=params)
    ...
```
**Хорошо:**
```python
def do_something(url, params):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        ...
    except requests.exceptions.HTTPError as e:
        logging.error(f'Ошибка HTTPError: {e}')
        ...
    except requests.exceptions.ConnectionError as e:
        logging.error(f'Ошибка ConnectionError: {e}')
        ...
```

