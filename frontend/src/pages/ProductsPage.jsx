import React from 'react';
import Layout from '../components/Layout';
import ProductList from '../components/ProductList';

const ProductsPage = () => {
  return (
    <Layout>
      <div>
        <h1 className="text-3xl font-bold mb-8">All Products</h1>
        <ProductList />
      </div>
    </Layout>
  );
};

export default ProductsPage;