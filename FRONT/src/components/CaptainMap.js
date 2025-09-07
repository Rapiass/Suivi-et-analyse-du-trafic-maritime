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
import neighborIconImg from "../Resources/images/sunny.png";
import WeatherInfo from "./WeatherInfo";
import apiRoutes from "../apiroutes.js";

// Icône pour le bateau du capitaine
const customIcon = L.icon({
  iconUrl: pin,
  iconSize: [50, 50],
  iconAnchor: [10, 20],
  popupAnchor: [0, -10],
});

// Icône pour les voisins
const neighborIcon = L.icon({
  iconUrl: neighborIconImg,
  iconSize: [50, 50],
  iconAnchor: [10, 20],
  popupAnchor: [0, -10],
});

const CaptainMap = ({ refreshKey }) => {
  const [vessels, setVessels] = useState([]);
  const [neighbors, setNeighbors] = useState([]);
  const [coords, setCoords] = useState({ lat: null, lon: null });
  const [loading, setLoading] = useState(false);
  const [error, setErrorMsg] = useState("");

  const MapClickHandler = () => {
    useMapEvents({
      click: (e) => {
        setCoords({ lat: e.latlng.lat, lon: e.latlng.lng });
      },
    });
    return null;
  };

  useEffect(() => {
    fetchCaptainVessels();
  }, [refreshKey]);

  const fetchCaptainVessels = async () => {
    try {
      const token = localStorage.getItem("token");
      const response = await axios.get(apiRoutes.captainVessel, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setVessels(response.data);
    } catch (error) {
      console.error(error);
      if (error.response) {
        const detail = error.response.data?.detail;
        if (typeof detail === "object" && detail.message) {
          setErrorMsg(detail.message);
        } else {
          setErrorMsg(detail || "Erreur inconnue du serveur");
        }
      } else {
        setErrorMsg("Erreur de communication avec le serveur");
      }
    }
  };

  const fetchNeighbors = async () => {
    try {
      const token = localStorage.getItem("token");

      // On prend les coordonnées du premier bateau (celui du capitaine)
      const lat = vessels[0]?.LAT;
      const lon = vessels[0]?.LON;

      if (lat == null || lon == null) {
        console.warn("Pas de coordonnées pour le bateau du capitaine.");
        return;
      }
      const response = await axios.get(apiRoutes.captainNeighborsVessels(lat,lon), {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setNeighbors(response.data);
    } catch (error) {
      console.error("Erreur lors de la récupération des voisins :", error);
    }
  };

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

        {/* Bateau du capitaine */}
        {vessels
          .filter((vessel) => vessel.LAT != null && vessel.LON != null)
          .map((vessel) => (
            <Marker
              key={vessel.MMSI}
              position={[vessel.LAT, vessel.LON]}
              icon={customIcon}
            >
              <Popup>
                <h3>🚢 {vessel.VesselName || "Nom inconnu"}</h3>
                <p>
                  <strong>MMSI:</strong> {vessel.MMSI}
                </p>
                <p>
                  <strong>Latitude:</strong> {vessel.LAT.toFixed(4)}
                </p>
                <p>
                  <strong>Longitude:</strong> {vessel.LON.toFixed(4)}
                </p>
                <button onClick={fetchNeighbors}>Voir les voisins</button>
              </Popup>
            </Marker>
          ))}

        {/* Voisins */}
        {neighbors
          .filter((vessel) => vessel.LAT != null && vessel.LON != null)
          .map((vessel) => (
            <Marker
              key={`neighbor-${vessel.MMSI}`}
              position={[vessel.LAT, vessel.LON]}
              icon={neighborIcon}
            >
              <Popup>
                <h3>🧭 Voisin : {vessel.VesselName || "Nom inconnu"}</h3>
                <p>
                  <strong>MMSI:</strong> {vessel.MMSI}
                </p>
                <p>
                  <strong>Latitude:</strong> {vessel.LAT.toFixed(4)}
                </p>
                <p>
                  <strong>Longitude:</strong> {vessel.LON.toFixed(4)}
                </p>
              </Popup>
            </Marker>
          ))}

        <ScaleControl position="bottomleft" />
        <MapClickHandler />
      </MapContainer>

      {coords.lat && coords.lon && (
        <WeatherInfo lat={coords.lat} lon={coords.lon} />
      )}

      {error && (
        <div className="error">
          <span className="error-icon">⚠️</span>
          {error}
        </div>
      )}
    </div>
  );
};

export default CaptainMap;
