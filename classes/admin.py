from django.contrib import admin
from classes.models import ShowClass, ClassEntry
# Register your models here.

class ClassEntryAdmin(admin.ModelAdmin):
    model = ClassEntry
    readonly_fields = ('preview_tag', 'modified', 'created')
    fields = ('img', ('thumbnail', 'preview_tag'), 'title', 'caption', ('created', 'modified'), 'show_class', 'entrant', 'age', 'comments')
    ordering = ('-created',)
    list_display = ('title', 'entrant', 'age', 'modified','show_class')

class ShowClassAdmin(admin.ModelAdmin):
    model = ShowClass
    readonly_fields = ('preview_tag',)
    fields = ('img', ('thumbnail', 'preview_tag'), 'name', 'slug', 'description')
    list_display = ('name',)

admin.site.register(ClassEntry, ClassEntryAdmin)
admin.site.register(ShowClass, ShowClassAdmin)
