from pydantic import BaseModel
from typing import Optional

# Définition du modèle Vessel en utilisant Pydantic
# BaseModel est la classe de base de Pydantic pour créer des modèles de données avec validation automatique
class GETVesselModel_Shipowner(BaseModel):
    
    # Champ "MMSI" : numéro d'identification à neuf chiffres unique à chaque navire obtenu lors de l'obtention d'une licence radio, obligatoire et doit être une chaîne de caractères
    MMSI: str

    # Champ "IMO" : numéro d'identification composé de trois lettres et sept chiffres unique à chaque navire, numéro attribué à la construction du navire, doit être une chaîne de caractères
    IMO: Optional[str]

    # Champ "CallSign" : identifiant unique utilisé lors des communications radio, doit être une chaîne de caractères
    CallSign: Optional[str]

    # Champ "IDVesselType" : type de navire, fait référence a la clé primaire de la table "VesselType", doit être un entier
    IDVesselType: Optional[int] = 0

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
    
    # Champ "IDCountry" : identifiant propre a chaque pays, fait référence a la table "Country", doit être une chaîne de caractères
    NameCountry: Optional[str]

    # Champ "TransceiverClass" : type du materiel de communication radio, doit être une chaîne de caractères
    TransceiverClass: Optional[str]

    # Champ "IDCompany" : numéro d'identification de l'entreprise, doit être un entier
    IDCompany: Optional[int]
    
    # Champ "LAT" : Latitude de la position du bateau, obligatoire et doit être un nombre décimal
    LAT: Optional[float] 

    # Champ "LON" : Longitude de la position du bateau, obligatoire et doit être un nombre décimal
    LON: Optional[float] 

    # Champ "SOG" : Speed Over Ground, vitesse du bateau, optionnel et doit être un nombre décimal
    SOG: Optional[float]

    # Champ "COG" : Course Over Ground, direction du bateau, obligatoire et doit être un nombre décimal
    COG: Optional[float]
    
    # Champ "Heading" : Degré de direction du bateau (son cap), obligatoire et doit être un nombre décimal
    Heading: Optional[float]

    # Champ "Status" : Statut du bateau défini par le COLREGS, obligatoire et doit être un entier
    # Statut 15 = Indéfini
    Status: Optional[int]

    # Champ "Region" : Région du globe où se trouve le bateau, optionnel et doit être une chaîne de caractères
    Region: Optional[str]
