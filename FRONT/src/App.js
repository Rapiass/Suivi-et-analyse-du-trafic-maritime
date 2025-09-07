import React, { useState, useEffect } from "react";
import Navigation from "./Navigation.js";
import "./styles/styles.css";

function App() {
  const [role, setRole] = useState(localStorage.getItem("role") || "");

  useEffect(() => {
    localStorage.setItem("role", role);
  }, [role]); //Sauvegarde à chaque changement

  return <Navigation role={role} setRole={setRole} />;
}

export default App;
