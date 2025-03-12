import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import { useProductContext } from '../context/ProductContext';

const ProductDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { getProductById } = useProductContext();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const data = await getProductById(id);
        setProduct(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, [id, getProductById]);

  const handleGoBack = () => {
    navigate('/products');
  };

  if (loading) {
    return (
      <Layout>
        <div className="min-h-screen">
          <LoadingSpinner size="large" message="Loading product details..." />
        </div>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout>
        <div className="p-4">
          <ErrorMessage 
            error={{ message: error }}
            onRetry={() => {
              setLoading(true);
              setError(null);
              getProductById(id)
                .then(data => setProduct(data))
                .catch(err => setError(err.message))
                .finally(() => setLoading(false));
            }}
          />
          <button
            onClick={handleGoBack}
            className="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            Back to Products
          </button>
        </div>
      </Layout>
    );
  }

  if (!product) {
    return (
      <Layout>
        <div className="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded relative" role="alert">
          <strong className="font-bold">Not Found!</strong>
          <span className="block sm:inline"> Product not found</span>
        </div>
        <button
          onClick={handleGoBack}
          className="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          Back to Products
        </button>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-4xl mx-auto px-4 py-8">
        <button
          onClick={handleGoBack}
          className="mb-6 bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded inline-flex items-center"
        >
          <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Back to Products
        </button>

        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="p-8">
            <h1 className="text-4xl font-bold mb-4 text-gray-900">{product.name}</h1>
            <div className="border-b border-gray-200 mb-6"></div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div>
                <h2 className="text-xl font-semibold mb-4 text-gray-700">Product Details</h2>
                <p className="text-gray-600 mb-6 leading-relaxed">{product.description}</p>
                
                <div className="space-y-4">
                  <div className="flex items-center">
                    <span className="text-gray-600 font-medium w-24">SKU:</span>
                    <span className="text-gray-800">{product.sku}</span>
                  </div>
                  <div className="flex items-center">
                    <span className="text-gray-600 font-medium w-24">Category:</span>
                    <span className="text-gray-800">{product.category}</span>
                  </div>
                </div>
              </div>
              
              <div className="bg-gray-50 p-6 rounded-lg">
                <div className="mb-6">
                  <span className="text-3xl font-bold text-blue-600">${product.price}</span>
                  {product.price_currency && (
                    <span className="text-gray-500 ml-2">{product.price_currency}</span>
                  )}
                </div>
                
                <div className="space-y-4">
                  <div className="flex items-center">
                    <span className="text-gray-600 font-medium w-32">Stock Status:</span>
                    <span className={`font-semibold ${product.inventory_count > 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {product.inventory_count > 0 ? 'In Stock' : 'Out of Stock'}
                    </span>
                  </div>
                  <div className="flex items-center">
                    <span className="text-gray-600 font-medium w-32">Inventory Count:</span>
                    <span className="text-gray-800">{product.inventory_count}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default ProductDetailPage;
