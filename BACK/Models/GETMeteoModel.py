from pydantic import BaseModel

class GETMeteoModel(BaseModel):
    time: str
    temperature: str
    rain: str
    cloud_cover: str
    wind_direction: str
    wind_speed: str

class GETMeteoModel_Premium(BaseModel):
    time: str
    airTemperature: float
    pressure: float
    humidity: float
    cloudCover: float
    precipitation: float
    visibility: float
    windSpeed: float
    windDirection: float
    waveHeight: float
    waveDirection: float