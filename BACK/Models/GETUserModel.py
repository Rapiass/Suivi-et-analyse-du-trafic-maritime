from pydantic import BaseModel
from typing import Optional

# Définition du modèle User en utilisant Pydantic
# BaseModel est la classe de base de Pydantic pour créer des modèles de données avec validation automatique
class GETUserModel(BaseModel):
    IDUser: int
    Login: str
    Role: Optional[str] = None  # Rend le champ optionnel
