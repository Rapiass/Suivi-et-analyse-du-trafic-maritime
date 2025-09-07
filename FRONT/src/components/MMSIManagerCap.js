import React, { useState } from "react";
import axios from "axios";
import apiRoutes from "../apiroutes.js";

function MMSIManagerCap({ onMmsiAdded }) {
  const [showPopup, setShowPopup] = useState(false);
  const [mmsi, setMmsi] = useState("");
  const [errorMsg, setErrorMsg] = useState("");

  const handleSubmit = async () => {
    try {
      const response = await axios.post(
        apiRoutes.addMmsiCaptain(mmsi),
        {},
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );
      if (response.status === 200) {
        setMmsi("");
        setShowPopup(false);
        onMmsiAdded(); // ← comme handleApplyFilters !
      } else {
        alert("Erreur lors de l’ajout du MMSI.");
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

  return (
    <div className="mmsi-manager">
      <button className="MCButtonAdd" onClick={() => setShowPopup(true)}>
        🔧 Ajouter / Modifier MMSI
      </button>

      {showPopup && (
        <div className="popup-overlay">
          <div className="popup-content">
            <h3>Entrer le MMSI</h3>
            <input
              type="text"
              value={mmsi}
              onChange={(e) => setMmsi(e.target.value)}
              placeholder="Ex: 123456789"
            />
            <div className="popup-buttons">
              <button className="MCButton" onClick={handleSubmit}>
                Valider
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

export default MMSIManagerCap;
