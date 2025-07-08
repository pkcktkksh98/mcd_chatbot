from pydantic import BaseModel
from typing import Optional

class OutletBase(BaseModel):
    name: str
    address: str
    waze_link: str
    hours: Optional[str]
    lat: Optional[float]
    lng: Optional[float]
    state: str

class Outlet(OutletBase):
    id: int
    name: str
    address: str
    state: str
    telephone: Optional[str]
    email: Optional[str]
    lat: Optional[float]
    lng: Optional[float]
    features: Optional[str]
    google_maps: str
    waze_link: str

    class Config:
        orm_mode = True
