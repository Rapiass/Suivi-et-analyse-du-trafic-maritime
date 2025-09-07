class UserHasVessel:
    def __init__(self, IDUser, MMSI, IsCaptain):
        self.IDUser = IDUser
        self.MMSI = MMSI
        self.IsCaptain = IsCaptain

    def __init__(self):
        self.IDUser = None
        self.MMSI = None
        self.IsCaptain = None

    def Hydrate(self, row):
        for key in row.keys():
            if key in self.__dict__:
                self._hydrate_(key, row[key])

    def _hydrate_(self, key, value):
        match key:
            case 'IDUser':
                self.IDUser = value
            case 'MMSI':
                self.MMSI = value
            case 'IsCaptain':
                self.IsCaptain = value