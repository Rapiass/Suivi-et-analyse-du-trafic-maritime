from pydantic import BaseModel
from typing import Optional

# Définition du modèle Company en utilisant Pydantic
# BaseModel est la classe de base de Pydantic pour créer des modèles de données avec validation automatique
class GETCompanyModel(BaseModel):
    # Champ "IDCompany" : titre de la tâche, obligatoire et doit être une chaîne de caractères
    IDCompany: int
    
    # Champ "NameCompany", obligatoire servant à préciser le nom de l'entreprise auquel le bateau est relié 
    NameCompany: str
    
    # Champ "IDCountry", correspondant à l'identifiant d'un pays afin de relier les tables Company et Country, il est optionnel, et vaut par défaut None
    IDCountry: Optional[int] = None