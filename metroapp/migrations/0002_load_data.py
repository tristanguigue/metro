# -*- coding: utf-8 -*-
from django.db import migrations
from django.conf import settings
from django.core.management import call_command
from ..models import Station, Segment
import csv

LINE_FOLDER = settings.DATA_FOLDER + 'gtfs/' + line


def load_gtfs(apps, schema_editor):
    lines = ['1', '2', '3', '3b', '4', '5', '6', '7', '7b', '8', '9', '10', '11',
             '12', '13', '14']

    for line in lines:
        routes = []

        with open(line_folder + '/routes.txt', 'rU', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                routes.append(row['route_id'])

        routes_trip = []
        with open(line_folder + '/trips.txt', 'rU', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            routes_covered = []
            for row in reader:
                if row['route_id'] not in routes_covered:
                    routes_trip.append(row['trip_id'])
                    routes_covered.append(row['route_id'])

        with open(line_folder + '/stop_times.txt', 'rU', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            segment = []
            current_trip = None
            previous_stop = None
            for row in reader:
                if row['trip_id'] != current_trip:
                    if row['trip_id'] not in routes_trip:
                        continue
                    current_trip = row['trip_id']
                    previous_stop = None

                stop_id = int(row['stop_id'])
                stop_sequence = row['stop_sequence']

                stn = Station(id=stop_id)
                stn.lines.append(line)
                stn.save()

                if previous_stop is not None:
                    sgm = Segment(a=current_stop, b=previous_stop)
                    sgm.save()

        with open(line_folder + '/stops.txt', 'rU', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                stn = Station.get(id=int(row['stop_id']))
                stn.name = row['stop_name']
                stn.location = Geometry(row['stop_lat'], row['stop_lon'])


def remove_data(apps, schema_editor):
    if not settings.TESTING:
        call_command('flush')


class Migration(migrations.Migration):

    dependencies = [
        ('metroapp', '0001_initial')
    ]

    operations = [
        migrations.RunPython(
            load_gtfs,
            reverse_code=remove_data),
    ]