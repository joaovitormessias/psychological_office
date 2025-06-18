import React from 'react';

const Spinner = ({ size = 'md', color = 'text-blue-500', className = '' }) => {
  const sizes = {
    sm: 'w-4 h-4 border-2',
    md: 'w-8 h-8 border-4',
    lg: 'w-12 h-12 border-4',
  };

  const sizeClasses = sizes[size] || sizes.md;

  return (
    <div className="flex justify-center items-center">
      <div
        className={`animate-spin rounded-full ${sizeClasses} border-t-transparent border-solid ${color} ${className}`}
        style={{ borderTopColor: 'transparent' }} // Ensure the top border is transparent for the spin effect
      ></div>
    </div>
  );
};

export default Spinner;
