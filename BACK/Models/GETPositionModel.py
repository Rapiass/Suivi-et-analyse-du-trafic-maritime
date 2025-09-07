from pydantic import BaseModel
from typing import Optional
import datetime

### Définition du modèle pour la table Position de la base de données lors d'une requête GET (Back -> Front)
class GETPositionModel(BaseModel):

    ### Définition des champs de la table

    # Champ "MMSI" : Maritime Mobile Service Identity du bateau, obligatoire et doit être une chaîne de caractères
    MMSI: str 

    # Champ "BaseDateTime" : Date et heure de la position (format YYYY-MM-DD:HH-MM-SS), obligatoire et doit être une date
    BaseDateTime: datetime.datetime

    # Champ "LAT" : Latitude de la position du bateau, obligatoire et doit être un nombre décimal
    LAT: float 

    # Champ "LON" : Longitude de la position du bateau, obligatoire et doit être un nombre décimal
    LON: float 

    # Champ "SOG" : Speed Over Ground, vitesse du bateau, optionnel et doit être un nombre décimal
    SOG: Optional[float] = None

    # Champ "COG" : Course Over Ground, direction du bateau, obligatoire et doit être un nombre décimal
    COG: Optional[float] = None 
    
    # Champ "Heading" : Degré de direction du bateau (son cap), obligatoire et doit être un nombre décimal
    Heading: Optional[float] = None

    # Champ "Status" : Statut du bateau défini par le COLREGS, obligatoire et doit être un entier
    # Statut 15 = Indéfini
    Status: int = 15

    # Champ "Region" : Région du globe ou se trouve le bateau, optionnel et doit être une chaîne de caractères
    Region: str = "Not found"
