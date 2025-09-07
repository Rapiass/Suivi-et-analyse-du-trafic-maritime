from fastapi import APIRouter, HTTPException, Depends
from Database import db
from Routes.JWT_Manage import get_current_user
from Models.GETVesselModel_Shipowner import GETVesselModel_Shipowner
from typing import List

router = APIRouter()

@router.get("/armateur/vessels", response_model=List[GETVesselModel_Shipowner])
def get_ships(current_user: dict = Depends(get_current_user)):
    """
    Récupère la liste de tous les bateaux appartenant à l'armateur connecté.

    Cette fonction exécute une requête SQL pour obtenir des informations détaillées sur chaque bateau de l'armateur.
    Elle effectue une jointure avec les tables UserHasVessel, Vessel, Position, NavigationStatus, Country pour obtenir les informations

    Returns:
        list[GETVesselModel_Shipowner]: Une liste d'objets GETVesselModel_Shipowner contenant les informations des vessels.

    Raises:
        HTTPException: Si aucune donnée n'est trouvée, retourne un code 404 avec le message "No ships found for this user.".
                       En cas d'erreur de base de données, retourne un code 500 avec un message d'erreur.
                       Si une autre erreur survient, retourne un code 400 avec un message d'erreur.
    """
    if current_user['Role'] != 'Armateur':
        raise HTTPException(
            status_code=403, 
            detail="You are not allowed to access this resource."
        )
        
    try:
        # Requête SQL
        query = """
            SELECT 
            V.MMSI,
            V.IMO,
            V.CallSign,
            V.IDVesselType,
            V.VesselName,
            V.Length,
            V.Width,
            V.Draft,
            V.Cargo,
            c.NameCountry,
            V.TransceiverClass,
            V.IDCompany,
            P.LAT,
            P.LON,
            P.SOG,
            P.COG,
            P.Heading,
            P.Status,
            P.Region
        FROM Vessel V
        INNER JOIN UserHasVessel UHV ON V.MMSI = UHV.MMSI
        LEFT JOIN (
            SELECT 
                p.MMSI,
                p.LAT,
                p.LON,
                p.SOG,
                p.COG,
                p.Heading,
                p.Status,
                p.Region,
                p.BaseDateTime
            FROM Position p
            INNER JOIN (
                SELECT MMSI, MAX(BaseDateTime) AS MaxDate
                FROM Position
                GROUP BY MMSI
            ) latest ON p.MMSI = latest.MMSI AND p.BaseDateTime = latest.MaxDate
            LEFT JOIN NavigationStatus NS ON NS.Status = p.Status
        ) P ON V.MMSI = P.MMSI
        INNER JOIN Country c ON c.IDCountry = V.IDCountry
        WHERE UHV.IDUser = %s;


        """

        # Exécution de la requête
        results = db.DQL(query, (current_user['IDUser'],))
    

        # Vérification si aucun résultat n'est trouvé
        if not results: 
            raise HTTPException(status_code=404, detail="No ships found for this user.")
            
        return [GETVesselModel_Shipowner(**result) for result in results]
    # Gestion des erreurs spécifiques à la base de données
    except db.DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    
    # Gestion des autres erreurs
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unexpected error: {str(e)}")


