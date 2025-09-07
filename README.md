# AIS Tracking System  
### Suivi et analyse du trafic maritime  

## Description  
**AIS** (_Automatic Identification System_) est un système permettant d’identifier les navires et leur position.  
Il est utilisé principalement pendant la navigation pour améliorer la sécurité en évitant les collisions.  

Les données produites peuvent également être utilisées en dehors de la navigation pour étudier les routes et les flux.  

Le projet global consiste à réaliser une application qui met en avant les possibilités offertes par l’exploitation des données issues du système **AIS**.  

**Profils utilisateurs :**  
- **Armateur** : accès aux données de son ou ses navires.  
- **Capitaine** : visualisation des navires autour de lui.  
- **Expert maritime** : étude des trajectoires par type de navire, période, etc.  
- **Administrateur** : gestion des utilisateurs et attribution des rôles.  

## Fonctionnalités principales  
- Authentification et gestion des rôles via token (**JWT**).  
- Interface cartographique dynamique avec **Leaflet**.  
- Vue personnalisée selon le type d’utilisateur.  
- Gestion des utilisateurs et rôles depuis un tableau de bord administrateur.  
- Récupération des données navires en temps réel depuis la base.  

---

## Technologies utilisées  

### Backend  
- **FastAPI** (framework Python rapide et moderne)  
- **SQLite** (base de données)  
- **SQLAlchemy** (ORM pour gérer la base)  
- **JWT** pour l’authentification sécurisée  

### Frontend  
- **React**  
- **Leaflet** pour l’affichage cartographique  

---

## Structure du projet
AIS-Tracking-System/

--- BACK/             
--- --- Routes/

--- --- Models/

--- --- ETL/

--- --- main.py           
--- --- models.py         
--- --- Database.py       

--- FRONT/            
--- --- src/

--- --- --- components/  

--- --- --- pages/      

--- --- --- apiroutes.js
--- --- --- App.js
--- --- package.json

--- README.md            


## Installation
### Backend
cd BACK  
pip install -r requirements.txt  
uvicorn main:app --reload  

### Frontend
cd FRONT  
npm install  
npm start  

## Authors
Projet réalisé dans le cadre d'un Master 1 BDIA - Université de Bourgogne

Alexandre ANSTETT  (1ere partie uniquement)
Garance BOURGOGNE  (1ere partie uniquement)
Lucas GIRAUD  (1ere partie uniquement)
Sebastien MOREL  
Antoine PARIGOT  (1ere partie uniquement)
Noel QAEZE  
Lestat ROBERTO DA GRACA  
Bastien SECULA  (1ere partie uniquement)
Théophile TEINTURIER  (1ere partie uniquement)
