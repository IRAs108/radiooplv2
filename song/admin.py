from django.contrib import admin
from .models import SongDatabase, Country, Artist, Genre, Style, Label

# Register your models here.

class CountryAdmin(admin.ModelAdmin):
    search_fields = ['name', 'short']
    ordering = ['name']
    list_display = ['name', 'short']

class CountryAdmin(admin.ModelAdmin):
    pass

class GenreAdmin(admin.ModelAdmin):
    pass


class StyleAdmin(admin.ModelAdmin):
    pass


class LabelAdmin(admin.ModelAdmin):
    pass


class ArtistAdmin(admin.ModelAdmin):
    pass



class SongAdmin(admin.ModelAdmin):
    search_fields = ['name', 'ds_genre__name', 'ds_country__name', 'ds_style__name', 'ds_year']
    list_display = ['name', 'ds_album', 'ds_year', 'ds_genre_f', 'ds_style_f', 'ds_country_f', 'sp_pop', 'sp_b', 'yt_b',
                    'total_plays', 'stations_f']
    list_filter = ['stations__name', 'ds_year', 'ds_genre__name', 'ds_style__name', 'ds_country__name']
    list_editable = ['ds_year']







admin.site.register(Country, CountryAdmin)
#admin.site.register(Station, StationAdmin)
#admin.site.register(HistLast, LastHistAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(SongDatabase, SongAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Style, StyleAdmin)
admin.site.register(Label, LabelAdmin)
#admin.site.register(History, HistoryAdmin)