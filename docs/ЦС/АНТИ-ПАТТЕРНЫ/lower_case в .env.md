# Анти-паттерн: "lower_case в .env"

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

