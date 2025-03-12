import api from './api';

const productService = {
  async getAllProducts({ page = 1, limit = 10, category = null, search = null } = {}) {
    const skip = (page - 1) * limit;
    let url = `/api/v1/products?skip=${skip}&limit=${limit}`;

    if (search) {
      url = `/api/v1/products/search/?query=${encodeURIComponent(search)}&skip=${skip}&limit=${limit}`;
    } else if (category) {
      url = `/api/v1/products/category/${encodeURIComponent(category)}?skip=${skip}&limit=${limit}`;
    }

    const response = await api.get(url);
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
