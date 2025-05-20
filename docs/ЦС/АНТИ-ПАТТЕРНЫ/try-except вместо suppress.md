
<div class="sticky-header">
  <div>
    <h1 style="margin: 0;">try-except вместо suppress</h1>
    <p style="margin: 0;">Анти-паттерн</p>
  </div>
</div>
***

Иногда требуется игнорировать исключение.
Вместо блока try except игнорировать ошибку лучше с помощью контекстного менеджера suppress.

***

### Пример 


                                    **Плохо:**

                                    ```python
                                    try:
    do_something()
except NotImportantError:
    pass
                                    ```


                                    **Плохо:**

                                    ```python
                                    try:
    do_something()
except NotImportantError:
    continue
                                    ```


                                    **Хорошо:**

                                    ```python
                                    from contextlib import suppress

with suppress(NotImportantError):
    do_something()
                                    ```


