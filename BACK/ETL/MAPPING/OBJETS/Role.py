class Role:
    def __init__(self, IDRole, Role):
        self.IDRole = IDRole
        self.Role = Role

    def __init__(self):
        self.IDRole = None
        self.Role = None

    def Hydrate(self, row):
        for key in row.keys():
            if key in self.__dict__:
                self._hydrate_(key, row[key])

    def _hydrate_(self, key, value):
        match key:
            case 'IDRole':
                self.IDRole = value
            case 'Role':
                self.Role = f"\"{value}\""