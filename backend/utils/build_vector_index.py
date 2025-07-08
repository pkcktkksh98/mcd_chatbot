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
        text = (
            f"Name: {o.name}\n"
            f"State: {o.state}\n"
            f"Address: {o.address}\n"
            f"Telephone: {o.telephone or 'N/A'}\n"
            f"Email: {o.email or 'N/A'}\n"
            f"Features: {o.features or 'N/A'}\n"
            f"Google Maps: {o.google_maps or 'N/A'}\n"
            f"Waze: {o.waze_link or 'N/A'}"
        )
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
