import React from 'react';
import { Link } from 'react-router-dom';

const ProductCard = ({ product }) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-4 transition-transform hover:scale-105">
      <div className="relative pb-2">
        {product.category && (
          <span className="absolute top-0 right-0 bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded">
            {product.category}
          </span>
        )}
        <h3 className="text-lg font-semibold mb-2">{product.name}</h3>
        <p className="text-gray-600 mb-2 line-clamp-2">{product.description}</p>
      </div>
      <div className="flex justify-between items-center mb-4">
        <p className="text-lg font-bold text-blue-600">${product.price}</p>
        {product.stock > 0 ? (
          <span className="text-green-600 text-sm">In Stock ({product.stock})</span>
        ) : (
          <span className="text-red-600 text-sm">Out of Stock</span>
        )}
      </div>
      <div className="mt-4">
        <Link
          to={`/products/${product.id}`}
          className="block text-center bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors"
        >
          View Details
        </Link>
      </div>
    </div>
  );
};

export default ProductCard;
