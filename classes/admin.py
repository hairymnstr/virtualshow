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

class ShowClassAdmin(admin.ModelAdmin):
    model = ShowClass
    fields = ('section', 'name', 'slug', 'description', 'show_age')
    list_display = ('name', 'section')

class ShowSectionAdmin(admin.ModelAdmin):
    model = ShowSection
    fields = ('name', 'slug', 'description')
    list_display = ('name',)

admin.site.register(ClassEntry, ClassEntryAdmin)
admin.site.register(ShowClass, ShowClassAdmin)
admin.site.register(ShowSection, ShowSectionAdmin)
