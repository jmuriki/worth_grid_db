import nested_admin

from django.contrib import admin
from django.db import models
from django.forms import TextInput
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import (
    InterfaceSubCatalog,
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


CHAR_FIELD_LINE_OVERRIDE = {models.CharField: {'widget': TextInput(attrs={'size': 100})}}
# SINGLE_LINE_TEXT_OVERRIDE = {models.TextField: {'widget': TextInput(attrs={'size': 100})}}


class InterfaceInline(admin.TabularInline):
    model = Interface.subcatalogs.through
    extra = 1

class InterfaceCatalogInline(admin.TabularInline):
    model = InterfaceCatalog
    fk_name = 'interface'
    extra = 0
    raw_id_fields = ('subcatalog',)
    ordering = ('order_position',)

class FunctionInline(admin.TabularInline):
    model = Function
    extra = 0
    fields = ('order_position', 'job', 'description',)
    ordering = ('order_position',)

class StoryInline(admin.TabularInline):
    model = Story
    extra = 0
    fields = ('order_position', 'title', 'got_wanted', 'description',)
    ordering = ('order_position',)

class StoryContextInline(admin.TabularInline):
    model = StoryContext
    extra = 0
    fields = ('order_position', 'text',)
    ordering = ('order_position',)
    formfield_overrides = CHAR_FIELD_LINE_OVERRIDE

class StartPointInline(admin.TabularInline):
    model = StartPoint
    extra = 1
    formfield_overrides = CHAR_FIELD_LINE_OVERRIDE

class StoryAcceptorInline(admin.TabularInline):
    model = StoryAcceptor
    extra = 0
    fields = ('order_position', 'text',)
    ordering = ('order_position',)
    formfield_overrides = CHAR_FIELD_LINE_OVERRIDE

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


class InterfaceSubCatalogFilter(admin.SimpleListFilter):
    title = 'Каталоги Интерфейсов'
    parameter_name = 'subcatalogs'

    def lookups(self, request, model_admin):
        subcatalogs = InterfaceSubCatalog.objects.all().order_by('title')
        return [(subcatalog.id, subcatalog.title) for subcatalog in subcatalogs]

    def queryset(self, request, queryset):
        if self.value():
            if hasattr(queryset.model, 'subcatalogs'):
                return queryset.filter(subcatalogs__id=self.value())
            elif hasattr(queryset.model, 'stories'):
                return queryset.filter(stories__interface__subcatalogs__id=self.value()).distinct()
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


@admin.register(InterfaceSubCatalog)
class InterfaceSubCatalogAdmin(admin.ModelAdmin):
    list_display   = ('title', 'get_interfaces', 'order_position',)
    search_fields  = ('title', 'interfaces__title')
    inlines = (InterfaceInline,)

    formfield_overrides = CHAR_FIELD_LINE_OVERRIDE

    def get_interfaces(self, obj):
        interfaces = obj.interfaces.all()
        interfaces_titles = [interface.title for interface in interfaces]
        return ", ".join(interfaces_titles)
    get_interfaces.short_description = 'Интерфейсы'


@admin.register(Interface)
class InterfaceAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'description',)
    search_fields = ('title', 'subtitle')
    list_filter = (InterfaceSubCatalogFilter,)
    inlines = (InterfaceCatalogInline,)
    
    formfield_overrides = CHAR_FIELD_LINE_OVERRIDE


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'interface', 'order_position',)
    search_fields = ('title',)
    list_filter = (InterfaceFilter,)
    inlines = (FunctionInline,)

    formfield_overrides = CHAR_FIELD_LINE_OVERRIDE


@admin.register(Function)
class FunctionAdmin(admin.ModelAdmin):
    list_display = ('job', 'get_role', 'get_interfaces', 'order_position',)
    search_fields = ('job',)
    list_filter = ('role', 'role__interface')
    raw_id_fields = ('role',)
    inlines = (
        StoryInline,
    )

    formfield_overrides = CHAR_FIELD_LINE_OVERRIDE

    def get_role(self, obj):
        return obj.role.title
    get_role.short_description = 'Роль'

    def get_interfaces(self, obj):
        return obj.role.interface.title
    get_interfaces.short_description = 'Интерфейс'


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'function', 'get_role', 'get_interface', 'order_position',)
    search_fields = ('title',)
    list_filter = ('function__role__interface', 'function__role', 'function',)
    raw_id_fields = ('function',)
    inlines = (
        StoryContextInline,
        StartPointInline,
        StoryAcceptorInline,
    )

    formfield_overrides = CHAR_FIELD_LINE_OVERRIDE

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


@admin.register(StoryAcceptor)
class StoryAcceptorAdmin(admin.ModelAdmin):
    list_display = (
        'get_interface',
        'get_role',
        'get_job',
        'get_story',
        'text',
    )

    list_select_related = ('story__function__role__interface',)

    list_filter = (
        ('story__function__role__interface', admin.RelatedOnlyFieldListFilter),
        ('story__function__role', admin.RelatedOnlyFieldListFilter),
        'story__function__job',
        ('story', admin.RelatedOnlyFieldListFilter),
    )

    raw_id_fields = ('story',)

    formfield_overrides = CHAR_FIELD_LINE_OVERRIDE

    def get_interface(self, obj):
        return obj.story.function.role.interface.title
    get_interface.short_description = 'Интерфейс'
    get_interface.admin_order_field = 'story__function__role__interface__title'

    def get_role(self, obj):
        return obj.story.function.role.title
    get_role.short_description = 'Роль'
    get_role.admin_order_field = 'story__function__role__title'

    def get_job(self, obj):
        return obj.story.function.job
    get_job.short_description = 'Ключевая Функция'
    get_job.admin_order_field = 'story__function__job'

    def get_story(self, obj):
        return obj.story.title
    get_story.short_description = 'Типичная История'
    get_story.admin_order_field = 'story__title'


@admin.register(AntiPattern)
class AntiPatternAdmin(nested_admin.NestedModelAdmin):
    list_display = ('title', 'subtitle', 'get_tags',)
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
