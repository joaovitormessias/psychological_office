import { createContext, useContext, useEffect, useState } from "react";
import api from "../services/api";
import { useNavigate } from "react-router-dom";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  const login = async (username, password) => {
    const res = await api.post("/token/", { username, password });
    localStorage.setItem("token", res.data.access);
    await fetchUser();
  };

  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
    navigate("/");
  };

  const fetchUser = async () => {
    try {
      // CRITICAL BUG: Fetching all users and taking the first one is incorrect.
      // This will not reliably get the currently logged-in user's data.
      // TODO: Replace this with an endpoint like `/api/usuarios/me/` that returns
      // the data for the currently authenticated user (request.user on the backend).
      // Example: const res = await api.get("/usuarios/me/"); setUser(res.data);
      const res = await api.get("/usuarios/"); // Current problematic call
      setUser(res.data[0]); // This line is the main issue.

      // If a '/usuarios/me/' endpoint is not immediately available, and if the user ID
      // were available from the token (e.g., decoded from JWT), a temporary client-side
      // filter could be (inefficiently) used:
      // const userIdFromToken = getUserIdFromToken(); // Implement this if possible
      // const currentUser = res.data.find(user => user.id === userIdFromToken);
      // setUser(currentUser);
      // However, the /usuarios/me/ endpoint is the standard and correct solution.

    } catch (error) {
      console.log("Failed to fetch user or token expired:", error);
      logout(); // Log out if fetching user fails (e.g. token invalid)
    }
  };

  // TODO: Implement refresh token handling.
  // Currently, only the access token is stored. If it expires, the user must log in again.
  // The /token/ endpoint also provides a refresh token. This should be stored securely
  // (e.g., localStorage or httpOnly cookie if backend supports it) and used to get a new
  // access token via the /token/refresh/ endpoint when the current access token expires.
  // This is typically handled in an API interceptor.

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) fetchUser();
  }, []);

  return (
    <AuthContext.Provider value={{ user, login, logout, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
