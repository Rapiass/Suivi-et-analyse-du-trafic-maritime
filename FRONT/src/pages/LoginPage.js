import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import logo from "../Resources/images/merry.png";
import Footer from "../components/Footer.js";
import apiRoutes from "../apiroutes.js";

function LoginPage({ setRole }) {
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const response = await axios.post(apiRoutes.login, {
        Login: login,
        Password: password,
      });

      const { access_token, Role } = response.data;
      localStorage.setItem("token", access_token);
      console.log("role login :",Role)
      setRole(Role); // ✅ Met à jour l'état du front avec le rôle
      // Redirige en fonction du rôle
      if (Role === "Admin") {
        navigate("/admin");
      } else {
        navigate("/dashboard");
      }
    } catch (error) {
      console.error("Erreur lors de la connexion :", error);
      setError("Échec de la connexion. Vérifiez vos identifiants.");
    }
  };

  return (
    <div className="container">
      <header className="header">
        <img src={logo} alt="Logo" className="logo" />
      </header>
      <h2>Connexion</h2>
      <form onSubmit={handleLogin} className="form-container">
        <input
          type="text"
          placeholder="Login"
          value={login}
          onChange={(e) => setLogin(e.target.value)}
          className="input-field"
          required
        />

        <input
          type="password"
          placeholder="Mot de passe"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="input-field"
          required
        />

        <button type="submit" className="btn-primary">
          Se connecter
        </button>
        {error && <p className="error">{error}</p>}
        <p>
          Pas encore de compte ?{" "}
          <a
            href="#"
            onClick={(e) => {
              e.preventDefault();
              navigate("/signup");
            }}
          >
            Inscris-toi ici
          </a>
        </p>
      </form>

      <Footer />
    </div>
  );
}

export default LoginPage;
