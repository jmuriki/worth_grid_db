
<div class="sticky-header">
  <div>
    <h1 style="margin: 0;">Избегание list comprehensions</h1>
    <p style="margin: 0;">Анти-паттерн</p>
  </div>
</div>
***

List comprehensions позволяют легко создавать коллекции, но использовать данный функционал рекомендуется только для простых циклов for.

***

### Пример 1


                                    **Плохо:**

                                    ```python
                                    comments = []
for comment in tag_comments:
    comments.append(comment.find('span').text)
                                    ```


**Хорошо:**

```python
comments = [comment.find('span').text for comment in tag_comments]
```

***

### Пример 2


                                    **Плохо:**

                                    ```python
                                    numbers = [...]
even_numbers = []
for number in numbers:
    if number % 2 == 0:
        even_numbers.append(number)
                                    ```


                                    **Хорошо:**

                                    ```python
                                    numbers = [...]
even_numbers = [num for num in numbers if num % 2 == 0]
                                    ```


