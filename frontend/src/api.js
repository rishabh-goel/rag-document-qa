const API_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, options);
  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    throw new Error(payload.detail ?? `Request failed (${response.status})`);
  }
  return response.status === 204 ? null : response.json();
}

export const api = {
  listDocuments: () => request("/documents"),
  uploadDocument: (file) => {
    const formData = new FormData();
    formData.append("file", file);
    return request("/documents", { method: "POST", body: formData });
  },
  deleteDocument: (id) => request(`/documents/${id}`, { method: "DELETE" }),
  ask: (question) => request("/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  }),
};
