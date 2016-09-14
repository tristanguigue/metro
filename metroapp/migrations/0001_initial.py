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
                ('color', models.CharField(max_length=50)),
                ('average_speed', models.FloatField()),
                ('yearly_traffic', models.FloatField()),
                ('yearly_entries', models.FloatField(null=True)),
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
                ('location', django.contrib.gis.db.models.fields.GeometryField(null=True, geography=True)),
                ('name', models.CharField(max_length=150, unique=True)),
                ('yearly_entries', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StationLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='linestations', to='metroapp.Line')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='metroapp.Station')),
                ('yearly_entries', models.FloatField(null=True)),
                ('yearly_exits', models.FloatField(null=True)),
                ('weight_transfer', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('traffic', models.FloatField()),
                ('lineA', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_transfers', to='metroapp.Line')),
                ('routes', ArrayField(models.IntegerField(), null=True)),
                ('lineB', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incoming_transfers', to='metroapp.Line')),
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
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_edges', to='metroapp.StationLine'),
        ),
        migrations.AddField(
            model_name='edge',
            name='stationB',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incoming_edges', to='metroapp.StationLine'),
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
        migrations.AlterUniqueTogether(
            name='transfer',
            unique_together=set([('lineA', 'lineB', 'station', 'routes')]),
        ),
    ]
