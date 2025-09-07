from fastapi import APIRouter, HTTPException, Depends
from Database import db
from Models.GETUserModel import GETUserModel
from Models.GETCaptainVessel import GETCaptainVessel
from Routes.JWT_Manage import get_current_user
from typing import List

router = APIRouter()

from typing import List

@router.get("/captain", response_model=List[GETUserModel])
def get_captains():
    """
    Récupère la liste de tous les capitaines

    Cette fonction exécute une requête SQL pour obtenir des informations détaillées sur chaque Capitaine.
    Elle effectue une jointure avec les tables UserHasRole, User

    Returns:
        list[GETUserModel]: Une liste d'objets GETUserModel contenant les informations des capitaines.

    Raises:
        HTTPException: Si aucune donnée n'est trouvée, retourne un code 404 avec le message "No captain found".
                       En cas d'erreur de base de données, retourne un code 500 avec un message d'erreur.
                       Si une autre erreur survient, retourne un code 400 avec un message d'erreur.
"""
    try:
        # Requête SQL pour obtenir la liste des capitaines
        query = """
            SELECT u.IDUser, u.Name, u.Firstname, u.Login 
            FROM User u 
            JOIN UserHasRole ur ON u.IDUser = ur.IDUser 
            WHERE ur.IDRole = 2
        """
        result = db.DQL(query)

        # Si aucun capitaine n'est trouvé
        if not result:
            raise HTTPException(status_code=404, detail="No captain found")
        
        # Crée une liste d'objets GETUserModel pour chaque capitaine
        captains = [GETUserModel(
            IDUser=row["IDUser"],
            Name=row["Name"],
            Firstname=row["Firstname"],
            Login=row["Login"]
        ) for row in result]
        
        return captains

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching captains: {e}")
    
    
# Endpoint pour obtenir un capitaine par son ID
@router.get("/captain/{id}", response_model=GETUserModel)
def get_captain(id: int):
    """
    Récupère les informations d'un Capitaine par son ID

    Cette fonction exécute une requête SQL pour obtenir des informations détaillées sur un Capitaine.
    Elle effectue une jointure avec les tables UserHasRole, User

    Returns:
        GETUserModel: Une liste d'objets GETUserModel contenant les informations d'un User.

    Raises:
        HTTPException: Si aucune donnée n'est trouvée, retourne un code 404 avec le message "No captain found with the provided ID".
                       En cas d'erreur de base de données, retourne un code 500 avec un message d'erreur.
                       Si une autre erreur survient, retourne un code 400 avec un message d'erreur.
    """
    try:
        # Requête SQL pour obtenir un capitaine par son ID
        query = """
            SELECT u.IDUser, u.Name, u.Firstname, u.Login 
            FROM User u 
            JOIN UserHasRole ur ON u.IDUser = ur.IDUser 
            WHERE ur.IDRole = 2 AND u.IDUser = %s;
        """
        result = db.DQL(query, (id,))
        
        # Retourne une erreur si aucun capitaine n'est trouvé
        if not result:
            raise HTTPException(status_code=404, detail="No captain found with the provided ID")

        # Crée un objet GETUserModel avec les informations du capitaine
        captain = GETUserModel(
            IDUser=result[0]["IDUser"],
            Name=result[0]["Name"],
            Firstname=result[0]["Firstname"],
            Login=result[0]["Login"]
        )
        return captain

    # Retourne une erreur si une exception est levée
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching captain: {e}")
    
# Endpoint pour avoir la liste des bateaux d'un capitaine et leur position
@router.get("/captain/vessels/position_bateau")
def get_vessels_position(current_user: dict = Depends(get_current_user)):
    """
    Récupère les informations de position du bateau d'un Capitaine par son ID

    Cette fonction exécute une requête SQL pour obtenir des informations détaillées sur la position du bateau.
    Elle effectue une jointure avec les tables Vessel, UserHasVessel, Position

    Returns:
        [GETCaptainVessel]: Une liste d'objets GETCaptainVessel contenant les informations d'un bateau.

    Raises:
        HTTPException: Si aucune donnée n'est trouvée, retourne un code 404 avec le message "No vessel for the provide captain ID".
                       En cas d'erreur de base de données, retourne un code 500 avec un message d'erreur.
                       Si une autre erreur survient, retourne un code 400 avec un message d'erreur.
    """
    if current_user['Role'] != 'Capitaine':
        raise HTTPException(status_code=403, detail="You are not a captain")
    try:
        # Requête SQL pour obtenir les bateaux d'un capitaine
        query = """
            SELECT v.MMSI, v.VesselName, p.LAT AS Latitude, p.LON AS Longitude 
            FROM Vessel v 
            JOIN UserHasVessel uv ON v.MMSI = uv.MMSI 
            JOIN Position p ON v.MMSI = p.MMSI 
            WHERE uv.IDUser = %s;
        """
        result = db.DQL(query, (current_user["IDUser"],))

        # Retourne une erreur si aucun bateau n'est trouvé pour le capitaine
        if not result:
            raise HTTPException(status_code=404, detail="No vessel for the provide captain ID")

        # Crée un objet GETVesselModel avec les informations des bateaux du capitaine
        captain_vessels = [GETCaptainVessel(
            MMSI=row["MMSI"],
            VesselName=row["VesselName"],
            LAT=row["Latitude"],
            LON=row["Longitude"]
        ) for row in result]
        
        return captain_vessels

    # Retourne une erreur si une exception est levée
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching vessels: {e}")


