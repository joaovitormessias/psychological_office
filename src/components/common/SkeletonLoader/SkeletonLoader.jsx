import React from 'react';

const SkeletonLoader = ({ type = 'text', lines = 3, className = '', count = 1 }) => {
  const pulseClass = 'bg-gray-300 animate-pulse';

  const renderTextLines = () => {
    return Array.from({ length: lines }).map((_, index) => (
      <div
        key={index}
        className={`${pulseClass} h-4 rounded mt-2 ${
          index === lines - 1 && lines > 1 ? 'w-3/4' : 'w-full' // Last line shorter
        }`}
      ></div>
    ));
  };

  const renderAvatar = () => (
    <div className={`${pulseClass} rounded-full h-12 w-12 ${className}`}></div>
  );

  const renderCard = () => (
    <div className={`p-4 border border-gray-200 rounded shadow ${className}`}>
      <div className={`${pulseClass} h-8 w-1/2 mb-4 rounded`}></div> {/* Title */}
      {renderTextLines()}
      <div className={`${pulseClass} h-10 w-1/3 mt-4 rounded`}></div> {/* Button/Action */}
    </div>
  );

  const renderCustom = () => (
    <div className={`${pulseClass} ${className}`}></div>
  );

  const skeletons = [];
  for (let i = 0; i < count; i++) {
    let skeletonContent;
    switch (type) {
      case 'text':
        skeletonContent = renderTextLines();
        break;
      case 'avatar':
        skeletonContent = renderAvatar();
        break;
      case 'card':
        skeletonContent = renderCard();
        break;
      case 'custom':
      default:
        skeletonContent = renderCustom();
        break;
    }
    skeletons.push(<div key={i} className={type !== 'custom' && type !== 'avatar' ? `w-full ${className}` : className}>{skeletonContent}</div>);
  }

  if (count > 1 && (type === 'text' || type === 'card')) {
    return <div className="space-y-4">{skeletons}</div>;
  }
  return <>{skeletons}</>;
};

export default SkeletonLoader;
