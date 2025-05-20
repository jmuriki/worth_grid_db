
<div class="sticky-header">
  <div>
    <h1 style="margin: 0;">Опасные default настройки</h1>
    <p style="margin: 0;">Анти-паттерн</p>
  </div>
</div>
***

Настройки с дефолтными значениями будут иногда попросту забывать заполнить, поэтому дефолтные значения должны быть безопасными - в этом их смысл.

***

### Пример 1

DEBUG по умолчанию должен быть `False`. Это спасёт программиста, если он забудет указать эту настройку на prod-сервере.


                                    **Плохо:**

                                    ```python
                                    from environs import Env


def main():
    env = Env()
    env.read_env()

    DEBUG = env.bool(DEBUG, True)
                                    ```


                                    **Хорошо:**

                                    ```python
                                    from environs import Env


def main():
    env = Env()
    env.read_env()

    DEBUG = env.bool(DEBUG, False)
                                    ```

***

### Пример 2

Настройка SECRET_KEY — это секретный ключ, с помощью которого шифруют пароли пользователей сайта. Если SECRET_KEY попадёт не в те руки, то под угрозой взлома окажутся пароли всех пользователей сайта. Доверить ключ можно только администратору сервера: он спрячет ключ на сервере и сообщит его сайту при запуске через переменную окружения. SECRET_KEY не должен иметь никаких default настроек. Так мы предотвратим риск утечки default значения в случае, если забудем указать SECRET_KEY при запуске приложения.


                                    **Плохо:**

                                    ```python
                                    from environs import Env


def main():
    env = Env()
    env.read_env()

    SECRET_KEY = env.str('SECRET_KEY', 'value_if_secret_key_is_empty')
                                    ```


                                    **Хорошо:**

                                    ```python
                                    from environs import Env


def main():
    env = Env()
    env.read_env()

    SECRET_KEY = env.str('SECRET_KEY')
                                    ```


