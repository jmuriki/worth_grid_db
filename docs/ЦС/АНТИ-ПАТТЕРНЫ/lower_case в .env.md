
<div class="sticky-header">
  <div>
    <h1 style="margin: 0;">lower_case в .env</h1>
    <p style="margin: 0;">Анти-паттерн</p>
  </div>
</div>
***

Исторически сложилось так, что переменные окружения принято называть в верхнем регистре с символом подчеркивания. Следуйте общепринятым правилам, чтобы не усложнять жизнь другим разработчикам!

***

### Пример 


                                    **Плохо:**

                                    ```python
                                    from environs import Env

def main():
    env = Env()
    env.read_env()
    tg_chat_id = env.str('tg_chat_id')
                                    ```


                                    **Хорошо:**

                                    ```python
                                    from environs import Env

def main():
    env = Env()
    env.read_env()
    tg_chat_id = env.str('TG_CHAT_ID')
                                    ```


