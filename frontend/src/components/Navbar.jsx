import { Link, useNavigate } from "react-router-dom";

export default function Navbar() {
  const role = localStorage.getItem("role");
  const navigate = useNavigate();

  function logout() {
    localStorage.clear();
    navigate("/login");
  }

  return (
    <div style={{ padding: 12, borderBottom: "1px solid #ddd" }}>
      <Link to="/dashboard">📊 Dashboard</Link>

      {role === "admin" && (
        <Link style={{ marginLeft: 15 }} to="/admin/users">
          👥 Manage Users
        </Link>
      )}

      <button style={{ float: "right" }} onClick={logout}>
        Logout
      </button>
    </div>
  );
}
