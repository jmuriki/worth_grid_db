
<div>
    <h1 style="margin: 0;">Избыточные if-else</h1>
    <p style="margin: 0;">Анти-паттерн</p>
</div>

***

Избыточные проверки if-else усложняют чтение кода.

***

### Пример 1

При таком высушивании код избавляется ещё и от [[../Мусор/Избыточные True и False|избыточных True и False]].

**Плохо:**
```python
def get_link_status(link):
    ...
    if link_status:
        return True
    else:
        return False
```
**Хорошо:**
```python
def get_link_status(link):
    ...
    return bool(link_status)
```
***

### Пример 2

**Плохо:**
```python
def is_active_user(user):
    ...
    user_status = False
    return True if user_status else False
```
**Плохо:**
```python
def is_active_user(user):
    ...
    user_status = True
    return True if user_status else False
```
**Хорошо:**
```python
def is_active_user(user):
    ...
    user_status = False
    return user_status
```
**Хорошо:**
```python
def is_active_user(user):
    ...
    user_status = True
    return user_status
```
***

### Пример 3

В данном случае проверять `image_src` беcсмысленно. Функция всё равно вернёт какое-то значение отличное от `None`.

**Плохо:**
```python
def get_book_image_url(soup, book_page_url):
    img_rel_path = soup.find('div', class_='bookimage').find('img')['src']
    img_src = urljoin(book_page_url, img_rel_path)
    return img_src

...
image_src = get_book_image_url(soup, book_url)
if image_src:
    download_image(image_src)
```
**Хорошо:**
```python
def get_book_image_url(soup, book_page_url):
    img_rel_path = soup.find('div', class_='bookimage').find('img')['src']
    img_src = urljoin(book_page_url, img_rel_path)
    return img_src

...
image_src = get_book_image_url(soup, book_url)
download_image(image_src)
```

