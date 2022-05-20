from django.db import models

# Create your models here.

from django.utils.text import slugify

# Create your models here.

class Stream(models.Model):
    name = models.CharField(max_length=150)
    url = models.URLField(max_length=200, blank=True)
    STREAM_CHOICES = (
    ("LISTENOGG", "Listen OGG"),
    ("LISTENMP3", "Listen MP3"),
    ("LISTENAAC", "Listen AAC"),
    ("LISTENERS", "Listeners"),
    ("LISTENERSOGG", "Listeners OGG"),
    ("LISTENERSMP3", "Listeners MP3"),
    ("LISTENERSAAC", "Listeners AAC"),
    ("METADATA", "Metadane"),
    )

    type = models.CharField(max_length=16,
                  choices=STREAM_CHOICES,
                  default="LISTENMP3")
    def __str__(self):
        return self.name


class RStation(models.Model):
    name = models.CharField(max_length=150)
    website = models.URLField(max_length=200, blank=True)
    stream = models.ManyToManyField(Stream)
    country = models.ForeignKey('Country', on_delete=models.PROTECT)
    state = models.ForeignKey('State', on_delete=models.PROTECT)
    city = models.ForeignKey('City', on_delete=models.PROTECT)
    img = models.ImageField(upload_to='stations/', width_field='width', height_field='height', blank=True)
    width = models.IntegerField(editable=False, null=True)
    height = models.IntegerField(editable=False, null=True)
    info = models.TextField(null=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    tagurl = models.ForeignKey(Stream, on_delete=models.PROTECT, related_name="titler", blank=True, null=True)
    methodtag = models.IntegerField()

    listenersurl = models.ManyToManyField(Stream, related_name="listeners", blank=True, null=True)
    listenermethod = models.SmallIntegerField()

    playlist_sp_url = models.CharField(max_length=100, default="None")
    playlist_yt_url = models.CharField(max_length=100, default="None")




    def __str__(self):
        return self.name
    def _generate_unique_slug(self):
        unique_slug = slugify(self.name)
        num = 1
        while RStation.objects.filter(slug=unique_slug).exists():
            slug = '{}-{}'.format(unique_slug, num)
            num += 1
            return slug
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)



class Country(models.Model):
    name = models.CharField(max_length=100)
    short = models.CharField(max_length=4)
    #ludn = models.IntegerField()
    img = models.ImageField(upload_to='country/', width_field='width', height_field='height', blank=True)
    width = models.IntegerField(editable=False, null=True)
    height = models.IntegerField(editable=False, null=True)
    # w przyszlosci dodac obrazek flagi

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=150)
    country = models.ForeignKey('Country', on_delete=models.PROTECT)
    #ludn = models.IntegerField()
    img = models.ImageField(upload_to='state/', width_field='width', height_field='height', blank=True)
    width = models.IntegerField(editable=False, null=True)
    height = models.IntegerField(editable=False, null=True)
    # w przyszlosci dodac obrazek flagi

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=150)
    state = models.ForeignKey('State', on_delete=models.PROTECT)
    #ludn = models.IntegerField()
    img = models.ImageField(upload_to='city/', width_field='width', height_field='height', blank=True)
    width = models.IntegerField(editable=False, null=True)
    height = models.IntegerField(editable=False, null=True)
    # w przyszlosci dodac obrazek flagi

    def __str__(self):
        return self.name

