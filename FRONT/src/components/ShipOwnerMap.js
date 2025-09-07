import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import pin from "../Resources/images/merry.png";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  ScaleControl,
} from "react-leaflet";
import apiRoutes from "../apiroutes.js";

const ShipownerMap = ({ refreshKey }) => {
  const [vessels, setVessels] = useState([]);
  const [searchMMSI, setSearchMMSI] = useState(""); // État du MMSI pour filtrage
  const [selectedVessels, setSelectedVessels] = useState([]); // Bateaux sélectionnés
  const navigate = useNavigate();
  const customIcon = L.icon({
    iconUrl: pin,
    iconSize: [20, 20],
    iconAnchor: [10, 20],
    popupAnchor: [0, -10],
  });

  useEffect(() => {
    const fetchVessels = async () => {
      const token = localStorage.getItem("token");

      try {
        const response = await axios.get(apiRoutes.vesselsShipOwner, {
          headers: { Authorization: `Bearer ${token}` },
        });

        const fetchedVessels = response.data;
        setVessels(fetchedVessels);
        setSelectedVessels(fetchedVessels.map((v) => v.MMSI)); //Tous sélectionnés par défaut
      } catch (error) {
        console.error("Erreur lors de la récupération des bateaux :", error);
      }
    };
    fetchVessels();
  }, [refreshKey]);

  // Filtrage des navires par MMSI
  const filteredVessels = vessels.filter((vessel) =>
    vessel.MMSI.toLowerCase().includes(searchMMSI.toLowerCase())
  );

  // Mise à jour du filtre MMSI
  const handleFilterChange = (filters) => {
    setSearchMMSI(filters.mmsi); // Met à jour l'état de recherche MMSI
  };

  // Gestion des sélections de bateaux
  const handleSelectionChange = (mmsi) => {
    setSelectedVessels((prevSelected) =>
      prevSelected.includes(mmsi)
        ? prevSelected.filter((item) => item !== mmsi)
        : [...prevSelected, mmsi]
    );
  };

  // Bateaux à afficher selon les sélections
  const vesselsToDisplay = filteredVessels.filter((vessel) =>
    selectedVessels.includes(vessel.MMSI)
  );

  return (
    <>
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
          <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

          {/* Affichage des marqueurs des bateaux sélectionnés */}
          {vesselsToDisplay
            .filter((vessel) => vessel.LAT != null && vessel.LON != null)
            .map((vessel) => (
              <Marker
                key={vessel.MMSI}
                position={[vessel.LAT, vessel.LON]}
                icon={customIcon}
              >
                <Popup>
                  <strong>{vessel.VesselName}</strong>
                  <br />
                  MMSI: {vessel.MMSI}
                  <br />
                  IMO: {vessel.IMO}
                  <br />
                  Pays: {vessel.NameCountry}
                </Popup>
              </Marker>
            ))}
          <ScaleControl position="bottomleft" />
        </MapContainer>

        {/* Tableau des bateaux */}
        <div className="vessel-list">
          <h3>Liste des Bateaux</h3>
          <table>
            <thead>
              <tr>
                <th>Selectionner</th>
                <th>Nom du Bateau</th>
                <th>MMSI</th>
                <th>Pays</th>
                <th>Région</th>
              </tr>
            </thead>
            <tbody>
              {filteredVessels.map((vessel) => (
                <tr key={vessel.MMSI}>
                  <td>
                    <input
                      type="checkbox"
                      checked={selectedVessels.includes(vessel.MMSI)}
                      onChange={() => handleSelectionChange(vessel.MMSI)}
                    />
                  </td>
                  <td>{vessel.VesselName}</td>
                  <td>{vessel.MMSI}</td>
                  <td>{vessel.NameCountry}</td>
                  <td>{vessel.Region}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
};

export default ShipownerMap;
