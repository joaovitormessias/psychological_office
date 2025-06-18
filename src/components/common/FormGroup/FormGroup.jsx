import React from 'react';

const FormGroup = ({ label, htmlFor, error, children, className = '' }) => {
  return (
    <div className={`mb-4 ${className}`}>
      {label && (
        <label htmlFor={htmlFor} className="block text-gray-700 text-sm font-bold mb-2">
          {label}
        </label>
      )}
      {children}
      {error && <p className="text-red-500 text-xs italic mt-1">{typeof error === 'string' ? error : 'This field has an error.'}</p>}
    </div>
  );
};

export default FormGroup;
