import React from "react";
import { useNavigate } from "react-router-dom";
import logo from "../Resources/images/merry.png";

function Header() {
  const navigate = useNavigate();

  // Fonction de déconnexion
  const handleLogout = () => {
    localStorage.removeItem("role"); // Effacer les données stockées
    localStorage.removeItem("token");
    sessionStorage.clear(); // Nettoyer la session
    navigate("/login"); // Retour à l'accueil
  };

  return (
    <header className="header">
      <img src={logo} alt="Logo" className="logo" />
      <button className="btn-back" onClick={handleLogout}>
        🚪 Se Déconnecter
      </button>
    </header>
  );
}

export default Header;
