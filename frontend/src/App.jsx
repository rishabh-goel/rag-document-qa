import { useEffect, useState } from "react";
import { api } from "./api.js";

const ACCEPTED_TYPES = ".pdf,.docx,.txt,.md,.csv";

function SourceList({ sources }) {
  if (!sources?.length) return null;
  return (
    <div className="sources" aria-label="Sources">
      {sources.map((source, index) => (
        <details key={`${source.document_id}-${source.chunk_index}`}>
          <summary>
            Source {index + 1} · {source.filename}
            {source.page ? ` · page ${source.page}` : ""}
          </summary>
          <p>{source.excerpt}</p>
        </details>
      ))}
    </div>
  );
}

function App() {
  const [documents, setDocuments] = useState([]);
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState("");
  const [notice, setNotice] = useState("");
  const [uploading, setUploading] = useState(false);
  const [asking, setAsking] = useState(false);

  const loadDocuments = async () => {
    try {
      setDocuments(await api.listDocuments());
      setNotice("");
    } catch {
      setNotice("The API is unavailable. Start FastAPI on port 8000, then refresh.");
    }
  };

  useEffect(() => {
    loadDocuments();
  }, []);

  const handleUpload = async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    setUploading(true);
    setNotice("");
    try {
      const result = await api.uploadDocument(file);
      await loadDocuments();
      setNotice(`Indexed ${result.document.filename} into ${result.document.chunks} chunks.`);
    } catch (error) {
      setNotice(error.message);
    } finally {
      setUploading(false);
      event.target.value = "";
    }
  };

  const handleDelete = async (id) => {
    try {
      await api.deleteDocument(id);
      await loadDocuments();
    } catch (error) {
      setNotice(error.message);
    }
  };

  const handleAsk = async (event) => {
    event.preventDefault();
    const trimmedQuestion = question.trim();
    if (!trimmedQuestion || asking) return;
    setQuestion("");
    setMessages((current) => [...current, { role: "user", content: trimmedQuestion }]);
    setAsking(true);
    setNotice("");
    try {
      const result = await api.ask(trimmedQuestion);
      setMessages((current) => [...current, { role: "assistant", content: result.answer, sources: result.sources }]);
    } catch (error) {
      setMessages((current) => [...current, { role: "assistant", content: `Unable to answer: ${error.message}` }]);
    } finally {
      setAsking(false);
    }
  };

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-mark">✦</span>
          <div><strong>Atlas</strong><small>Document intelligence</small></div>
        </div>
        <label className={`upload-card ${uploading ? "is-busy" : ""}`}>
          <input type="file" accept={ACCEPTED_TYPES} onChange={handleUpload} disabled={uploading} />
          <span className="upload-icon">↑</span>
          <strong>{uploading ? "Indexing document…" : "Add a document"}</strong>
          <small>PDF, DOCX, TXT, MD, or CSV</small>
        </label>
        <section className="document-list" aria-label="Indexed documents">
          <div className="section-heading"><span>Library</span><span>{documents.length}</span></div>
          {documents.length === 0 ? <p className="empty">No documents indexed yet.</p> : documents.map((document) => (
            <article className="document-row" key={document.id}>
              <div><strong>{document.filename}</strong><small>{document.chunks} chunks</small></div>
              <button className="icon-button" onClick={() => handleDelete(document.id)} aria-label={`Delete ${document.filename}`}>×</button>
            </article>
          ))}
        </section>
      </aside>

      <section className="chat-panel">
        <header><div><p className="eyebrow">RETRIEVAL-AUGMENTED GENERATION</p><h1>Ask your documents anything.</h1></div><span className="status-dot">Private workspace</span></header>
        {notice && <div className="notice" role="status">{notice}</div>}
        <div className="conversation" aria-live="polite">
          {messages.length === 0 && <div className="empty-state"><span>⌁</span><h2>Grounded answers, not guesses.</h2><p>Upload a document, then ask a specific question. Every response includes the passages it used.</p></div>}
          {messages.map((message, index) => (
            <article className={`message ${message.role}`} key={index}>
              <div className="message-label">{message.role === "user" ? "YOU" : "ATLAS"}</div>
              <div><p>{message.content}</p><SourceList sources={message.sources} /></div>
            </article>
          ))}
          {asking && <article className="message assistant"><div className="message-label">ATLAS</div><div className="thinking"><i></i><i></i><i></i> Searching your library…</div></article>}
        </div>
        <form className="composer" onSubmit={handleAsk}>
          <input value={question} onChange={(event) => setQuestion(event.target.value)} placeholder="Ask a question about your documents…" disabled={asking} aria-label="Question" />
          <button type="submit" disabled={asking || !question.trim()}>Ask <span>↵</span></button>
        </form>
      </section>
    </main>
  );
}

export default App;
