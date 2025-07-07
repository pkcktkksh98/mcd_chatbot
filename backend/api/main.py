from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel

from db.database import get_db_session
from api import crud, schemas

# from db.database import SessionLocal
from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from api.schemas import Outlet

# New imports for RAG
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
from db.models import McdOutlet
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VEC_PATH = os.path.join(BASE_DIR, "..", "utils", "vector_index.faiss")
META_PATH = os.path.join(BASE_DIR, "..", "utils", "vector_meta.npy")

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your frontend later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Existing Endpoints ----------

@app.get("/outlets")
def get_outlets(state: str, db: Session = Depends(get_db_session)):
    return crud.get_outlets_by_state(db, state)
    

@app.get("/outlets/{outlet_id}", response_model=Outlet)
def get_outlet(outlet_id: int, db: Session = Depends(get_db_session)):
    outlet = crud.get_outlet_by_id(db, outlet_id)
    if not outlet:
        raise HTTPException(status_code=404, detail="Outlet not found")
    return outlet

@app.get("/search")
def search_outlets(keyword: str, db: Session = Depends(get_db_session)):
    return crud.search_outlets_by_hours(db, keyword)

# ---------- RAG Endpoint (New) ----------

class Query(BaseModel):
    q: str

# Load RAG assets once at startup
try:
    index = faiss.read_index(VEC_PATH)
    ids = np.load(META_PATH)
    embed_model = SentenceTransformer("all-MiniLM-L6-v2")

    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")
    gen_model = AutoModelForCausalLM.from_pretrained(
        "mistralai/Mistral-7B-Instruct-v0.1", device_map="auto"
    )
except Exception as e:
    print("Error loading RAG components:", e)
    index, ids, embed_model, tokenizer, gen_model = None, None, None, None, None

@app.post("/rag")
def rag_query(query: Query, db: Session = Depends(get_db_session)):
    if not all([index, ids is not None, embed_model, tokenizer, gen_model]):
        raise HTTPException(status_code=500, detail="RAG components not initialized.")

    # 1. Retrieve top relevant outlets
    q_emb = embed_model.encode([query.q]).astype("float32")
    D, I = index.search(q_emb, k=5)
    matched_ids = [int(ids[i]) for i in I[0]]

    outlets = db.query(McdOutlet).filter(McdOutlet.id.in_(matched_ids)).all()

    # 2. Build context
    context = "\n".join(
        f"- {o.name} ({o.hours or 'N/A'}): {o.address}" for o in outlets
    )

    # 3. Generate response using local model
    prompt = f"Context:\n{context}\n\nQ: {query.q}\nA:"
    inputs = tokenizer(prompt, return_tensors="pt").to(gen_model.device)
    output = gen_model.generate(**inputs, max_new_tokens=150)
    answer = tokenizer.decode(output[0], skip_special_tokens=True)

    return {"answer": answer}