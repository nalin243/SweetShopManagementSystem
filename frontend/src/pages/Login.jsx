import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const { login } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await login(email, password);
      navigate("/");
    } catch {
      setError("Invalid email or password");
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen px-4">
      <div className="bg-white/70 backdrop-blur-md p-8 rounded-2xl shadow-lg w-full max-w-sm border border-white/30">
        <h1 className="text-3xl font-semibold text-center text-indigo-600 mb-6">
        Sweet Shop Login
        </h1>
        {error && <p className="text-red-500 text-sm mb-3 text-center">{error}</p>}

        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            className="w-full p-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-400"
            placeholder="Email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <input
            className="w-full p-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-400"
            placeholder="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <button className="w-full py-3 bg-indigo-500 hover:bg-indigo-600 text-white rounded-xl transition">
            Log In
          </button>
        </form>

        <p className="text-sm text-center mt-4 text-gray-700">
          Don’t have an account?{" "}
          <Link to="/register" className="text-pink-600 hover:underline">
            Register
          </Link>
        </p>
      </div>
    </div>
  );
}
