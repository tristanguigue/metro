import json

from django.conf import settings
from django.core.management.base import BaseCommand

from metroapp.models import Station

STATION_NAME_MAP = {
    "LOUVRE": "Louvre-Rivoli",
    "FRANKLIN D. ROOSEVELT": "Franklin-Roosevelt",
    "CHATEAU-LANDON": "Château Landon",
    "LA COURNEUVE-8 MAI 1945": "La Courneuve-8-Mai-1945",
    "BOULOGNE-PONT DE SAINT-CLOUD": "Boulogne Pont de Saint-Cloud",
    "BOBIGNY-PANTIN-RAYMOND QUENEAU": "Bobigny-Pantin (Raymond Queneau)",
    "LA DEFENSE": "La Défense (Grande Arche)",
    "CHAUSSEE D'ANTIN-LA FAYETTE": "Chaussée d'Antin (La Fayette)",
    "PLACE CLICHY": "Place de Clichy",
    "AUBERVILLIERS-PANTIN-QUATRE CHEMINS": "Aubervilliers Pantin (4 Chemins)",
    "CLUNY LA SORBONNE": "Cluny-La Sorbonne",
    "AVENUE EMILE ZOLA": "Avenue Emile-Zola",
    "CRETEIL-POINTE DU LAC": "Pointe du Lac",
    "CHATILLON-MONTROUGE": "Châtillon Montrouge",
    "QUATRE-SEPTEMBRE": "Quatre Septembre",
    "SAINT-PHILIPPE-DU-ROULE": "Saint-Philippe du Roule",
    "NOTRE-DAME-DE-LORETTE": "Notre-Dame de Lorette",
    "PIERRE CURIE": "Pierre et Marie Curie",
    "NOTRE-DAME-DES-CHAMPS": "Notre-Dame des Champs",
    "VILLEJUIF-PAUL VAILLANT-COUTURIER": "Villejuif-Paul Vaillant Couturier (Hôpital Paul Brousse)",
    "SAINT-MANDE-TOURELLE": "Saint-Mandé"
}


class Command(BaseCommand):
    help = 'Load yearly station entries'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open(settings.DATA_FOLDER + '/station_yearly_entries.json') as jsonfile:
            entries_stations = json.load(jsonfile)

            for station in entries_stations:
                if 'station' not in station['fields']:
                    continue
                if station['fields']['reseau'] == 'RER':
                    continue

                station_name = station['fields']['station']
                if station_name in STATION_NAME_MAP:
                    station_name = STATION_NAME_MAP[station_name]

                res = Station.objects.filter(name__unaccent__iexact=station_name)
                if not res:
                    res = Station.objects.filter(name__unaccent__icontains=station_name)

                if not res:
                    station_name = '-'.join(station_name.split())

                res = Station.objects.filter(name__unaccent__iexact=station_name)
                if not res:
                    res = Station.objects.filter(name__unaccent__icontains=station_name)

                if res:
                    stn = res[0]
                    stn.yearly_entries = station['fields']['trafic']
                    stn.save()

        self.stdout.write(self.style.SUCCESS('Successfully imported entries'))
