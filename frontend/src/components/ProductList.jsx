import React, { useState, useEffect } from 'react';
import ProductCard from './ProductCard';
import { useProductContext } from '../context/ProductContext';

const ProductList = () => {
  const {
    products,
    loading,
    error,
    hasMore,
    category,
    searchQuery,
    loadMore,
    filterByCategory,
    searchProducts
  } = useProductContext();

  const [searchInput, setSearchInput] = useState('');
  const [debouncedSearch, setDebouncedSearch] = useState('');

  // Debounce search input
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedSearch(searchInput);
    }, 500);

    return () => clearTimeout(timer);
  }, [searchInput]);

  // Apply debounced search
  useEffect(() => {
    searchProducts(debouncedSearch);
  }, [debouncedSearch, searchProducts]);

  const handleSearchChange = (e) => {
    setSearchInput(e.target.value);
  };

  const handleCategoryChange = (e) => {
    filterByCategory(e.target.value === 'all' ? null : e.target.value);
  };

  const categories = ['Electronics', 'Clothing', 'Books', 'Home & Garden']; // Add your categories here

  return (
    <div className="space-y-6">
      {/* Search and Filter Controls */}
      <div className="flex flex-col md:flex-row gap-4">
        <div className="flex-1">
          <input
            type="text"
            placeholder="Search products..."
            value={searchInput}
            onChange={handleSearchChange}
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div className="w-full md:w-48">
          <select
            value={category || 'all'}
            onChange={handleCategoryChange}
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Categories</option>
            {categories.map((cat) => (
              <option key={cat} value={cat}>
                {cat}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Loading State */}
      {loading && products.length === 0 && (
        <div className="flex justify-center items-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          Error: {error}
        </div>
      )}

      {/* Empty State */}
      {!loading && !error && products.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          <p className="text-xl">No products found</p>
          <p className="mt-2">Try adjusting your search or filters</p>
        </div>
      )}

      {/* Product Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {products.map((product) => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>

      {/* Load More Button */}
      {hasMore && !loading && !error && (
        <div className="flex justify-center mt-8">
          <button
            onClick={loadMore}
            className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Load More
          </button>
        </div>
      )}

      {/* Loading More Indicator */}
      {loading && products.length > 0 && (
        <div className="flex justify-center mt-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
        </div>
      )}
    </div>
  );
};

export default ProductList;
