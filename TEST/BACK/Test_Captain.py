import pytest
from fastapi.testclient import TestClient
from main import app  # Importez votre application FastAPI
from unittest.mock import MagicMock
from DB.Database import db
from BACK.Routes.JWT_Manage import create_access_token

# Configurez le client de test
client = TestClient(app)

# Fixture qui simule la récupération des capitaines depuis la base de données
@pytest.fixture
def mock_captains_data(monkeypatch):
    mock_data = [
        {"IDUser": 1, "Name": "Smith", "Firstname": "John", "Login": "jsmith"},
        {"IDUser": 2, "Name": "Doe", "Firstname": "Jane", "Login": "jdoe"},
    ]

    # Simuler la fonction db.DQL pour qu'elle retourne mock_data
    def mock_dql(query, params=None):
        return mock_data

    # Remplacer la fonction db.DQL avec la version mockée
    monkeypatch.setattr(db, "DQL", mock_dql)
    return mock_data  # Retourner les données mockées pour qu'elles so

def test_get_captains_success(mock_captains_data):
    # Effectuer une requête GET à l'endpoint "/captain"
    response = client.get("/captain")
    
    # Vérifier que le statut HTTP est 200
    assert response.status_code == 200

    # Vérifier que la réponse JSON correspond aux données simulées dans la fixture
    assert response.json() == mock_captains_data
# test_get_captains_not_found
def test_get_captains_not_found(monkeypatch):
    def mock_dql(query, params=None):
        return []  # Pas de données
    
    monkeypatch.setattr(db, "DQL", mock_dql)
    
    response = client.get("/captain")
    assert response.status_code == 404

# test_get_captain_not_found
def test_get_captain_not_found(monkeypatch):
    def mock_dql(query, params):
        return []
    
    monkeypatch.setattr(db, "DQL", mock_dql)
    
    response = client.get("/captain/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "No captain found with the provided ID"}

def test_get_captain_success(monkeypatch):
    # Données simulées
    mock_data = [{"IDUser": 1, "Name": "Smith", "Firstname": "John", "Login": "jsmith"}]

    def mock_dql(query, params):
        assert params == (1,)
        return mock_data

    monkeypatch.setattr(db, "DQL", mock_dql)

    response = client.get("/captain/1")
    assert response.status_code == 200
    assert response.json() == mock_data[0]

    
def test_get_vessels_position_success(monkeypatch):
    mock_data = [
        {
            "MMSI": "123456789",
            "VesselName": "Oceanic",
            "BaseDateTime": "2024-12-04T15:30:00",
            "LAT": 12.34,
            "LON": 56.78,
            "SOG": 20.5,
            "COG": 180.0,
            "Heading": 180.0,
            "Status": 15,
            "Region": "Atlantic",
            "IMO": "IMO1234567",
            "CallSign": "CALLSIGN",
            "VesselType": 2,
            "Length": 300.5,
            "Width": 50.0,
            "Draft": 12.0,
            "Cargo": "Container",
            "IDCountry": "US",
            "TransceiverClass": "A",
            "IDCompany": 123
        }
    ]
    
    def mock_dql(query, params):
        return mock_data  # Simule la réponse de la base de données
    
    monkeypatch.setattr(db, "DQL", mock_dql)

    def mock_get_current_user():
        return {"IDUser": 1}  # Simule un utilisateur connecté avec un rôle "User"
    
    monkeypatch.setattr("BACK.Routes.JWT_Manage.get_current_user", mock_get_current_user)

    # Simulez l'ajout d'un token valide
    token = create_access_token({"UserId": 1})  # Crée un token pour l'utilisateur avec ID 1
    headers = {"Authorization": f"Bearer {token}"}  # Ajoute le token dans les headers

    response = client.get("/captain/1/position_bateau", headers=headers)  # Effectue la requête GET
    assert response.status_code == 200  # Vérifie que la réponse a un code 200 (OK)
    assert response.json() == mock_data  # Vérifie que les données retournées sont celles simulées

# test_get_vessels_position_not_found
def test_get_vessels_position_not_found(monkeypatch):
    def mock_dql(query, params):
        return []
    
    monkeypatch.setattr(db, "DQL", mock_dql)
    
    def mock_get_current_user():
        return {"IDUser": 1, "Role": "Admin"}
    
    monkeypatch.setattr("BACK.Routes.JWT_Manage.get_current_user", mock_get_current_user)
    
    response = client.get("/captain/999/position_bateau")
    assert response.status_code == 404
    
