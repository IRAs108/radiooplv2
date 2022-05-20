from django.contrib import admin
from .models import Listeners

# Register your models here.
class ListenersAdmin(admin.ModelAdmin):
    search_fields = ['station.name']
    list_display = ['time', 'station', 'listeners']

admin.site.register(Listeners, ListenersAdmin)