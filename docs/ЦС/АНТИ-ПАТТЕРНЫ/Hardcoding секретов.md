
<div class="sticky-header">
  <div>
    <h1 style="margin: 0;">Hardcoding секретов</h1>
    <p style="margin: 0;">Анти-паттерн</p>
  </div>
</div>
***

Основные проблемы хранения секретов/конфигураций в коде проекта - это риск утечки секретов, нарушение безопасности и сложность изменения секретов/конфигураций.

***

### Пример 1

Настройки доступа к базе данных не должны быть частью кода, их необходимо выносить в переменные окружения, чтобы при необходимости было легко их поменять.


                                **Плохо:**

                                ```python
                                def main():
POSTGRES_DSN = 'postgres://postgres:postgres@postgres:5432/postgres'
                                ```


                                    **Хорошо:**

                                    ```python
                                    from environs import Env


def main():
    env = Env()
    env.read_env()

    POSTGRES_DSN = env.str('POSTGRES_DSN')
                                    ```


                                    **Хорошо:**

                                    ```python
                                    import os

from dotenv import load_dotenv


def main():
    load_dotenv()

    POSTGRES_DSN = os.getenv('POSTGRES_DSN')
                                    ```

***

### Пример 2

Адрес `http://localhost:8000` может измениться. Следует вынести его в отдельную настройку - это позволит менять адрес за пределами кода.


                                **Плохо:**

                                ```python
                                def main():
product_url = 'http://localhost:8000/api/products'
cart_url = 'http://localhost:8000/api/carts'
                                ```


                                    **Хорошо:**

                                    ```python
                                    from environs import Env
from urllib.parse import urljoin


def main():
    env = Env()
    env.read_env()

    base_url = env.str('SERVICE_URL')
    product_url = urljoin(base_url, 'api/products')
    cart_url = urljoin(base_url, 'api/carts')
                                    ```

***

### Пример 3

Настройка SECRET_KEY — это секретный ключ, с помощью которого шифруют пароли пользователей сайта. Если SECRET_KEY попадет не в те руки, то под угрозой взлома окажутся пароли всех пользователей сайта. Доверить ключ можно только администратору сервера: он спрячет ключ на сервере и сообщит его сайту при запуске через переменную окружения.


                                **Плохо:**

                                ```python
                                def main():
SECRET_KEY = 'cdl3v0giob0_q!or$c2-7kvrui69pg^f$y'
                                ```


                                    **Хорошо:**

                                    ```python
                                    from environs import Env


def main():
    env = Env()
    env.read_env()

    SECRET_KEY = env.str('SECRET_KEY')
                                    ```


                                    **Хорошо:**

                                    ```python
                                    import os

from dotenv import load_dotenv


def main():
    load_dotenv()

    SECRET_KEY = os.getenv('SECRET_KEY')
                                    ```

***

### Пример 4

Настройка ALLOWED_HOSTS нужна для безопасности вашего сайта. Она защищает от нескольких видов атак злоумышленников. Для защиты нужно, чтобы в этой переменной был указан домен, в котором развёрнут сайт. Как правило, default настройку для ALLOWED_HOSTS ставят `['127.0.0.1', 'localhost']`.


                                **Плохо:**

                                ```python
                                def main():
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
                                ```


                                    **Хорошо:**

                                    ```python
                                    from environs import Env


def main():
    env = Env()
    env.read_env()

    ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', ['127.0.0.1', 'localhost'])
                                    ```

***

### Пример 5

DEBUG активирует отладочный режим работы сайта. На локальной машине значение этой переменной обычно равняется `True`, а на production сервере — `False`. Как правило, в качестве default значения для DEBUG указывают `False`.


                                **Плохо:**

                                ```python
                                def main():
DEBUG = False
                                ```


                                **Плохо:**

                                ```python
                                def main():
DEBUG = True
                                ```


                                    **Хорошо:**

                                    ```python
                                    from environs import Env


def main():
    env = Env()
    env.read_env()

    DEBUG = env.bool(DEBUG, False)
                                    ```