# Endpoint pour obtenir les informations du bateau de l'armateur sélectionné
@router.get("/armateur/vessels/{mmsi}", response_model=GETVesselModel_Shipowner)
def get_ship_info(mmsi: str, current_user: dict = Depends(get_current_user)):
    """
    Récupère le bateau specifier par son MMSI appartenant à l'armateur connecté.

    Cette fonction exécute une requête SQL pour obtenir des informations détaillées sur un bateau.
    Elle effectue une jointure avec les tables UserHasVessel, Vessel, Position, NavigationStatus, Country pour obtenir les informations

    Returns:
        lGETVesselModel_Shipowner: contenant les informations des vessels.

    Raises:
        HTTPException: Si aucune donnée n'est trouvée, retourne un code 404 avec le message "No ships found for this user.".
                       En cas d'erreur de base de données, retourne un code 500 avec un message d'erreur.
                       Si une autre erreur survient, retourne un code 400 avec un message d'erreur.
    """
    if current_user['Role'] != 'Armateur':
        raise HTTPException(
            status_code=403, 
            detail="You are not allowed to access this resource."
        )
        
    try:
        query = """
            SELECT V.MMSI,V.IMO,V.CallSign,V.IDVesselType,V.VesselName,
            V.Length,V.Width,V.Draft,V.Cargo,c.NameCountry ,V.TransceiverClass,V.IDCompany,
            P.LAT, P.LON, P.SOG, P.COG, P.Heading, P.Status, P.Region
            FROM Vessel V 
            INNER JOIN UserHasVessel UHV ON V.MMSI = UHV.MMSI 
            LEFT JOIN (
                SELECT * FROM `Position` p 
                NATURAL JOIN NavigationStatus
                ORDER BY BaseDateTime DESC
            ) P ON V.MMSI = P.MMSI
            INNER JOIN Country c ON c.IDCountry = V.IDCountry  
            WHERE UHV.IDUser = %s
            AND UHV.MMSI = %s
        """
        result = db.DQL(query, (current_user['IDUser'], mmsi))
        
        if not result:
            raise HTTPException(status_code=404, detail="No ship found for this user")

        return GETVesselModel_Shipowner(**result[0])  # result[0] car DQL renvoie une liste
    except db.DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching ship info: {e}")

@router.post("/armateur/addmmsi/{mmsi}")
def assign_ship_to_owner(mmsi: str, current_user: dict = Depends(get_current_user)):
    """
    Assigne un bateau existant à l'armateur connecté, si aucun autre armateur ne l'a déjà.

    Args:
        mmsi (str): Le MMSI du bateau à associer

    Returns:
        dict: Message de confirmation

    Raises:
        HTTPException: Si le bateau n'existe pas, est déjà assigné à un armateur, ou autre erreur
    """
    if current_user["Role"] != "Armateur":
        raise HTTPException(status_code=403, detail="You are not allowed to access this resource.")

    try:
        # Vérifie que le bateau existe
        vessel_check = db.DQL("SELECT * FROM Vessel WHERE MMSI = %s", (mmsi,))
        if not vessel_check:
            raise HTTPException(status_code=404, detail="Vessel not found.")

        # Vérifie si un autre armateur l'a déjà (IsCaptain = 0)
        already_assigned = db.DQL(
            "SELECT * FROM UserHasVessel WHERE MMSI = %s AND IsCaptain = 0", (mmsi,)
        )
        if already_assigned:
            raise HTTPException(status_code=400, detail="This vessel is already assigned to another shipowner.")

        # Vérifie si l'utilisateur a déjà ce bateau (ça peut arriver si IsCaptain=1 pour lui)
        existing_link = db.DQL(
            "SELECT * FROM UserHasVessel WHERE IDUser = %s AND MMSI = %s",
            (current_user["IDUser"], mmsi)
        )
        if existing_link:
            raise HTTPException(status_code=400, detail="You already have this vessel assigned.")

        # Ajoute l'association
        db.DML(
            "INSERT INTO UserHasVessel (IDUser, MMSI, IsCaptain) VALUES (%s, %s, %s)",
            (current_user["IDUser"], mmsi, 0)
        )

        return {"message": f"Vessel {mmsi} successfully assigned to armateur."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error assigning vessel: {e}")


@router.delete("/armateur/delmmsi/{mmsi}")
def unassign_ship_from_owner(mmsi: str, current_user: dict = Depends(get_current_user)):
    """
    Supprime l'association d'un bateau avec l'armateur connecté.

    Args:
        mmsi (str): Le MMSI du bateau à dissocier

    Returns:
        dict: Message de confirmation

    Raises:
        HTTPException: Si le bateau n'est pas associé ou autre erreur
    """
    if current_user["Role"] != "Armateur":
        raise HTTPException(status_code=403, detail="You are not allowed to access this resource.")

    try:
        # Vérifie si le lien existe
        check_query = "SELECT * FROM UserHasVessel WHERE IDUser = %s AND MMSI = %s"
        result = db.DQL(check_query, (current_user["IDUser"], mmsi))
        if not result:
            raise HTTPException(status_code=404, detail="This vessel is not assigned to you.")

        # Supprime l'association
        delete_query = "DELETE FROM UserHasVessel WHERE IDUser = %s AND MMSI = %s"
        db.DML(delete_query, (current_user["IDUser"], mmsi))

        return {"message": f"Vessel {mmsi} unassigned from armateur successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error unassigning vessel: {e}")
