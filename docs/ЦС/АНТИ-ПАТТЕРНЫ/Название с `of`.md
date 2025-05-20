
<div class="sticky-header">
  <div>
    <h1 style="margin: 0;">Название с `of`</h1>
    <p style="margin: 0;">Анти-паттерн</p>
  </div>
</div>
***

Названия переменных не должны быть слишком длинными или содержать излишнюю информацию, если того не требует контекст. Предлог `of` создаёт избыточность в названии. При формировании составных названий для переменных принято помещать главное слово в конец. Использование `of` нарушает этот принцип, так как главное слово становиться первым.

***

### Пример 1


**Плохо:**

```python
number_of_active_users = ...
```


**Хорошо:**

```python
active_users_num = ...
```

***

### Пример 2


                                **Плохо:**

                                ```python
                                def get_info_of_user(user_id):
...
                                ```


                                **Хорошо:**

                                ```python
                                def get_user_info(user_id):
...
                                ```

***

### Пример 3


                                **Плохо:**

                                ```python
                                class ProductOfCompany:
def __init__(self, name, price):
    self.name = name
    self.price = price
                                ```


                                **Хорошо:**

                                ```python
                                class Product:
def __init__(self, name, price):
    self.name = name
    self.price = price
                                ```


