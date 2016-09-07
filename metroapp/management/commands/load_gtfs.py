import csv

from django.conf import settings
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand

from metroapp.models import Edge, Line, Station, StationLine

LINE_FOLDER = settings.DATA_FOLDER + 'gtfs/RATP_GTFS_METRO_'


class Command(BaseCommand):
    help = 'Load gtfs data'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        lines = Line.objects.all()

        for line in lines:
            routes = []
            line_folder = LINE_FOLDER + line.pk

            with open(line_folder + '/routes.txt', 'rU', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    routes.append(row['route_id'])

            routes_trip = {}
            with open(line_folder + '/trips.txt', 'rU', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                routes_covered = []
                for row in reader:
                    if row['route_id'] not in routes_covered:
                        routes_trip[row['trip_id']] = row['route_id']
                        routes_covered.append(row['route_id'])

            station_ids = {}
            with open(line_folder + '/stops.txt', 'rU', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    station_id = int(row['stop_id'])
                    station_name = row['stop_name']

                    stn = Station.objects.get_or_create(
                        name=row['stop_name'],
                        defaults={
                            'location': Point(float(row['stop_lat']), float(row['stop_lon']))
                        })

                    station_ids[station_id] = station_name

            with open(line_folder + '/stop_times.txt', 'rU', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                current_trip = None
                previous_stop = None
                for row in reader:
                    if row['trip_id'] != current_trip:
                        if row['trip_id'] not in routes_trip:
                            continue
                        current_trip = row['trip_id']
                        previous_stop = None

                    stop_id = int(row['stop_id'])
                    stn = Station.objects.get(name=station_ids[stop_id])
                    current_stop = StationLine.objects.get_or_create(station=stn, line=line)[0]

                    if previous_stop is not None:
                        edge = Edge.objects.get_or_create(
                            stationA=previous_stop,
                            stationB=current_stop,
                            defaults={'routes': []})[0]
                        edge.routes.append(routes_trip[current_trip])
                        edge.save()

                    previous_stop = current_stop

        self.stdout.write(self.style.SUCCESS('Successfully imported gtfs data'))
