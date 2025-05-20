
<div class="sticky-header">
  <div>
    <h1 style="margin: 0;">null=True или blank=True вместе с default</h1>
    <p style="margin: 0;">Анти-паттерн</p>
  </div>
</div>
***

Сочетание `null=True` или `blank=True` вместе с `default` значением должно настораживать, поскольку может вызывать сложное и неявное поведение.

***

### Пример 1

Если для поля предусмотрено значение `default`, то параметр `null=True` в большинстве случаев становится избыточным, так как при отсутствии значения поле всегда получит значение по умолчанию, и в базе не окажется `NULL`. Это может привести к двусмысленности, когда логически отсутствующее значение может быть представлено и как `default`, и как `NULL`, что снижает читаемость кода и усложняет логику.


                                    **Плохо:**

                                    ```python
                                    from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, default="Unknown")
                                    ```


                                    **Хорошо:**

                                    ```python
                                    from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100, blank=True, default="Unknown")
                                    ```

***

### Пример 2

В Django параметр `blank=True` позволяет форме принимать пустые значения для этого поля, то есть разрешает оставить это поле пустым при заполнении формы. `blank=True` должен использоваться только при необходимости разрешить пустое значение при валидации формы. Если пользователь оставит поле `name` пустым в форме, то в валидированной форме пустая строка будет заменена на значение по умолчанию "Unknown".

```python
from django.db import models


class Product(models.Model):
name = models.CharField(max_length=100, blank=True, default="Unknown")

def __str__(self):
return self.name
```


