from django.contrib.gis.db import models as gismodels
from django.contrib.postgres.fields import ArrayField
from django.db import models

TRANSFER_COEFFICIENT = 0.05


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
    color = models.CharField(max_length=50)

    def yearly_entries(self, excluded_station):
        stations = StationLine.objects.filter(line=self)
        if excluded_station:
            stations = stations.exclude(station=excluded_station)
        return sum([station.yearly_entries for station in stations])


class Station(models.Model):
    location = gismodels.GeometryField(null=True)
    name = models.CharField(max_length=150, unique=True)
    yearly_entries = models.IntegerField(null=True)
    lines = models.ManyToManyField(Line, through='StationLine', related_name='stations')


class StationLine(models.Model):
    station = models.ForeignKey(Station)
    line = models.ForeignKey(Line)

    @property
    def is_terminus(self):
        incoming_routes = self.incoming_edges.values_list('routes', flat=True)
        incoming_routes = [item for route in incoming_routes for item in route]
        outgoing_routes = self.outgoing_edges.values_list('routes', flat=True)
        outgoing_routes = [item for route in outgoing_routes for item in route]
        return set(incoming_routes) != set(outgoing_routes)

    @property
    def yearly_entries(self):
        # TODO: improve split between lines
        # * transfer_weigth / len(self.station.lines.all())
        total_yearly_traffic = sum(self.station.lines.values_list('yearly_traffic', flat=True))
        return self.line.yearly_traffic * self.station.yearly_entries / total_yearly_traffic

    @property
    def weight_transfer(self):
        if self.station.lines.count() <= 1:
            return 0

        # TODO: Add angle coefficient
        return TRANSFER_COEFFICIENT * sum(
            [line.yearly_entries(self.station)
                for line in self.station.lines.exclude(id=self.line)])

    def got_out(self, occupancy, routes):
        weigth_rest = self.get_weight_after(routes)
        return occupancy * (self.yearly_entries + self.weight_transfer) / \
            (self.yearly_entries + weigth_rest + self.weight_transfer)

    def got_in(self, routes):
        weigth_rest = self.get_weight_after(routes)
        weigth_before = self.get_weight_before(routes)
        return (self.yearly_entries) * weigth_rest / \
            (weigth_rest + weigth_before)

    def get_weight_after(self, routes):
        weight_after = 0
        for edge in self.outgoing_edges.filter(routes__overlap=routes):
            weight_after += edge.stationB.yearly_entries
            weight_after += edge.stationB.weight_transfer
            weight_after += edge.stationB.get_weight_after(edge.routes)

        return weight_after

    def get_weight_before(self, routes):
        weight_before = 0
        for edge in self.outgoing_edges.exclude(routes__overlap=routes):
            weight_before += edge.stationB.yearly_entries
            weight_before += edge.stationB.get_weight_after(edge.routes)

        return weight_before

    class Meta:
        unique_together = ('station', 'line')


class Edge(models.Model):
    stationA = models.ForeignKey(StationLine, related_name='outgoing_edges')
    stationB = models.ForeignKey(StationLine, related_name='incoming_edges')
    traffic = models.FloatField(null=True)
    routes = ArrayField(models.IntegerField(), null=True)

    def navigate(self, occupancy, routes):
        self.traffic = occupancy
        self.save()

        edges = self.stationB.outgoing_edges.filter(routes__overlap=routes)
        next_routes = [item for edge in edges for item in edge.routes]

        incoming_edges = self.stationB.incoming_edges\
            .filter(routes__overlap=next_routes)\
            .exclude(id=self.id)

        if incoming_edges:
            for edge in incoming_edges:
                if not edge.traffic:
                    return
                occupancy += edge.traffic

        occupancy -= self.stationB.got_out(occupancy, routes)
        occupancy += self.stationB.got_in(routes)

        if len(edges) == 1:
            edges[0].navigate(occupancy, routes)

        elif len(edges) > 1:
            total_weight = self.stationB.get_weight_after(routes)
            for edge in edges:
                route_weight = edge.stationB.yearly_entries + edge.stationB.get_weight_after(routes)
                edge.navigate(occupancy * route_weight / total_weight, routes)

    class Meta:
        unique_together = ('stationA', 'stationB')
