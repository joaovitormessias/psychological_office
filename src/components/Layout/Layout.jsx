import React from 'react';
import { Outlet } from 'react-router-dom';
import { ToastContainer } from 'react-toastify'; // Import

const Layout = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-gray-800 text-white p-4">
        <h1 className="text-xl">Psychology Clinic App</h1>
        {/* Navigation links can be added here later */}
      </header>
      <main className="flex-grow p-4 bg-gray-100">
        <Outlet /> {/* Child routes will render here */}
      </main>
      <footer className="bg-gray-700 text-white p-3 text-center">
        <p>&copy; 2023 ClinicName</p>
      </footer>
      <ToastContainer /> {/* Add ToastContainer here */}
    </div>
  );
};

export default Layout;
