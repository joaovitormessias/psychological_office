import React from 'react';

const TableRow = ({ children, className = '', onClick }) => {
  const hoverClasses = onClick ? 'hover:bg-gray-100 cursor-pointer' : '';
  return (
    <tr className={`${hoverClasses} ${className}`} onClick={onClick}>
      {children}
    </tr>
  );
};

export default TableRow;
