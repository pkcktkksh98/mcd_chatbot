from pydantic import BaseModel
from typing import Optional

class OutletBase(BaseModel):
    name: str
    address: str
    waze_link: Optional[str]
    hours: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]

class Outlet(OutletBase):
    id: int

    class Config:
        orm_mode = True
