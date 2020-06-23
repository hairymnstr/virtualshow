from django.shortcuts import render
from django.views.generic import DetailView, ListView, View
from classes.models import ClassEntry, ShowClass, EntryImage

# Create your views here.
class EntryDetail(DetailView):
    model = ClassEntry
    slug_field = 'label'
    
class EntryList(View):
    template = "classes/showclass_detail.html"
    
    def get(self, request, slug, *args, **kwargs):
        entries = EntryImage.objects.filter(entry__show_class__slug=slug)
        return render(request, self.template, {'entries': entries})
    
class ClassList(ListView):
    model = ShowClass
