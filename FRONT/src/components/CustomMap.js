import React, { useState, useEffect } from "react";
import ReactDOM from "react-dom";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import pin from "../Resources/images/merry.png"; // Chemin vers ton fichier pin.png

// Configuration de l'icône personnalisée
const customIcon = L.icon({
  iconUrl: pin,
  iconSize: [20, 20], // Taille de l'icône
  iconAnchor: [10, 20], // Centre l'icône au point d'ancrage
  popupAnchor: [0, -10], // Positionne le popup au-dessus de l'icône
});

function CustomMap() {
  const [bateaux, setBateaux] = useState([]); // État pour stocker les données des bateaux

  // Charger les données JSON
  useEffect(() => {
    fetch("/bateaux.json") // Chemin vers le fichier JSON
      .then((response) => {
        if (!response.ok) {
          throw new Error("Erreur lors du chargement des données");
        }
        return response.json();
      })
      .then((data) => setBateaux(data))
      .catch((error) => console.error("Erreur:", error));
  }, []);

  return (
    <MapContainer
      center={[0, 0]}
      zoom={1}
      style={{ height: "600px", width: "100%" }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      {bateaux.map((bateau) => {
        return (
          <Marker
            key={bateau.id}
            position={[bateau.latitude, bateau.longitude]}
            icon={customIcon}
          >
            <Popup>
              <strong>{bateau.nom}</strong>
              <br />
              Statut : {bateau.status}
            </Popup>
          </Marker>
        );
      })}
    </MapContainer>
  );
}

const rootElement = document.getElementById("root");
ReactDOM.render(<CustomMap />, rootElement);

export default CustomMap;
