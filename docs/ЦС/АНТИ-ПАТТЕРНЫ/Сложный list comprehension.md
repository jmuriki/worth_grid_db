
<div class="sticky-header">
  <div>
    <h1 style="margin: 0;">Сложный list comprehension</h1>
    <p style="margin: 0;">Анти-паттерн</p>
  </div>
</div>
***

`List comprehension` в `Python` – мощный инструмент для создания списков, позволяющий написать лаконичный и элегантный код. Однако, когда в одном `list comprehension` выполняется слишком много действий – например, вложенные вычисления, условные операторы, множественные вложенные циклы или побочные эффекты – это приводит к ухудшению читаемости и поддерживаемости кода.

***

### Пример 

Данный `list comprehension` не только фильтрует элементы и создает кортеж с двумя значениями, но и содержит вызов логгера. Такой код трудно читать и понимать, что может привести к проблемам при модификации логики.


                                    **Плохо:**

                                    ```python
                                    numbers = [1, 2, 3, 4, 5]

result = [(num * 2, num ** 2) for num in numbers if (num % 2 == 0) and (logger.info(f"Processing {num}") or True)]
                                    ```


                                    **Хорошо:**

                                    ```python
                                    numbers = [1, 2, 3, 4, 5]
result = []

for num in numbers:
    if num % 2 == 0:
        logger.info(f"Processing {num}")
        doubled_num = num * 2
        squared_num = num ** 2
        result.append((doubled_num, squared_num))
                                    ```


