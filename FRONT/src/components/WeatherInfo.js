// src/components/WeatherInfo.js
import React, { useState, useEffect } from "react";
import axios from "axios";
import apiRoutes from "../apiroutes.js"; // Importer les routes API

const WeatherInfo = ({ lat, lon }) => {
  const [weatherData, setWeatherData] = useState(null);
  const [premiumData, setPremiumData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [premiumLoading, setPremiumLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    setWeatherData(null);
    setPremiumData(null);
    setError("");
  }, [lat, lon]);

  const fetchWeather = async () => {
    if (!lat || !lon) return;
    setLoading(true);
    setError("");

    try {
      const response = await axios.get(apiRoutes.getWeather(lat, lon)); // Utiliser la route centralisée pour la météo
      setWeatherData(response.data);
    } catch (err) {
      console.error("Erreur météo simple :", err);
      setError("Impossible de récupérer la météo.");
    }
    setLoading(false);
  };

  const fetchPremiumWeather = async () => {
    if (!lat || !lon) return;
    setPremiumLoading(true);
    setError("");

    try {
      const response = await axios.get(apiRoutes.getPremiumWeather(lat, lon)); // Utiliser la route centralisée pour la météo premium
      setPremiumData(response.data);
    } catch (err) {
      console.error("Erreur météo premium :", err);
      setError("Impossible de récupérer la météo premium.");
    }
    setPremiumLoading(false);
  };

  return (
    <div className="weather-container">
      <h3>Coordonnées sélectionnées</h3>
      <p>
        <strong>Latitude :</strong> {lat}
      </p>
      <p>
        <strong>Longitude :</strong> {lon}
      </p>

      <button onClick={fetchWeather} disabled={loading}>
        {loading ? "Chargement..." : "Voir la météo"}
      </button>

      <button
        onClick={fetchPremiumWeather}
        disabled={premiumLoading}
        style={{ marginLeft: "10px", backgroundColor: "#ffd700" }}
      >
        {premiumLoading ? "Chargement premium..." : "Voir la météo Premium"}
      </button>

      {error && <p className="error">{error}</p>}

      {weatherData && (
        <div className="weather-info">
          <h3>Météo actuelle</h3>
          <p>
            <strong>Heure :</strong> {weatherData.time}
          </p>
          <p>
            <strong>Température :</strong> {weatherData.temperature} °C
          </p>
          <p>
            <strong>Pluie :</strong> {weatherData.rain} mm
          </p>
          <p>
            <strong>Couverture nuageuse :</strong> {weatherData.cloud_cover} %
          </p>
          <p>
            <strong>Direction du vent :</strong> {weatherData.wind_direction} °
          </p>
          <p>
            <strong>Vitesse du vent :</strong> {weatherData.wind_speed} km/h
          </p>
        </div>
      )}

      {premiumData && (
        <div className="weather-info premium">
          <h3>🌟 Météo Premium</h3>
          <p>
            <strong>Heure (Paris) :</strong>{" "}
            {new Date(premiumData.time).toLocaleString("fr-FR", {
              timeZone: "Europe/Paris",
            })}
          </p>

          <p>
            <strong>Température :</strong> {premiumData.airTemperature} °C
          </p>
          <p>
            <strong>Pression :</strong> {premiumData.pressure} hPa
          </p>
          <p>
            <strong>Humidité :</strong> {premiumData.humidity} %
          </p>
          <p>
            <strong>Couverture nuageuse :</strong> {premiumData.cloudCover} %
          </p>
          <p>
            <strong>Précipitations :</strong> {premiumData.precipitation} mm
          </p>
          <p>
            <strong>Visibilité :</strong> {premiumData.visibility} m
          </p>
          <p>
            <strong>Vitesse du vent :</strong> {premiumData.windSpeed} km/h
          </p>
          <p>
            <strong>Direction du vent :</strong> {premiumData.windDirection} °
          </p>
          <p>
            <strong>Hauteur des vagues :</strong> {premiumData.waveHeight} m
          </p>
          <p>
            <strong>Direction des vagues :</strong> {premiumData.waveDirection}{" "}
            °
          </p>
        </div>
      )}
    </div>
  );
};

export default WeatherInfo;
