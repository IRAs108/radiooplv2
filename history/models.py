from django.db import models
from radios.models import RStation
from song.models import SongDatabase

# Create your models here.
class HistoryTitler(models.Model):
    rds = models.CharField(max_length=150)
    station = models.ForeignKey(RStation, on_delete=models.CASCADE)
    listeners = models.IntegerField(default=0)
    date = models.DateTimeField()
    song = models.ForeignKey(SongDatabase, on_delete=models.CASCADE)

    def __str__(self):
        return "{date} - {station} - {text}".format(date=self.date, station=self.station, text=self.rds)

    def spo(self):
        pio = self.song.sp_uri.replace("spotify:track:", "")
        return pio

    def last(self):
        now = self.date
        return now