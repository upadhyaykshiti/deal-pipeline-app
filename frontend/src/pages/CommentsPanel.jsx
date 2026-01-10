import { useEffect, useState } from "react";
import api from "../api";

export default function CommentsPanel({ deal }) {
  const role = localStorage.getItem("role");
  const [comments, setComments] = useState([]);
  const [text, setText] = useState("");

  useEffect(() => {
    load();
  }, []);

  async function load() {
    const res = await api.get(`/comments/deals/${deal.id}`);
    setComments(res.data);
  }

  async function submit() {
    if (!text) return;
    await api.post(`/comments/deals/${deal.id}?body=${text}`);
    setText("");
    load();
  }

  return (
    <div style={{ marginTop: 20 }}>
      <h4>Comments</h4>

      {role === "partner" && !deal.ic_locked && (
        <>
          <textarea
            value={text}
            onChange={e => setText(e.target.value)}
            style={{ width: "100%" }}
          />
          <button onClick={submit}>Add Comment</button>
        </>
      )}

      {comments.map(c => (
        <div
          key={c.id}
          style={{ borderBottom: "1px solid #eee", padding: 6 }}
        >
          {c.body}
          <div style={{ fontSize: 11, color: "#999" }}>
            {new Date(c.created_at).toLocaleString()}
          </div>
        </div>
      ))}
    </div>
  );
}
