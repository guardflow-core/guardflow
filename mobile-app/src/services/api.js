/**
 * GuardFlow API Service
 * Serviço para comunicação com o backend FastAPI
 */

import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Configuração base da API
const API_BASE_URL = __DEV__ 
  ? 'http://localhost:8002'  // Desenvolvimento
  : 'https://api.guardflow.app';  // Produção

// Criar instância do axios
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para adicionar token de autenticação
api.interceptors.request.use(
  async (config) => {
    try {
      const token = await AsyncStorage.getItem('auth_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    } catch (error) {
      console.error('Erro ao obter token:', error);
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para tratamento de respostas
api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    if (error.response?.status === 401) {
      // Token expirado ou inválido
      await AsyncStorage.removeItem('auth_token');
      await AsyncStorage.removeItem('user_data');
      // Redirecionar para login
    }
    return Promise.reject(error);
  }
);

// Serviços de autenticação
export const authService = {
  // Login
  async login(email, password) {
    try {
      const response = await api.post('/api/v1/auth/login', {
        email,
        password,
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Erro ao fazer login');
    }
  },

  // Registro
  async register(userData) {
    try {
      const response = await api.post('/api/v1/auth/register', userData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Erro ao registrar usuário');
    }
  },

  // Logout
  async logout() {
    try {
      await AsyncStorage.removeItem('auth_token');
      await AsyncStorage.removeItem('user_data');
      return true;
    } catch (error) {
      throw new Error('Erro ao fazer logout');
    }
  },

  // Verificar token
  async verifyToken() {
    try {
      const response = await api.get('/api/v1/auth/verify');
      return response.data;
    } catch (error) {
      throw new Error('Token inválido');
    }
  },
};

// Serviços de produtos
export const productService = {
  // Buscar produtos
  async getProducts(search = '', category = '') {
    try {
      const response = await api.get('/api/v1/products', {
        params: { search, category },
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Erro ao buscar produtos');
    }
  },

  // Buscar produto por ID
  async getProductById(id) {
    try {
      const response = await api.get(`/api/v1/products/${id}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Erro ao buscar produto');
    }
  },

  // Reconhecer produto por imagem
  async recognizeProduct(imageUri) {
    try {
      const formData = new FormData();
      formData.append('image', {
        uri: imageUri,
        type: 'image/jpeg',
        name: 'product.jpg',
      });

      const response = await api.post('/api/v1/products/recognize', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Erro ao reconhecer produto');
    }
  },
};

// Serviços de carrinho
export const cartService = {
  // Adicionar produto ao carrinho
  async addToCart(productId, quantity = 1) {
    try {
      const response = await api.post('/api/v1/cart/add', {
        product_id: productId,
        quantity,
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Erro ao adicionar ao carrinho');
    }
  },

  // Remover produto do carrinho
  async removeFromCart(productId) {
    try {
      const response = await api.delete(`/api/v1/cart/remove/${productId}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Erro ao remover do carrinho');
    }
  },

  // Atualizar quantidade
  async updateQuantity(productId, quantity) {
    try {
      const response = await api.put(`/api/v1/cart/update/${productId}`, {
        quantity,
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Erro ao atualizar quantidade');
    }
  },

  // Buscar carrinho
  async getCart() {
    try {
      const response = await api.get('/api/v1/cart');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Erro ao buscar carrinho');
    }
  },

  // Limpar carrinho
  async clearCart() {
    try {
      const response = await api.delete('/api/v1/cart/clear');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Erro ao limpar carrinho');
    }
  },
};

// Serviços de pagamento
export const paymentService = {
  // Processar pagamento
  async processPayment(paymentData) {
    try {
      const response = await api.post('/api/v1/payment/process', paymentData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Erro ao processar pagamento');
    }
  },

  // Gerar PIX
  async generatePix(amount) {
    try {
      const response = await api.post('/api/v1/payment/pix', { amount });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Erro ao gerar PIX');
    }
  },

  // Verificar status do pagamento
  async checkPaymentStatus(paymentId) {
    try {
      const response = await api.get(`/api/v1/payment/status/${paymentId}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Erro ao verificar status');
    }
  },
};

// Serviços ESG
export const esgService = {
  // Calcular score ESG
  async calculateEsgScore(products) {
    try {
      const response = await api.post('/api/v1/esg/calculate', { products });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Erro ao calcular score ESG');
    }
  },

  // Buscar dashboard ESG
  async getEsgDashboard() {
    try {
      const response = await api.get('/api/v1/esg/dashboard');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Erro ao buscar dashboard ESG');
    }
  },

  // Tokenizar compra
  async tokenizePurchase(purchaseData) {
    try {
      const response = await api.post('/api/v1/esg/tokenize', purchaseData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Erro ao tokenizar compra');
    }
  },
};

// Serviços de usuário
export const userService = {
  // Buscar perfil
  async getProfile() {
    try {
      const response = await api.get('/api/v1/user/profile');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Erro ao buscar perfil');
    }
  },

  // Atualizar perfil
  async updateProfile(userData) {
    try {
      const response = await api.put('/api/v1/user/profile', userData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Erro ao atualizar perfil');
    }
  },

  // Buscar histórico
  async getHistory() {
    try {
      const response = await api.get('/api/v1/user/history');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Erro ao buscar histórico');
    }
  },
};

// Health check
export const healthService = {
  async checkHealth() {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      throw new Error('Serviço indisponível');
    }
  },
};

export default api;


