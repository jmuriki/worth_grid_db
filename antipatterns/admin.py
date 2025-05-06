import nested_admin

from django.contrib import admin
from django.db import models
from django.forms import TextInput
from django.utils.html import format_html
from django.utils.safestring import mark_safe


from antipatterns.models import (
    AntiPattern,
    AntiPatternExample,
    Snippet,
)


admin.site.site_header = "Ценностная сетка"
admin.site.site_title = "Ценностная сетка"
admin.site.index_title = "Административная панель"


CHAR_FIELD_LINE_OVERRIDE = {models.CharField: {'widget': TextInput(attrs={'size': 100})}}


class SnippetInline(nested_admin.NestedTabularInline):
    model = Snippet
    extra = 0
    fields = ('order_position', 'anti_pattern_present', 'fix_status', 'lang_ident', 'code',)
    ordering = ('order_position',)

class AntiPatternExampleInline(nested_admin.NestedTabularInline):
    model = AntiPatternExample
    extra = 0
    fields = ('order_position', 'description', 'acceptors',)
    raw_id_fields = ('acceptors',)
    inlines = [SnippetInline,]


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


@admin.register(AntiPattern)
class AntiPatternAdmin(nested_admin.NestedModelAdmin):
    list_display = ('id', 'title', 'subtitle', 'get_tags',)
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


@admin.register(AntiPatternExample)
class AntiPatternExampleAdmin(admin.ModelAdmin):
    list_display = ('anti_pattern', 'description', 'get_snippet_codes')
    list_filter = (AntiPatternFilter,)
    raw_id_fields = ('anti_pattern', 'acceptors',)
    ordering = ('order_position',)
    inlines = (SnippetInline,)
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


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "anti_pattern":
            kwargs["queryset"] = AntiPattern.objects.order_by('title')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
