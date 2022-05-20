# Generated by Django 3.1.7 on 2021-03-04 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('img', models.ImageField(blank=True, height_field='height', upload_to='city/', width_field='width')),
                ('width', models.IntegerField(editable=False, null=True)),
                ('height', models.IntegerField(editable=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('short', models.CharField(max_length=4)),
                ('img', models.ImageField(blank=True, height_field='height', upload_to='country/', width_field='width')),
                ('width', models.IntegerField(editable=False, null=True)),
                ('height', models.IntegerField(editable=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('img', models.ImageField(blank=True, height_field='height', upload_to='state/', width_field='width')),
                ('width', models.IntegerField(editable=False, null=True)),
                ('height', models.IntegerField(editable=False, null=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='radios.country')),
            ],
        ),
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('url', models.URLField(blank=True)),
                ('type', models.CharField(choices=[('LISTENOGG', 'Listen OGG'), ('LISTENMP3', 'Listen MP3'), ('LISTENAAC', 'Listen AAC'), ('LISTENERS', 'Listeners'), ('LISTENERSOGG', 'Listeners OGG'), ('LISTENERSMP3', 'Listeners MP3'), ('LISTENERSAAC', 'Listeners AAC'), ('METADATA', 'Metadane')], default='LISTENMP3', max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('website', models.URLField(blank=True)),
                ('img', models.ImageField(blank=True, height_field='height', upload_to='stations/', width_field='width')),
                ('width', models.IntegerField(editable=False, null=True)),
                ('height', models.IntegerField(editable=False, null=True)),
                ('info', models.TextField(null=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('methodtag', models.IntegerField()),
                ('listenermethod', models.SmallIntegerField()),
                ('playlist_sp_url', models.CharField(default='None', max_length=100)),
                ('playlist_yt_url', models.CharField(default='None', max_length=100)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='radios.city')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='radios.country')),
                ('listenersurl', models.ManyToManyField(blank=True, null=True, related_name='listeners', to='radios.Stream')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='radios.state')),
                ('stream', models.ManyToManyField(to='radios.Stream')),
                ('tagurl', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='titler', to='radios.stream')),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='radios.state'),
        ),
    ]