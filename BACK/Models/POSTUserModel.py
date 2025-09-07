from pydantic import BaseModel
from typing import Optional

# Définition du modèle User en utilisant Pydantic
# BaseModel est la classe de base de Pydantic pour créer des modèles de données avec validation automatique
class POSTUserModel(BaseModel):

    # Champ "Login" : login de l'utilisateur
    Login: str

    # Champ "Password" : mot de passe obligatoire de l'utilisateur
    Password: str 

    # Champ "Role" : role obligatoire de l'utilisateur
    IDRole: int

