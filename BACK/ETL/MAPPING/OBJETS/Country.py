class Country:
    def __init__(self, IDCountry, NameCountry):
        self.IDCountry = IDCountry
        self.NameCountry = NameCountry

    def __init__(self):
        self.IDCountry = None
        self.NameCountry = None

    def Hydrate(self, row):
        for key in row.keys():
            self._hydrate_(key, row[key])

    def _hydrate_(self, key, value):
        match key :
            case 'IDCountry':
                self.IDCountry=value
            case 'NameCountry':
                self.NameCountry=f"\"{value}\""
