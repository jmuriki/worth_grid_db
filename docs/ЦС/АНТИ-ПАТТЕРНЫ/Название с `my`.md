
<div>
    <h1 style="margin: 0;">Название с `my`</h1>
    <p style="margin: 0;">Анти-паттерн</p>
</div>

***

Местоимение `my` чаще всего является излишним и способно больше запутать, чем помочь понять код. Особенно плохо, если отсутствуют другие переменные, названия которых противопоставлялись бы `my`. Сложно придумать пример названия, в котором `my` нельзя было бы заменить более точным словом.

***

### Пример 1

**Плохо:**
```python
with open(file_path, "w") as my_file:
    ...
```
**Хорошо:**
```python
with open(file_path, "w") as file:
    ...
```
***

### Пример 2

**Плохо:**
```python
from environs import Env


def main():
    env = Env()
    env.read_env()
    my_vk_access_token =  env.str('VK_ACCESS_TOKEN')
```
**Хорошо:**
```python
from environs import Env


def main():
    env = Env()
    env.read_env()
    vk_access_token =  env.str('VK_ACCESS_TOKEN')
```
***

### Пример 3

**Плохо:**
```python
def get_my_user_info(user_id):
    ...
```
**Хорошо:**
```python
def get_user_info(user_id):
    ...
```
***

### Пример 4

В мультипользовательском планировшике задач может быть уместно называть коллекцию задач, назначенных пользователю данного аккаунта, используя `my`, но и в таком случае лучше заменить `my` на `current_user`:

**Допустимо:**
```python
def get_tasks(user_id):
    ...
    return my_tasks, group_tasks
```
**Хорошо:**
```python
def get_tasks(user_id):
    ...
    return current_user_tasks, group_tasks
```

