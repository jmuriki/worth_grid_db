from django.core.validators import MinValueValidator
from django.db import models

from taggit.managers import TaggableManager


class InterfaceSubCatalog(models.Model):
    title = models.CharField(
        verbose_name='Название Подкаталога',
        max_length=50,
        unique=True,
    )
    order_position = models.PositiveIntegerField(
        verbose_name='Позиция Подкаталога в Каталоге',
        help_text='Чем меньше, тем выше Подкаталог в Каталоге.',
        default=1,
        validators=[MinValueValidator(1)],
    )

    class Meta:
        verbose_name = 'Подкаталог Интерфейсов'
        verbose_name_plural = 'Подкаталоги Интерфейсов'
        ordering = ('order_position',)


    def __str__(self):
        return self.title


class Interface(models.Model):
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
    logo = models.ImageField(
        verbose_name='Лого',
        upload_to='interfaces/',
        blank=True,
        null=True,
    )
    illustration = models.ImageField(
        verbose_name='Иллюстрация',
        upload_to='interfaces/',
        blank=True,
        null=True,
    )
    subcatalogs = models.ManyToManyField(
        InterfaceSubCatalog,
        verbose_name='Подкаталоги',
        related_name='interfaces',
        through='InterfaceCatalog',
        through_fields=('interface', 'subcatalog'),
        blank=True,
    )

    class Meta:
        verbose_name = 'Интерфейс'
        verbose_name_plural = 'Интерфейсы'
        ordering = ('title',)

    def __str__(self):
        return self.title

    @property
    def ordered_subcatalogs(self):
        return InterfaceSubCatalog.objects.filter(
            interfacecatalog__interface=self
        ).order_by('interfacecatalog__order_position')


class InterfaceCatalog(models.Model):
    interface = models.ForeignKey(
        Interface,
        verbose_name='Интерфейс',
        related_name='interfaces',
        on_delete=models.CASCADE,
    )
    subcatalog = models.ForeignKey(
        InterfaceSubCatalog,
        verbose_name='Подкаталог Интерфейсов',
        related_name='subcatalogs',
        on_delete=models.CASCADE,
    )
    order_position = models.PositiveIntegerField(
        verbose_name='Позиция Интерфейса в Подкаталоге',
        help_text='Чем меньше, тем выше Интерфейс в Подкаталоге.',
        default=1,
        validators=[MinValueValidator(1)],
    )
    class Meta:
        verbose_name = 'Связь Интерфейса и Подкаталога'
        verbose_name_plural = 'Связи Интерфейсов и Подкаталогов'
        ordering = ('order_position',)
        constraints = [
            models.UniqueConstraint(
                fields=['interface', 'subcatalog'],
                name='unique_interface_subcatalog'
            )
        ]

    def __str__(self):
        return f'{self.interface} → {self.order_position} → {self.subcatalog}'


class Role(models.Model):
    interface = models.ForeignKey(
        Interface,
        verbose_name='Интерфейс',
        related_name='roles',
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        verbose_name='Название',
        max_length=50,
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
    logo = models.ImageField(
        verbose_name='Лого',
        upload_to='user_types/',
        blank=True,
        null=True,
    )
    illustration = models.ImageField(
        verbose_name='Иллюстрация',
        upload_to='roles/',
        blank=True,
        null=True,
    )
    order_position = models.PositiveIntegerField(
        verbose_name='Очередь',
        help_text='Чем меньше, тем выше Роль в Интерфейсе.',
        default=1,
        validators=[MinValueValidator(1)],
    )

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

    def __str__(self):
        return self.title


class Function(models.Model):
    role = models.ForeignKey(
        Role,
        verbose_name='Роль Пользователя',
        related_name='functions',
        on_delete=models.CASCADE,
    )
    job = models.CharField(
        verbose_name='Название Ключевой Функции',
        max_length=50,
    )
    description = models.TextField(
        verbose_name='Описание Ключевой Функции',
        blank=True,
    )
    order_position = models.PositiveIntegerField(
        verbose_name='Очередь',
        help_text='Чем меньше, тем выше Функция в Роли.',
        default=1,
        validators=[MinValueValidator(1)],
    )

    class Meta:
        verbose_name = 'Функция'
        verbose_name_plural = 'Функции'
        constraints = [
            models.UniqueConstraint(
                fields=['role', 'job'],
                name='unique_role_function'
            )
        ]

    def __str__(self):
        return self.job


class Story(models.Model):
    function = models.ForeignKey(
        Function,
        verbose_name='Ключевая Функция',
        related_name='stories',
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        verbose_name='Название Истории',
        max_length=50,
    )
    got_wanted = models.BooleanField(
        verbose_name='Пользователь получил желаемый результат',
        help_text='Укажите, является данная История успешной или отказной.',
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
    )
    order_position = models.PositiveIntegerField(
        verbose_name='Очередь',
        help_text='Чем меньше, тем выше История в Функции.',
        default=1,
        validators=[MinValueValidator(1)],
    )

    class Meta:
        verbose_name = 'История'
        verbose_name_plural = 'Истории'
        constraints = [
            models.UniqueConstraint(
                fields=['function', 'title'],
                name='unique_function_story'
            )
        ]

    def __str__(self):
        return self.title


class StoryContext(models.Model):
    story = models.ForeignKey(
        Story,
        verbose_name='История',
        related_name='context_points',
        on_delete=models.CASCADE,
    )
    text = models.CharField(
        verbose_name='Когда',
        help_text='Важный нюанс ситуации, в которой находится Пользователь.',
        max_length=100,
    )
    order_position = models.PositiveIntegerField(
        verbose_name='Очередь',
        help_text='Чем меньше, тем выше в списке данная строка.',
        default=1,
        validators=[MinValueValidator(1)],
    )

    class Meta:
        verbose_name = 'Cитуация'
        verbose_name_plural = 'Предыстория'

    def __str__(self):
        return self.text


class StartPoint(models.Model):
    story = models.OneToOneField(
        Story,
        verbose_name='История',
        related_name='start_point',
        on_delete=models.CASCADE,
    )
    text = models.CharField(
        verbose_name='В момент начала',
        max_length=100,
    )

    class Meta:
        verbose_name = 'Старт'
        verbose_name_plural = 'Старт'

    def __str__(self):
        return self.text


class StoryAcceptor(models.Model):
    story = models.ForeignKey(
        Story,
        verbose_name='История',
        related_name='acceptors',
        on_delete=models.CASCADE,
    )
    text = models.CharField(
        verbose_name='Акцептор',
        max_length=100,
    )
    order_position = models.PositiveIntegerField(
        verbose_name='Очередь',
        help_text='Чем меньше, тем выше в списке данный Акцептор.',
        default=1,
        validators=[MinValueValidator(1)],
    )

    class Meta:
        verbose_name = 'Условие'
        verbose_name_plural = 'Условия'

    def __str__(self):
        return self.text


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
        verbose_name='Очередь',
        help_text='Чем меньше, тем выше Пример в Анти-паттерне.',
        default=1,
        validators=[MinValueValidator(1)],
    )
    acceptors = models.ManyToManyField(
        StoryAcceptor,
        verbose_name='Акцепторы',
        related_name='anti_pattern_examples',
        blank=True,
    )

    class Meta:
        verbose_name = 'Пример'
        verbose_name_plural = 'Примеры'

    def __str__(self):
        return f'Пример к Анти-паттерну "{self.anti_pattern.title}"'


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
        verbose_name='Очередь',
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
