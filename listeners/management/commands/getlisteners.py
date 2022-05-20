from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from radios.models import RStation
from listeners.models import Listeners
import urllib.request, json 


class Command(BaseCommand):
    help = 'Pobieranie statystyk sluchalności'

    def add_arguments(self, parser):
        parser.add_argument('--test', action='store_true', help='Testowa komenda', )
        parser.add_argument('--getlisteners', action='store_true', help='Pobieranie słuchalności', )



    def handle(self, *args, **options):

        if options['test']:
            print("Tu wykonują się testowe komendy")


        if options['getlisteners']:
            dtn = timezone.now()
            for st in RStation.objects.all():
                if st.listenermethod==1:
                    listnrs = st.listenersurl.all()
                    count = 0
                    for lis in listnrs:
                        print(lis.name)
                        with urllib.request.urlopen(lis.url) as url:
                            listenersjson = json.loads(url.read().decode())
                            #print(listenersjson)
                        count_str = 0
                        for listeners1 in listenersjson['data']:
                            #print(listeners1['country_name'])
                            #print(listeners1['country_code'])
                            #print(listeners1['count'])
                            count_str += listeners1['count']
                        #print(count_str)
                        count += count_str #suma słuchaczy
                    print(count)
                    listn = Listeners(station=st, listeners=count, time=dtn)
                    listn.save()