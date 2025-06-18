import React from 'react';

const SelectBox = ({
  id,
  name,
  value,
  onChange,
  onBlur,
  disabled = false,
  options = [], // Array of { value: 'val', label: 'Label' }
  register, // from react-hook-form
  error, // boolean or message string
  className = '',
  placeholder = 'Select an option', // Optional placeholder
}) => {
  const baseClasses = "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline";
  const errorClasses = error ? "border-red-500" : "";
  const disabledClasses = disabled ? "bg-gray-200 cursor-not-allowed" : "";

  const selectProps = {
    id,
    name,
    disabled,
    className: `${baseClasses} ${errorClasses} ${disabledClasses} ${className}`,
  };

  const optionElements = options.map(option => (
    <option key={option.value} value={option.value}>
      {option.label}
    </option>
  ));

  if (placeholder) {
    optionElements.unshift(
      <option key="" value="" disabled>
        {placeholder}
      </option>
    );
  }

  if (register) {
    // If using react-hook-form
    return (
      <select {...selectProps} {...register(name)}>
        {optionElements}
      </select>
    );
  }

  // For controlled components
  selectProps.value = value;
  selectProps.onChange = onChange;
  selectProps.onBlur = onBlur;

  return (
    <select {...selectProps}>
      {optionElements}
    </select>
  );
};

export default SelectBox;
