from django.core.management.base import BaseCommand

from metroapp.models import Edge, Line, StationLine, Transfer


class Command(BaseCommand):
    help = 'Initialise traffic for each segment'

    def add_arguments(self, parser):
        pass

    def run_simulation(self, lines, transfers):
        Edge.objects.all().update(traffic=None)
        StationLine.objects.all().update(yearly_exits=None)

        for line in lines:
            stations = StationLine.objects.filter(line=line)
            termini = []

            for station in stations:
                if station.is_terminus:
                    termini.append(station)

            for terminus in termini:
                print(terminus.station.name)
                edge = terminus.outgoing_edges.first()
                occupancy = {
                    'primary': terminus.yearly_entries,
                    'secondary': 0
                }

                edge.navigate(occupancy, edge.routes, transfers)

    def handle(self, *args, **options):
        Edge.objects.all().update(traffic=None)
        Transfer.objects.all().delete()

        station_lines = StationLine.objects.all()
        for station_line in station_lines:
            station_line.yearly_entries = station_line.get_yearly_entries()
            station_line.save()

        lines = Line.objects.all()
        for line in lines:
            line.yearly_entries = line.get_yearly_entries()
            line.save()

        station_lines = StationLine.objects.all()
        for station_line in station_lines:
            station_line.weight_transfer = station_line.get_weight_transfer()
            station_line.save()

        self.run_simulation(lines, False)
        self.run_simulation(lines, True)

        self.stdout.write(self.style.SUCCESS('Traffic initialised'))
