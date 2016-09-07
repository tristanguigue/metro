# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.postgres.fields import ArrayField
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.CharField(max_length=2, primary_key=True)),
                ('average_speed', models.FloatField()),
                ('yearly_traffic', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='RollingStock',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True)),
                ('acceleration', models.FloatField()),
                ('deceleration', models.FloatField(null=True)),
                ('max_speed', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Edge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('traffic', models.FloatField(null=True)),
                ('routes', ArrayField(models.IntegerField(), null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', django.contrib.gis.db.models.fields.GeometryField(srid=4326, null=True)),
                ('name', models.CharField(max_length=150, unique=True)),
                ('yearly_entries', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StationLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='metroapp.Line')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='metroapp.Station')),
            ],
        ),
        migrations.AddField(
            model_name='station',
            name='lines',
            field=models.ManyToManyField(related_name='stations', through='metroapp.StationLine', to='metroapp.Line'),
        ),
        migrations.AddField(
            model_name='edge',
            name='stationA',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departure_stations', to='metroapp.StationLine'),
        ),
        migrations.AddField(
            model_name='edge',
            name='stationB',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arrival_stations', to='metroapp.StationLine'),
        ),
        migrations.AddField(
            model_name='line',
            name='rolling_stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='metroapp.RollingStock'),
        ),
        migrations.AlterUniqueTogether(
            name='edge',
            unique_together=set([('stationA', 'stationB')]),
        ),
        migrations.AlterUniqueTogether(
            name='stationline',
            unique_together=set([('station', 'line')]),
        ),
    ]
