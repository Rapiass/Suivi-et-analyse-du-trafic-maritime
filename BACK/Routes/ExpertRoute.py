from Database import db
from Models.GETVesselModel import GETVesselModel
from Models.GETVesselRegionModel import GETVesselRegionModel
from Models.GETPositionModel import GETPositionModel
from Routes.JWT_Manage import get_current_user
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List

router = APIRouter()
"""
    Récupère la liste de tous les bateaux.

    Cette fonction exécute une requête SQL pour obtenir des informations détaillées sur chaque bateau.
    Elle effectue une jointure avec les tables VesselType, Country, Company, Position et 
    NavigationStatus afin d'obtenir une vue complète de chaque bateau.

    Args:
        current_user (dict): L'utilisateur actuel, vérifié par JWT pour s'assurer que l'utilisateur est autorisé.

    Returns:
        list[GETVesselModel]: Une liste d'objets GETVesselModel contenant les informations des bateaux.

    Raises:
        HTTPException: Si aucune donnée n'est trouvée, retourne un code 404 avec le message "No vessels found".
                       En cas d'erreur de base de données, retourne un code 500 avec un message d'erreur.
                       Si une autre erreur survient, retourne un code 400 avec un message d'erreur.
"""
# Endpoint pour récupérer tous les bateaux 


@router.get("/expert", response_model=List[GETVesselModel])
def get_vessels(
    vesselType: Optional[int] = Query(None, alias="vesselType"),  # paramètre optionnel, par défaut None
    region: Optional[str] = Query(None, alias="region"),  # paramètre optionnel, par défaut None
    current_user: dict = Depends(get_current_user)
):
    if current_user['Role'] != 'Expert':
        raise HTTPException(status_code=403, detail="You are not allowed to access this resource")

    try:
        query = """
            SELECT
                v.MMSI, v.IMO, v.CallSign, vt.IDVesselType AS VesselType, vt.Description AS VesselDescription, v.VesselName, 
                v.Length, v.Width, v.Draft, v.Cargo, c.NameCountry,  
                v.TransceiverClass, comp.NameCompany, 
                p.BaseDateTime, p.LAT, p.LON, p.SOG, p.COG, p.Heading, 
                ns.Status, p.Region
            FROM Vessel v
            LEFT JOIN VesselType vt ON v.IDVesselType = vt.IDVesselType 
            LEFT JOIN Country c ON v.IDCountry = c.IDCountry
            LEFT JOIN Company comp ON v.IDCompany = comp.IDCompany
            LEFT JOIN (
                SELECT p1.*
                FROM Position p1
                INNER JOIN (
                    SELECT MMSI, MAX(BaseDateTime) AS MaxTime
                    FROM Position
                    WHERE BaseDateTime BETWEEN (NOW() - INTERVAL 2 YEAR - INTERVAL 10 MINUTE)
                                        AND (NOW() - INTERVAL 2 YEAR)
                    GROUP BY MMSI
                ) p2 ON p1.MMSI = p2.MMSI AND p1.BaseDateTime = p2.MaxTime
            ) p ON v.MMSI = p.MMSI
            LEFT JOIN NavigationStatus ns ON p.Status = ns.Status
            WHERE 1=1
        """
        params = []

        if vesselType is not None:
            query += " AND vt.IDVesselType = %s"
            params.append(vesselType)
        if region:
            query += " AND p.Region = %s"
            params.append(region)

        results = db.DQL(query, tuple(params))

        vessels = []
        for row in results:
            position_data = {
                "MMSI": row["MMSI"],
                "BaseDateTime": row["BaseDateTime"],
                "LAT": row["LAT"],
                "LON": row["LON"],
                "SOG": row["SOG"],
                "COG": row["COG"],
                "Heading": row["Heading"],
                "Status": row["Status"] if row["Status"] is not None else 15,
                "Region": row["Region"] if row["Region"] else "Not found",
            }

            vessel_data = {k: row[k] for k in [
                "MMSI", "IMO", "CallSign", "VesselType", "VesselDescription", "VesselName", "Length",
                "Width", "Draft", "Cargo", "NameCountry", "TransceiverClass", "NameCompany"
            ]}
            vessel_data["Position"] = GETPositionModel(**position_data)

            vessels.append(GETVesselModel(**vessel_data))

        return vessels

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching vessels: {str(e)}")



