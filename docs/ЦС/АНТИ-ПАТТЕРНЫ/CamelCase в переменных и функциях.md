# Анти-паттерн: "CamelCase в переменных и функциях"

***

Иногда данные приходят в альтернативном стиле написания из-за того, что они создавались на другом языке, правила которого отличаются от Python, например, JavaScript.

***

### Пример 

**Плохо:**
```python
class Postcard(BaseModel):
    holidayId: str
    name_ru: str
    body: Union[str, List[str]]
```
**Хорошо:**
```python
class Postcard(BaseModel):
    holiday_id: str = Field(alias='holidayId')
    name_ru: str
    body: Union[str, List[str]]
```

