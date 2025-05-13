
<div>
    <h1 style="margin: 0;">Название vs Path</h1>
    <p style="margin: 0;">Анти-паттерн</p>
</div>

***

Работа с файлами неразрывно связана с путями, названиями файлов и их расширениями. Возьмёшься за одно – понадобится всё остальное. Поэтому малейший промах в названии переменной гарантированно приведёт к путанице.

***

### Пример 1

Если разработчик столкнётся с переменной `filename`, он будет ожидать и другую переменную, содержащую путь к папке с данным файлом, чтобы собрать полный путь.

**Плохо:**
```python
def download_image(url, filename, params=None):
    response = requests.get(url, params=params)
    response.raise_for_status()

    with open(filename, 'wb') as file:
        file.write(response.content)
```
**Хорошо:**
```python
def download_image(url, filepath, params=None):
    response = requests.get(url, params=params)
    response.raise_for_status()

    with open(filepath, 'wb') as file:
        file.write(response.content)
```
***

### Пример 2

**Плохо:**
```python
from pathlib import Path


filename = Path(files_folder_path) / filename
with open(filename, 'r') as file:
    ...
```
**Хорошо:**
```python
from pathlib import Path


filepath = Path(files_folder_path) / filename
with open(filepath, 'r') as file:
    ...
```

