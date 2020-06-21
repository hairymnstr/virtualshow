from django.conf.urls import url
from game.views import LocationDetail, TransportDetail

urlpatterns = [
    url(r'^location/(?P<slug>[-\w]+)/?$', LocationDetail.as_view()),
    url(r'^transport/(?P<slug>[-\w]+)/?$', TransportDetail.as_view()),
]
