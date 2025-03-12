import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ProductProvider } from './context/ProductContext';

// Import pages
import HomePage from './pages/HomePage';
import ProductsPage from './pages/ProductsPage';
import ProductDetailPage from './pages/ProductDetailPage';
import NotFoundPage from './pages/NotFoundPage';

// Import components
import Layout from './components/Layout';

// Import styles
import './App.css';

/**
 * Main application component that sets up routing and context providers.
 * Wraps the entire application with necessary providers and defines routes.
 */
function App() {
  return (
    <ProductProvider>
      <Router>
        <Routes>
          <Route element={<Layout />}>
            {/* Home page route */}
            <Route path="/" element={<HomePage />} />
            
            {/* Products routes */}
            <Route path="/products" element={<ProductsPage />} />
            <Route path="/products/:id" element={<ProductDetailPage />} />
            
            {/* 404 Not Found route */}
            <Route path="*" element={<NotFoundPage />} />
          </Route>
        </Routes>
      </Router>
    </ProductProvider>
  );
}

export default App;