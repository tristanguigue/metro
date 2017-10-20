import json

from django.core.management.base import BaseCommand

from metroapp.models import Station


class Command(BaseCommand):
    help = 'Serialize lines and stations for D3'

    def add_arguments(self, parser):
        pass

    def serialize(self, stations):
        station_list = []
        for station in stations:
            station_list.append({
                "timeGained": station.time_gained / (3600 * 24 * 365.25),
                "name": station.name,
                "line": station.lines.first().id,
            })
        return station_list

    def handle(self, *args, **options):

        stations = list(Station.objects.all())
        for station in stations:
            try:
                res = station.remove()
                station.time_gained = res['time_difference']
            except:
                station.time_gained = 0

        self.stdout.write(self.style.SUCCESS('Bottom'))
        stations.sort(key=lambda x: x.time_gained)
        self.stdout.write(json.dumps(
            self.serialize(stations[:20]), ensure_ascii=False
        ))

        self.stdout.write(self.style.SUCCESS('Top'))
        stations.sort(key=lambda x: x.time_gained, reverse=True)
        self.stdout.write(json.dumps(
            self.serialize(stations[:20]), ensure_ascii=False
        ))
