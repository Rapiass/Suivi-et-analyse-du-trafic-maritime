import React, { useEffect, useState } from "react";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  ScaleControl,
  useMapEvents,
} from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import axios from "axios";
import pin from "../Resources/images/merry.png";
import Filters from "./Filters";
import WeatherInfo from "./WeatherInfo";
import apiRoutes from "../apiroutes.js";

// Définition de l'icône personnalisée pour les marqueurs
const customIcon = L.icon({
  iconUrl: pin,
  iconSize: [20, 20],
  iconAnchor: [10, 20],
  popupAnchor: [0, -10],
});

const ExpertMap = () => {
  const [vessels, setVessels] = useState([]);
  const [filters, setFilters] = useState({ vesselType: "", region: "" });
  const [availableTypes, setAvailableTypes] = useState([]);
  const [availableRegions, setAvailableRegions] = useState([]);
  const [coords, setCoords] = useState({ lat: null, lon: null });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const MapClickHandler = () => {
    useMapEvents({
      click: (e) => {
        setCoords({ lat: e.latlng.lat, lon: e.latlng.lng });
      },
    });
    return null;
  };

  // Récupérer les données des bateaux et générer dynamiquement les filtres
  useEffect(() => {
    fetchVessels(filters);
  }, [filters]);

  async function fetchVessels(filters) {
    setLoading(true);
    setError("");
    try {
      const token = localStorage.getItem("token"); // Récupérer le token stocké

      // Filtrer les paramètres pour ne pas envoyer les valeurs vides
      const filteredFilters = {};
      if (filters.vesselType) filteredFilters.vesselType = filters.vesselType; // Envoyer l'ID du type, pas la description
      if (filters.region) filteredFilters.region = filters.region;

      const response = await axios.get(apiRoutes.getVesselsExpert, {
        headers: { Authorization: `Bearer ${token}` },
        params: filteredFilters,
      });

      setVessels(response.data);

      // Générer dynamiquement les filtres avec ID et description
      const types = response.data.map((vessel) => ({
        id: vessel.VesselType, // L'ID du type de navire
        description: vessel.VesselDescription, // La description à afficher
      }));
      const regions = new Set(
        response.data.map((vessel) => vessel.Position.Region)
      );

      setAvailableTypes(types);
      setAvailableRegions([...regions]);
    } catch (error) {
      console.error("Erreur lors de la récupération des bateaux :", error);
      setError("Impossible de récupérer les données des navires.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="divMap">
      <MapContainer
        className="map"
        center={[0, 0]}
        zoom={2}
        minZoom={1}
        maxBounds={[
          [-85, -180],
          [85, 180],
        ]}
        maxBoundsViscosity={1.0}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />
        {vessels.map((vessel) => (
          <Marker
            key={vessel.MMSI}
            position={[vessel.Position.LAT, vessel.Position.LON]}
            icon={customIcon}
          >
            <Popup>
              <div>
                <h3>{vessel.VesselName}</h3>
                <p>MMSI: {vessel.MMSI}</p>
                <p>Status: {vessel.Position.Status}</p>
                <p>Company: {vessel.NameCompany}</p>
              </div>
            </Popup>
          </Marker>
        ))}

        <ScaleControl position="bottomleft" />
        <MapClickHandler />
      </MapContainer>

      {/* Composant pour les filtres avec options dynamiques */}
      <Filters
        onFilterChange={setFilters}
        availableTypes={availableTypes}
        availableRegions={availableRegions}
      />
      {coords.lat && coords.lon && (
        <WeatherInfo lat={coords.lat} lon={coords.lon} />
      )}
      {/* Affichage d'un message d'erreur si quelque chose se passe mal */}
      {error && (
        <div className="error">
          <span className="error-icon">⚠️</span>
          {error}
        </div>
      )}
    </div>
  );
};

export default ExpertMap;
