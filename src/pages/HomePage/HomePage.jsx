// src/pages/HomePage/HomePage.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import useAuth from '../../hooks/useAuth';
// import { Button } from '../../components/common'; // If using Button for cards

const HomePage = () => {
  const { user, logout } = useAuth();

  const secretaryModules = [
    { name: "Manage Patients", path: "/patients", description: "View, edit, and manage patient records." },
    { name: "Add New Patient", path: "/patients/add", description: "Register a new patient in the system." },
    // { name: "Schedule Appointments", path: "/appointments/schedule", description: "Schedule new appointments for patients." },
  ];

  const professionalModules = [
    { name: "View Patients", path: "/patients", description: "Access patient records and history." },
    // { name: "My Schedule", path: "/my-schedule", description: "View your upcoming appointments." },
    // { name: "Conduct Consultation", path: "/consultations/active", description: "Start or continue patient consultations." }
  ];

  const modules = user?.role === 'SECRETARIA' ? secretaryModules :
                  user?.role === 'PROFISSIONAL_SAUDE' ? professionalModules : [];

  return (
    <div className="p-6 bg-gray-50 min-h-[calc(100vh-theme(spacing.32))]"> {/* Adjust min-height based on layout */}
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-8">
            <div>
                <h1 className="text-3xl font-bold text-gray-800">Welcome, {user?.name || 'User'}!</h1>
                <p className="text-md text-gray-600">Your role: <span className="font-semibold">{user?.role}</span></p>
                <p className="mt-1 text-gray-600">Select a module to get started.</p>
            </div>
            <button
                onClick={logout}
                className="bg-red-500 hover:bg-red-600 text-white font-semibold py-2 px-4 rounded-lg shadow hover:shadow-md transition duration-150 ease-in-out"
            >
                Logout
            </button>
        </div>

        {modules.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {modules.map((mod) => (
              <Link
                key={mod.name}
                to={mod.path}
                className="block p-6 bg-white rounded-xl shadow-lg hover:shadow-2xl transform hover:-translate-y-1 transition-all duration-300 ease-in-out"
              >
                <h2 className="text-xl font-semibold text-blue-600 mb-2">{mod.name}</h2>
                <p className="text-gray-600 text-sm">{mod.description}</p>
              </Link>
            ))}
          </div>
        ) : (
          <p className="text-center text-gray-500">No modules available for your role or role not defined.</p>
        )}
      </div>
    </div>
  );
};

export default HomePage;
