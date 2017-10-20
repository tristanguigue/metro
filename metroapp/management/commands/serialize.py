import json

from django.core.management.base import BaseCommand

from metroapp.models import Edge, Station

OUTPUT_DIR = './metroapp/static/data/'


class Command(BaseCommand):
    help = 'Serialize lines and stations for D3'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        features = []
        for station in Station.objects.all():
            try:
                res_remove = station.remove()
            except:
                res_remove = None

            features.append({
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [station.location.x, station.location.y]
                },
                'properties': {
                    'pk': station.pk,
                    'name': station.name,
                    'yearly_entries': station.yearly_entries,
                    'remove': res_remove
                }
            })

        station_geojson = {
            'type': 'FeatureCollection',
            'crs': {
                'type': 'name',
                'properties': {'name': 'EPSG:4326'}
            },
            'features': features
        }

        with open(OUTPUT_DIR + 'stations.json', 'w') as out:
            json.dump(station_geojson, out)

        edge_list = []
        for edge in Edge.objects.all():
            edge_list.append({
                'stationA': edge.stationA.station.id,
                'stationB': edge.stationB.station.id,
                'line': edge.stationA.line.id,
                'color': edge.stationA.line.color,
                'traffic': edge.traffic
            })

        with open(OUTPUT_DIR + 'edges.json', 'w') as out:
            json.dump(edge_list, out)

        self.stdout.write(self.style.SUCCESS('Serialized'))
