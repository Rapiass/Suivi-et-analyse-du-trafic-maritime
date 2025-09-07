import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import logo from "../Resources/images/merry.png";
import Footer from "../components/Footer.js";
import axios from "axios";
import apiRoutes from "../apiroutes.js";
function Signup() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    login: "",
    password: "",
    role: 1, // Valeur par défaut
  });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    if (!formData.login || !formData.password) {
      setError("Le nom et le mot de passe sont requis.");
      return;
    }
    try {
      await axios.post(
        apiRoutes.register,
        {
          Login: formData.login,
          Password: formData.password,
          IDRole: parseInt(formData.role),
        },
        {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        }
      );
      setSuccess("Inscription réussie ! Redirection en cours ...");
      setFormData({ login: "", password: "", role: 1 });
      setError("");
      navigate("/");
    } catch (err) {
      setError("Erreur lors de l'ajout de l'utilisateur.");
    }
  };

  return (
    <div className="container">
      <header className="header">
        <img src={logo} alt="Logo" className="logo" />
      </header>
      <h2>Inscription</h2>
      {error && <p className="error">{error}</p>}
      {success && <p className="success">{success}</p>}
      <form className="form-container" onSubmit={handleSubmit}>
        <input
          type="text"
          name="login"
          placeholder="Login"
          value={formData.login}
          onChange={handleChange}
          className="input-field"
          required
        />

        <input
          type="password"
          name="password"
          placeholder="Mot de passe"
          value={formData.password}
          onChange={handleChange}
          className="input-field"
          required
        />

        <select
          name="role"
          value={formData.role}
          onChange={handleChange}
          className="input-field"
          required
        >
          <option value="1">Capitaine</option>
          <option value="2">Armateur</option>
          <option value="3">Expert</option>
        </select>

        <button className="btn-primary" type="submit">
          S'inscrire
        </button>
        <p>
          Déjà un compte ?{" "}
          <a
            href="#"
            onClick={(e) => {
              e.preventDefault();
              navigate("/");
            }}
          >
            Connecte-toi ici
          </a>
        </p>
      </form>

      <Footer />
    </div>
  );
}

export default Signup;
