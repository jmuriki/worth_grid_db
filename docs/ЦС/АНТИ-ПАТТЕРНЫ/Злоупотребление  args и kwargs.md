
<div>
    <h1 style="margin: 0;">Злоупотребление  args и kwargs</h1>
    <p style="margin: 0;">Анти-паттерн</p>
</div>

***

Нет смысла использовать `*args` и/или `**kwargs` в функциях или методах, у которых известны аргументы. Это только снижает читаемость кода и его понимание.
Использование `*args` и/или `**kwargs` не даёт информации об аргументах функции, IDE не подсказывает, какие параметры можно передать в функцию, тем самым, повышается риск передачи лишних или неправильных параметров.
Используйте `*args` и/или `**kwargs`, когда их гибкость оправдана, например, для обёрток, декораторов или для передачи множества дополнительных параметров.

***

### Пример 1

**Плохо:**
```python
def add_numbers(*args):
    if len(args) != 2:
        raise ValueError('Функция ожидает ровно два аргумента')
    return args[0] + args[1]

result = add_numbers(3, 7)
```
**Хорошо:**
```python
def add_numbers(num1, num2):
    return num1 + num2

result = add_numbers(3, 7)
```
***

### Пример 2

**Плохо:**
```python
def create_user(**kwargs):
    username = kwargs.get('username')
    email = kwargs.get('email')
    age = kwargs.get('age')

    if not username or not email:
        raise ValueError('username and email are required')
    return {
        'username': username,
        'email': email,
        'age': age if age else 'unknown',
    }

user1 = create_user(username='john_doe', email='john@example.com', age=30)
user2 = create_user(username='jane_doe', email='jane@example.com')
```
**Хорошо:**
```python
def create_user(username, email, age=None):
    if not username or not email:
        raise ValueError('username and email are required')
    return {
        'username': username,
        'email': email,
        'age': age if age else 'unknown',
    }

user1 = create_user(username='john_doe', email='john@example.com', age=30)
user2 = create_user(username='jane_doe', email='jane@example.com')
```
***

### Пример 3

Не всегда мы можем видеть `args` и `kwargs` в параметрах функции: такой нейминг - лишь соглашение между программистами. Иногда название может быть другим.

**Плохо:**
```python
def display_user_info(user_info):
    name = user_info.get('name')
    age = user_info.get('age')
    work = user_info.get('work')
    ...
```
**Хорошо:**
```python
def display_user_info(name, age, work):
    ...
```

