import React from "react";
import axios from "axios";
import apiRoutes from "../apiroutes.js";

const FileManagement = () => {
  const handleDownloadFile = async (filename) => {
    try {
      const response = await axios.get(apiRoutes.downloadFile(filename), {
        responseType: "blob",
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", filename); // Nom du fichier à télécharger
      document.body.appendChild(link);
      link.click();
    } catch (error) {
      console.error("Erreur lors du téléchargement du fichier:", error);
      alert("Une erreur est survenue lors du téléchargement.");
    }
  };

  return (
    <div className="file-management">
      <h2>Gestion des fichiers</h2>
      <div className="file-list">
        {/* Bouton de téléchargement*/}
        <button
          className="Downloadbutton"
          onClick={() => handleDownloadFile("examplefile.txt")}
        >
          Télécharger ExampleFile.txt
        </button>
      </div>
    </div>
  );
};

export default FileManagement;
