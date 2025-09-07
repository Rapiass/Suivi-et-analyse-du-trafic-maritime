class Company:
    def __init__(self, IDCompany, NameCompany, IDCountry):
        self.IDCompany = IDCompany
        self.NameCompany = NameCompany
        self.IDCountry = IDCountry

    def __init__(self):
        self.IDCompany = None
        self.NameCompany = None
        self.IDCountry = None

    def Hydrate(self, row):
        for key in row.keys():
            if key in self.__dict__:
                self._hydrate_(key, row[key])

    def _hydrate_(self, key, value):
        match key:
            case 'IDCompany':
                self.IDCompany = value
            case 'NameCompany':
                self.NameCompany = f"\"{value}\""
            case 'IDCountry':
                self.IDCountry = value