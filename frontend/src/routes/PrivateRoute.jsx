import { Navigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

const PrivateRoute = ({ children, roles }) => {
  const { user } = useAuth();

  if (!user) return <Navigate to="/" />;

  if (roles && !roles.includes(user.role)) {
    return <Navigate to="/dashboard" />;
  }

  return children;
};

export default PrivateRoute;
