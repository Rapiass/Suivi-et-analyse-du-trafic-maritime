from shapely.geometry import Point, Polygon

# Définir les limites des océans et mers
oceans = {
          # haut gauche, haut droite, bas droit , bas gauche                      
    "Mer Méditerranée": Polygon([(-7, 40), (10, 47), (40, 32), (20, 20) , (-7,32)]),
    "Mer des Caraïbes": Polygon([(-90, 20), (-60, 20), (-60, 7), (-83, 10)]),
    "Mer Rouge": Polygon([(32, 30), (45, 30), (45, 12), (32, 12)]),
    "Mer du Nord": Polygon([(-5, 60), (6, 60),(7, 51),(0, 51)]),
    "Mer noire": Polygon([(28, 47), (42, 47), (42, 40), (28, 40)]),
    "Mer Baltique": Polygon([(7, 66), (30, 66), (30, 53), (7, 53)]),
    "Golfe du Mexique": Polygon([(-100, 32), (-80, 32),(-80, 28),(-90, 20)]),
    "Mer de Chine méridionale": Polygon([(105, 23), (121, 23), (121, 0), (105, 0)]),
    #"Mer de Béring": Polygon([(-175, 66), (-162, 66), (-162, 52), (-175, 52)]),
    #"Mer d'Arabie": Polygon([(50, 25), (75, 25), (75, 5), (50, 5)]),
    "Mer de Barents": Polygon([(20, 80), (60, 80), (60, 66), (20, 66)]),
    "La Manche": Polygon([(-5, 51.5), (1, 51.5), (1, 49.5), (-5, 49.5)]),
    "Mer de Tasman": Polygon([(150, -29), (160, -29), (160, -44), (150, -44)]),
    "Mer de Sargasses": Polygon([(-70, 35), (-55, 35), (-55, 20), (-70, 20)]),
    "Mer d'Azov": Polygon([(36, 46), (40, 46), (40, 43), (36, 43)]),
    "Mer de Norvège": Polygon([(0, 72), (10, 72), (10, 60), (0, 60)]),
    #"Mer de Weddell": Polygon([(-60, -70), (-40, -70), (-40, -80), (-60, -80)]),
    "Mer d'Andaman": Polygon([(90, 15), (100, 15), (100, 5), (90, 5)]),
    #"Golfe de Gascogne": Polygon([(-10, 48), (-5, 48), (-5, 42), (-10, 42)]),
    "Mer de Corail": Polygon([(140, -10), (160, -10), (160, -20), (150, -20)]),
    "Mer de Java": Polygon([(105, 0), (120, 0), (120, -7), (105, -7)]),
    #"Mer d'Irlande": Polygon([(-10, 57), (-5, 57), (-5, 51), (-10, 51)]),
    #"Mer Méditerranée orientale": Polygon([(30, 40), (40, 40), (40, 30), (30, 30)]),
    "Mer de l'Arabie": Polygon([(45, 15), (65, 23), (75, 7), (45, 7)]),
    "Océan Pacifique": Polygon([(-180, 60), (-120, 60), (-120, -60), (-180, -60)]),
    "Océan Atlantique": Polygon([(-70, 70), (-20, 70), (-20, -60), (-70, -60)]),
    "Océan Indien": Polygon([(20, 30), (120, 30), (120, -60), (20, -60)]),
    "Océan Arctique": Polygon([(-180, 90), (180, 90), (180, 66), (-180, 66)]),
    "Océan Austral": Polygon([(-180, -60), (180, -60), (180, -90), (-180, -90)]),
}

# Fonction pour déterminer la région d'un point
def determine_region(lon, lat):
    point = Point(lon, lat)
    for region, polygon in oceans.items():
        if polygon.contains(point):
            return region
    return "Hors des zones maritimes définies"

class Position:
    def __init__(self, MMSI, BaseDateTime, LAT, LON, SOG, COG, Heading, Status, Region):
        self.MMSI = MMSI
        self.BaseDateTime = BaseDateTime
        self.LAT = LAT
        self.LON = LON
        self.SOG = SOG
        self.COG = COG
        self.Heading = Heading
        self.Status = Status
        self.Region = Region

    def __init__(self):
        self.MMSI = None
        self.BaseDateTime = None
        self.LAT = None
        self.LON = None
        self.SOG = None
        self.COG = None
        self.Heading = None
        self.Status = None
        self.Region = ""

    def Hydrate(self, row):
        for key in row.keys():
            self._hydrate_(key, row[key])

    def _hydrate_(self, key, value):
        match key:
            case 'MMSI':
                self.MMSI = value
            case 'BaseDateTime':
                self.BaseDateTime = f"\"{value}\""
            case 'LAT':
                self.LAT = value
            case 'LON':
                self.LON = value
            case 'SOG':
                self.SOG = value
            case 'COG':
                self.COG = value
            case 'Heading':
                self.Heading = value
            case 'Status':
                self.Status = value

        if(self.LAT and self.LON and not self.Region):
            self.Region = f"\"{determine_region(self.LON,self.LAT)}\""