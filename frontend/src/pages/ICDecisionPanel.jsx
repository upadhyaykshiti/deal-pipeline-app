


import { useState } from "react";
import api from "../api";

// export default function ICDecisionPanel({ deal, onDecision }) {
export default function ICDecisionPanel({ deal, onDecision = () => {} }) {

  const role = localStorage.getItem("role");
  const userName = localStorage.getItem("name") || "Partner";

  const [comment, setComment] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  // Only partner + only before IC lock
  if (role !== "partner" || deal.ic_locked) return null;

  async function approve() {
    try {
      setLoading(true);
      await api.post(
        `/ic/deals/${deal.id}/approve?comment=${comment}`
      );

      setMessage(
        `Partner ${userName} approved Deal “${deal.name}”`
      );

      onDecision(); // 🔥 refresh deal → hides Vote & Comment
    } finally {
      setLoading(false);
    }
  }

  async function reject() {
    try {
      setLoading(true);
      await api.post(
        `/ic/deals/${deal.id}/reject?comment=${comment}`
      );

      setMessage(
        `Partner ${userName} rejected Deal “${deal.name}”`
      );

      onDecision();
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ marginTop: 20 }}>
      <h3>Final IC Decision</h3>

      <textarea
        placeholder="Decision comment (optional)"
        value={comment}
        onChange={e => setComment(e.target.value)}
        style={{ width: "100%" }}
        disabled={loading}
      />

      <div style={{ marginTop: 10 }}>
        <button onClick={approve} disabled={loading}>
          Approve
        </button>
        <button
          style={{ marginLeft: 10 }}
          onClick={reject}
          disabled={loading}
        >
          Reject
        </button>
      </div>

      {message && (
        <div
          style={{
            marginTop: 12,
            padding: 10,
            background: "#f0fff4",
            border: "1px solid #38a169",
            borderRadius: 4,
            color: "#22543d"
          }}
        >
          ✅ {message}
        </div>
      )}
    </div>
  );
}
