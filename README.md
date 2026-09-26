# RAG Document Q&A

A local Python document-question-answering app. It indexes PDF, DOCX, TXT, Markdown, and CSV documents into ChromaDB, retrieves relevant passages, and produces grounded answers with citations.

## Run it

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Configure the model:

   ```bash
   cp .env.example .env
   # Add OPENAI_API_KEY to .env
   ```

   To exercise ingestion and retrieval without an API key, set `LLM_PROVIDER=none` in `.env`. The app will return the best retrieved passage instead of a generated answer.

3. Start the API and React UI in separate terminals:

   ```bash
   uvicorn app.api:app --reload
   cd frontend
   cp .env.example .env
   npm install
   npm run dev
   ```

Open `http://localhost:5173`. The API docs are at `http://localhost:8000/docs`.

## API

- `POST /documents` — multipart field `file`; extracts text, chunks it, creates embeddings, and persists them.
- `GET /documents` — list indexed documents.
- `DELETE /documents/{id}` — delete a document and all its vectors.
- `POST /ask` — body: `{"question":"…", "document_ids":["optional-id"], "top_k":5}`.

Each response contains the answer and retrieved source excerpts, including filename, page (when available), and relevance.

## Design notes

- The interface is React with Vite; it calls FastAPI directly and renders expandable source citations.
- Embeddings run locally through SentenceTransformers (`all-MiniLM-L6-v2` by default). The first run downloads the model.
- ChromaDB, the uploaded files, and the document registry persist locally; restart-safe retrieval comes for free.
- The generation prompt instructs the model to use only retrieved context and to state when an answer is absent.
- The simple character-based chunker is deliberate for a portable MVP. Replace it with a tokenizer-aware splitter if you move to very large or multilingual corpora.

## Verify

```bash
python3 -m pytest -q
```
