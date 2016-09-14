from django.contrib.gis.db import models as gismodels
from django.contrib.gis.db.models.functions import Distance
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Q

TRANSFER_COEFFICIENT = 0.025
DEFAULT_ACC_DEC = 1  # m/s2
TIME_STOP = 17  # seconds
MAX_SPEED = 18  # m/s


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
        if self.station.lines.count() <= 1:
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

        print(self.line.id, self.station.name, ' occ1 ', occupancy['primary'] / 1000000)
        print(self.line.id, self.station.name, ' occ2 ', occupancy['secondary'] / 1000000)

        if self.station.lines.count() > 1:

            if not transfers:
                for line in self.station.lines.exclude(id=self.line.id):
                    weight_line = line.yearly_entries - StationLine.objects.get(
                        line=line, station=self.station).yearly_entries
                    traffic = occupancy['primary'] * TRANSFER_COEFFICIENT * weight_line / \
                        (self.yearly_entries + weigth_rest_with_transfer + weight_transfer)
                    out_transfers += traffic

                    Transfer.objects.update_or_create(
                        lineA=self.line, lineB=line, station=self.station, routes=routes,
                        defaults={'traffic': traffic})

            list_transfers = Transfer.objects.filter(station=self.station, lineA=self.line,
                                                     routes=routes)
            out_transfers = sum([transfer.traffic for transfer in list_transfers])

            # print(self.line.id, self.station.name, ' out_old ', out_transfers / 1000000)

        if transfers:
            out_primary = occupancy['primary'] * self.yearly_entries / \
                (self.yearly_entries + weigth_rest_with_transfer + weight_transfer)
            out_secondary = occupancy['secondary'] * self.yearly_entries / \
                (self.yearly_entries + weigth_rest_no_transfer)

            if not self.yearly_exits:
                self.yearly_exits = 0
            self.yearly_exits += out_primary + out_secondary
            self.save()

            return {
                'primary': out_transfers + out_primary,
                'secondary': out_secondary
            }

        return {
            'primary': occupancy['primary'] * self.yearly_entries /
            (self.yearly_entries + weigth_rest_no_transfer),
            'secondary': 0
        }

    def got_in(self, routes, transfers):
        weigth_rest_no_transfer = self.get_weight_after(routes, False)
        weigth_before_no_transfer = self.get_weight_before(routes, False)

        weigth_rest_with_transfer = self.get_weight_after(routes, True)
        weigth_before_with_transfer = self.get_weight_before(routes, True)

        in_transfers = 0
        if transfers:
            list_transfers = Transfer.objects.filter(station=self.station, lineB=self.line)
            in_transfers = sum([transfer.traffic for transfer in list_transfers])

            return {
                'primary': self.yearly_entries * weigth_rest_with_transfer /
                (weigth_rest_with_transfer + weigth_before_with_transfer),
                'secondary': in_transfers * weigth_rest_no_transfer /
                (weigth_rest_no_transfer + weigth_before_no_transfer)
            }

        return {
            'primary': self.yearly_entries * weigth_rest_no_transfer /
            (weigth_rest_no_transfer + weigth_before_no_transfer),
            'secondary': 0
        }

    def get_weight_after(self, routes, transfers):
        weight_after = 0
        for edge in self.outgoing_edges.filter(routes__overlap=routes):
            weight_after += edge.stationB.yearly_entries
            if transfers:
                weight_after += edge.stationB.weight_transfer
            weight_after += edge.stationB.get_weight_after(edge.routes, transfers)
        return weight_after

    def get_weight_before(self, routes, transfers):
        weight_before = 0
        for edge in self.outgoing_edges.exclude(routes__overlap=routes):
            weight_before += edge.stationB.yearly_entries
            if transfers:
                weight_before += edge.stationB.weight_transfer
            weight_before += edge.stationB.get_weight_after(edge.routes, transfers)
        return weight_before

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
                    return
                occupancy['primary'] += edge.traffic

        got_out = self.stationB.got_out(occupancy, routes, transfers)
        occupancy['primary'] -= got_out['primary']
        occupancy['secondary'] -= got_out['secondary']
        got_in = self.stationB.got_in(routes, transfers)
        occupancy['primary'] += got_in['primary']
        occupancy['secondary'] += got_in['secondary']

        # If we have several outgoing branches, we split the traffic
        if len(edges) == 1:
            edges[0].navigate(occupancy, routes, transfers)
        elif len(edges) > 1:
            total_weight = self.stationB.get_weight_after(routes, transfers)
            for edge in edges:
                route_weight = edge.stationB.yearly_entries + edge.stationB.get_weight_after(
                    routes, transfers)
                edge.navigate(
                    {'primary': occupancy['primary'] * route_weight / total_weight,
                     'secondary': occupancy['secondary'] * route_weight / total_weight},
                    routes, transfers)

    class Meta:
        unique_together = ('stationA', 'stationB')