"""
    Récupère les bateaux situés dans une région spécifique.

    Cette fonction exécute une requête SQL pour obtenir les informations des bateaux en fonction de la région
    spécifiée. Elle utilise des jointures avec les tables VesselType, Country, Company, Position et 
    NavigationStatus pour obtenir des informations détaillées sur chaque bateau.

    Args:
        region (str): La région pour laquelle on veut obtenir la liste des bateaux.
        current_user (dict): L'utilisateur actuel, vérifié par JWT pour s'assurer que l'utilisateur est autorisé.

    Returns:
        list[GETVesselRegionModel]: Une liste d'objets GETVesselRegionModel contenant les informations des 
                                    bateaux présents dans la région spécifiée.

    Raises:
        HTTPException: Si aucun bateau n'est trouvé dans la région, retourne un code 404 avec le message 
                       "No vessels found in the specified region". 
                       En cas d'autre erreur, retourne un code 500 avec le message d'erreur correspondant.
"""
# Endpoint pour récupérer tous les bateaux par région
@router.get("/expert/{region}", response_model=list[GETVesselRegionModel])
def get_vessels_region(region: str, current_user: dict = Depends(get_current_user)):

    if current_user['Role'] != 'Expert':
            raise HTTPException(status_code=403, detail="You are not allowed to access this resource")
    try:
        query = """
              SELECT
                v.MMSI, v.IMO, v.CallSign, vt.IDVesselType AS VesselType, v.VesselName, 
                v.Length, v.Width, v.Draft, v.Cargo, c.NameCountry,  
                v.TransceiverClass, comp.NameCompany, 
                p.BaseDateTime, p.LAT, p.LON, p.SOG, p.COG, p.Heading, 
                ns.Status, p.Region
            FROM Vessel v
            LEFT JOIN VesselType vt ON v.IDVesselType = vt.IDVesselType 
            LEFT JOIN Country c ON v.IDCountry = c.IDCountry
            LEFT JOIN Company comp ON v.IDCompany = comp.IDCompany
            LEFT JOIN Position p ON v.MMSI = p.MMSI
            LEFT JOIN NavigationStatus ns ON p.Status = ns.Status
            WHERE TRIM(LOWER(p.Region)) = TRIM(LOWER(%s));
        """
        results = db.DQL(query, (region,))

        if not results:
            raise HTTPException(status_code=404, detail="No vessels found in the specified region")
        
        return [GETVesselRegionModel(**vessel) for vessel in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching vessels by region: {str(e)}")
# Endpoint pour récupérer tous les bateaux par type
@router.get("/expert/{vessel_type}", response_model=list[GETVesselModel])
def get_vessels_by_type(vessel_type: int, current_user: dict = Depends(get_current_user)):
    
    if current_user['Role'] != 'Expert':
        raise HTTPException(status_code=403, detail="You are not allowed to access this resource")
    
    try:
        query = """
            SELECT
                v.MMSI, v.IMO, v.CallSign, vt.IDVesselType AS VesselType, vt.Description AS VesselDescription, v.VesselName, 
                v.Length, v.Width, v.Draft, v.Cargo, c.NameCountry,  
                v.TransceiverClass, comp.NameCompany, 
                p.BaseDateTime, p.LAT, p.LON, p.SOG, p.COG, p.Heading, 
                ns.Status, p.Region
            FROM Vessel v
            LEFT JOIN VesselType vt ON v.IDVesselType = vt.IDVesselType 
            LEFT JOIN Country c ON v.IDCountry = c.IDCountry
            LEFT JOIN Company comp ON v.IDCompany = comp.IDCompany
            LEFT JOIN Position p ON v.MMSI = p.MMSI
            LEFT JOIN NavigationStatus ns ON p.Status = ns.Status
            WHERE vt.IDVesselType = %s;
        """
        results = db.DQL(query, (vessel_type,))

        if not results:
            raise HTTPException(status_code=404, detail="No vessels found for the specified type")
        
        vessels = []
        for vessel in results:
            # Default status in case there is no status in the data
            status = vessel["Status"] if vessel["Status"] is not None else 15

            # Create the position data
            position_data = {
                "MMSI": vessel["MMSI"],
                "BaseDateTime": vessel["BaseDateTime"],
                "LAT": vessel["LAT"],
                "LON": vessel["LON"],
                "SOG": vessel["SOG"],
                "COG": vessel["COG"],
                "Heading": vessel["Heading"],
                "Status": status,
                "Region": vessel["Region"]
            }

            # Vessel data includes VesselType and VesselDescription
            vessel_data = {k: vessel[k] for k in [
                "MMSI", "IMO", "CallSign", "VesselType", "VesselDescription", "VesselName", "Length", 
                "Width", "Draft", "Cargo", "NameCountry", "TransceiverClass", "NameCompany"
            ]}
            
            # Adding position data to vessel data
            vessel_data["Position"] = GETPositionModel(**position_data)

            # Add the vessel to the list of vessels
            vessels.append(GETVesselModel(**vessel_data))

        return vessels

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching vessels by type: {str(e)}")

@router.get("/expert/{region}/{vessel_type}", response_model=list[GETVesselModel])
def get_vessels_by_region_and_type(region: str, vessel_type: int, current_user: dict = Depends(get_current_user)):

    if current_user['Role'] != 'Expert':
        raise HTTPException(status_code=403, detail="You are not allowed to access this resource")
    
    try:
        query = """
            SELECT
                v.MMSI, v.IMO, v.CallSign, vt.IDVesselType AS VesselType, vt.Description AS VesselDescription, v.VesselName, 
                v.Length, v.Width, v.Draft, v.Cargo, c.NameCountry,  
                v.TransceiverClass, comp.NameCompany, 
                p.BaseDateTime, p.LAT, p.LON, p.SOG, p.COG, p.Heading, 
                ns.Status, p.Region
            FROM Vessel v
            LEFT JOIN VesselType vt ON v.IDVesselType = vt.IDVesselType 
            LEFT JOIN Country c ON v.IDCountry = c.IDCountry
            LEFT JOIN Company comp ON v.IDCompany = comp.IDCompany
            LEFT JOIN Position p ON v.MMSI = p.MMSI
            LEFT JOIN NavigationStatus ns ON p.Status = ns.Status
            WHERE TRIM(LOWER(p.Region)) = TRIM(LOWER(%s)) AND vt.IDVesselType = %s;
        """
        results = db.DQL(query, (region, vessel_type))

        if not results:
            raise HTTPException(status_code=404, detail="No vessels found for the specified region and vessel type")
        
        vessels = []
        for vessel in results:
            # Default status in case there is no status in the data
            status = vessel["Status"] if vessel["Status"] is not None else 15

            # Create the position data
            position_data = {
                "MMSI": vessel["MMSI"],
                "BaseDateTime": vessel["BaseDateTime"],
                "LAT": vessel["LAT"],
                "LON": vessel["LON"],
                "SOG": vessel["SOG"],
                "COG": vessel["COG"],
                "Heading": vessel["Heading"],
                "Status": status,
                "Region": vessel["Region"]
            }

            # Vessel data includes VesselType and VesselDescription
            vessel_data = {k: vessel[k] for k in [
                "MMSI", "IMO", "CallSign", "VesselType", "VesselDescription", "VesselName", "Length", 
                "Width", "Draft", "Cargo", "NameCountry", "TransceiverClass", "NameCompany"
            ]}
            
            # Adding position data to vessel data
            vessel_data["Position"] = GETPositionModel(**position_data)

            # Add the vessel to the list of vessels
            vessels.append(GETVesselModel(**vessel_data))

        return vessels

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching vessels by region and type: {str(e)}")
