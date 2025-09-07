from pydantic import BaseModel

class GETCaptainVessel(BaseModel):
    MMSI: str
    VesselName: str
    LAT: float
    LON: float
    