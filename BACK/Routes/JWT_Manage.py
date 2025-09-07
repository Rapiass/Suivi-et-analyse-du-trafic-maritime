import jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

# Clé secrète pour signer les tokens JWT
SECRET_KEY = "LeProjetAISEtLes9JoyeuxDev"
ALGORITHM = "HS256"
# Durée de vie du token d'accès en minutes (ici 30 minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2PasswordBearer pour obtenir le token à partir de l'en-tête Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

"""
    Crée un token JWT avec une date d'expiration.
    
    :param data: Données à inclure dans le token sous forme de dictionnaire.
    :return: Token JWT encodé.
"""
def create_access_token(data: dict):
    to_encode = data.copy()  # Copie des données pour éviter de les modifier
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Ajoute la date d'expiration au payload
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

"""
    Vérifie et décode un token JWT.
    
    :param token: Le token à vérifier.
    :return: Payload décodé si le token est valide.
    :raises HTTPException: Si le token a expiré ou est invalide.
"""
def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
"""
    Récupère l'utilisateur actuel à partir du token JWT.
    
    :param token: Le token JWT à vérifier.
    :return: Payload du token décodé.
"""
def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_jwt_token(token)
