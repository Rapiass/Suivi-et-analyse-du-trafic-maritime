from fastapi import APIRouter, HTTPException, Depends
from Database import db
from Models.POSTUserModel import POSTUserModel
from Models.POSTUserLoginModel import POSTUserLoginModel
from Models.GETUserModel import GETUserModel
from Routes.JWT_Manage import create_access_token, get_current_user
from HashagePassword import hash_password, check_password
router = APIRouter()

@router.get("/user", response_model=GETUserModel)
def get_user(current_user: dict = Depends(get_current_user)):
    """
    Récupère les informations d'un utilisateur via son token bearer.

    Cette fonction exécute une requête SQL pour obtenir des informations détaillées sur un utilisateur.

    Returns:
        GETUserModel: contenant les informations d'un user.

    Raises:
        HTTPException: Si aucune donnée n'est trouvée, retourne un code 404 avec le message "No ships found for this user.".
                       En cas d'erreur de base de données, retourne un code 500 avec un message d'erreur.
    """
    try:
        # Utilisation de la fonction DQL pour exécuter la requête
        result = db.DQL("SELECT IDUser, Login FROM User WHERE IDUser = %s", (current_user["IDUser"],))
        
        # Si aucun utilisateur n'est trouvé
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Créer un objet GETUserModel avec les données récupérées
        return GETUserModel(**result[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {e}")

# Endpoint pour ajouter un utilisateur
@router.post("/register")
def create_user(user: POSTUserModel):
    """
    Crée un utilisateur et lui attribue un rôle dans la base de données.

    Args:
        user (POSTUserModel): Les informations de l'utilisateur (Login, Password, RoleID).

    Returns:
        dict: Un message de confirmation et le login de l'utilisateur.

    Raises:
        HTTPException: En cas d'erreur de base de données ou si le rôle est invalide.
    """
    try:
        print("Données reçues:", user.dict())
        # Vérifier si le rôle existe
        role_exists = db.DQL("SELECT IDRole FROM Role WHERE IDRole = %s", (user.IDRole,))
        if not role_exists:
            raise HTTPException(status_code=400, detail="Invalid Role ID")

        # Ajouter l'utilisateur
        db.DML("INSERT INTO User (Login, Password) VALUES (%s, %s)", 
               (user.Login, hash_password(user.Password)))

        # Récupérer l'ID de l'utilisateur nouvellement créé
        user_id = db.DQL("SELECT IDUser FROM User WHERE Login = %s", (user.Login,))[0]["IDUser"]

        # Associer l'utilisateur au rôle
        db.DML("INSERT INTO UserHasRole (IDUser, IDRole) VALUES (%s, %s)", (user_id, user.IDRole))

        return {"message": "User created successfully", "Login": user.Login, "RoleID": user.IDRole}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inserting user: {e}")


@router.post("/login")
def login(user: POSTUserLoginModel):
    query = """
    SELECT U.IDUser, Login, Password, r.Role 
    FROM User U 
    JOIN UserHasRole uhr ON uhr.IDUser = U.IDUser 
    JOIN Role r ON r.IDRole = uhr.IDRole 
    WHERE LOWER(U.Login) = LOWER(%s)
    """

    try:
        # 🔥 DEBUG: Afficher le login envoyé
        print(f"Tentative de connexion avec Login: {user.Login}")

        result = db.DQL(query, (user.Login,))
        
        # 🔥 DEBUG: Afficher le résultat de la requête
        print(f"Résultat SQL: {result}")

        if not result:
            raise HTTPException(status_code=401, detail="User not found")  # ⚠️ L'utilisateur n'existe pas
        
        # 🔥 DEBUG: Vérifier les mots de passe
        print(f"Password fourni: {user.Password}")
        print(f"Password en base: {result[0]['Password']}")

        if not check_password(user.Password, result[0]["Password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Création du token JWT
        user_data = result[0]
        access_token = create_access_token(data={
            "Login": user_data["Login"], 
            "IDUser": user_data["IDUser"], 
            "Role": user_data["Role"]
        })
        return {"access_token": access_token, "token_type": "bearer","Role":user_data["Role"]}
    
    except Exception as e:
        print(f"Erreur complète : {str(e)}")  # 🔥 DEBUG
        raise HTTPException(status_code=500, detail=f"Error during login: {str(e)}")

