"""
Importation de FastAPI depuis la bibliothèque fastapi
FastAPI est le famework utilisé ici pour créer une API web moderne et rapide
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import httpx
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio
import time
import os
import sys
import subprocess

"""
Importation du routeur "task_router" depuis un autre fichier appelé "taskRoute" dans un dossier "routers"
Ce routeur contient probablement des routes spécifiques liées à la gestion des tâches
"""
from Routes.CaptainRoute import router as captain_router
from Routes.ExpertRoute import router as expert_router
from Routes.ShipownerRoute import router as shipowner_router
from Routes.UserRoute import router as user_router
from Routes.MeteoRoute import router as meteo_router
from Routes.AdminRoute import router as admin_router
"""
Création d'une instance de l'application FastAPI
Cette instance va permettre de définir les routes et les comportements de l'API
"""

# Rediriger explicitement print vers stdout
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)

app = FastAPI()
for route in app.routes:
    print(f"Route détectée : {route.path} - Méthode : {route.methods}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À limiter en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""
Création d'un sheduler en arrière plan
il executera run_etl tous les jours à 00h00

"""
def run_etl():
    try:
        print("test")
        script_path = os.path.join(os.path.dirname(__file__), "ETL", "main.py")
        result = subprocess.run(["python", script_path], capture_output=True, text=True)
        print("ETL Output:", result.stdout)
        print("ETL Error:", result.stderr)
        return {"status": "ETL executed", "output": result.stdout, "error": result.stderr}
    except Exception as e:
        return {"error": str(e)}

scheduler = BackgroundScheduler()
scheduler.add_job(run_etl)
scheduler.start()





"""
Ajout du routeur "task_router" à l'application FastAPI
Cela permet d'inclure des routes supplémentaires (comme celles liées à la gestion des tâches) définies dans le fichier "taskRoute"
Cela permet de structurer l'application en modules et de séparer le code en plusieurs fichiers pour plus de clarté et de maintenabilité
"""
print("📌 Vérification du routeur météo :", meteo_router.routes)

app.include_router(captain_router)
app.include_router(expert_router)
app.include_router(shipowner_router)
app.include_router(user_router)
app.include_router(meteo_router)
app.include_router(admin_router)

print("🚀 Vérification après l'ajout des routes :")
for route in app.routes:
    print(f"➡️ {route.path} - Méthodes : {route.methods}")

