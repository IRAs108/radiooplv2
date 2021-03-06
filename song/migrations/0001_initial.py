# Generated by Django 3.1.7 on 2021-03-04 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('radios', '0002_auto_20210304_1303'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=600)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('short', models.CharField(max_length=5)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=600)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Style',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='SongDatabase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=600)),
                ('name', models.CharField(max_length=600)),
                ('clip', models.CharField(default='None', max_length=20)),
                ('sp_uri', models.CharField(default='None', max_length=50)),
                ('sp_prev', models.CharField(default='None', max_length=200)),
                ('sp_pop', models.IntegerField(default=0)),
                ('ds_album', models.CharField(default='None', max_length=300)),
                ('ds_img', models.CharField(default='None', max_length=400)),
                ('ds_thm', models.CharField(default='None', max_length=400)),
                ('ds_year', models.IntegerField(default=0)),
                ('total_plays', models.IntegerField()),
                ('slug', models.SlugField(max_length=500, null=True, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('artist', models.ManyToManyField(to='song.Artist')),
                ('ds_country', models.ManyToManyField(to='song.Country', verbose_name='countries')),
                ('ds_genre', models.ManyToManyField(to='song.Genre', verbose_name='genres')),
                ('ds_label', models.ManyToManyField(to='song.Label', verbose_name='labels')),
                ('ds_style', models.ManyToManyField(to='song.Style', verbose_name='styles')),
                ('feat', models.ManyToManyField(related_name='feat', to='song.Artist')),
                ('stations', models.ManyToManyField(to='radios.Station')),
            ],
        ),
    ]
