from .mapping import TABLES, MAPPING
from .OBJETS.Vessel import Vessel
from .OBJETS.VesselType import VesselType
from .OBJETS.Position import Position
from .OBJETS.NavigationStatus import NavigationStatus
from .OBJETS.Company import Company
from .OBJETS.Country import Country
from .OBJETS.Role import Role
from .OBJETS.User import User
from .OBJETS.UserHasRole import UserHasRole
from .OBJETS.UserHasVessel import UserHasVessel


IDS = {
    'Country' : ('IDCountry',),
    'VesselType': ('VesselType',),
    'Vessel': ('MMSI',),
    'NavigationStatus': ('NavStatus',),
    'Position': ('MMSI', 'BaseDateTime'),
    'Role': ('IDRole',),
    'User': ('IDUser',),
    'Company' : ('IDCompany',),
    'UserHasRole' : ('IDUser','IDRole'),
    'UserHasVessel' : ('IDUser','MMSI')
}

class Mapper:
    """
    Objectif, classer la ligne dans chaque un objet.
    Définir la solution de stockage
    """

    def __init__(self)->None:
        """
        Définis la solution de stockage 
        Nous sommes actuellement partis sur un dictionnaire de dictionaire
        """

        self.global_data = {table : {} for table in TABLES}

    def _FactoryObject(self, object_:str):
        objects = {
            'Vessel': Vessel(),
            'VesselType':VesselType(),
            'Country':Country(),
            'Position':Position(),
            'NavigationStatus':NavigationStatus(),
            'Role':Role(),
            'User':User(),
            'Company':Company(),
            'UserHasRole':UserHasRole(),
            'UserHasVessel':UserHasVessel()
            }
        return objects[object_]

    def ReadRow(self, row:dict= {})->bool:
        """
        Lit une ligne et stocke les données dans le bon endroit.

        row: dict, La ligne à lire
            DEFAULT ""
        """

        if(row == {}) : raise Exception("Row must be non-empty")



        #Je navigue dans toutes mes tables
        for table in IDS.keys() :

            #Je reconstitue l'ID de la table
            idTable = []
            for single_id in IDS[table]:
                if single_id in row:
                    idTable.append(row[single_id])
            idTable = tuple(idTable)
            
            # Je regarde si on à deja un object ayant le même id (doublons ou nouveau status)
            # Dans ce cas je ne le refais pas
            # Sinon je le créer et je l'hydrate 
            if(idTable not in self.global_data[table].keys() and idTable != () and len(idTable) == len(IDS[table])):
                #Création et hydratation des objets 
                temp_object = self._FactoryObject(table)
                temp_object.Hydrate(row)
                self.global_data[table][idTable] = temp_object

    
    def GetAllObject(self)->dict:
        """
        Renvoie l'entiereté des données à renvoyer 
        """
        return self.global_data

            
        
            

