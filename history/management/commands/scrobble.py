from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from radios.models import RStation
import urllib.request, json 
from history.models import HistoryTitler
from song.models import SongDatabase, Artist, Genre, Style, Country, Label
from redis import StrictRedis
from ._get_rds import get_meta_revma, get_meta_rmfon, get_meta_eurozet, replacer
#from ._yt2mp3_util import get_video_url
from ._discogs import get_disc
from ._spotify import sp_data, add_track_to_playlist
from youtube_search import YoutubeSearch



class Command(BaseCommand):
    help = 'Pobieranie danych titlera'

    def add_arguments(self, parser):
        parser.add_argument('--test', action='store_true', help='Testowa komenda', )
        parser.add_argument('--import', action='store_true', help='Import bazy', )
        parser.add_argument('--get', action='store_true', help='Pobieranie danych titlera', )
        parser.add_argument('--add', action='store_true', help='Przenoszenie danych titlera', )



    def handle(self, *args, **options):

        if options['test']:
             metadate = get_meta_rmfon("https://www.rmfon.pl/stacje/playlista_5.json.txt")
             print(metadate)

        if options['import']:
            print("Importuje baze")
            with open('history.json') as json_file:
                data = json.load(json_file)
                for p in data:
                    if p['fields']['station']==5:
                        print(p)
                        hist = HistoryTitler(rds=p['fields']['rds'], listeners=p['fields']['listeners'], date=p['fields']['date'])
                        hist.station = RStation.objects.filter(pk=5).last()
                        hist.song = SongDatabase.objects.filter(pk=p['fields']['song']).last()
                        hist.save()

        if options['get']:
            print("Pobieram dane titlera")
            rd = StrictRedis(host='localhost', port=6379, db=1)
            rdn = StrictRedis(host='localhost', port=6379, db=1)
            stations = RStation.objects.all()

            for st in stations:
                print(st)
                if st.methodtag==1: # revma
                    metadate = get_meta_revma(st.tagurl.url)
                    print(metadate)
                elif st.methodtag==2:
                    metadate = get_meta_rmfon(st.tagurl.url)
                elif st.methodtag==3:
                    metadate = get_meta_eurozet(st.tagurl.url)

                if st.listenermethod==1:
                    listnrs = st.listenersurl.all()
                    count = 0
                    for lis in listnrs:
                        with urllib.request.urlopen(lis.url) as url:
                            listenersjson = json.loads(url.read().decode())
                        count_str = 0
                        for listeners1 in listenersjson['data']:
                            count_str += listeners1['count']
                        count += count_str #suma słuchaczy
                    print(count) 
                
                # Tutaj zapisuje do kolejki redis
                klucz = "station:" + str(st.id)
                czas = str(timezone.now())
                wartosc = str(czas) + "|" + metadate + "|" + str(count)
                rd.lpush(klucz, wartosc)
                rd.close()
                #a tutaj obecnie nadawany
                now = replacer(metadate)
                try:
                    now2 = now['rds']
                except:
                    print("Pomijam")
                    continue

                klucz = klucz + ":n"
                rdn.set(klucz, now2, 200)




                ###STARY KOD###
                #if st.service_ndj_url != "None":
                #    metadata = get_meta_service(st.service_ndj_url, st.service_ndj_id)

                #else:
                #    metadata = get_meta_stream(st.stream_url)

                # print(st)
                #klucz = "station:" + str(st.id)
                #czas = str(timezone.now())
                #wartosc = str(czas) + "|" + metadata[0] + "|" + str(metadata[1])
                # print(wartosc)

                #rd.lpush(klucz, wartosc)
                #rd.close()
                #try:
                #    now = str(replacer(metadata[0])['rds'])
                #except:
                #    now = "STACJA OBECNIE NIE EMITUJE UTWORU"
                #klucz = klucz + ":n"
                #rdn.set(klucz, now, 200)
                ###STARY KOD###

        if options['add']:
            # print('Test')
            rd = StrictRedis(host='localhost', port=6379, db=1)
            rdc = StrictRedis(host='localhost', port=6379, db=2)
            for st in RStation.objects.all():
                klucz = "station:" + str(st.id)
                try:
                    try:
                        last_song_h = HistoryTitler.objects.filter(station=st).last()
                        last = last_song_h.rds
                    except:
                        last = "Init"
                    
                except:
                    continue

                ln = rd.llen(klucz)
                for i in range(ln):
                    try:
                        nowrds = rd.rpop(klucz).decode("utf-8")
                        nowrds = str(nowrds).split("|")
                        now = replacer(nowrds[1])
                        nrd = now['rds']
                    except:
                        continue
                    # print(last)
                    # print(nrd)
                    if last == nrd:
                        continue
                    else:
                        print(now)
                        date_n = nowrds[0]
                        listeners_n = nowrds[2]
                        last = now['rds']
                        try:
                            song = SongDatabase.objects.filter(name=now["rds"]).last()
                        except:
                            continue
                        if song is None:

                            # GET METADATA FROM SPOTIFY DISCOGS YOUTUBE
                            name = now['rds']
                            artist = name.split(' - ')[0]
                            title = name.split(' - ')[1]
                            clip = ""
                            """
                            clip = get_video_url({"artist_name": artist, "track_name": title})
                            if clip is None:
                                clip = "None"
                            else:
                                clip = clip.replace("https://www.youtube.com/watch?v=", "")
                            """
                            ytsearch = YoutubeSearch(name, max_results=1).to_dict()
                            try:
                                clip = ytsearch[0]["id"]
                            except:
                                clip = "None"
                            disc_style = ["None"]

                            disc_data = get_disc(name)
                            if disc_data is None:
                                disc_alb = "None"
                                disc_label = "None"
                                disc_genre = ["None"]
                                disc_style = ["None"]
                                disc_country = "None"
                                disc_image = "None"
                                disc_thumb = "None"
                                disc_year = 0
                            else:
                                """
                                print("Album: {name}".format(name=disc_data[0]))
                                print("Label: {name}".format(name=disc_data[1]))
                                print("Genre: {name}".format(name=disc_data[2]))
                                print("Style: {name}".format(name=disc_data[3]))
                                print("Country: {name}".format(name=disc_data[4]))
                                print("Image: {name}".format(name=disc_data[5]))
                                print("Thumb: {name}".format(name=disc_data[6]))
                                """
                                disc_alb = disc_data[0]
                                disc_label = disc_data[1]
                                disc_genre = disc_data[2]
                                disc_style = disc_data[3]
                                disc_country = disc_data[4]
                                disc_image = disc_data[5]
                                disc_thumb = disc_data[6]
                                disc_year = disc_data[7]

                            spd = sp_data(name)

                            spd_uri = "None"
                            spd_preview = "None"
                            spd_popularity = 0

                            for i, t in enumerate(spd['tracks']['items']):
                                spd_popularity = int(t['popularity'])
                                spd_preview = t['preview_url']
                                spd_uri = t['uri']

                            if spd_preview is None:
                                spd_preview = "None"

                            # END

                            if spd_uri != "None":
                                add_track_to_playlist(st.playlist_sp_url, spd_uri)
                            # print("Dodano do playlisty Spotify")

                            song = SongDatabase(title=now["title"], name=now["rds"], clip=clip, sp_uri=spd_uri,
                                        sp_prev=spd_preview,
                                        sp_pop=spd_popularity, ds_album=disc_alb, ds_img=disc_image, ds_thm=disc_thumb,
                                        ds_year=disc_year, total_plays=1)

                            song.save()
                            for art in now['artist']:
                                s_art = Artist.objects.filter(name=art).last()
                                if s_art is None:
                                    s_art = Artist(name=art)
                                    s_art.save()
                                song.artist.add(s_art)
                                song.save()

                            sfe = Artist.objects.filter(name=now["feat"]).last()
                            if sfe is None:
                                sfe = Artist(name=now["feat"])
                                sfe.save()
                            song.feat.add(sfe)
                            song.save()

                            country = Country.objects.filter(name=disc_country).last()
                            if country is None:
                                country = Country(name=disc_country)
                                country.save()
                            song.ds_country.add(country)
                            song.save()

                            for gnr in disc_genre:
                                genre = Genre.objects.filter(name=gnr).last()
                                if genre is None:
                                    genre = Genre(name=gnr)
                                    genre.save()
                                song.ds_genre.add(genre)
                                song.save()
                            try:
                                for gnr in disc_style:
                                    style = Style.objects.filter(name=gnr).last()
                                    if style is None:
                                        style = Style(name=gnr)
                                        style.save()
                                    song.ds_style.add(style)
                                    song.save()
                            except:
                                print("Error")
                            label = Label.objects.filter(name=disc_label).last()
                            if label is None:
                                label = Label(name=disc_label)
                                label.save()
                            song.ds_label.add(label)
                            song.save()

                        # print(song)
                        total = int(HistoryTitler.objects.filter(song=song).count()) + 1
                        # print(total)
                        song.stations.add(st)
                        song.total_plays = total
                        song.save()

                        # lhs = History.objects.filter(station=hist.station).last()
                        # if lhs != hist:
                        move = HistoryTitler(rds=now['rds'], listeners=listeners_n, station=st,
                                       date=date_n
                                       , song=song)
                        move.save()

                        songm = "m;" + str(st.id) + ";" + str(song.id)
                        songt = "w;" + str(st.id) + ";" + str(song.id)
                        # print(songm)
                        rdc.incr(songm)
                        rdc.incr(songt)


                        
