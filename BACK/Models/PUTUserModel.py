from pydantic import BaseModel
from typing import Optional

class PUTUserModel(BaseModel):
    Login: str
    Password: Optional[str] = None  # Mot de passe facultatif
    IDRole: int
