
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api";

import ICDecisionPanel from "./ICDecisionPanel";
import CommentsPanel from "./CommentsPanel";
import VotePanel from "./VotePanel";

export default function ICMemo() {
  const { id } = useParams();
  const dealId = id;
  const role = localStorage.getItem("role");

  const [deal, setDeal] = useState(null);
  const [versions, setVersions] = useState([]);
  const [readOnly, setReadOnly] = useState(false);

  const [form, setForm] = useState({
    summary: "",
    market: "",
    product: "",
    traction: "",
    risks: "",
    open_questions: ""
  });

  useEffect(() => {
    loadDeal();
    loadVersions();
  }, [dealId]);

  async function loadDeal() {
    const res = await api.get("/deals");
    const found = res.data.find(d => d.id === Number(dealId));
    setDeal(found);
  }


  async function loadVersions() {
      const res = await api.get(`/memos/deals/${dealId}/memo/versions`);
      setVersions(res.data);

      // Load latest version into editor
      if (res.data.length > 0) {
        setForm(res.data[0].snapshot);
        setReadOnly(false);
    }
    }


  

  async function loadVersion(versionId, isCurrent) {
  if (isCurrent) {
    loadVersions();
    return;
  }

  const res = await api.get(`/memos/memo/version/${versionId}`);
  setForm(res.data.snapshot);
  setReadOnly(true);
}

  async function save() {
     await api.post(`/memos/deals/${dealId}/memo`, form);
    alert("Saved new version");
    loadVersions();
  }


  if (!deal) return <div>Loading...</div>;

  return (
    <div style={{ display: "flex", gap: 20, padding: 20 }}>
      {/* LEFT */}
      <div style={{ flex: 1 }}>
        <h2>
          IC Memo — {deal.name} (#{deal.id})
        </h2>

        {readOnly && (
          <div style={{
            background: "#fff3cd",
            padding: 8,
            marginBottom: 10,
            borderRadius: 4
          }}>
            Viewing older version (read-only)
          </div>
        )}

        {Object.keys(form).map(k => (
          <div key={k}>
            <h4>{k}</h4>
            <textarea
              rows={4}
              style={{ width: "100%" }}
              value={form[k]}
              disabled={readOnly || role === "partner" || deal.ic_locked}
              onChange={e =>
                setForm({ ...form, [k]: e.target.value })
              }
            />
          </div>
        ))}

        {(role === "admin" || role === "analyst") &&
          !deal.ic_locked &&
          !readOnly && (
            <button onClick={save}>Save Version</button>
          )}

        <hr />

        {/* Partner panels */}
        <VotePanel deal={deal} />
        <CommentsPanel deal={deal} />
        <ICDecisionPanel 
          deal={deal} 
          onDecision={deal} 
        /> 

      </div>

      {/* RIGHT */}
      <div style={{ width: 260 }}>
        <h3>Version History</h3>

        {versions.map((v, index) => (
          <div
            key={v.id}
            onClick={() => loadVersion(v.id, index === 0)}
            style={{
              cursor: "pointer",
              padding: 6,
              marginBottom: 6,
              borderRadius: 4,
              background: index === 0 ? "#e6f7ff" : "#f7f7f7"
            }}
          >
            <div style={{ fontSize: 12 }}>
              {new Date(v.created_at).toLocaleString()}
            </div>
            {index === 0 && (
              <div style={{ fontSize: 11, color: "green" }}>
                Current
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
