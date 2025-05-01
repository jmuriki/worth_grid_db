from django.db import models
from django.core.exceptions import ValidationError


class InterfaceGroup(models.Model):
    short_name = models.CharField(
        verbose_name='Короткое название',
        max_length=255,
        unique=True,
    )
    title = models.CharField(
        verbose_name='Развёрнутое название',
        max_length=255,
        unique=True,
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
    )
    logo = models.ImageField(
        verbose_name='Логотип',
        upload_to='interfaces/',
        blank=True,
        null=True,
    )
    preview = models.ImageField(
        verbose_name='Изображение',
        upload_to='interfaces/',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Группа Интерфейсов'
        verbose_name_plural = 'Группы Интерфейсов'

    def __str__(self):
        return self.short_name


class Interface(models.Model):
    short_name = models.CharField(
        verbose_name='Короткое название',
        max_length=255,
        unique=True,
    )
    title = models.CharField(
        verbose_name='Развёрнутое название',
        max_length=255,
        unique=True,
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
    )
    logo = models.ImageField(
        verbose_name='Логотип',
        upload_to='interfaces/',
        blank=True,
        null=True,
    )
    preview = models.ImageField(
        verbose_name='Изображение',
        upload_to='interfaces/',
        blank=True,
        null=True,
    )
    groups = models.ManyToManyField(
        InterfaceGroup,
        verbose_name='Группы',
        related_name='interfaces',
        blank=True,
    )

    class Meta:
        verbose_name = 'Интерфейс'
        verbose_name_plural = 'Интерфейсы'

    def __str__(self):
        return self.short_name


class UserType(models.Model):
    role = models.CharField(
        verbose_name='Роль',
        max_length=255,
        unique=True,
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
    )
    logo = models.ImageField(
        verbose_name='Логотип',
        upload_to='user_types/',
        blank=True,
        null=True,
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='user_types/',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Тип пользователя'
        verbose_name_plural = 'Типы пользователей'

    def __str__(self):
        return self.role


class Function(models.Model):
    title = models.CharField(
        verbose_name='Название',
        max_length=255,
        unique=True,
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
    )

    class Meta:
        verbose_name = 'Функция'
        verbose_name_plural = 'Функции'

    def __str__(self):
        return self.title


class AntiPatternGroup(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=255,
        unique=True,
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
    )

    class Meta:
        verbose_name = 'Группа Анти-паттернов'
        verbose_name_plural = 'Группы Анти-паттернов'

    def __str__(self):
        return self.name


class AntiPattern(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=255,
        unique=True,
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
    )
    groups = models.ManyToManyField(
        AntiPatternGroup,
        verbose_name='Группы',
        related_name='anti_patterns',
        blank=True,
    )

    class Meta:
        verbose_name = 'Анти-паттерн'
        verbose_name_plural = 'Анти-паттерны'

    def __str__(self):
        return self.name


class Example(models.Model):
    anti_pattern = models.ForeignKey(
        AntiPattern,
        verbose_name='Анти-паттерн',
        related_name='examples',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=255,
        blank=True,
    )
    description = models.TextField(
        verbose_name='Описание примера',
        blank=True,
    )

    class Meta:
        verbose_name = 'Пример'
        verbose_name_plural = 'Примеры'

    def __str__(self):
        groups = ''.join(str(group.name) for group in self.anti_pattern.groups.all())
        return f'Группы Анти-паттернов: {groups}'


SNIPPET_TYPE_CHOICES = [
    ('bad', 'Плохо'),
    ('good', 'Хорошо'),
    ('acceptable', 'Допустимо'),
    ('exception', 'Исключение'),
    ('legacy', 'Наследство'),
]

class Snippet(models.Model):
    example = models.ForeignKey(
        Example,
        verbose_name='Пример',
        related_name='snippets',
        null=True,
        on_delete=models.SET_NULL,
    )
    type = models.CharField(
        verbose_name='Тип примера',
        max_length=10,
        choices=SNIPPET_TYPE_CHOICES,
        blank=True,
    )
    code = models.TextField(
        verbose_name='Код',
    )

    class Meta:
        verbose_name = 'Пример к Анти-паттерну'
        verbose_name_plural = 'Сниппеты'

    def __str__(self):
        return self.example.anti_pattern.name


class Story(models.Model):
    title = models.CharField(
        verbose_name='Название',
        max_length=255,
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
    )
    function = models.ForeignKey(
        Function,
        verbose_name='Ключевая Функция',
        related_name='stories',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    user_type = models.ForeignKey(
        UserType,
        verbose_name='Роль Пользователя',
        related_name='stories',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    interface = models.ForeignKey(
        Interface,
        verbose_name='Интерфейс',
        related_name='stories',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = 'История'
        verbose_name_plural = 'Истории'

    def __str__(self):
        return self.title


class ContextPoint(models.Model):
    story = models.ForeignKey(
        Story,
        verbose_name='История',
        related_name='context_points',
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        verbose_name='Когда',
    )

    class Meta:
        verbose_name = 'Важный нюанс ситуации, в которой находится Пользователь'
        verbose_name_plural = 'Предыстория'

    def __str__(self):
        return ''


class StartPoint(models.Model):
    story = models.ForeignKey(
        Story,
        verbose_name='История',
        related_name='start_points',
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        verbose_name='Начало',
    )

    class Meta:
        verbose_name = 'Описание'
        verbose_name_plural = 'Старт'

    def __str__(self):
        return ''


class SuccessPoint(models.Model):
    story = models.ForeignKey(
        Story,
        verbose_name='История',
        related_name='success_points',
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        verbose_name='Критерий успеха',
    )
    anti_pattern = models.ManyToManyField(
        AntiPattern,
        verbose_name='Анти-паттерны',
        related_name='success_points',
        blank=True,
    )
    # example = models.ManyToManyField(
    #     Example,
    #     verbose_name='Примеры',
    #     related_name='success_points',
    #     blank=True,
    # )

    class Meta:
        verbose_name = 'Условие успеха'
        verbose_name_plural = 'Успех'

    def __str__(self):
        return ''


class RefusalPoint(models.Model):
    story = models.ForeignKey(
        Story,
        verbose_name='История',
        related_name='refusal_points',
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        verbose_name='Критерий отказа',
    )
    anti_pattern = models.ManyToManyField(
        AntiPattern,
        verbose_name='Анти-паттерны',
        related_name='refusal_points',
        blank=True,
    )
    # example = models.ManyToManyField(
    #     Example,
    #     verbose_name='Примеры',
    #     related_name='refusal_points',
    #     blank=True,
    # )

    class Meta:
        verbose_name = 'Условие отказа'
        verbose_name_plural = 'Отказ'

    def __str__(self):
        return ''
