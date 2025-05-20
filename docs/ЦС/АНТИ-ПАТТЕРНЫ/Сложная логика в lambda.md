
<div class="sticky-header">
  <div>
    <h1 style="margin: 0;">Сложная логика в lambda</h1>
    <p style="margin: 0;">Анти-паттерн</p>
  </div>
</div>
***

`lambda`-функции хороши для краткого описания простых операций или выражений, а использование их для сложной логики, объемного, многострочного кода с ветвлениями, циклами или вложенными вызовами снижает читаемость кода.

***

### Пример 


**Плохо:**

```python
do_something = lambda num: num**2 + 2*num - 1 if num > 0 else num**2 - 2*num + 1
```


                                **Хорошо:**

                                ```python
                                def do_something(num):
if num > 0:
    return num**2 + 2*num - 1
else:
    return num**2 - 2*num + 1
                                ```


                                **Хорошо:**

                                ```python
                                def do_something(num):
return num**2 + 2*num - 1 if num > 0 else num**2 - 2*num + 1
                                ```


