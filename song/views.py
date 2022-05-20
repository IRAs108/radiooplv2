from django.shortcuts import render
from song.models import SongDatabase
from radios.models import RStation
from history.models import HistoryTitler
from django.views.generic import DetailView
from datetime import datetime
from datetime import timedelta
from django.core import serializers
from django.http import JsonResponse, HttpResponse


# Create your views here.
class SongDetailView(DetailView):
    model = SongDatabase
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        style = kwargs['object'].ds_style.all()
        year = kwargs['object'].ds_year
        similar = SongDatabase.objects.all().filter(ds_style__in=style, ds_year__gte=year - 3, ds_year__lte=year + 1).order_by(
            '-total_plays')[:10]
        #similar = similar.order_by('?')[:5]
        context['similar'] = similar
        #context['form'] = SimpleEditSong(
        #    initial={'id': kwargs['object'].id, 'clip': kwargs['object'].clip, 'spo_uri': kwargs['object'].sp_uri,
        #             'rok': kwargs['object'].ds_year
        #             })
        context['data'] = {'Python': 52.9, 'Jython': 1.6, 'Iron Python': 27.7}
        context['line_data'] = list(enumerate(range(1, 20)))
        rrr = {}
        for st in RStation.objects.all():
            ile = HistoryTitler.objects.all().filter(station=st, song=kwargs['object']).count()
            if ile > 0:
                rrr[st.name] = ile
        context['data'] = rrr
        ll = []
        for dayy in range(90, 1, -1):
            ile = HistoryTitler.objects.all().filter(song=kwargs['object'], date__gte=datetime.now() - timedelta(days=dayy),
                                               date__lte=datetime.now() - timedelta(days=dayy - 1)).count()
            ll.append((dayy, ile))
            # ll.reverse()
        context['line_data'] = ll
        em = HistoryTitler.objects.filter(song=kwargs['object']).order_by('-date')[:50]
        context['emisje'] = em

        return context

def getsongaj(request):
    spk = request.GET.get('s')
    data = SongDatabase.objects.all().filter(pk=spk)
    qs_json = serializers.serialize('json', data)

    return HttpResponse(qs_json, content_type='application/json')

def searchsongajax(request):
    query = request.GET.get('search')
    data = SongDatabase.objects.filter(name__icontains=query).order_by('-total_plays')[:20]
    qs_json = serializers.serialize('json', data)

    return HttpResponse(qs_json, content_type='application/json')