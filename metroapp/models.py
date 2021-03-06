from django.contrib.gis.db import models as gismodels
from django.contrib.gis.db.models.functions import Distance
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import MultipleObjectsReturned
from django.db import models
from django.db.models import Q

from metroapp.exceptions import CantRemoveTerminus, CantRemoveTransferStation

TRANSFER_COEFFICIENT = 0.2
IN_TRANSFER_COEFFICIENT = 1.3
DEFAULT_ACC_DEC = 1  # m/s2
TIME_STOP = 17  # seconds
MAX_SPEED = 18  # m/s
WALKING_SPEED = 1.39  # m/s
NO_TRANSFER_STOPS = [188, 189, 190, 97, 104, 24, 129]
GAMMA = 0.85


class RollingStock(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    acceleration = models.FloatField()
    deceleration = models.FloatField(null=True)
    max_speed = models.FloatField()


class Line(models.Model):
    id = models.CharField(max_length=2, primary_key=True)
    rolling_stock = models.ForeignKey(RollingStock)
    average_speed = models.FloatField()
    yearly_traffic = models.FloatField()
    yearly_entries = models.FloatField(null=True)
    color = models.CharField(max_length=50)

    def get_yearly_entries(self):
        return sum(self.linestations.values_list('yearly_entries', flat=True))


class Station(models.Model):
    location = gismodels.GeometryField(null=True, geography=True)
    name = models.CharField(max_length=150, unique=True)
    yearly_entries = models.IntegerField(null=True)
    lines = models.ManyToManyField(Line, through='StationLine', related_name='stations')

    def remove(self):
        try:
            station_line = StationLine.objects.get(station=self)
        except MultipleObjectsReturned:
            raise CantRemoveTransferStation

        return station_line.remove()


class StationLine(models.Model):
    station = models.ForeignKey(Station)
    line = models.ForeignKey(Line, related_name='linestations')
    yearly_entries = models.FloatField(null=True)
    yearly_exits = models.FloatField(null=True)
    weight_transfer = models.FloatField(null=True)

    @property
    def is_terminus(self):
        incoming_routes = self.incoming_edges.values_list('routes', flat=True)
        incoming_routes = [item for route in incoming_routes for item in route]
        outgoing_routes = self.outgoing_edges.values_list('routes', flat=True)
        outgoing_routes = [item for route in outgoing_routes for item in route]
        return set(incoming_routes) != set(outgoing_routes)

    def get_yearly_entries(self):
        total_yearly_traffic = sum(self.station.lines.values_list('yearly_traffic', flat=True))
        return self.line.yearly_traffic * self.station.yearly_entries / total_yearly_traffic

    def get_weight_transfer(self):
        if self.station.lines.count() <= 1 or self.station.id in NO_TRANSFER_STOPS:
            return 0

        # TODO: Add angle coefficient
        return TRANSFER_COEFFICIENT * sum(
            [(line.yearly_entries - StationLine.objects.get(line=line, station=self.station)
                .yearly_entries) for line in self.station.lines.exclude(id=self.line.id)])

    def got_out(self, occupancy, routes, transfers):
        weigth_rest_with_transfer = self.get_weight_after(routes, True)
        weigth_rest_no_transfer = self.get_weight_after(routes, False)

        out_transfers = 0
        weight_transfer = self.weight_transfer

        if self.station.lines.count() > 1 and self.station.id not in NO_TRANSFER_STOPS:
            for line in self.station.lines.exclude(id=self.line.id):
                weight_line = line.yearly_entries - StationLine.objects.get(
                    line=line, station=self.station).yearly_entries
                traffic = occupancy['primary'] * TRANSFER_COEFFICIENT * weight_line / \
                    (self.yearly_entries + weigth_rest_with_transfer + weight_transfer)
                out_transfers += traffic

                if not transfers:
                    Transfer.objects.update_or_create(
                        lineA=self.line, lineB=line, station=self.station, routes=routes,
                        defaults={'traffic': traffic})

        if transfers:
            out_primary = occupancy['primary'] * self.yearly_entries / \
                (self.yearly_entries + weigth_rest_with_transfer + weight_transfer)

            out_secondary = occupancy['secondary'] * self.yearly_entries / \
                (self.yearly_entries + weigth_rest_no_transfer)

            if not self.yearly_exits:
                self.yearly_exits = 0
            self.yearly_exits += out_primary + out_secondary
            self.save()

            print(self.line.id, self.station.name,
                  ' out primary ', round(out_primary / 1000000, 1),
                  ', out secondary ', round(out_secondary / 1000000, 1),
                  ', out transfer ', round(out_transfers / 1000000, 1))

            return {
                'primary': out_transfers + out_primary,
                'secondary': out_secondary,
                'out_transfers': out_transfers
            }

        out_primary = occupancy['primary'] * self.yearly_entries / (self.yearly_entries + weigth_rest_no_transfer)

        print(self.line.id, self.station.name,
              ' out primary ', round(out_primary / 1000000, 1),
              ', out secondary ', round(0 / 1000000, 1),
              ', out transfer ', round(out_transfers / 1000000, 1))

        return {
            'primary': out_primary,
            'secondary': 0,
            'out_transfers': 0
        }

    def got_in(self, routes, transfers):
        weigth_rest_no_transfer = self.get_weight_after(routes, False)
        weigth_before_no_transfer = self.get_weight_before(routes, False)

        weigth_rest_with_transfer = self.get_weight_after(routes, True)
        weigth_before_with_transfer = self.get_weight_before(routes, True)

        in_transfers = 0
        if transfers:
            list_transfers = Transfer.objects.filter(station=self.station, lineB=self.line)
            in_transfers = IN_TRANSFER_COEFFICIENT * sum([transfer.traffic for transfer in list_transfers])
            in_primary = self.yearly_entries * weigth_rest_with_transfer / (weigth_rest_with_transfer + weigth_before_with_transfer)
            in_secondary = in_transfers * weigth_rest_no_transfer / (weigth_rest_no_transfer + weigth_before_no_transfer)

            print(self.line.id, self.station.name,
                  ' in primary ', round(in_primary / 1000000, 1),
                  ', in transfer ', round(in_secondary / 1000000, 1))

            return {
                'primary': in_primary,
                'secondary': in_secondary,
            }

        in_primary = self.yearly_entries * weigth_rest_with_transfer / (weigth_rest_with_transfer + weigth_before_with_transfer)

        print(self.line.id, self.station.name,
              ' in primary ', round(in_primary / 1000000, 1),
              ', in transfer ', round(0 / 1000000, 1))

        return {
            'primary': in_primary,
            'secondary': 0,
        }

    def get_weight_after(self, routes, transfers, dump_factor=1, dumping=True):
        weight_after = 0
        if not dumping:
            dump_factor = 1

        for edge in self.outgoing_edges.filter(routes__overlap=routes):
            weight_after += dump_factor * edge.stationB.yearly_entries
            if transfers:
                weight_after += dump_factor * edge.stationB.weight_transfer
            weight_after += edge.stationB.get_weight_after(
                edge.routes, transfers, dump_factor * GAMMA, dumping)
        return weight_after

    def get_weight_before(self, routes, transfers, dump_factor=1, dumping=True):
        weight_before = 0
        if not dumping:
            dump_factor = 1

        for edge in self.outgoing_edges.exclude(routes__overlap=routes):
            weight_before += dump_factor * edge.stationB.yearly_entries
            if transfers:
                weight_before += dump_factor * edge.stationB.weight_transfer
            weight_before += edge.stationB.get_weight_after(
                edge.routes, transfers, dump_factor * GAMMA, dumping)
        return weight_before

    def remove(self):
        if self.is_terminus:
            raise CantRemoveTerminus

        time_gained_individual = self.time_gained_when_removed()
        traffic_surrounding = self.traffic_surrounding()
        time_gained = time_gained_individual * traffic_surrounding

        time_lost_individual = self.distance_to_closest_station() / WALKING_SPEED
        time_lost = (self.yearly_entries + self.yearly_exits) * time_lost_individual

        return {
            'time_gained': time_gained,
            'time_lost': time_lost,
            'time_difference': time_gained - time_lost,
            'time_difference_per_person': (time_gained - time_lost) / traffic_surrounding
        }

    def time_gained_when_removed(self):
        acceleration = self.line.rolling_stock.acceleration
        deceleration = self.line.rolling_stock.deceleration

        if not acceleration:
            acceleration = DEFAULT_ACC_DEC
        if not deceleration:
            deceleration = DEFAULT_ACC_DEC

        return TIME_STOP + MAX_SPEED / (2 * acceleration) + MAX_SPEED / (2 * deceleration)

    def traffic_surrounding(self):
        return sum(Edge.objects.filter(Q(stationA=self) | Q(stationB=self))
                   .values_list('traffic', flat=True))

    def distance_to_closest_station(self):
        location = self.station.location
        min_distance = None

        for edge in Edge.objects.filter(stationA=self)\
                .annotate(distance=Distance('stationB__station__location', location)):

            if min_distance is None or edge.distance.m < min_distance:
                min_distance = edge.distance.m

        for edge in Edge.objects.filter(stationB=self)\
                .annotate(distance=Distance('stationA__station__location', location)):

            if min_distance is None or edge.distance.m < min_distance:
                min_distance = edge.distance.m

        return min_distance

    class Meta:
        unique_together = ('station', 'line')


class Transfer(models.Model):
    station = models.ForeignKey(Station)
    lineA = models.ForeignKey(Line, related_name='outgoing_transfers')
    routes = ArrayField(models.IntegerField(), null=True)
    lineB = models.ForeignKey(Line, related_name='incoming_transfers')
    traffic = models.FloatField()

    unique_together = ('lineA', 'lineB', 'station', 'routes')


class Edge(models.Model):
    stationA = models.ForeignKey(StationLine, related_name='outgoing_edges')
    stationB = models.ForeignKey(StationLine, related_name='incoming_edges')
    traffic = models.FloatField(null=True)
    routes = ArrayField(models.IntegerField(), null=True)

    def navigate(self, occupancy, routes, transfers):
        self.traffic = sum(occupancy.values())
        self.save()

        edges = self.stationB.outgoing_edges.filter(routes__overlap=routes)
        next_routes = [item for edge in edges for item in edge.routes]

        # If we have incoming branches, merge traffic
        incoming_edges = self.stationB.incoming_edges\
            .filter(routes__overlap=next_routes)\
            .exclude(id=self.id)

        if incoming_edges:
            for edge in incoming_edges:
                if not edge.traffic:
                    return 0, 0
                occupancy['primary'] += edge.traffic

        print(self.stationB.line.id, self.stationB.station.name,
              ' before primary ', round(occupancy['primary'] / 1000000, 1),
              ', before secondary ', round(occupancy['secondary'] / 1000000, 1))

        got_out = self.stationB.got_out(occupancy, routes, transfers)
        occupancy['primary'] -= got_out['primary']
        occupancy['secondary'] -= got_out['secondary']
        total_out_transfer = got_out['out_transfers']

        got_in = self.stationB.got_in(routes, transfers)
        occupancy['primary'] += got_in['primary']
        occupancy['secondary'] += got_in['secondary']
        total_in_transfer = got_in['secondary']

        print(self.stationB.line.id, self.stationB.station.name,
              ' after primary ', round(occupancy['primary'] / 1000000, 1),
              ', after secondary ', round(occupancy['secondary'] / 1000000, 1))

        # If we have several outgoing branches, we split the traffic
        if len(edges) == 1:
            in_transfer, out_transfer = edges[0].navigate(occupancy, routes, transfers)
            total_in_transfer += in_transfer
            total_out_transfer += out_transfer
        elif len(edges) > 1:
            total_weight = self.stationB.get_weight_after(routes, transfers, 1, False)
            for edge in edges:
                route_weight = edge.stationB.yearly_entries + edge.stationB.get_weight_after(
                    routes, transfers, 1, False)
                in_transfer, out_transfer = edge.navigate(
                    {'primary': occupancy['primary'] * route_weight / total_weight,
                     'secondary': occupancy['secondary'] * route_weight / total_weight},
                    routes, transfers)
                total_in_transfer += in_transfer
                total_out_transfer += out_transfer
        return total_in_transfer, total_out_transfer

    class Meta:
        unique_together = ('stationA', 'stationB')
