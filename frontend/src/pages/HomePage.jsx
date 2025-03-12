import React from 'react';
import Layout from '../components/Layout';
import ProductList from '../components/ProductList';

const HomePage = () => {
  return (
    <Layout>
      <div>
        <h1 className="text-3xl font-bold mb-8">Featured Products</h1>
        <ProductList />
      </div>
    </Layout>
  );
};

export default HomePage;