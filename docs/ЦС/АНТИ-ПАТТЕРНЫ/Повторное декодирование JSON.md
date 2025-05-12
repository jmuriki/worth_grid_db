# Анти-паттерн: "Повторное декодирование JSON"

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

