from django.contrib import admin
from django.db import models
from django.forms import TextInput
from django.utils.html import format_html

from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin

from .models import (
    InterfaceCatalogSection,
    InterfaceCatalog,
    Interface,
    Role,
    Function,
    AntiPattern,
    Story,
    StoryContext,
    StartPoint,
    StoryAcceptor,
    AntiPatternExample,
    Snippet,
)


admin.site.site_header = "Ценностная сетка"
admin.site.site_title = "Ценностная сетка"
admin.site.index_title = "Административная панель"


SINGLE_LINE_TEXT_OVERRIDE = {
    models.TextField: {'widget': TextInput(attrs={'size': 80})},
}


class InterfaceInline(admin.TabularInline):
    model = Interface.sections.through
    extra = 1
    verbose_name = "Интерфейс"
    verbose_name_plural = "Интерфейсы"

# class InterfaceCatalogInline(admin.TabularInline):
#     model = InterfaceCatalog
#     extra = 0
#     fields = ('interface', 'interface_position',)
#     sortable_field_name = 'interface_position'

class StoryAcceptorInline(admin.TabularInline):
    model = StoryAcceptor
    extra = 1
    verbose_name = "Анти-паттерн"
    verbose_name_plural = "Анти-паттерны"

# class AntiPatternInline(admin.TabularInline):
#     model = AntiPattern.sections.through
#     extra = 1
#     verbose_name = "Анти-паттерн"
#     verbose_name_plural = "Анти-паттерны"


class StoryInline(admin.StackedInline):
    model = Story
    extra = 1
    formfield_overrides = SINGLE_LINE_TEXT_OVERRIDE

class StoryContextInline(admin.StackedInline):
    model = StoryContext
    extra = 1
    formfield_overrides = SINGLE_LINE_TEXT_OVERRIDE

class StartPointInline(admin.StackedInline):
    model = StartPoint
    extra = 1
    formfield_overrides = SINGLE_LINE_TEXT_OVERRIDE

class StoryAcceptorInline(admin.StackedInline):
    model = StoryAcceptor
    extra = 1
    formfield_overrides = SINGLE_LINE_TEXT_OVERRIDE

# class AntiPatternExampleInline(admin.StackedInline):
#     model = AntiPatternExample
#     extra = 1

class SnippetInline(admin.StackedInline):
    model = Snippet
    extra = 1

# class StoryAcceptorPatternInline(admin.TabularInline):
#     model = StoryAcceptor._meta.get_field('anti_pattern_examples').remote_field.through

#     fk_name  = 'anti_pattern_examples'
#     extra = 1
#     verbose_name = 'Нарушенный Акцептор'
#     verbose_name_plural = 'Нарушенные Акцепторы'

#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         formfield = super().formfield_for_foreignkey(db_field, request, **kwargs)
#         if db_field.name == 'anti_pattern_examples':
#             formfield.label_from_instance = lambda obj: (
#                 f"{obj.story.function.role.interface.title} — "
#                 f"{obj.story.function.title} — "
#                 f"{obj.story.title} — "
#                 f"{obj.text}"
#             )
#         return formfield


class InterfaceCatalogSectionFilter(admin.SimpleListFilter):
    title = 'Каталоги Интерфейсов'
    parameter_name = 'sections'

    def lookups(self, request, model_admin):
        sections = InterfaceCatalogSection.objects.all().order_by('title')
        return [(section.id, section.title) for section in sections]

    def queryset(self, request, queryset):
        if self.value():
            if hasattr(queryset.model, 'sections'):
                return queryset.filter(sections__id=self.value())
            elif hasattr(queryset.model, 'stories'):
                return queryset.filter(stories__interface__sections__id=self.value()).distinct()
        return queryset

class InterfaceFilter(admin.SimpleListFilter):
    title = 'Интерфейсы'
    parameter_name = 'interface'

    def lookups(self, request, model_admin):
        interfaces = Interface.objects.all().order_by('title')
        return [(interface.id, interface.title) for interface in interfaces]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(interface__id=self.value())
        return queryset

