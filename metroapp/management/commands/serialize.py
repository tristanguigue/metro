import json

from django.core import serializers
from django.core.management.base import BaseCommand

from metroapp.models import Edge, Station

OUTPUT_DIR = './metroapp/static/data/'


class Command(BaseCommand):
    help = 'Serialize lines and stations for D3'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open(OUTPUT_DIR + 'stations.json', 'w') as out:
            serializers.serialize('geojson', Station.objects.all(),
                                  geometry_field='location',
                                  fields=('pk', 'name', 'yearly_entries'),
                                  stream=out)

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
