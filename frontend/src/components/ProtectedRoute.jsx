import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function ProtectedRoute({ children, adminOnly = false }) {
  const { user } = useAuth();

  if (!user) {
    // Not logged in → redirect to Login
    return <Navigate to="/login" />;
  }

  if (adminOnly && user.role !== "admin") {
    // Logged in but not admin
    return <Navigate to="/" />;
  }

  return children;
}
