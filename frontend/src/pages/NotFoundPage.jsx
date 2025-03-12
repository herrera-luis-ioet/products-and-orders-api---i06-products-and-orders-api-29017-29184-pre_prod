import React from 'react';
import { Link } from 'react-router-dom';
import Layout from '../components/Layout';

const NotFoundPage = () => {
  return (
    <Layout>
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">404 - Page Not Found</h1>
        <p className="text-gray-600 mb-8">
          The page you are looking for does not exist.
        </p>
        <Link
          to="/"
          className="bg-blue-500 text-white px-6 py-3 rounded hover:bg-blue-600"
        >
          Go Home
        </Link>
      </div>
    </Layout>
  );
};

export default NotFoundPage;