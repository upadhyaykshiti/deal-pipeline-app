

import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Kanban from "./pages/Kanban";
import ICMemo from "./pages/ICMemo";
import AdminUsers from "./pages/AdminUsers";

/* ---------- Auth ---------- */
const isAuth = () => !!localStorage.getItem("token");
const role = () => localStorage.getItem("role");

/* ---------- Guards ---------- */
function ProtectedRoute({ children }) {
  return isAuth() ? children : <Navigate to="/" replace />;
}

function AdminRoute({ children }) {
  if (!isAuth()) return <Navigate to="/" replace />;
  if (role() !== "admin") return <Navigate to="/dashboard" replace />;
  return children;
}

/* ---------- App ---------- */
export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* ✅ ROOT ALWAYS LOGIN */}
        <Route path="/" element={<Login />} />

        {/* Optional alias */}
        <Route path="/login" element={<Login />} />

        {/* Dashboard → ALL roles */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Kanban />
            </ProtectedRoute>
          }
        />

        {/* IC Memo → Analyst + Partner + Admin */}
        <Route
          path="/deals/:id/memo"
          element={
            <ProtectedRoute>
              <ICMemo />
            </ProtectedRoute>
          }
        />

        {/* Admin only */}
        <Route
          path="/admin/users"
          element={
            <AdminRoute>
              <AdminUsers />
            </AdminRoute>
          }
        />

        {/* ❌ Any unknown route → Login */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
