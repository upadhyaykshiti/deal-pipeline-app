

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  async function submit(e) {
    e.preventDefault();
    setLoading(true);

    try {
      const res = await api.post("/auth/login", {
        email,
        password,
      });

      // ✅ STORE TOKEN + ROLE
      localStorage.setItem("token", res.data.token);
      localStorage.setItem("role", res.data.role);

      navigate("/dashboard");
    } catch (err) {
      alert("Invalid email or password");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <h2 style={styles.title}>Login Page</h2>
        <p style={styles.subtitle}>
          Sign in to access your dashboard
        </p>

        <form onSubmit={submit}>
          <div style={styles.field}>
            <label>Email</label>
            <input
              style={styles.input}
              type="email"
              placeholder="admin@example.com"
              value={email}
              onChange={e => setEmail(e.target.value)}
              required
            />
          </div>

          <div style={styles.field}>
            <label>Password</label>
            <input
              style={styles.input}
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={e => setPassword(e.target.value)}
              required
            />
          </div>

          <button style={styles.button} disabled={loading}>
            {loading ? "Signing in..." : "Login"}
          </button>
        </form>

        <div style={styles.footer}>
          <small>Admin / Analyst / Partner access</small>
        </div>
      </div>
    </div>
  );
}

/* ---------- Styles ---------- */
const styles = {
  page: {
    height: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "#f3f4f6",
  },
  card: {
    width: 360,
    padding: 24,
    background: "#fff",
    borderRadius: 8,
    boxShadow: "0 10px 25px rgba(0,0,0,0.1)",
  },
  title: {
    marginBottom: 4,
    textAlign: "center",
  },
  subtitle: {
    marginBottom: 20,
    textAlign: "center",
    color: "#666",
    fontSize: 14,
  },
  field: {
    display: "flex",
    flexDirection: "column",
    marginBottom: 14,
    fontSize: 14,
  },
  input: {
    padding: 10,
    borderRadius: 4,
    border: "1px solid #ccc",
    marginTop: 4,
  },
  button: {
    width: "100%",
    padding: 10,
    marginTop: 10,
    background: "#111827",
    color: "white",
    border: "none",
    borderRadius: 4,
    cursor: "pointer",
  },
  footer: {
    marginTop: 16,
    textAlign: "center",
    color: "#888",
  },
};
