/**
 * Configuration settings for the frontend application.
 * Contains environment-specific settings and API configuration.
 */

// Base URL for the backend API
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// API version path
export const API_VERSION = '/api/v1';

// Full API URL
export const API_URL = `${API_BASE_URL}${API_VERSION}`;

// API endpoints
export const API_ENDPOINTS = {
  products: `${API_URL}/products`,
  orders: `${API_URL}/orders`,
  health: `${API_BASE_URL}/health`,
};

// Application settings
export const APP_CONFIG = {
  name: 'Products and Orders',
  version: '1.0.0',
  defaultPageSize: 10,
};