from django.shortcuts import render
from django.views.generic import ListView, DetailView
from requests import request
from radios.models import RStation
from history.models import HistoryTitler
from song.models import SongDatabase
from django.db.models import Count
from django.core import serializers
from django.http import JsonResponse, HttpResponse


# Create your views here.

def HomePage(request):
    template_name = 'home.html'

    return render(request, 'home.html')



class RadioListView(ListView):
    model = RStation

class RadioDetailView(DetailView):
    model = RStation
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        krr = []
        krrt = []
        # query = self.request.GET.get('st')
        # st = History.objects.all().filter(station=query).order_by('-date')
        context = super().get_context_data(**kwargs)
        hist = HistoryTitler.objects.all().filter(station=kwargs['object']).order_by('-date')[:40]
        # page = self.GET.get('page')
        # paginator = Paginator(hist, 10)
        # page = 1
        # context_object_name = 'history'
        # paginate_by = 10
        # template_name = 'scrobbel/station_detail.html'
        context['last_hist'] = hist

        for hh in hist:
            try:
                cnt = int(rd.get("m;" + str(kwargs['object'].id) + ";" + str(hh.song.id)))
            except:
                cnt = 0
            krr.append(cnt)
        for hh in hist:
            try:
                cnt = int(rd.get("w;" + str(kwargs['object'].id) + ";" + str(hh.song.id)))
            except:
                cnt = 0
            krrt.append(cnt)
        zipped = zip(hist, krr, krrt)
        context['last_hist'] = zipped
        context['historia'] = hist
        try:
            context['now'] = str(nw.get("station:" + str(kwargs['object'].id) + ":n").decode("utf-8"))
        except:
            context['now'] = "None"
        toplist = SongDatabase.objects.filter(stations=kwargs['object']).order_by('-total_plays')[:20]
        newsong = SongDatabase.objects.filter(stations=kwargs['object']).order_by('-pk')[:20]
        uniquesong = SongDatabase.objects.annotate(stn=Count('stations')).filter(stations=kwargs['object']).filter(stn=1).order_by('-total_plays')[:20]
        context['toplist'] = toplist
        context['newsong'] = newsong
        context['unique'] = uniquesong

        return context

def getstations(request):
    # spk = request.GET.get('s')
    data = RStation.objects.all()
    qs_json = serializers.serialize('json', data)

    return HttpResponse(qs_json, content_type='application/json')