import React from 'react';

const Table = ({ headers = [], children, className = '' }) => {
  return (
    <div className={`overflow-x-auto shadow-md sm:rounded-lg ${className}`}>
      <table className="min-w-full divide-y divide-gray-200 bg-white text-sm">
        <thead className="bg-gray-50">
          <tr>
            {headers.map((header, index) => (
              <th
                key={index}
                scope="col"
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                {typeof header === 'object' ? header.label : header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {children}
        </tbody>
      </table>
    </div>
  );
};

export default Table;
