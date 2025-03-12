import api from './api';

const productService = {
  async getAllProducts() {
    const response = await api.get('/api/v1/products');
    return response.data;
  },

  async getProductById(id) {
    const response = await api.get(`/api/v1/products/${id}`);
    return response.data;
  },

  async createProduct(productData) {
    const response = await api.post('/api/v1/products', productData);
    return response.data;
  },

  async updateProduct(id, productData) {
    const response = await api.put(`/api/v1/products/${id}`, productData);
    return response.data;
  },

  async deleteProduct(id) {
    const response = await api.delete(`/api/v1/products/${id}`);
    return response.data;
  }
};

export default productService;