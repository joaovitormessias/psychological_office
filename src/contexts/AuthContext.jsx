import React, { createContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthService } from '../services/AuthService';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('authToken'));
  const [loading, setLoading] = useState(true); // True initially to check localStorage
  const navigate = useNavigate();

  useEffect(() => {
    const storedUser = localStorage.getItem('authUser');
    const storedToken = localStorage.getItem('authToken');
    if (storedUser && storedToken) {
      try {
        setUser(JSON.parse(storedUser));
        setToken(storedToken);
      } catch (error) {
        console.error("Error parsing stored user data:", error);
        localStorage.removeItem('authUser');
        localStorage.removeItem('authToken');
      }
    }
    setLoading(false); // Done checking localStorage
  }, []);

  const login = async (email, password) => {
    setLoading(true);
    try {
      const response = await AuthService.login(email, password);
      localStorage.setItem('authToken', response.token);
      localStorage.setItem('authUser', JSON.stringify(response.user));
      setUser(response.user);
      setToken(response.token);
      setLoading(false);
      return response; // Return response for LoginPage to handle navigation
    } catch (error) {
      setLoading(false);
      throw error; // Re-throw for LoginPage to handle
    }
  };

  const logout = () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('authUser');
    setUser(null);
    setToken(null);
    navigate('/login', { replace: true });
  };

  const value = {
    user,
    token,
    isAuthenticated: !!token, // Derived state: true if token exists
    loading,
    login,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
