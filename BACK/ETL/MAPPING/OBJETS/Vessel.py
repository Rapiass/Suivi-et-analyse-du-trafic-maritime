import re

class Vessel:
    def __init__(self, MMSI, IMO, CallSign, IDVesselType, VesselName, Length, Width, Draft, Cargo, IDCountry, TransceiverClass, IDCompany):
        self.MMSI = MMSI
        self.IMO = IMO
        self.CallSign = CallSign
        self.IDVesselType = IDVesselType
        self.VesselName = VesselName
        self.Length = Length
        self.Width = Width
        self.Draft = Draft
        self.Cargo = Cargo
        self.IDCountry = IDCountry
        self.TransceiverClass = TransceiverClass
        self.IDCompany = IDCompany

    def __init__(self):
        self.MMSI = None
        self.IMO = None
        self.CallSign = None
        self.IDVesselType = None
        self.VesselName = None
        self.Length = None
        self.Width = None
        self.Draft = None
        self.Cargo = None
        self.IDCountry = None
        self.TransceiverClass = None
        self.IDCompany = ""



    def Hydrate(self, row):
        for key in row.keys():
            self._hydrate_(key, row[key])
        
    def _hydrate_(self, key, value):
        match key:
            case 'MMSI':
                self.MMSI = value
                self.IDCountry = value[:3]
            case 'IMO':
                self.IMO = f"\"{value}\""
            case 'CallSign':
                self.CallSign = f"\"{value}\""
            case 'VesselType':
                self.IDVesselType = value
            case 'VesselName':
                temp_val = re.sub("'"," ",re.sub(r'"',' ', value))
                self.VesselName = f"\"{temp_val}\""
            case 'Length':
                self.Length = value
            case 'Width':
                self.Width = value
            case 'Draft':
                self.Draft = value
            case 'Cargo':
                self.Cargo = value
            case 'TransceiverClass':
                self.TransceiverClass = f"\"{value}\""
            case 'IDCompany':
                self.IDCompany = value





