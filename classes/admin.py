from django.contrib import admin
from classes.models import ShowClass, ClassEntry, EntryImage, ShowSection
# Register your models here.

class EntryImageInline(admin.TabularInline):
    model = EntryImage
    readonly_fields = ('preview_tag',)
    fields = ('img', ('thumbnail', 'preview_tag'))

class ClassEntryAdmin(admin.ModelAdmin):
    model = ClassEntry
    readonly_fields = ('modified', 'created')
    fields = ('title', 'caption', ('created', 'modified'), 'show_class', 'entry_no', 'entrant', 'age', 'place', 'comments')
    ordering = ('show_class', 'entry_no')
    list_display = ('title', 'entrant', 'age', 'modified', 'place', 'show_class', 'entry_no')
    inlines = [EntryImageInline]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(show_class__section__group__in=request.user.groups.all())
    
    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['show_class'].queryset = ShowClass.objects.filter(section__group__in=request.user.groups.all())
        return super(ClassEntryAdmin, self).render_change_form(request, context, *args, **kwargs)

class ShowClassAdmin(admin.ModelAdmin):
    model = ShowClass
    fields = ('section', 'name', 'slug', 'description', 'show_age')
    list_display = ('name', 'section')

class ShowSectionAdmin(admin.ModelAdmin):
    model = ShowSection
    fields = ('name', 'slug', 'description', 'group')
    list_display = ('name',)

admin.site.register(ClassEntry, ClassEntryAdmin)
admin.site.register(ShowClass, ShowClassAdmin)
admin.site.register(ShowSection, ShowSectionAdmin)
