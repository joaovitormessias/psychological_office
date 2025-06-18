// src/pages/HealthProfessionalDashboardPage/HealthProfessionalDashboardPage.jsx
import React from 'react';
import useAuth from '../../hooks/useAuth';

const HealthProfessionalDashboardPage = () => {
  const { user, logout } = useAuth();
  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold text-green-700 mb-4">Health Professional Dashboard</h2>
      <p className="text-lg">Welcome, {user?.name || 'Health Professional'}!</p>
      <p>This is your dedicated dashboard.</p>
      {/* Add Professional-specific components/links here */}
      <button
        onClick={logout}
        className="mt-6 bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
      >
        Logout
      </button>
    </div>
  );
};
export default HealthProfessionalDashboardPage;
