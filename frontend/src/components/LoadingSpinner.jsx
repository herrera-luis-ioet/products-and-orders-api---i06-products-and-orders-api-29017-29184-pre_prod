import React from 'react';
import PropTypes from 'prop-types';

const LoadingSpinner = ({ size = 'medium', message = 'Loading...' }) => {
  const spinnerSizes = {
    small: 'w-4 h-4',
    medium: 'w-8 h-8',
    large: 'w-12 h-12'
  };

  return (
    <div className="flex flex-col items-center justify-center p-4">
      <div
        className={`${spinnerSizes[size]} border-4 border-gray-200 rounded-full animate-spin border-t-blue-600`}
        role="status"
        aria-label="loading"
      />
      {message && (
        <p className="mt-2 text-gray-600">{message}</p>
      )}
    </div>
  );
};

LoadingSpinner.propTypes = {
  size: PropTypes.oneOf(['small', 'medium', 'large']),
  message: PropTypes.string
};

export default LoadingSpinner;