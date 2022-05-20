"""
Definition of urls for radiooplv2.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls.static import static # new
from django.conf import settings # new 
from radios.views import RadioListView, RadioDetailView, getstations, HomePage
from history.views import radionow
from song.views import searchsongajax
from song.views import SongDetailView
from history.views import history_list
from history.views import datepicksong
from history.views import Historia
from song.views import getsongaj


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ajax/now/', radionow, name="now"),
    path('ajax/search/', searchsongajax, name="search"),
    path('stacje', RadioListView.as_view(), name='station_list'),
    path('', HomePage, name='home'),
    path('stacja/<slug>/', RadioDetailView.as_view(), name='station_detail'),
    path('utwor/<slug>/', SongDetailView.as_view(), name='song_detail'),
    path('last/', history_list, name='history_list'),
    path('ajax/datepicker', datepicksong, name='datepicksong'),
    path('ajax/song', getsongaj, name='getsongaj'),
    path('historia/', Historia, name='history'),
    path('android/stations/', getstations, name='getstations'),

]
if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
