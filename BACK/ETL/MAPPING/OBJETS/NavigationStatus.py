class NavigationStatus:
    def __init__(self, Status, Description):
        self.Status = Status
        self.Description = Description

    def __init__(self):
        self.Status = None
        self.Description = None

    def Hydrate(self, row):
        for key in row.keys():
            self._hydrate_(key, row[key])

    def _hydrate_(self, key, value):
        match key:
            case 'NavStatus':
                self.Status = value
            case 'Description':
                self.Description = f"\"{value}\""