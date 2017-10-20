import json

from django.core.management.base import BaseCommand

from metroapp.models import Edge


class Command(BaseCommand):
    help = 'Serialize lines and stations for D3'

    def add_arguments(self, parser):
        pass

    def serialize(self, edges):
        edge_list = []
        for edge in edges:
            edge_list.append({
                "stationA": edge.stationA.station.name,
                "stationB": edge.stationB.station.name,
                "line": edge.stationA.line.id,
                "traffic": edge.total
            })
        return edge_list

    def handle(self, *args, **options):

        edges = list(Edge.objects.all())
        for edge in edges:
            edge.total = edge.traffic
            try:
                reverse_edge = Edge.objects.get(stationB=edge.stationA, stationA=edge.stationB)
                edge.total += reverse_edge.traffic
            except:
                pass

        self.stdout.write(self.style.SUCCESS('Bottom'))
        edges.sort(key=lambda x: x.total)
        self.stdout.write(json.dumps(
            self.serialize(edges[:20]), ensure_ascii=False
        ))

        self.stdout.write(self.style.SUCCESS('Top'))
        edges.sort(key=lambda x: x.total, reverse=True)
        self.stdout.write(json.dumps(
            self.serialize(edges[:20]), ensure_ascii=False
        ))
