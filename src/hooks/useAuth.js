import { useContext } from 'react';
import AuthContext from '../contexts/AuthContext'; // Adjust path if your context is elsewhere

const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined || context === null) {
    // null check also because AuthContext is initialized with null
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default useAuth;
