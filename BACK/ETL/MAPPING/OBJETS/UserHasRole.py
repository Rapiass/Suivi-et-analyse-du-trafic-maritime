class UserHasRole:
    def __init__(self, IDUser, IDRole):
        self.IDUser = IDUser
        self.IDRole = IDRole

    def __init__(self):
        self.IDUser = None
        self.IDRole = None


    def Hydrate(self, row):
        for key in row.keys():
            if key in self.__dict__:
                self._hydrate_(key, row[key])

    def _hydrate_(self, key, value):
        match key:
            case 'IDUser':
                self.IDUser = value
            case 'IDRole':
                self.IDRole = value