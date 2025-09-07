from pydantic import BaseModel
from typing import Optional
import datetime

### Définition du modèle pour récuperer les bateaux par region avec l'expert
class GETVesselRegionModel(BaseModel):

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

    # Champ "Region" : Région du globe ou se trouve le bateau, optionnel doit être une chaîne de caractères
    Region: str = "Not found"

    # Champ "IMO" : numéro d'identification composé de trois lettres et sept chiffres unique à chaque navire, numéro attribué à la construction du navire, doit être une chaîne de caractères
    IMO: Optional[str]

    # Champ "CallSign" : identifiant unique utilisé lors des communications radio, doit être une chaîne de caractères
    CallSign: Optional[str]

    # Champ "VesselType" : type de navire, fait référence a la clé primaire de la table "VesselType", doit être un entier
    VesselType: Optional[int] = 0

    # Champ "VesselName" : nom du navire, doit être une chaîne de caractères
    VesselName: Optional[str]

    # Champ "Length" : longueur du navire, doit être un nombre décimal
    Length: Optional[float]

    # Champ "Width" : largeur du navire, doit être un nombre décimal
    Width: Optional[float]

    # Champ "Draft" : distance entre la ligne de flotaison et le point le plus bas de la coque, doit être un nombre décimal
    Draft: Optional[float]

    # Champ "Cargo" : type de cargo voir table "NAIS", doit être une chaîne de caractères
    Cargo: Optional[str]
    
    # Champ "IDCountry" : identifiant propre à chaque pays, fait référence a la table "Country", doit être une chaîne de caractères
    NameCountry: Optional[str] = None 

    # Champ "TransceiverClass" : type du matériel de communication radio, doit être une chaîne de caractères
    TransceiverClass: Optional[str]

    # Champ "IDCompany" : numéro d'identification de l'entreprise, doit être un entier
    NameCompany: Optional[str] = None