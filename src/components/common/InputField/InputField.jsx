import React from 'react';

const InputField = ({
  id,
  name,
  type = 'text',
  placeholder,
  value,
  onChange,
  onBlur,
  disabled = false,
  register, // from react-hook-form
  error, // boolean or message string
  className = '',
}) => {
  const baseClasses = "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline";
  const errorClasses = error ? "border-red-500" : "";
  const disabledClasses = disabled ? "bg-gray-200 cursor-not-allowed" : "";

  const inputProps = {
    id,
    name,
    type,
    placeholder,
    disabled,
    className: `${baseClasses} ${errorClasses} ${disabledClasses} ${className}`,
  };

  if (register) {
    // If using react-hook-form, spread its props
    return <input {...inputProps} {...register(name)} />;
  }

  // For controlled components (value/onChange)
  inputProps.value = value;
  inputProps.onChange = onChange;
  inputProps.onBlur = onBlur;

  return <input {...inputProps} />;
};

export default InputField;
