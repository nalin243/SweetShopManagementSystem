import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();

  return (
    <nav className="flex justify-between items-center px-6 py-4 bg-white/70 backdrop-blur-md border-b border-white/30 shadow-sm">
      <Link to="/" className="font-bold text-2xl text-indigo-600">
        Sweet Shop
      </Link>

      <div className="flex gap-4 items-center">
        {user ? (
          <>
            <span className="text-gray-700">Hi, {user.email}</span>
   {/*         {user.role === "admin" && (
              <Link
                to="/admin/add"
                className="bg-pink-500 hover:bg-pink-600 text-white px-4 py-2 rounded-xl transition"
              >
                + Add Sweet
              </Link>
            )}*/}
            <button
              onClick={logout}
              className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-4 py-2 rounded-xl transition"
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <Link
              to="/login"
              className="bg-indigo-500 hover:bg-indigo-600 text-white px-4 py-2 rounded-xl transition"
            >
              Login
            </Link>
            <Link
              to="/register"
              className="bg-pink-500 hover:bg-pink-600 text-white px-4 py-2 rounded-xl transition"
            >
              Register
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}
