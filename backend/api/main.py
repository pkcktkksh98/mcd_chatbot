from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from typing import List,Optional
from pydantic import BaseModel


from db.database import get_db_session
from api import crud, schemas

# from db.database import SessionLocal
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from api.schemas import Outlet


# New imports for RAG
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers.utils.quantization_config import BitsAndBytesConfig
import torch
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
def get_outlets(state: Optional[str] = None, db: Session = Depends(get_db_session)):
    if state:
        return crud.get_outlets_by_state(db, state)
    else:
        return crud.get_all_outlets(db)
    

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
bnb_config = BitsAndBytesConfig(load_in_4bit=True)
try:
    index = faiss.read_index(VEC_PATH)
    ids = np.load(META_PATH)
    embed_model = SentenceTransformer("all-MiniLM-L6-v2",device="cuda")

    gen_model = AutoModelForCausalLM.from_pretrained(
        "mistralai/Mistral-7B-Instruct-v0.1",quantization_config=bnb_config, device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")
    print("MODEL LOADED!")
except Exception as e:
    print("Error loading RAG components:", e)
    index, ids, embed_model, tokenizer, gen_model = None, None, None, None, None

@app.post("/rag")
def rag_query(query: Query, db: Session = Depends(get_db_session)):
    if not all([index, ids is not None, embed_model, tokenizer, gen_model]):
        raise HTTPException(status_code=500, detail="RAG components not initialized.")

    # 1. Retrieve top relevant outlets
    q_emb = embed_model.encode([query.q]).astype("float32") #type:ignore

    D, I = index.search(q_emb, k=60)#type:ignore
    matched_ids = [int(ids[i]) for i in I[0]]#type:ignore

    outlets = db.query(McdOutlet).filter(McdOutlet.id.in_(matched_ids)).all()

    # 2. Build context
    context = "\n".join(
        f"""{i+1}.
    Name: {o.name}
    Address: {o.address}
    Telephone: {o.telephone or 'N/A'}
    Email: {o.email or 'N/A'}
    Latitude: {o.lat}
    Longitude: {o.lng}
    State: {o.state}
    Features: {o.features or 'N/A'}
    Waze: {o.waze_link or 'N/A'}
    Google Maps: {o.google_maps or 'N/A'}
    """
        for i, o in enumerate(outlets)
    )
    

    # 3. Generate response using local model
    prompt = (
        f"You are a helpful assistant that answers questions based on provided outlet data.\n\n"
        f"Do not make up answers. If the answer is not found in the data, reply: 'Sorry, I could not find that information in the outlet database.'\n\n"
        f"Context:\n{context}\n\n"
        f"Q: {query.q}\n"
        f"A:"
        )
    device = "cuda" if torch.cuda.is_available() else "cpu"
    inputs = tokenizer(prompt, return_tensors="pt").to(device)#type:ignore
    output = gen_model.generate(**inputs, max_new_tokens=1000,pad_token_id=tokenizer.pad_token_id)#type:ignore
    decoded = tokenizer.decode(output[0], skip_special_tokens=True)#type:ignore
    answer = decoded.split("A:")[-1].strip()

    return {"answer": answer}