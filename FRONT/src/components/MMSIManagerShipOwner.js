// src/components/MMSIManagerShipOwner.js
import React, { useState } from "react";
import axios from "axios";
import apiRoutes from "../apiroutes.js";

function MMSIManagerShipOwner({ onMmsiChange }) {
  const [showPopup, setShowPopup] = useState(false);
  const [mmsi, setMmsi] = useState("");
  const [action, setAction] = useState(null); // "add" ou "delete"
  const [errorMsg, setErrorMsg] = useState("");

  const handleSubmit = async () => {
    const url =
      action === "add"
        ? apiRoutes.addMmsiShipOwner(mmsi)
        : apiRoutes.delMmsi(mmsi);

    try {
      const response =
        action === "add"
          ? await axios.post(
              url,
              {},
              {
                headers: {
                  Authorization: `Bearer ${localStorage.getItem("token")}`,
                },
              }
            )
          : await axios.delete(url, {
              headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`,
              },
            });

      if (response.status === 200) {
        setMmsi("");
        setShowPopup(false);
        setErrorMsg("");
        onMmsiChange(); // Rafraîchir les données
      } else {
        alert("Erreur lors du traitement du MMSI.");
      }
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

  const openPopup = (type) => {
    setAction(type); // "add" ou "delete"
    setShowPopup(true);
    setErrorMsg("");
  };

  return (
    <div className="mmsi-manager">
      <button className="MCButtonAdd" onClick={() => openPopup("add")}>
        ➕ Ajouter un MMSI
      </button>
      <button className="MCButtonAdd" onClick={() => openPopup("delete")}>
        🗑️ Supprimer un MMSI
      </button>

      {showPopup && (
        <div className="popup-overlay">
          <div className="popup-content">
            <h3>{action === "add" ? "Ajouter" : "Supprimer"} un MMSI</h3>
            <input
              type="text"
              value={mmsi}
              onChange={(e) => setMmsi(e.target.value)}
              placeholder="Ex: 987654321"
            />
            <div className="popup-buttons">
              <button className="MCButton" onClick={handleSubmit}>
                {action === "add" ? "Ajouter" : "Supprimer"}
              </button>
              <button className="MCButton" onClick={() => setShowPopup(false)}>
                Annuler
              </button>
            </div>
            {errorMsg && <p className="error-message">{errorMsg}</p>}
          </div>
        </div>
      )}
    </div>
  );
}

export default MMSIManagerShipOwner;
