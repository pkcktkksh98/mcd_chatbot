from sqlalchemy.orm import Session
from db.models import McdOutlet

def get_all_outlets(db: Session):
    return db.query(McdOutlet).all()

def get_outlet_by_id(db: Session, outlet_id: int):
    return db.query(McdOutlet).filter(McdOutlet.id == outlet_id).first()

def search_outlets_by_hours(db: Session, keyword: str):
    return db.query(McdOutlet).filter(McdOutlet.hours.like(f"%{keyword}%")).all()