import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import useAuth from './hooks/useAuth';
import { Layout } from './components/Layout';
import { LoginPage } from './pages/LoginPage';
import { PrivateRoute } from './components/PrivateRoute';
import { SecretaryDashboardPage } from './pages/SecretaryDashboardPage';
import { HealthProfessionalDashboardPage } from './pages/HealthProfessionalDashboardPage';
import { HomePage } from './pages/HomePage'; // Import new HomePage
import { PatientListPage } from './pages/PatientListPage'; // Import PatientListPage

// AppContent will contain the routing logic and can use useAuth
const AppContent = () => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center text-xl">Loading App...</div>;
  }

  return (
    <Routes>
      <Route
        path="/login"
        element={isAuthenticated ? <Navigate replace to="/home" /> : <LoginPage />}
      />
      <Route element={<PrivateRoute />}> {/* Protected routes wrapper */}
        <Route element={<Layout />}> {/* Layout for protected pages */}
          <Route path="/" element={<Navigate replace to="/home" />} />
          <Route path="/home" element={<HomePage />} />
          <Route path="/secretary-dashboard" element={<SecretaryDashboardPage />} />
          <Route path="/professional-dashboard" element={<HealthProfessionalDashboardPage />} />
          <Route path="/patients" element={<PatientListPage />} /> {/* Add Patient List Route */}
          {/* Other protected routes will go here */}
        </Route>
      </Route>
      <Route path="*" element={<div className="p-4 text-center">404 - Page Not Found</div>} /> {/* Catch-all */}
    </Routes>
  );
};

function App() {
  return (
    <Router>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </Router>
  );
}

export default App;
