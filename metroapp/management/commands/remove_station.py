from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.core.management.base import BaseCommand

from metroapp.models import Station, StationLine

WALKING_SPEED = 1.39  # m/s


class Command(BaseCommand):
    help = 'Remove station'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        station_id = 8

        try:
            station = Station.objects.get(id=station_id)
        except ObjectDoesNotExist:
            self.stdout.write(self.style.ERROR('Station does not exists'))
            return

        try:
            station_line = StationLine.objects.get(station=station)
        except MultipleObjectsReturned:
            self.stdout.write(self.style.ERROR('Transfer station cannot be removed'))
            return

        time_gained_individual = station_line.time_gained_when_removed()
        print('time gained individual ', time_gained_individual)
        traffic_surrounding = station_line.traffic_surrounding()
        print('traffic surrounding ', traffic_surrounding)
        time_gained = time_gained_individual * traffic_surrounding

        print('distance to closest ', station_line.distance_to_closest_station())
        time_lost_individual = station_line.distance_to_closest_station() / WALKING_SPEED
        print('time lost individual ', time_lost_individual)
        time_lost = (station_line.yearly_entries + station_line.yearly_exits) * time_lost_individual

        self.stdout.write(self.style.SUCCESS('Time gained: ' + str(time_gained)))
        self.stdout.write(self.style.SUCCESS('Time lost: ' + str(time_lost)))

        self.stdout.write(self.style.SUCCESS('Difference: ' + str(time_gained - time_lost)))
        self.stdout.write(self.style.SUCCESS('Per person: ' +
                          str((time_gained - time_lost) / traffic_surrounding)))
