from django.contrib import admin
from django.db import models
from django.forms import TextInput
from django.utils.html import format_html

from .models import (
    InterfaceGroup,
    Interface,
    UserType,
    Function,
    AntiPatternGroup,
    AntiPattern,
    Story,
    ContextPoint,
    StartPoint,
    SuccessPoint,
    RefusalPoint,
    Example,
    Snippet,
)


admin.site.site_header = "Ценностная сетка"
admin.site.site_title = "Ценностная сетка"
admin.site.index_title = "Административная панель"


SINGLE_LINE_TEXT_OVERRIDE = {
    models.TextField: {'widget': TextInput(attrs={'size': 80})},
}


class InterfaceInline(admin.TabularInline):
    model = Interface.groups.through
    extra = 1
    verbose_name = "Интерфейс"
    verbose_name_plural = "Интерфейсы"

class AntiPatternInline(admin.TabularInline):
    model = AntiPattern.groups.through
    extra = 1
    verbose_name = "Анти-паттерн"
    verbose_name_plural = "Анти-паттерны"

class ContextPointInline(admin.StackedInline):
    model = ContextPoint
    extra = 1
    formfield_overrides = SINGLE_LINE_TEXT_OVERRIDE

class StartPointInline(admin.StackedInline):
    model = StartPoint
    extra = 1
    formfield_overrides = SINGLE_LINE_TEXT_OVERRIDE

class SuccessPointInline(admin.StackedInline):
    model = SuccessPoint
    extra = 1
    filter_horizontal = ('anti_pattern',)
    # filter_horizontal = ('example',)
    formfield_overrides = SINGLE_LINE_TEXT_OVERRIDE

class RefusalPointInline(admin.StackedInline):
    model = RefusalPoint
    extra = 1
    filter_horizontal = ('anti_pattern',)
    # filter_horizontal = ('example',)
    formfield_overrides = SINGLE_LINE_TEXT_OVERRIDE

class ExampleInline(admin.StackedInline):
    model = Example
    extra = 1

class SnippetInline(admin.StackedInline):
    model = Snippet
    extra = 1


class SuccessPatternInline(admin.TabularInline):
    model = SuccessPoint._meta.get_field('anti_pattern').remote_field.through
    fk_name  = 'antipattern'
    # model = SuccessPoint._meta.get_field('example').remote_field.through
    # fk_name  = 'example'
    extra = 1
    verbose_name = 'Критерий успеха'
    verbose_name_plural = 'Нарушенные критерии успеха'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        formfield = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'successpoint':
            formfield.label_from_instance = lambda obj: (
                f"{obj.story.interface.short_name if obj.story.interface else 'Без интерфейса'} — "
                f"{obj.story.function.title if obj.story.function else 'Без функции'} — "
                f"{obj.story.title} — "
                f"{obj.text}"
            )
        return formfield

class RefusalPatternInline(admin.TabularInline):
    model = RefusalPoint._meta.get_field('anti_pattern').remote_field.through
    fk_name  = 'antipattern'
    # model = RefusalPoint._meta.get_field('example').remote_field.through
    # fk_name  = 'example'
    extra = 1
    verbose_name = 'Критерий отказа'
    verbose_name_plural = 'Нарушенные критерии отказа'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        formfield = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'refusalpoint':
            formfield.label_from_instance = lambda obj: (
                f"{obj.story.interface.short_name if obj.story.interface else 'Без интерфейса'} — "
                f"{obj.story.function.title if obj.story.function else 'Без функции'} — "
                f"{obj.story.title} — "
                f"{obj.text}"
            )
        return formfield


class InterfaceGroupFilter(admin.SimpleListFilter):
    title = 'Группы Интерфейсов'
    parameter_name = 'groups'

    def lookups(self, request, model_admin):
        groups = InterfaceGroup.objects.all().order_by('short_name')
        return [(group.id, group.short_name) for group in groups]

    def queryset(self, request, queryset):
        if self.value():
            if hasattr(queryset.model, 'groups'):
                return queryset.filter(groups__id=self.value())
            elif hasattr(queryset.model, 'stories'):
                return queryset.filter(stories__interface__groups__id=self.value()).distinct()
        return queryset


class InterfaceFilter(admin.SimpleListFilter):
    title = 'Интерфейсы'
    parameter_name = 'interface'

    def lookups(self, request, model_admin):
        interfaces = Interface.objects.all().order_by('short_name')
        return [(interface.id, interface.short_name) for interface in interfaces]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(interface__id=self.value())
        return queryset


class UserTypeFilter(admin.SimpleListFilter):
    title = 'Пользователи'
    parameter_name = 'user_type'

    def lookups(self, request, model_admin):
        user_types = UserType.objects.all().order_by('role')
        return [(user_type.id, user_type.role) for user_type in user_types]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user_type__id=self.value())
        return queryset


