from django.db import models
from datetime import datetime
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from radios.models import RStation




# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=50)
    short = models.CharField(max_length=5)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

class Artist(models.Model):
    name = models.CharField(max_length=600)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Style(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Label(models.Model):
    name = models.CharField(max_length=600)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class SongDatabase(models.Model):
    artist = models.ManyToManyField(Artist)
    title = models.CharField(max_length=900)
    name = models.CharField(max_length=900)
    feat = models.ManyToManyField(Artist, related_name="feat")

    clip = models.CharField(max_length=20, default="None")

    sp_uri = models.CharField(max_length=50, default="None")
    sp_prev = models.CharField(max_length=200, default="None")
    sp_pop = models.IntegerField(default=0)

    ds_album = models.CharField(max_length=300, default="None")
    ds_img = models.CharField(max_length=400, default="None")
    ds_thm = models.CharField(max_length=400, default="None")
    ds_country = models.ManyToManyField(Country, verbose_name='countries')
    ds_label = models.ManyToManyField(Label, verbose_name='labels')
    ds_genre = models.ManyToManyField(Genre, verbose_name='genres')
    ds_style = models.ManyToManyField(Style, verbose_name='styles')
    ds_year = models.IntegerField(default=0)

    total_plays = models.IntegerField()
    stations = models.ManyToManyField(RStation)
    slug = models.SlugField(unique=True, null=True, max_length=500)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('song_detail',
                       args=[str(self.slug)])

    def __str__(self):
        return self.name

    def ds_genre_f(self):
        return "|".join([p.name for p in self.ds_genre.all()])

    def ds_style_f(self):
        return "|".join([p.name for p in self.ds_style.all()])

    def ds_country_f(self):
        return "|".join([p.name for p in self.ds_country.all()])

    def stations_f(self):
        return "|".join([p.name for p in self.stations.all()])

    def sp_b(self):
        if self.sp_uri != "None":
            return True
        else:
            return False

    def yt_b(self):
        if self.clip != "None":
            return True
        else:
            return False

    def spo(self):
        pio = self.sp_uri.replace("spotify:track:", "")
        return pio

    sp_b.boolean = True
    yt_b.boolean = True

    #def emisje(self):
    #    em = HistoryTitler.objects.filter(song=self).order_by('-date')[:50]
    #    return em

    def _generate_unique_slug(self):
        unique_slug = slugify(self.name)
        num = 1
        while SongDatabase.objects.filter(slug=unique_slug).count() > 0:
            slug = '{}-{}'.format(unique_slug, num)
            num += 1
            unique_slug = slug
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)


