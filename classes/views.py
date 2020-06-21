from django.shortcuts import render
from django.views.generic import DetailView, ListView
from classes.models import ClassEntry, ShowClass

# Create your views here.
class EntryDetail(DetailView):
    model = ClassEntry
    slug_field = 'label'
    
class EntryList(DetailView):
    model = ShowClass
    
class ClassList(ListView):
    model = ShowClass
