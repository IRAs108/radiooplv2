from django.shortcuts import render
import redis
from history.models import HistoryTitler
from song.models import SongDatabase
from radios.models import RStation
from datetime import datetime
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers




# Create your views here.
rd = redis.Redis(host='localhost', port=6379, db=2)
nw = redis.Redis(host='localhost', port=6379, db=1)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'



def radionow(request):
    station = request.GET.get('st')
    position = request.GET.get('p')
    if position:
        h = HistoryTitler.objects.all().filter(station=station).order_by('-date')[int(position)]
        rds = h.rds
        song = h.song
        # d = h.date.tz('Europe/Warsaw')
        d = timezone.localtime(h.date, pytz.timezone('Europe/Warsaw'))
    else:
        try:
            rds = str(nw.get("station:" + station + ":n").decode('utf8'))
        except:
            rds = "None"
        song = SongDatabase.objects.all().filter(name=rds).first()
        d = datetime.now()

    if song:
        sp = song.sp_uri
        youtube = song.clip
        prev = song.sp_prev
        year = song.ds_year
        img = song.ds_img
    else:
        sp = "None"
        youtube = "None"
        prev = "None"
        year = 0
        d = datetime.now()
        img = "None"
    artit = rds.split(" - ")
    try:
        title = artit[1]
    except:
        title = "None"
    name = RStation.objects.filter(pk=station).last().name
    if d.minute < 10:
        minuty = "0" + str(d.minute)
    else:
        minuty = str(d.minute)

    time = str(d.hour) + ":" + minuty
    now = {"date": d, "time": time, "rds": rds, "name": name, "spotify": sp.replace("spotify:track:", ""),
           "youtube": youtube, "preview": prev,
           "year": year, "img": img, "artist": artit[0], "title": title}
    return JsonResponse(now)

def Historia(request):
    stations = RStation.objects.all()[:3]
    return render(request, 'history/history.html', {'stations': stations})


def history_list(request):
    station = request.GET.get('st')
    history = HistoryTitler.objects.all().filter(station=station).order_by('-date')
    paginator = Paginator(history, 20)
    page = request.GET.get('page')
    try:
        history = paginator.page(page)
    except PageNotAnInteger:

        history = paginator.page(1)
    except EmptyPage:
        if is_ajax(request=request):
            return HttpResponse('')
        history = paginator.page(paginator.num_pages)
    if is_ajax(request=request):
        return render(request,
                      'ajax/last_ajax.html',
                      {'section': 'rds', 'rds': history})
    return render(request,
                  'ajax/last.html',
                  {'section': 'rds', 'rds': history, 'station': station})


def datepicksong(request):
    year = request.GET.get('y')
    month = request.GET.get('m')
    day = request.GET.get('d')
    hour = request.GET.get('h')
    st = request.GET.get('s')
    dtm = datetime(year=int(year), month=int(month)+1, day=int(day), hour=int(hour))
    history = HistoryTitler.objects.all().filter(station=st, date__gt=dtm).order_by('date')[:20]
    qs_json = serializers.serialize('json', history)

    return HttpResponse(qs_json, content_type='application/json')

