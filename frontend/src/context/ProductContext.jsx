import React, { createContext, useContext, useState } from 'react';
import { useProducts } from '../hooks/useProducts';

const ProductContext = createContext();

export const useProductContext = () => {
  const context = useContext(ProductContext);
  if (!context) {
    throw new Error('useProductContext must be used within a ProductProvider');
  }
  return context;
};

export const ProductProvider = ({ children }) => {
  const { products, loading, error, fetchProducts, getProductById } = useProducts();
  const [selectedProduct, setSelectedProduct] = useState(null);

  const value = {
    products,
    loading,
    error,
    fetchProducts,
    getProductById,
    selectedProduct,
    setSelectedProduct
  };

  return (
    <ProductContext.Provider value={value}>
      {children}
    </ProductContext.Provider>
  );
};