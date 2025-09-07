import React from "react";
import ReactDOM from "react-dom/client"; // createRoot pour React 18
import App from "./App"; // Composant principal de l'application

// Crée le root et monte l'application
const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
