import api from './api';

const orderService = {
  async getAllOrders() {
    const response = await api.get('/api/v1/orders');
    return response.data;
  },

  async getOrderById(id) {
    const response = await api.get(`/api/v1/orders/${id}`);
    return response.data;
  },

  async createOrder(orderData) {
    const response = await api.post('/api/v1/orders', orderData);
    return response.data;
  },

  async updateOrder(id, orderData) {
    const response = await api.put(`/api/v1/orders/${id}`, orderData);
    return response.data;
  },

  async deleteOrder(id) {
    const response = await api.delete(`/api/v1/orders/${id}`);
    return response.data;
  }
};

export default orderService;