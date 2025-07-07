import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from db.database import SessionLocal
from db.models import McdOutlet

OUTPUT_FILE = "vector_index.faiss"
META_FILE = "vector_meta.npy"
MODEL_NAME = "all-MiniLM-L6-v2"

def build_index():
    # 1. Load data
    db = SessionLocal()
    outlets = db.query(McdOutlet).all()
    db.close()

    texts, ids = [], []
    for o in outlets:
        text = f"Name: {o.name}\nState: {o.state}\nAddress: {o.address}\nHours: {o.hours or 'N/A'}"
        texts.append(text)
        ids.append(o.id)

    # 2. Embed texts
    model = SentenceTransformer(MODEL_NAME)
    embeddings = np.array(model.encode(texts, show_progress_bar=True), dtype="float32")

    # 3. Build FAISS index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    # 4. Save
    faiss.write_index(index, OUTPUT_FILE)
    np.save(META_FILE, np.array(ids))
    print(f"Indexed {len(ids)} outlets into FAISS")

if __name__ == "__main__":
    build_index()
