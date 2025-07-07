from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from db.database import SessionLocal
from api import crud, schemas

from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from db.database import get_db_session
from api import crud
from fastapi.middleware.cors import CORSMiddleware
from api.schemas import Outlet
from typing import List
app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your frontend later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/outlets")
def get_outlets(state: str, db: Session = Depends(get_db_session)):
    return crud.get_outlets_by_state(db, state)
    

@app.get("/outlets/{outlet_id}", response_model=schemas.Outlet)
def get_outlet(outlet_id: int, db: Session = Depends(get_db_session)):
    outlet = crud.get_outlet_by_id(db, outlet_id)
    if not outlet:
        raise HTTPException(status_code=404, detail="Outlet not found")
    return outlet

@app.get("/search")
def search_outlets(keyword: str, db: Session = Depends(get_db_session)):
    return crud.search_outlets_by_hours(db, keyword)
