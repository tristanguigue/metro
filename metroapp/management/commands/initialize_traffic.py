from django.core.management.base import BaseCommand

from metroapp.models import Edge, Line, StationLine, Transfer, IN_TRANSFER_COEFFICIENT


class Command(BaseCommand):
    help = 'Initialise traffic for each segment'

    def add_arguments(self, parser):
        pass

    def run_simulation(self, lines, transfers):
        Edge.objects.all().update(traffic=None)
        StationLine.objects.all().update(yearly_exits=None)

        total_out_transfer = 0
        total_in_transfer = 0
        all_termini = []
        for line in lines:
            stations = StationLine.objects.filter(line=line)
            termini = []

            for station in stations:
                if station.is_terminus:
                    termini.append(station)
                    all_termini.append(station)

            for terminus in termini:
                edge = terminus.outgoing_edges.first()
                in_transfers = 0
                if transfers:
                    list_transfers = Transfer.objects.filter(station=edge.stationA.station, lineB=edge.stationA.line)
                    in_transfers = IN_TRANSFER_COEFFICIENT * sum([transfer.traffic for transfer in list_transfers])

                occupancy = {
                    'primary': terminus.yearly_entries,
                    'secondary': in_transfers
                }

                in_transfers, out_transfers = edge.navigate(occupancy, edge.routes, transfers)
                total_in_transfer += in_transfers
                total_out_transfer += out_transfers

        print('Checking balance in transfer and out transfer')
        print(total_in_transfer, total_out_transfer)

        print('Checking balance incoming and outgoing from termini')
        total_in = 0
        total_out = 0
        for terminus in all_termini:
            if terminus.station.lines.count() == 1:
                out_edge = terminus.outgoing_edges.first()
                in_edge = terminus.incoming_edges.first()
                total_in += in_edge.traffic
                total_out += out_edge.traffic
                print(terminus.line.id, terminus.station.name,
                      round(in_edge.traffic / 1000000, 1),
                      round(out_edge.traffic / 1000000, 1))

        print('Total ', round(total_in / 1000000, 1), round(total_out / 1000000, 1))


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

        list_transfers = Transfer.objects.all()
        print(sum([transfer.traffic for transfer in list_transfers]))

        self.run_simulation(lines, True)

        self.stdout.write(self.style.SUCCESS('Traffic initialised'))