@router.post("/captain/addmmsi/{mmsi}")
def assign_vessel_to_captain(
    mmsi: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Assigne un bateau à un capitaine (ou remplace son bateau actuel si nécessaire)
    """
    if current_user['Role'] != 'Capitaine':
        raise HTTPException(status_code=403, detail="You are not a captain")

    try:
        # Vérifie si le bateau existe
        vessel_check_query = "SELECT * FROM Vessel WHERE MMSI = %s"
        vessel_result = db.DQL(vessel_check_query, (mmsi,))
        if not vessel_result:
            raise HTTPException(status_code=404, detail="Vessel not found")

        # Vérifie si un capitaine a déjà ce bateau
        existing_captain_query = """
            SELECT uv.IDUser FROM UserHasVessel uv
            JOIN UserHasRole ur ON uv.IDUser = ur.IDUser
            WHERE uv.MMSI = %s AND ur.IDRole = 1 
        """
        existing_captain = db.DQL(existing_captain_query, (mmsi,))
        if existing_captain:
            raise HTTPException(status_code=400, detail="This vessel is already assigned to another captain")

        # Supprime tout ancien bateau de ce capitaine
        delete_query = """
            DELETE FROM UserHasVessel 
            WHERE IDUser = %s AND MMSI IN (
                SELECT MMSI FROM UserHasVessel WHERE IDUser = %s
            )
        """
        db.DML(delete_query, (current_user["IDUser"], current_user["IDUser"]))

        # Associe le bateau
        insert_query = "INSERT INTO UserHasVessel (IDUser, MMSI, IsCaptain) VALUES (%s, %s,%s)"
        db.DML(insert_query, (current_user["IDUser"], mmsi,1))

        return {"message": f"Vessel {mmsi} assigned to captain successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error assigning vessel: {e}")
  
@router.delete("/captain/delmmsi")
def unassign_vessel(current_user: dict = Depends(get_current_user)):
    """
    Supprime l'association entre un capitaine et son bateau actuel.

    Returns:
        dict: Message de confirmation

    Raises:
        HTTPException: Si aucun bateau n'était associé ou en cas d'erreur
    """
    if current_user['Role'] != 'Capitaine':
        raise HTTPException(status_code=403, detail="You are not a captain")

    try:
        # Vérifie s'il y a un bateau assigné
        check_query = "SELECT * FROM UserHasVessel WHERE IDUser = %s"
        check_result = db.DQL(check_query, (current_user["IDUser"],))
        if not check_result:
            raise HTTPException(status_code=404, detail="No vessel currently assigned to this captain")

        # Supprime l'association
        delete_query = "DELETE FROM UserHasVessel WHERE IDUser = %s"
        db.DML(delete_query, (current_user["IDUser"],))

        return {"message": "Vessel successfully unassigned from captain"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error unassigning vessel: {e}")

@router.get("/captain/voisins/{lat}/{lon}", response_model=List[GETCaptainVessel])
def get_neighboring_vessels_by_coordinates(
    lat: float,  # Latitude passée en paramètre
    lon: float,  # Longitude passée en paramètre
    current_user: dict = Depends(get_current_user)
):
    """
    Récupère les bateaux situés dans un rayon de 3° autour de la position donnée par latitude et longitude.

    Args:
        lat (float): Latitude du point central de la recherche.
        lon (float): Longitude du point central de la recherche.
        current_user (dict): L'utilisateur actuel, vérifié par JWT pour s'assurer que l'utilisateur est autorisé.

    Returns:
        List[GETCaptainVessel]: Liste des bateaux voisins avec position.
    
    Raises:
        HTTPException: Si le rôle n'est pas Capitaine ou en cas d'erreur de récupération des données.
    """
    if current_user['Role'] != 'Capitaine':
        raise HTTPException(status_code=403, detail="You are not a captain")

    try:
        # Rayon de recherche défini à 3°
        radius = 3.0

        # Calcul des bornes de latitude et de longitude autour du point donné
        lat_min = lat - radius
        lat_max = lat + radius
        lon_min = lon - radius
        lon_max = lon + radius

        # Étape 2: chercher les autres bateaux dans la zone définie
        voisins_query = """
            SELECT v.MMSI, v.VesselName, p.LAT AS Latitude, p.LON AS Longitude
            FROM Vessel v
            JOIN Position p ON v.MMSI = p.MMSI
            WHERE p.LAT BETWEEN %s AND %s
              AND p.LON BETWEEN %s AND %s
              AND p.BaseDateTime = (
                  SELECT MAX(BaseDateTime) FROM Position WHERE MMSI = v.MMSI
              )
              AND v.MMSI NOT IN (
                  SELECT MMSI FROM UserHasVessel WHERE IDUser = %s
              );
        """

        # Exécution de la requête pour récupérer les voisins
        result = db.DQL(
            voisins_query,
            (lat_min, lat_max, lon_min, lon_max, current_user["IDUser"])
        )

        if not result:
            return []  # Aucun voisin trouvé

        # Formatage de la réponse
        voisins = [GETCaptainVessel(
            MMSI=row["MMSI"],
            VesselName=row["VesselName"],
            LAT=row["Latitude"],
            LON=row["Longitude"]
        ) for row in result]

        return voisins

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching neighboring vessels: {e}")

