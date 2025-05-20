
<div class="sticky-header">
  <div>
    <h1 style="margin: 0;">Обёртка над requests</h1>
    <p style="margin: 0;">Анти-паттерн</p>
  </div>
</div>
***

Если функция не упрощает код, то от нее лучше избавиться. Лишняя абстракция затруднит понимание и усложнит внесение правок. Функции полезны, когда они инкапсулируют сложность, прячут её внутри себя и таким образом упрощают внешний код.

***

### Пример 


                                    **Плохо:**

                                    ```python
                                    import requests


def send_request(url):
    response = requests.get(url)
    response.raise_for_status()
    return response


def main():
    ...
    try:
        response = send_request(url)
    except:
        ...
                                    ```


                                    **Хорошо:**

                                    ```python
                                    import requests


def main():
    ...
    try:
        response = requests.get(url)
        response.raise_for_status()
    except:
        ...
                                    ```


