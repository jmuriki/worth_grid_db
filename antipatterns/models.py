from django.core.validators import MinValueValidator
from django.db import models

from taggit.managers import TaggableManager

from interfaces.models import StoryAcceptor


class AntiPattern(models.Model):
    title = models.CharField(
        verbose_name='Название',
        max_length=50,
        unique=True,
    )
    subtitle = models.CharField(
        verbose_name='Подзаголовок',
        max_length=100,
        blank=True,
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
    )
    tags = TaggableManager(
        verbose_name='Теги',
        blank=True,
    )

    class Meta:
        verbose_name = 'Анти-паттерн'
        verbose_name_plural = 'Анти-паттерны'

    def __str__(self):
        return self.title


class AntiPatternExample(models.Model):
    anti_pattern = models.ForeignKey(
        AntiPattern,
        verbose_name='Анти-паттерн',
        related_name='examples',
        on_delete=models.CASCADE,
    )
    description = models.TextField(
        verbose_name='Описание Примера',
        blank=True,
    )
    order_position = models.PositiveIntegerField(
        verbose_name='Очередь Примера',
        help_text='Чем меньше, тем выше Пример в Анти-паттерне.',
        default=1,
        validators=[MinValueValidator(1)],
    )
    acceptors = models.ManyToManyField(
        StoryAcceptor,
        verbose_name='Акцепторы',
        related_name='anti_pattern_examples',
        blank=True,
        through='AntiPatternExampleStoryAcceptor',
        through_fields=('anti_pattern_example', 'story_acceptor'),
    )

    class Meta:
        verbose_name = 'Пример'
        verbose_name_plural = 'Примеры'

    def __str__(self):
        return f'Пример к Анти-паттерну "{self.anti_pattern.title}"'


class AntiPatternExampleStoryAcceptor(models.Model):
    anti_pattern_example = models.ForeignKey(
        AntiPatternExample,
        verbose_name='Пример Анти-паттерна',
        related_name='acceptor_links',
        on_delete=models.CASCADE,
    )
    story_acceptor = models.ForeignKey(
        StoryAcceptor,
        verbose_name='Акцептор Истории',
        related_name='example_links',
        on_delete=models.CASCADE,
    )
    order_position = models.PositiveIntegerField(
        verbose_name='Очерёдность',
        help_text='Чем меньше число — тем выше Пример в списке выдачи.',
        default=1,
        validators=[MinValueValidator(1)],
    )
    comment = models.CharField(
        verbose_name='Как заметить?',
        help_text='Как заметить Анти-паттерн?',
        max_length=200,
        blank=True,
    )

    class Meta:
        verbose_name = 'Связь «Пример Анти-паттерна - Акцептор»'
        verbose_name_plural = 'Связи «Пример Анти-паттерна - Акцептор»'

    def __str__(self):
        return f'{self.anti_pattern_example} ↔ {self.story_acceptor}'


SNIPPET_FIX_STATUS_CHOICES = [
    ('not_fixable', 'Неисправимо'),
    ('fix_required', 'Требует исправления'),
    ('fix_not_required', 'Не требует исправления'),
]

class Snippet(models.Model):
    example = models.ForeignKey(
        AntiPatternExample,
        verbose_name='Пример',
        related_name='snippets',
        on_delete=models.CASCADE,
    )
    anti_pattern_present = models.BooleanField(
        verbose_name='Наличие Анти-паттерна',
    )
    fix_status = models.CharField(
        verbose_name='Статус исправления',
        max_length=20,
        choices=SNIPPET_FIX_STATUS_CHOICES,
    )
    lang_ident = models.CharField(
        verbose_name='Идентификатор языка',
        max_length=20,
        blank=True,
    )
    code = models.TextField(
        verbose_name='Код',
    )
    order_position = models.PositiveIntegerField(
        verbose_name='Очередь Спиппета',
        help_text='Чем меньше, тем выше Сниппет в Примере.',
        default=1,
        validators=[MinValueValidator(1)],
    )

    class Meta:
        verbose_name = 'Сниппет'
        verbose_name_plural = 'Сниппеты'

    def __str__(self):
        return f'Пример к Анти-паттерну "{self.example.anti_pattern.title}"'

    @property
    def status_label(self):
        status_labels_mapping = {
            (True, 'not_fixable'): 'Исключение',
            (True, 'fix_required'): 'Плохо',
            (True, 'fix_not_required'): 'Допустимо',
            (False, 'fix_not_required'): 'Хорошо',
        }
        return status_labels_mapping.get(
            (self.anti_pattern_present, self.fix_status),
            ''
        )
    status_label.fget.short_description = 'Резолюция сниппета'