# class FunctionFilter(admin.SimpleListFilter):
#     title = 'Ключевые Функции'
#     parameter_name = 'function'

#     def lookups(self, request, model_admin):
#         functions = Function.objects.all().order_by('job')
#         return [(function.id, function.job) for function in functions]

#     def queryset(self, request, queryset):
#         if self.value():
#             return queryset.filter(function__id=self.value())
#         return queryset

class AntiPatternFilter(admin.SimpleListFilter):
    title = 'Анти-паттерны'
    parameter_name = 'antipatterns'

    def lookups(self, request, model_admin):
        antipatterns = AntiPattern.objects.all().order_by('title')
        return [(antipattern.id, antipattern.title) for antipattern in antipatterns]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(anti_pattern__id=self.value())
        return queryset


@admin.register(Interface)
class InterfaceAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'description',)
    search_fields = ('title', 'subtitle')
    list_filter = (InterfaceCatalogSectionFilter,)


@admin.register(InterfaceCatalogSection)
class InterfaceCatalogSectionAdmin(admin.ModelAdmin):
    list_display   = ('title', 'get_interfaces')
    search_fields  = ('title',)
    inlines = (InterfaceInline,)

    def get_interfaces(self, obj):
        interfaces = obj.interfaces.all()
        interfaces_titles = [interface.title for interface in interfaces]
        return ", ".join(interfaces_titles)
    get_interfaces.short_description = 'Интерфейсы'


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('title', 'interface', 'description',)
    fields = ('title', 'position')
    sortable_field_name = 'position'
    search_fields = ('title',)
    list_filter = (InterfaceFilter,)


@admin.register(Function)
class FunctionAdmin(admin.ModelAdmin):
    list_display = ('job', 'get_role', 'get_interfaces', 'description',)
    search_fields = ('job',)
    list_filter = ('role', 'role__interface')
    inlines = (
        StoryInline,
    )

    def get_role(self, obj):
        return obj.role.title
    get_role.short_description = 'Роль'

    def get_interfaces(self, obj):
        return obj.role.interface.title
    get_interfaces.short_description = 'Интерфейс'


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'function', 'get_role', 'get_interface')
    search_fields = ('title',)
    list_filter = ('function__role__interface', 'function__role', 'function',)
    inlines = (
        StoryContextInline,
        StartPointInline,
        StoryAcceptorInline,
    )

    def get_role(self, obj):
        return obj.function.role.title
    get_role.short_description = 'Роль'

    def get_interface(self, obj):
        return obj.function.role.interface.title
    get_interface.short_description = 'Интерфейс'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "function":
            kwargs["queryset"] = Function.objects.order_by('job')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(AntiPattern)
class AntiPatternAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_tags', 'subtitle',)
    search_fields  = ('title', 'tags__name',)
    list_filter = ('tags', )
    list_per_page = 20

    def get_tags(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())
    get_tags.short_description = 'Теги'


SNIPPET_FIX_STATUS_CHOICES = [
    ('not_fixable', 'Неисправимо'),
    ('fix_requiered', 'Требует исправления'),
    ('fix_not_requiered', 'Не требует исправления'),
]

@admin.register(AntiPatternExample)
class AntiPatternExampleAdmin(admin.ModelAdmin):
    list_display = ('anti_pattern', 'description', 'get_snippet_codes')
    list_filter = (AntiPatternFilter,)
    inlines = (
        SnippetInline,
    )
    list_per_page = 7

    def get_snippet_codes(self, obj):
        snippets = obj.snippets.all()
        if not snippets:
            return "-"

        codes = [
            format_html(
                "<div><strong>{}:</strong><br><pre><code>{}</code></pre></div>",
                snippet.status_label,
                snippet.code.strip().replace('{', '&lbrace;').replace('}', '&rbrace;')
            ) for snippet in snippets
        ]
        return format_html("".join(codes))
    get_snippet_codes.short_description = 'Сниппеты'


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "anti_pattern":
            kwargs["queryset"] = AntiPattern.objects.order_by('title')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
