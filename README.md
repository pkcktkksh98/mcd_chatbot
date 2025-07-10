# 🍔 McDonald's Malaysia Outlet Locator & Chatbot

An interactive web application that allows users to locate McDonald's outlets across Malaysia, filter by state, view outlet details on a map, and chat with a smart assistant to ask questions like "Which outlets are open 24 hours?" or "Where can I host a birthday party?"

---

## 📦 Features

- ✅ Interactive map of outlets (React Leaflet)
- ✅ Filter by Malaysian states
- ✅ View 5KM nearby outlets
- ✅ Intelligent chatbot (RAG-powered) for outlet-related queries
- ✅ Mobile and desktop responsive layout (Tailwind CSS)

---

## 🧠 Key Technologies & Architecture

### 🔧 Frontend
- **Framework**: [React](https://reactjs.org/) with [Vite](https://vitejs.dev/) – fast dev experience
- **Styling**: [Tailwind CSS](https://tailwindcss.com/) – utility-first, responsive, mobile-friendly
- **Mapping**: [React Leaflet](https://react-leaflet.js.org/) – for map rendering and interactivity
- **Chat UI**: Custom component with auto-scroll, typing effect, and prompt suggestions

### 🧠 Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) – async-friendly, lightweight, easy to build APIs
- **Database**: MySQL (via SQLAlchemy ORM) – stores all outlet data
- **RAG (Retrieval-Augmented Generation)**:
  - **Vector Store**: FAISS – for efficient semantic search
  - **Embedding Model**: Local [TinyLlama-1.1B-Chat](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0)
  - **Answering**: Local LLM inference with semantic context from outlet data

---

## 📁 Project Structure

```
mindhive_techassessment/
├── backend/
├── .env                         # Environment variables (e.g., DB connection, API keys)
├── .gitignore                   # Ignore virtual envs, cache files, etc.
├── requirements.txt             # Python dependencies
├── api/                         # FastAPI app logic
│   ├── crud.py                  # Database queries and business logic
│   ├── main.py                  # Main FastAPI application with route definitions
│   └──schemas.py                # Pydantic schemas for request/response validation
├── db/                          # Database setup and models
│   ├── database.py              # SQLAlchemy session and engine setup
│   ├── models.py                # SQLAlchemy ORM models
│   └──save_to_db.py             # Logic for saving scraped data into the DB
├── scraping/                    # Web scraping logic
│   └──  scrape_mcd.py           # Script to scrape McDonald's outlet data
├── utils/                       # Utility scripts
│   ├── build_vector_index.py    # Script to create FAISS vector index
│   ├── geocode.py               # Geocoding utility for address-to-coordinates
│   ├── state_extractor.py       # Extracts state names from scraped data
│   ├── vector_index.faiss       # FAISS vector index file
│   ├── vector_meta.npy          # Metadata for vector index (e.g., outlet info)          # FAISS, embedding helper
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── map/
│   │   │   │   ├── OutletMap.tsx
│   │   │   │   └── RecenterMap.tsx   
│   │   │   ├──chat/
│   │   │   │  ├── ChatBox.tsx
│   │   │   │  └── MessageBubble.tsx
│   │   │   
│   │   ├── utils/
│   │   │   └── stateCenters.ts
│   │   ├── App.tsx
│   │   └── index.css
│   ├── tailwind.config.js
│   └── vite.config.ts
└── README.md
```

---

## ⚙️ Setup Instructions

## 📦 Clone the Repository

```bash
git clone https://github.com/your-username/mindhive.git
cd mindhive
```

---

## 🐍 Create Python Virtual Environment

Make sure you have Python 3.10+ and `virtualenv` or `conda`.

### Using `venv`:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Or using `conda`:
```bash
conda create -n mindhive python=3.11 -y
conda activate mindhive
```

---

### 🛠️ Prepare the Database

1. **Install and start MySQL**  
   Make sure MySQL server is installed and running on your machine.

2. **Create a new database**  
   You can use the MySQL CLI or a GUI like phpMyAdmin to create a database named, for example:
   ```sql
   CREATE DATABASE mcd;
   ```

3. **Set up the `.env` file**  
   In the root of your backend project (same level as `requirements.txt`), create a `.env` file and add your database credentials:
   ```env
   DB_USER=your_mysql_username
   DB_PASS=your_mysql_password
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=mcd
   ```



✅ Now you're ready to run the backend API.

---

## 🏗️ How to Build the Vector Index

1. **Prepare Metadata**: Ensure your outlets are already stored in the database. You'll need to extract relevant text like:
   - name
   - address
   - features
   - state
   - hours

2. **Run the script**

```bash
python backend/utils/build_index.py
```

3. **Move Vector Index into utils**

```bash
mv embeddings.npy utils/
mv faiss.index utils/
```

4. **What it does**:
   - Fetches all outlet data from your database.
   - Concatenates fields into text chunks per outlet.
   - Encodes each chunk using SentenceTransformer embeddings.
   - Stores the vector index using FAISS and saves metadata for retrieval.

---

### 🔧 Backend

1.  **Install dependencies**  
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. **Create tables and insert outlet data**  
   - First, ensure your MySQL server allows connections with the credentials above.
   - Then run the following from your project root to scrape and insert outlet data:
   ```bash
   cd backend
   python -m scraping.scrape_all_states_and_store
   ```

   This will:
   - Scrape all outlet information from McDonald's Malaysia website.
     ```bash
     https://www.mcdonalds.com.my/locate-us
     ```
   - Geocode the outlet addresses.
   - Store them into the MySQL database automatically using SQLAlchemy ORM.

4. **Start FastAPI server**  
   ```bash
   uvicorn api.main:app --reload
   ```

---

### 🌐 Frontend

1. **Install Node dependencies**  
   ```bash
   cd frontend
   npm install
   ```

2. **Install Tailwind CSS**  
   ```bash
   npm install -D tailwindcss postcss autoprefixer
   npx tailwindcss init -p
   ```
3. **Start frontend dev server**  
   ```bash
   npm run dev
   ```

---

## 🤖 Chatbot Workflow (RAG-based)

1. User inputs a query (e.g. "Show outlets with McCafe in KL")
2. Query is semantically embedded
3. FAISS retrieves top relevant outlet documents
4. Retrieved context is passed to local **TinyLlama-1.1B-Chat** model
5. A summarized, grounded answer is returned

> Make sure your TinyLlama model is accessible locally from:
> ```
> C:\Users\petro\.cache\huggingface\hub\models--TinyLlama--TinyLlama-1.1B-Chat-v0.1
> ```

---

## ✅ Completed Checklist

- [x] Outlet scraper with category support
- [x] State-based outlet filter
- [x] Dynamic map with markers + 5KM radius
- [x] Chatbot backend (RAG + local model)
- [x] Chat UI with typing and suggestions
- [x] Tailwind CSS integration
- [x] Mobile and desktop responsive layout

---

## 💡 Future Improvements

- [ ] UI/UX polish with animated transitions
- [ ] Add marker clustering for dense areas
- [ ] Improve RAG prompt engineering
- [ ] Add filter by categories (Drive-Thru, McCafe, etc.)
- [ ] Host on Vercel (frontend) + Render or EC2 (backend)

---

## 📜 License

This project is for educational/technical assessment purposes.  
Feel free to fork and enhance it for learning or demo use.
