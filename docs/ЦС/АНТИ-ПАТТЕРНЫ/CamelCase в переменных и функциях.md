
<div class="sticky-header">
  <div>
    <h1 style="margin: 0;">CamelCase в переменных и функциях</h1>
    <p style="margin: 0;">Анти-паттерн</p>
  </div>
</div>
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


