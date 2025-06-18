// src/services/NotificationService.js
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css'; // Import CSS

// Default options (optional)
const defaultOptions = {
  position: "top-right",
  autoClose: 5000,
  hideProgressBar: false,
  closeOnClick: true,
  pauseOnHover: true,
  draggable: true,
  progress: undefined,
  theme: "light", // or "colored", "dark"
};

export const showSuccessToast = (message, options = {}) => {
  toast.success(message, { ...defaultOptions, ...options });
};

export const showErrorToast = (message, options = {}) => {
  toast.error(message, { ...defaultOptions, ...options });
};

export const showInfoToast = (message, options = {}) => {
  toast.info(message, { ...defaultOptions, ...options });
};

export const showWarningToast = (message, options = {}) => {
  toast.warn(message, { ...defaultOptions, ...options });
};
