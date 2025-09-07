class User:
    def __init__(self, IDUser,  Password, Login):
        self.IDUser = IDUser
        self.Password = Password
        self.Login = Login

    def __init__(self):
        self.IDUser = None
        self.Password = None
        self.Login = None


    def Hydrate(self, row):
        for key in row.keys():
            if key in self.__dict__:
                self._hydrate_(key, row[key])

    def _hydrate_(self, key, value):
        match key:
            case 'IDUser':
                self.IDUser = value
            case 'Password':
                self.Password = f"\"{value}\""
            case 'Login':
                self.Login = f"\"{value}\""