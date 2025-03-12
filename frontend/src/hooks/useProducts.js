import { useState, useEffect, useCallback } from 'react';
import productService from '../services/productService';

export const useProducts = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [category, setCategory] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [hasMore, setHasMore] = useState(true);
  const limit = 10;

  const fetchProducts = useCallback(async () => {
    try {
      setLoading(true);
      const data = await productService.getAllProducts({
        page,
        limit,
        category,
        search: searchQuery || null
      });
      
      if (page === 1) {
        setProducts(data);
      } else {
        setProducts(prev => [...prev, ...data]);
      }
      
      setHasMore(data.length === limit);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [page, category, searchQuery]);

  useEffect(() => {
    setPage(1);
    setProducts([]);
    fetchProducts();
  }, [category, searchQuery]);

  useEffect(() => {
    if (page > 1) {
      fetchProducts();
    }
  }, [page]);

  const getProductById = async (id) => {
    try {
      setLoading(true);
      const data = await productService.getProductById(id);
      return data;
    } catch (err) {
      setError(err.message);
      return null;
    } finally {
      setLoading(false);
    }
  };

  const loadMore = () => {
    if (!loading && hasMore) {
      setPage(prev => prev + 1);
    }
  };

  const filterByCategory = (newCategory) => {
    setCategory(newCategory);
  };

  const searchProducts = (query) => {
    setSearchQuery(query);
  };

  return {
    products,
    loading,
    error,
    hasMore,
    category,
    searchQuery,
    fetchProducts,
    getProductById,
    loadMore,
    filterByCategory,
    searchProducts
  };
};