class FunctionFilter(admin.SimpleListFilter):
    title = 'Ключевые Функции'
    parameter_name = 'function'

    def lookups(self, request, model_admin):
        functions = Function.objects.all().order_by('title')
        return [(function.id, function.title) for function in functions]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(function__id=self.value())
        return queryset


class AntiPatternGroupFilter(admin.SimpleListFilter):
    title = 'Группы Анти-паттернов'
    parameter_name = 'groups'

    def lookups(self, request, model_admin):
        groups = AntiPatternGroup.objects.all().order_by('name')
        return [(group.id, group.name) for group in groups]

    def queryset(self, request, queryset):
        if self.value():
            if hasattr(queryset.model, 'groups'):
                return queryset.filter(groups__id=self.value())
            elif hasattr(queryset.model, 'anti_pattern'):
                return queryset.filter(anti_pattern__groups__id=self.value())
        return queryset


class AntiPatternFilter(admin.SimpleListFilter):
    title = 'Анти-паттерны'
    parameter_name = 'antipatterns'

    def lookups(self, request, model_admin):
        antipatterns = AntiPattern.objects.all().order_by('name')
        return [(antipattern.id, antipattern.name) for antipattern in antipatterns]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(anti_pattern__id=self.value())
        return queryset


@admin.register(InterfaceGroup)
class InterfaceGroupAdmin(admin.ModelAdmin):
    list_display   = ('short_name', 'title', 'description',)
    search_fields  = ('short_name', 'title')
    inlines = (InterfaceInline,)
    list_filter = (InterfaceFilter,)


@admin.register(Interface)
class InterfaceAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'title', 'description',)
    search_fields = ('short_name', 'title')
    filter_horizontal = ('groups',)
    list_filter = (InterfaceGroupFilter,)


@admin.register(UserType)
class UserTypeAdmin(admin.ModelAdmin):
    list_display = ('role', 'description',)
    search_fields = ('role',)
    list_filter = (InterfaceGroupFilter,)
    list_filter = (InterfaceGroupFilter,)
    # list_filter = (InterfaceGroupFilter, InterfaceFilter,)  # TODO


@admin.register(Function)
class FunctionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'get_interfaces',)
    search_fields = ('title',)
    # list_filter = (InterfaceGroupFilter, InterfaceFilter,)  # TODO

    def get_interfaces(self, obj):
        story = obj.stories.first()
        if not story:
            return "-"
        return story.interface.short_name
    get_interfaces.short_description = 'Интерфейс'


@admin.register(AntiPatternGroup)
class AntiPatternGroupAdmin(admin.ModelAdmin):
    list_display   = ('name', 'description',)
    search_fields  = ('name',)
    inlines = (AntiPatternInline,)


@admin.register(AntiPattern)
class AntiPatternAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    search_fields  = ('name',)
    filter_horizontal = ('groups',)
    list_filter = (AntiPatternGroupFilter,)
    inlines = (SuccessPatternInline, RefusalPatternInline,)


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'function', 'user_type', 'interface')
    search_fields = ('title',)
    list_filter = (InterfaceFilter, UserTypeFilter, FunctionFilter)
    inlines = (
        ContextPointInline,
        StartPointInline,
        SuccessPointInline,
        RefusalPointInline,
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "function":
            kwargs["queryset"] = Function.objects.order_by('title')
        if db_field.name == "user_type":
            kwargs["queryset"] = UserType.objects.order_by('role')
        if db_field.name == "interface":
            kwargs["queryset"] = Interface.objects.order_by('short_name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


SNIPPET_TYPE_CHOISES = {
    'bad': 'Плохо',
    'good': 'Хорошо',
    'acceptable': 'Допустимо',
    'exception': 'Исключение',
    'legacy': 'Наследство',
}

@admin.register(Example)
class ExampleAdmin(admin.ModelAdmin):
    list_display = ('anti_pattern', 'description', 'get_snippet_codes')
    list_filter = (AntiPatternGroupFilter, AntiPatternFilter,)
    inlines = (
        SnippetInline,
        # SuccessPatternInline,
        # RefusalPatternInline,
    )

    def get_snippet_codes(self, obj):
        snippets = obj.snippets.all()
        if not snippets:
            return "-"
        codes = [
            format_html(
                "<div><strong>{}:</strong><br><pre><code>{}</code></pre></div>",
                SNIPPET_TYPE_CHOISES.get(snippet.type, snippet.type),
                snippet.code.strip().replace('{', '&lbrace;').replace('}', '&rbrace;')
            ) for snippet in snippets
        ]
        return format_html("".join(codes))
    get_snippet_codes.short_description = 'Коды сниппетов'


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "anti_pattern":
            kwargs["queryset"] = AntiPattern.objects.order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
