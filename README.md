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
  - **Embedding Model**: Local [Mistral-7B-Instruct](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1)
  - **Answering**: Local LLM inference with semantic context from outlet data

---

## 📁 Project Structure

```
mindhive_techassessment/
├── backend/
│   ├── api/               # FastAPI routes, RAG logic, schemas
│   ├── db/                # SQLAlchemy models and database logic
│   ├── scraping/          # Scraper for McDonald's outlet data
│   ├── utils/             # FAISS, embedding helper
│   ├── main.py            # App entry point
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatBox.tsx
│   │   │   ├── OutletMap.tsx
│   │   │   └── MessageBubble.tsx
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

### 🔧 Backend

1. **Create Python virtual environment**  
   ```bash
   conda create -n mindhive python=3.11
   conda activate mindhive
   ```

2. **Install dependencies**  
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Prepare the database**
   - Ensure MySQL is running
   - Create a DB named (e.g., `mcd_outlets`)
   - Configure `.env` file with DB credentials

4. **Scrape and load outlet data** (optional if DB already populated)  
   ```bash
   python scraping/scraper.py
   ```

5. **Start FastAPI server**  
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

3. **Configure Tailwind in `tailwind.config.js`**  
   ```js
   content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"]
   ```

4. **Start frontend dev server**  
   ```bash
   npm run dev
   ```

---

## 🤖 Chatbot Workflow (RAG-based)

1. User inputs a query (e.g. "Show outlets with McCafe in KL")
2. Query is semantically embedded
3. FAISS retrieves top relevant outlet documents
4. Retrieved context is passed to local **Mistral-7B-Instruct** model
5. A summarized, grounded answer is returned

> Make sure your Mistral model is accessible locally from:
> ```
> C:\Users\petro\.cache\huggingface\hub\models--mistralai--Mistral-7B-Instruct-v0.1
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