from django.db import models
from django.contrib.gis.db import models as gismodels


class RollingStock(models.Model):
    name = models.CharField(max_length=20)
    acceleration = models.FloatField()
    deceleration = models.FloatField()
    max_speed = models.FloatField()


class Line(models.Model):
    rolling_stock = models.ForeignKey(RollingStock)
    average_speed = models.FloatField()
    yearly_traffic = models.FloatField()


class Station(models.Model):
    location = gismodels.GeometryField()
    name = models.CharField(max_length=150)
    yearly_entries = models.IntegerField()
    lines = models.ManyToManyField(Line, through='StationLine', related_name='stations')


class StationLine(models.Model):
    station = models.ForeignKey(Station)
    line = models.ForeignKey(Line)
    sequence_order = models.PositiveIntegerField()


class Segment(models.Model):
    stationA = models.ForeignKey(StationLine, related_name='departure_stations')
    stationB = models.ForeignKey(StationLine, related_name='arrival_stations')
    trafficAB = models.FloatField()
    trafficBA = models.FloatField()
