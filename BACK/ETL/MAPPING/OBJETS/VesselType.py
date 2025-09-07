class VesselType:
    def __init__(self, IDVesselType, Description):
        self.IDVesselType = IDVesselType
        self.Description = Description

    def __init__(self):
        self.IDVesselType = None
        self.Description = None

    def Hydrate(self, row):
        for key in row.keys():
            self._hydrate_(key, row[key])

    def _hydrate_(self, key, value):
        match key:
            case 'VesselType':
                self.IDVesselType = value
            case 'Description':
                self.Description = f"\"{value}\""