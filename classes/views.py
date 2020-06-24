from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView, View
from django.http import Http404
from django.conf import settings
from classes.models import ClassEntry, ShowClass, EntryImage

# Create your views here.
class EntryList(View):
    template = "classes/showclass_detail.html"
    
    def get(self, request, slug, *args, **kwargs):
        if request.user.is_authenticated or settings.PUBLIC_VIEWING:
            showclass = get_object_or_404(ShowClass, slug=slug);
            entries = EntryImage.objects.filter(entry__show_class__slug=slug)
            return render(request, self.template, {'entries': entries, 'showclass': showclass})
        else:
            raise Http404('Not authorised')
    
class ClassList(View):
    template = "classes/showclass_list.html"
    template_unauth = "classes/showclass_preshow.html"
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated or settings.PUBLIC_VIEWING:
            showclass_list = ShowClass.objects.all()
            return render(request, self.template, {'showclass_list': showclass_list})
        else:
            return render(request, self.template_unauth, {})
