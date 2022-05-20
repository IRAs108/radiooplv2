from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from song.models import SongDatabase, Style, Genre, Label, Country, Artist
import json
from history.models import HistoryTitler
from radios.models import RStation


class Command(BaseCommand):
    help = 'Pobieranie danych titlera'

    def add_arguments(self, parser):
        parser.add_argument('--test', action='store_true', help='Testowa komenda', )
        parser.add_argument('--songs', action='store_true', help='Ładowanie pliku z utworami', )
        parser.add_argument('--style', action='store_true', help='Ladowanie pliku ze stylami muzycznymi', )
        parser.add_argument('--genre', action='store_true', help='Ladowanie pliku z gatunkami muzycznymi', )
        parser.add_argument('--country', action='store_true', help='Ladowanie pliku z państwami', )
        parser.add_argument('--artist', action='store_true', help='Ladowanie pliku z artystami muzycznymi', )
        parser.add_argument('--label', action='store_true', help='Ladowanie pliku z labelami muzycznymi', )
        parser.add_argument('--updatel', action='store_true', help='Aktualizacja radii i ilosci odtworzen', )







    def handle(self, *args, **options):

        if options['test']:
            print("Tu wykonują się testowe komendy")
            with open('songs.json') as json_file:
                data = json.load(json_file)
                for p in data:
                    print(p['fields']['name'])
        

        if options['updatel']:
            print("Aktualizacja ilosci odtworzen + stacje")
            for song in SongDatabase.objects.all():
                print(song.name)
                ilosc = HistoryTitler.objects.filter(rds=song.name).count()
                print(ilosc)
                song.listeners = ilosc
                song.save()
                for st in RStation.objects.all():
                    if HistoryTitler.objects.filter(rds=song.name, station=st):
                        song.stations.add(st)
                        song.save()
                


        if options['style']:
            print("Ladowanie styli muzycznych")
            with open('style.json') as json_file:
                data = json.load(json_file)
                for p in data:
                    st = Style(pk=p['pk'], name=p['fields']['name'])
                    st.save()
                    print(p)

        if options['genre']:
            print("Ladowanie gatunków muzycznych")
            with open('genre.json') as json_file:
                data = json.load(json_file)
                for p in data:
                    genre = Genre(pk=p['pk'], name=p['fields']['name'])
                    genre.save()
                    print(p['fields']['name'])

        if options['country']:
            print("Ladowanie panstw")
            with open('country.json') as json_file:
                data = json.load(json_file)
                for p in data:
                    country = Country(pk=p['pk'], name=p['fields']['name'], short=p['fields']['short'])
                    country.save()
                    print(p['fields']['name'])

        if options['artist']:
            print("Ladowanie artystów muzycznych")
            with open('artist.json') as json_file:
                data = json.load(json_file)
                for p in data:
                    artist = Artist(pk=p['pk'], name=p['fields']['name'])
                    artist.save()
                    print(p['fields']['name'])

        if options['label']:
            print("Ladowanie label'i muzycznych")
            with open('label.json') as json_file:
                data = json.load(json_file)
                for p in data:
                    label = Label(pk=p['pk'], name=p['fields']['name'])
                    label.save()
                    print(p['fields']['name'])

        if options['songs']:
            print("Ladowanie utworów muzycznych")
            with open('songs.json') as json_file:
                data = json.load(json_file)
                for p in data:
                    song = SongDatabase(pk=p['pk'], title=p['fields']['title'], name=p['fields']['name'], clip=p['fields']['clip'], sp_uri=p['fields']['sp_uri'], sp_prev=p['fields']['sp_prev'], sp_pop=p['fields']['sp_pop'], ds_album=p['fields']['ds_album'], ds_img=p['fields']['ds_img'], ds_thm=p['fields']['ds_thm'], ds_year=p['fields']['ds_year'], total_plays=p['fields']['total_plays'], slug=p['fields']['slug'], created=p['fields']['created'], updated=p['fields']['updated'])
                    #song = SongDatabase(pk=p['pk'], title=p['fields']['title'], name=p['fields']['name'], clip=p['fields']['clip'], sp_uri=p['fields']['sp_uri'], sp_prev=p['fields']['sp_prev'], sp_pop=p['fields']['sp_pop'], ds_album=p['fields']['ds_album'], ds_img=p['fields']['ds_img'], ds_thm=p['fields']['ds_thm'], ds_year=p['fields']['ds_year'], total_plays=p['fields']['total_plays'], slug=p['fields']['slug'], created=p['fields']['created'], updated=p['fields']['updated'])
                    
                    song.save()
                    print(p['fields']['name'])