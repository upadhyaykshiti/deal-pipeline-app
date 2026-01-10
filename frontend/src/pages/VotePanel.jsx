import { useEffect, useState } from "react";
import api from "../api";

export default function VotePanel({ deal }) {
  const role = localStorage.getItem("role");
  const [votes, setVotes] = useState([]);

  if (role !== "partner" || deal.ic_locked) return null;

  useEffect(() => {
    loadVotes();
  }, []);

  async function loadVotes() {
    const res = await api.get(`/votes/deals/${deal.id}`);
    setVotes(res.data);
  }

  async function vote(decision) {
    await api.post(`/votes/deals/${deal.id}?decision=${decision}`);
    loadVotes();
  }

  return (
    <div>
      <h4>Vote</h4>
      <button onClick={() => vote("approve")}>👍 Approve</button>
      <button onClick={() => vote("decline")} style={{ marginLeft: 8 }}>
        👎 Decline
      </button>

      <div style={{ fontSize: 13, marginTop: 6 }}>
        Total votes: {votes.length}
      </div>
    </div>
  );
}
