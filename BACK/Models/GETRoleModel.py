from pydantic import BaseModel

# Définition du modèle Role en utilisant Pydantic
# BaseModel est la classe de base de Pydantic pour créer des modèles de données avec validation automatique
class GETRoleModel(BaseModel):
    # Champ "IDRole" : identifiant du rôle, obligatoire et doit être un int
    IDRole: int
    
    # Champ "Role" : titre du rôle de l'utilisateur, doit être une chaîne de caractères
    Role: str
# Les deux attributs sont obligatoires tant que nous n'avons pas configuré la sécurité