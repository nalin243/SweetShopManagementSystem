import { createContext, useContext, useState, useEffect } from "react";
import api from "../api/apiClient";
import { jwtDecode } from "jwt-decode";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  //load user if exists
  const [user, setUser] = useState(() => {
    const token = localStorage.getItem("token");
    if (token) {
      try {
        const decoded = jwtDecode(token);
        return { email: decoded.sub, role: decoded.role };
      } catch {
        return null;
      }
    }
    return null;
  });


  const register = async ({ email, password }) => {
    const res = await api.post("/auth/signup", { email, password });
    const token = res.data.access_token;

    localStorage.setItem("token", token);
    const decoded = jwtDecode(token);
    setUser({ email: decoded.sub, role: decoded.role });
  };

  const login = async (email, password) => {
    const params = new URLSearchParams();
    params.append("username", email);
    params.append("password", password);

    const res = await api.post("/auth/login", params, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });

    const token = res.data.access_token;
    localStorage.setItem("token", token);

    const decoded = jwtDecode(token);
    setUser({ email: decoded.sub, role: decoded.role });
  };

  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
  };

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      try {
        const decoded = jwtDecode(token);
        setUser({ email: decoded.sub, role: decoded.role });
      } catch {
        logout();
      }
    }
  }, []);

  return (
    <AuthContext.Provider value={{ user, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
