from django.db import models
from radios.models import RStation

# Create your models here.

class Listeners(models.Model):
    station = models.ForeignKey(RStation, on_delete=models.PROTECT)
    listeners = models.SmallIntegerField()
    time = models.DateTimeField()
    def __str__(self):
        return str(self.time) +' '+self.station.name+' - '+str(self.listeners)
