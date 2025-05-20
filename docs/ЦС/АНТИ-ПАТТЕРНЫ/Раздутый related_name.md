
<div class="sticky-header">
  <div>
    <h1 style="margin: 0;">Раздутый related_name</h1>
    <p style="margin: 0;">Анти-паттерн</p>
  </div>
</div>
***

Нет смысла дублировать название модели в related_name - в прикладном коде он и так всегда следует за названием модели данных. Высушите related_name.

***

### Пример 

Сравните масло-масляный вариант и высушенный - очевидно, что короткий вариант лучше, с какой стороны ни посмотри.


                                    **Плохо:**

                                    ```python
                                    from django.db import models

class Owner(models.Model):
    ...
    flats = models.ManyToManyField(
        'Flat',
        verbose_name='Квартиры в собственности',
        related_name='flats_owners',
    )
    ...
                                    ```


                                    **Хорошо:**

                                    ```python
                                    from django.db import models

class Owner(models.Model):
    ...
    flats = models.ManyToManyField(
        'Flat',
        verbose_name='Квартиры в собственности',
        related_name='owners',
    )
    ...
                                    ```


