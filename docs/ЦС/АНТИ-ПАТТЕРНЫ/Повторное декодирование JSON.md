
<div>
    <h1 style="margin: 0;">Повторное декодирование JSON</h1>
    <p style="margin: 0;">Анти-паттерн</p>
</div>

***

Превращение JSON строки в структуру данных Python требует много процессорного времени. Этот ресурс не безграничен, поэтому нельзя допустить, чтобы программа транжирила его на неоправдано частые вызовы метода `response.json()`.

***

### Пример 

**Плохо:**
```python
...
for vacancy in response.json()['items']:
    ...
pages = response.json()['pages']
...
```
**Хорошо:**
```python
...
payload = response.json()
for vacancy in payload['items']:
    ...
pages = payload['pages']
...
```

