import React, { useState } from "react";
import CaptainMap from "../components/CaptainMap.js";
import ExpertMap from "../components/ExpertMap.js";
import ShipOwnerMap from "../components/ShipOwnerMap";
import CustomMap from "../components/CustomMap.js";
import { useNavigate } from "react-router-dom";
import "../styles/map.css";
import MMSIManagerCap from "../components/MMSIManagerCap.js";
import MMSIManagerShipOwner from "../components/MMSIManagerShipOwner.js";
import Header from "../components/Header";
import Footer from "../components/Footer.js";

function RoleBasedMap({ role }) {
  const navigate = useNavigate();
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [refreshKey, setRefreshKey] = useState(0);
  const handleRefresh = () => {
    setRefreshKey((prev) => prev + 1); // ou prev + 1
  };
  return (
    <div className="container">
      <Header />
      <div className="map-role-info">
        <div className={`map-role-badge ${role}`}>
          {role === "Capitaine" && "🛳️ Mode Capitaine"}
          {role === "Expert" && "📊 Mode Expert"}
          {role === "Armateur" && "🚢 Mode Armateur"}
          {!role && "⚠️ Aucun rôle valide"}
        </div>
      </div>

      <div className="map-container">
        {role === "Capitaine" ? (
          <CaptainMap refreshKey={refreshKey} />
        ) : role === "Expert" ? (
          <ExpertMap />
        ) : role === "Armateur" ? (
          <ShipOwnerMap refreshKey={refreshKey} />
        ) : (
          <p className="error">
            Veuillez vérifier vos identifiants ou contacter l’administrateur.
          </p>
        )}
      </div>
      <>
        {role === "Capitaine" ? (
          <MMSIManagerCap onMmsiAdded={handleRefresh} />
        ) : role === "Armateur" ? (
          <MMSIManagerShipOwner onMmsiChange={handleRefresh} />
        ) : null}
      </>
      <Footer />
    </div>
  );
}
export default RoleBasedMap;
