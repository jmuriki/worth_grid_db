
<div>
    <h1 style="margin: 0;">Использование import со звёздочкой</h1>
    <p style="margin: 0;">Анти-паттерн</p>
</div>

***

При использовании `import *` трудно понять, какие именно функции или переменные были импортированы из модуля.

***

### Пример 1

Хорошей практикой является импортирование только тех инструментов, которые необходимы.

**Плохо:**
```python
from math import *
```
**Хорошо:**
```python
from math import sqrt, sin
```
***

### Пример 2

Есть риск, что в разных модулях могут быть функции и/или переменные, которые имеют одинаковые названия, что приведёт к конфликту. Также это может привести к циклическому импорту.

**Плохо:**
```python
from basket_actions import *
from statistics import *
```
**Хорошо:**
```python
from basket_actions import add_product, clear_basket 
from statistics import average_product_price
```

