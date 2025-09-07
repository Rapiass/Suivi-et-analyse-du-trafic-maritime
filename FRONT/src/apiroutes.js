const BASE_URL = "http://172.31.60.24:8000"; // à modifier si nécessaire
//const BASE_URL = "http://localhost:8000";
//Route à adapter au besoin :
const apiRoutes = {
  //Connexion et Inscription
  login: `${BASE_URL}/login`,
  register: `${BASE_URL}/register`,
  //Shipowner
  vesselsShipOwner: `${BASE_URL}/armateur/vessels`,
  addMmsiShipOwner: (mmsi) => `${BASE_URL}/armateur/addmmsi/${mmsi}`,
  delMmsi: (mmsi) => `${BASE_URL}/armateur/delmmsi/${mmsi}`,
  //Captain
  captainNeighborsVessels: (lat, lon) =>`${BASE_URL}/captain/voisins/${lat}/${lon}`,
  captainVessel: `${BASE_URL}/captain/vessels/position_bateau`,
  addMmsiCaptain: (mmsi) => `${BASE_URL}/captain/addmmsi/${mmsi}`,
  //Expert
  getVesselsExpert: `${BASE_URL}/expert`,
  //Weather
  getWeather: (lat, lon) => `${BASE_URL}/meteo/${lat}/${lon}`,
  getPremiumWeather: (lat, lon) => `${BASE_URL}/meteo-premium/${lat}/${lon}`,
  //Admin
  getUsers: `${BASE_URL}/users`,
  addUser: `${BASE_URL}/users`,
  editUser: (userId) => `${BASE_URL}/users/${userId}`,
  deleteUser: (userId) => `${BASE_URL}/users/${userId}`,
  downloadFile: (filename) => `${BASE_URL}/files/${filename}`,
};
export default apiRoutes;
//Si l'on continue de créer beaucoup de route, merci de décomposer ce fichier en plusieurs sous fichier pour simplifier la lecture
