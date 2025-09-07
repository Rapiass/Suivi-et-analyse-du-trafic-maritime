from pydantic import BaseModel
from typing import Optional
from Models.GETPositionModel import GETPositionModel

# Définition du modèle Vessel en utilisant Pydantic
# BaseModel est la classe de base de Pydantic pour créer des modèles de données avec validation automatique
class GETVesselModel(BaseModel):
    MMSI: str
    IMO: Optional[str]
    CallSign: Optional[str]
    VesselType: Optional[int]
    VesselDescription: Optional[str]
    VesselName: Optional[str]
    Length: Optional[float]
    Width: Optional[float]
    Draft: Optional[float]
    Cargo: Optional[int]
    NameCountry: Optional[str]
    TransceiverClass: Optional[str]
    NameCompany: Optional[str]
    Position: Optional[GETPositionModel] = None
