from django.contrib import admin

# Register your models here.
from .models import RStation, Country, State, City, Stream
# Register your models here.

class StreamAdmin(admin.ModelAdmin):
    pass

class StationAdmin(admin.ModelAdmin):
    pass

class CountryAdmin(admin.ModelAdmin):
    pass

class StateAdmin(admin.ModelAdmin):
    pass

class CityAdmin(admin.ModelAdmin):
    pass

admin.site.register(RStation, StationAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Stream, StreamAdmin)
