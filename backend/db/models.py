from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class McdOutlet(Base):
    __tablename__ = "mcd_outlets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(String(500), nullable=False)
    state = Column(String(100), nullable=False)
    telephone = Column(String(100), default="")
    fax = Column(String(100), default="")            
    # email = Column(String(100), default="")           # (can be used if needed in future)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    features = Column(Text, default="")
    hours = Column(String(255), default="")           
    # google_maps = Column(String(500), nullable=True)
    waze_link = Column(String(500), nullable=True)
