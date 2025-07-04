from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from db.database import SessionLocal
from api import crud, schemas

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your frontend later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/outlets", response_model=list[schemas.Outlet])
def get_all_outlets(db: Session = Depends(get_db)):
    return crud.get_all_outlets(db)

@app.get("/outlets/{outlet_id}", response_model=schemas.Outlet)
def get_outlet(outlet_id: int, db: Session = Depends(get_db)):
    outlet = crud.get_outlet_by_id(db, outlet_id)
    if not outlet:
        raise HTTPException(status_code=404, detail="Outlet not found")
    return outlet

@app.get("/search")
def search_outlets(keyword: str, db: Session = Depends(get_db)):
    return crud.search_outlets_by_hours(db, keyword)
