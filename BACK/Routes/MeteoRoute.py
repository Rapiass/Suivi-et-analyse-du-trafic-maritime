from fastapi import APIRouter, HTTPException
from Models.GETMeteoModel import GETMeteoModel
from Models.GETMeteoModel import GETMeteoModel_Premium
import httpx
from datetime import datetime, timezone
from dateutil.parser import parse

router = APIRouter()

@router.get("/meteo/{lat}/{lon}", response_model=GETMeteoModel)
async def get_meteo(lat: str, lon: str):
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": "true",
            "hourly": "rain,cloudcover",
            "timezone": "Europe/Paris"
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

        current_weather = data.get("current_weather", {})
        now_local = current_weather.get("time")  # ex: '2025-04-17T20:15'

        # Initialisation valeurs par défaut
        rain = "N/A"
        cloud_cover = "N/A"

        if "hourly" in data and "time" in data["hourly"]:
            times = data["hourly"]["time"]
            try:
                # Trouver l'heure la plus proche
                current_time = parse(now_local)
                closest_time = min(times, key=lambda t: abs(parse(t) - current_time))
                idx = times.index(closest_time)
                rain = data["hourly"]["rain"][idx]
                cloud_cover = data["hourly"]["cloudcover"][idx]
            except Exception as e:
                print("Erreur lors du matching de l'heure :", str(e))

        return {
            "time": now_local,
            "temperature": str(current_weather.get("temperature", "N/A")),
            "rain": str(rain),
            "cloud_cover": str(cloud_cover),
            "wind_direction": str(current_weather.get("winddirection", "N/A")),
            "wind_speed": str(current_weather.get("windspeed", "N/A"))
        }

    except Exception as e:
        print("Erreur rencontrée :", str(e))
        raise HTTPException(status_code=500, detail=str(e))


STORMGLASS_API_KEY = "0f953692-1ba3-11f0-9606-0242ac130003-0f953700-1ba3-11f0-9606-0242ac130003"
STORMGLASS_API_KEY2="fc605642-1bc0-11f0-a68f-0242ac130003-fc60569c-1bc0-11f0-a68f-0242ac130003"

@router.get("/meteo-premium/{lat}/{lon}", response_model=GETMeteoModel_Premium)
async def get_premium_meteo(lat: str, lon: str):
    try:
        # Heure actuelle en UTC, format ISO
        now_utc = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0).isoformat()

        url = "https://api.stormglass.io/v2/weather/point"
        params = {
            "lat": lat,
            "lng": lon,
            "params": ",".join([
                "airTemperature",
                "pressure",
                "humidity",
                "cloudCover",
                "precipitation",
                "visibility",
                "windSpeed",
                "windDirection",
                "waveHeight",
                "waveDirection"
            ]),
            "start": now_utc,
            "end": now_utc
        }

        headers = {
            "Authorization": "fc605642-1bc0-11f0-a68f-0242ac130003-fc60569c-1bc0-11f0-a68f-0242ac130003"
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()

        print("Réponse API Premium :", data)

        # On récupère le premier (et unique) timestamp de la réponse
        hour_data = data.get("hours", [])[0]

        return {
            "time": hour_data.get("time", "N/A"),
            "airTemperature": hour_data.get("airTemperature", {}).get("sg", "N/A"),
            "pressure": hour_data.get("pressure", {}).get("sg", "N/A"),
            "humidity": hour_data.get("humidity", {}).get("sg", "N/A"),
            "cloudCover": hour_data.get("cloudCover", {}).get("sg", "N/A"),
            "precipitation": hour_data.get("precipitation", {}).get("sg", "N/A"),
            "visibility": hour_data.get("visibility", {}).get("sg", "N/A"),
            "windSpeed": hour_data.get("windSpeed", {}).get("sg", "N/A"),
            "windDirection": hour_data.get("windDirection", {}).get("sg", "N/A"),
            "waveHeight": hour_data.get("waveHeight", {}).get("sg", "N/A"),
            "waveDirection": hour_data.get("waveDirection", {}).get("sg", "N/A"),
        }

    except Exception as e:
        print("Erreur API Premium :", str(e))
        raise HTTPException(status_code=500, detail=f"Erreur API météo premium : {e}")