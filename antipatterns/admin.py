import nested_admin

from django.contrib import admin
from django.db import models
from django.forms import TextInput
from django.utils.html import format_html
from django.utils.safestring import mark_safe


from antipatterns.models import (
    AntiPattern,
    AntiPatternExample,
    AntiPatternExampleStoryAcceptor,
    Snippet,
)


admin.site.site_header = "Ценностная сетка"
admin.site.site_title = "Ценностная сетка"
admin.site.index_title = "Административная панель"


CHAR_FIELD_LINE_OVERRIDE = {
    models.CharField: {'widget': TextInput(attrs={'size': 100})}
}


class SnippetInline(nested_admin.NestedTabularInline):
    model = Snippet
    extra = 0
    fields = (
        'order_position', 'anti_pattern_present',
        'fix_status', 'status_label', 'lang_ident', 'code',
    )
    readonly_fields = ('status_label',)
    ordering = ('order_position',)

class AcceptorsInline(nested_admin.NestedTabularInline):
    model = AntiPatternExampleStoryAcceptor
    fk_name = 'anti_pattern_example'
    extra = 0
    fields = ('order_position', 'story_acceptor', 'comment',)
    raw_id_fields = ('story_acceptor',)
    ordering = ('order_position',)

    formfield_overrides = CHAR_FIELD_LINE_OVERRIDE

class AntiPatternExampleInline(nested_admin.NestedTabularInline):
    model = AntiPatternExample
    extra = 0
    fields = ('order_position', 'description',)
    inlines = [AcceptorsInline, SnippetInline,]


class AntiPatternFilter(admin.SimpleListFilter):
    title = 'Анти-паттерны'
    parameter_name = 'antipatterns'

    def lookups(self, request, model_admin):
        antipatterns = AntiPattern.objects.all().order_by('title')
        return [
            (antipattern.id, antipattern.title) for antipattern in antipatterns
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(anti_pattern__id=self.value())
        return queryset


@admin.register(AntiPattern)
class AntiPatternAdmin(nested_admin.NestedModelAdmin):
    list_display = ('id', 'title', 'subtitle', 'get_tags', 'get_exclusions',)
    search_fields  = ('title', 'tags__name',)
    list_filter = ('tags', )
    list_per_page = 20
    inlines = (AntiPatternExampleInline,)

    formfield_overrides = CHAR_FIELD_LINE_OVERRIDE

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        widget = form.base_fields['tags'].widget
        widget.attrs.update({'style': 'width: 61em'})
        return form

    def get_tags(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())
    get_tags.short_description = 'Теги'

    def get_exclusions(self, obj):
        for example in obj.examples.all().prefetch_related('snippets'):
            for snippet in example.snippets.all():
                if snippet.status_label == 'Исключение'\
                or snippet.status_label == 'Допустимо':
                    return format_html(
                        '<span style="color: green;">Есть Исключение</span>'
                    )
            return format_html(
                '<span style="color: red;">Не хватает Исключения</span>'
            )
        return format_html(
            '<span style="color: blue;">Только описание без сниппетов</span>'
        )
    get_exclusions.short_description = 'Статус'


@admin.register(AntiPatternExample)
class AntiPatternExampleAdmin(nested_admin.NestedModelAdmin):
    list_display = (
        'anti_pattern', 'description', 'get_snippet_codes', 'get_exclusions',
    )
    list_filter = (AntiPatternFilter,)
    raw_id_fields = ('anti_pattern',)
    ordering = ('order_position',)
    inlines = (AcceptorsInline, SnippetInline,)
    list_per_page = 7

    def get_snippet_codes(self, obj):
        snippets = obj.snippets.all()
        if not snippets:
            return "-"

        codes = [
            format_html(
                "<div><strong>{}:</strong><br><pre><code>{}</code></pre></div>",
                snippet.status_label,
                snippet.code.strip()
            ) for snippet in snippets
        ]
        return mark_safe("".join(codes))
    get_snippet_codes.short_description = 'Сниппеты'

    def get_exclusions(self, obj):
        for snippet in obj.snippets.all():
            if snippet.status_label == 'Исключение'\
            or snippet.status_label == 'Допустимо':
                return format_html(
                    '<span style="color: green;">Есть Исключение</span>'
                )
        return format_html(
            '<span style="color: red;">Не хватает Исключения</span>'
        )
    get_exclusions.short_description = 'Статус'


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "anti_pattern":
            kwargs["queryset"] = AntiPattern.objects.order_by('title')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
