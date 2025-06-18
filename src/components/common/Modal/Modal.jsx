import React, { useEffect } from 'react';

const Modal = ({
  isOpen,
  onClose,
  title,
  children,
  footerContent,
}) => {
  useEffect(() => {
    const handleEsc = (event) => {
      if (event.keyCode === 27) {
        onClose();
      }
    };
    if (isOpen) {
      window.addEventListener('keydown', handleEsc);
    }
    return () => {
      window.removeEventListener('keydown', handleEsc);
    };
  }, [isOpen, onClose]);

  if (!isOpen) {
    return null;
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 transition-opacity duration-300 ease-in-out">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full m-4 transform transition-all duration-300 ease-in-out scale-100">
        {/* Modal Header */}
        {title && (
          <div className="flex items-start justify-between p-5 border-b border-solid border-gray-300 rounded-t">
            <h3 className="text-xl font-semibold text-gray-700">{title}</h3>
            <button
              className="p-1 ml-auto bg-transparent border-0 text-black opacity-50 float-right text-3xl leading-none font-semibold outline-none focus:outline-none hover:opacity-75"
              onClick={onClose}
              aria-label="Close modal"
            >
              <span className="bg-transparent text-black h-6 w-6 text-2xl block outline-none focus:outline-none">×</span>
            </button>
          </div>
        )}

        {/* Modal Body */}
        <div className="relative p-6 flex-auto max-h-96 overflow-y-auto">
          {children}
        </div>

        {/* Modal Footer */}
        {footerContent && (
          <div className="flex items-center justify-end p-6 border-t border-solid border-gray-300 rounded-b">
            {footerContent}
          </div>
        )}
      </div>
    </div>
  );
};

export default Modal;
