import { useEffect, useState } from "react";
import api from "../api";
import Navbar from "../components/Navbar";

export default function AdminUsers() {
  const [users, setUsers] = useState([]);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("analyst");

  useEffect(() => {
    loadUsers();
  }, []);

  async function loadUsers() {
    const res = await api.get("/admin/users");
    setUsers(res.data);
  }

  async function createUser() {
    if (!email || !password) return alert("Email & password required");

    await api.post("/admin/users", null, {
      params: { email, password, role }
    });

    setEmail("");
    setPassword("");
    setRole("analyst");
    loadUsers();
  }

  async function updateRole(id, role) {
    await api.patch(`/admin/users/${id}`, null, {
      params: { role }
    });
    loadUsers();
  }

  async function deleteUser(id) {
    if (!window.confirm("Delete user?")) return;
    await api.delete(`/admin/users/${id}`);
    loadUsers();
  }

  return (
    <>
      {/* 🔹 NAVBAR */}
      <Navbar />

      {/* 🔹 PAGE CONTENT */}
      <div style={{ padding: 20 }}>
        <h2>👥 Manage Users</h2>

        {/* CREATE USER */}
        <div style={{ marginBottom: 20 }}>
          <input
            placeholder="Email"
            value={email}
            onChange={e => setEmail(e.target.value)}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            style={{ marginLeft: 8 }}
          />
          <select
            value={role}
            onChange={e => setRole(e.target.value)}
            style={{ marginLeft: 8 }}
          >
            <option value="admin">Admin</option>
            <option value="analyst">Analyst</option>
            <option value="partner">Partner</option>
          </select>
          <button style={{ marginLeft: 8 }} onClick={createUser}>
            Create
          </button>
        </div>

        {/* USER LIST */}
        <table border="1" cellPadding="6" width="100%">
          <thead>
            <tr>
              <th>Email</th>
              <th>Role</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.map(u => (
              <tr key={u.id}>
                <td>{u.email}</td>
                <td>
                  <select
                    value={u.role}
                    onChange={e => updateRole(u.id, e.target.value)}
                  >
                    <option value="admin">Admin</option>
                    <option value="analyst">Analyst</option>
                    <option value="partner">Partner</option>
                  </select>
                </td>
                <td>
                  <button onClick={() => deleteUser(u.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
