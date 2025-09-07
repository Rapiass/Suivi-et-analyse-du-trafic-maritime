from fastapi import APIRouter, HTTPException, Depends
from Database import db
from Models.GETUserModel import GETUserModel
from Models.POSTUserModel import POSTUserModel
from Models.PUTUserModel import PUTUserModel
from Routes.JWT_Manage import get_current_user
from HashagePassword import hash_password

router = APIRouter()

@router.get("/users", response_model=list[GETUserModel])
def get_all_users(current_user: dict = Depends(get_current_user)):
    """
    Récupère la liste de tous les utilisateurs avec leur rôle.
    Seul un administrateur peut accéder à cette ressource.
    """
    if current_user['Role'] != 'Admin':
        raise HTTPException(status_code=403, detail="You are not allowed to access this resource")
    
    try:
        results = db.DQL("""
            SELECT U.IDUser, U.Login, R.Role 
            FROM User U
            JOIN UserHasRole UHR ON U.IDUser = UHR.IDUser
            JOIN Role R ON UHR.IDRole = R.IDRole
        """)
        if not results:
            raise HTTPException(status_code=404, detail="No users found")
        return [GETUserModel(**user) for user in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {e}")

@router.post("/users")
def create_user(user: POSTUserModel, current_user: dict = Depends(get_current_user)):
    """
    Ajoute un nouvel utilisateur avec un rôle.
    Seul un administrateur peut ajouter un utilisateur.
    """
    if current_user['Role'] != 'Admin':
        raise HTTPException(status_code=403, detail="You are not allowed to add users")
    
    try:
        hashed_password = hash_password(user.Password)
        db.DML("INSERT INTO User (Login, Password) VALUES (%s, %s)", (user.Login, hashed_password))
        user_id = db.DQL("SELECT IDUser FROM User WHERE Login = %s", (user.Login,))[0]['IDUser']
        db.DML("INSERT INTO UserHasRole (IDUser, IDRole) VALUES (%s, %s)", (user_id, user.IDRole))
        return {"message": "User created successfully", "Login": user.Login, "RoleID": user.IDRole}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {e}")

@router.put("/users/{user_id}")
def update_user(user_id: int, user: PUTUserModel, current_user: dict = Depends(get_current_user)):
    """
    Met à jour un utilisateur (login, mot de passe et rôle).
    Seul un administrateur peut modifier un utilisateur.
    """
    if current_user['Role'] != 'Admin':
        raise HTTPException(status_code=403, detail="You are not allowed to update users")
    
    try:
        hashed_password = hash_password(user.Password) if user.Password else None
        if hashed_password:
            db.DML("UPDATE User SET Login = %s, Password = %s WHERE IDUser = %s", (user.Login, hashed_password, user_id))
        else:
            db.DML("UPDATE User SET Login = %s WHERE IDUser = %s", (user.Login, user_id))
        
        db.DML("UPDATE UserHasRole SET IDRole = %s WHERE IDUser = %s", (user.IDRole, user_id))
        return {"message": "User updated successfully", "IDUser": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating user: {e}")

@router.delete("/users/{user_id}")
def delete_user(user_id: int, current_user: dict = Depends(get_current_user)):
    """
    Supprime un utilisateur et son rôle.
    Seul un administrateur peut supprimer un utilisateur.
    """
    if current_user['Role'] != 'Admin':
        raise HTTPException(status_code=403, detail="You are not allowed to delete users")
    
    try:
        db.DML("DELETE FROM UserHasRole WHERE IDUser = %s", (user_id,))
        db.DML("DELETE FROM User WHERE IDUser = %s", (user_id,))
        return {"message": "User deleted successfully", "IDUser": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting user: {e}")
