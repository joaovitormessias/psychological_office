// src/pages/LoginPage/LoginPage.jsx
import React from 'react';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import useAuth from '../../hooks/useAuth'; // Changed from AuthService
import { useNavigate } from 'react-router-dom'; // Added useNavigate

const schema = yup.object().shape({
  email: yup.string().email('Invalid email format').required('Email is required'),
  password: yup.string().min(6, 'Password must be at least 6 characters').required('Password is required'),
});

const LoginPage = () => {
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm({
    resolver: yupResolver(schema),
  });
  const { login: authLogin } = useAuth(); // Get login from useAuth
  const navigate = useNavigate(); // Initialize useNavigate

  const onSubmit = async (data) => {
    try {
      // authLogin (from AuthContext) now handles setting user/token and localStorage
      // It also returns the user object (which includes the role) upon successful login
      const loggedInUser = await authLogin(data.email, data.password);
      console.log('Login successful via context. Role:', loggedInUser.user.role); // Access role from user object within response

      if (loggedInUser.user.role === "SECRETARIA") {
        navigate('/secretary-dashboard', { replace: true });
      } else if (loggedInUser.user.role === "PROFISSIONAL_SAUDE") {
        navigate('/professional-dashboard', { replace: true });
      } else {
        console.warn("Unknown role or no role defined, navigating to /home");
        navigate('/home', { replace: true }); // Fallback
      }
    } catch (error) {
      console.error('Login failed via context:', error.message); // Error from authLogin
      alert(`Login Failed: ${error.message}`); // Placeholder for user feedback
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
        <h2 className="text-2xl font-bold text-center text-gray-700 mb-6">Login</h2>
        <form onSubmit={handleSubmit(onSubmit)}>
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="email">
              Email
            </label>
            <input
              type="email"
              id="email"
              {...register('email')}
              className={`shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline ${errors.email ? 'border-red-500' : ''}`}
            />
            {errors.email && <p className="text-red-500 text-xs italic mt-1">{errors.email.message}</p>}
          </div>

          <div className="mb-6">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="password">
              Password
            </label>
            <input
              type="password"
              id="password"
              {...register('password')}
              className={`shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline ${errors.password ? 'border-red-500' : ''}`}
            />
            {errors.password && <p className="text-red-500 text-xs italic mt-1">{errors.password.message}</p>}
          </div>

          <div className="flex items-center justify-between">
            <button
              type="submit"
              disabled={isSubmitting}
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline disabled:bg-gray-400"
            >
              {isSubmitting ? 'Logging in...' : 'Login'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;
