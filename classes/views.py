from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView, View
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.conf import settings
from classes.models import ClassEntry, ShowClass, EntryImage, ShowSection

BANNER_LOGGED_IN = "You are currently logged in.  The content you are viewing is not all visible to the public until show day."
BANNER_EMBARGOED = "Entries will be visible on show day.  Please visit <a href='https://stithians.show/'>stithians.show</a> to download the schedules and find entry details."

# Create your views here.
class EntryList(View):
    template = "classes/showclass_detail.html"
    
    def get(self, request, slug, *args, **kwargs):
        if request.user.is_authenticated or settings.PUBLIC_VIEWING:
            showclass = get_object_or_404(ShowClass, slug=slug);
            if showclass.section.show_results:
                entries = EntryImage.objects.filter(entry__show_class__slug=slug)
            else:
                # don't order by placing yet!
                entries = EntryImage.objects.filter(entry__show_class__slug=slug).order_by('entry__entry_no')
            return render(request, self.template, {'entries': entries, 'showclass': showclass})
        else:
            raise PermissionDenied
    
class ClassList(View):
    template = "classes/showclass_list.html"
    
    def get(self, request, slug, *args, **kwargs):
        is_public = request.user.is_authenticated or settings.PUBLIC_VIEWING
        banner = None
        if not is_public:
            banner = BANNER_EMBARGOED
        elif request.user.is_authenticated:
            banner = BANNER_LOGGED_IN
        
        section = get_object_or_404(ShowSection, slug=slug)
        showclass_list = ShowClass.objects.filter(section__slug=slug)
        return render(request, self.template, {'showclass_list': showclass_list, 'section': section, 'public': is_public, 'banner': banner})

class SectionList(View):
    template = "classes/showsection_list.html"
    template_unauth = "classes/showclass_preshow.html"

    def get(self, request, *args, **kwargs):
        is_public = request.user.is_authenticated or settings.PUBLIC_VIEWING
        banner = None
        if not is_public:
            banner = BANNER_EMBARGOED
        elif request.user.is_authenticated:
            banner = BANNER_LOGGED_IN
        showsection_list = ShowSection.objects.all()
        return render(request, self.template, {'showsection_list': showsection_list, 'public': is_public, 'banner': banner})
        
