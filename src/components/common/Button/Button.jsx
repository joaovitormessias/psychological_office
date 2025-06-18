import React from 'react';

const Button = ({
  children,
  onClick,
  type = 'button',
  variant = 'primary', // primary, secondary, danger
  disabled = false,
  className = '',
}) => {
  const baseStyle = 'font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-150';

  const variants = {
    primary: 'bg-blue-500 hover:bg-blue-700 text-white',
    secondary: 'bg-gray-500 hover:bg-gray-700 text-white',
    danger: 'bg-red-500 hover:bg-red-700 text-white',
    outline_primary: 'bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white border border-blue-500 hover:border-transparent',
    outline_secondary: 'bg-transparent hover:bg-gray-500 text-gray-700 font-semibold hover:text-white border border-gray-500 hover:border-transparent',
  };

  const variantStyle = variants[variant] || variants.primary;

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`${baseStyle} ${variantStyle} ${className}`}
    >
      {children}
    </button>
  );
};

export default Button;
