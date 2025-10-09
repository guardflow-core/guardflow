/**
 * GuardFlow Web API Service
 * Serviço para comunicação com o backend FastAPI
 */

import axios, { AxiosInstance, AxiosResponse } from 'axios';

// Configuração base da API
const API_BASE_URL = process.env.NODE_ENV === 'development' 
  ? 'http://localhost:8002'  // Desenvolvimento
  : 'https://api.guardflow.app';  // Produção

// Criar instância do axios
const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para adicionar token de autenticação
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
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
  (error) => {
    if (error.response?.status === 401) {
      // Token expirado ou inválido
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user_data');
      // Redirecionar para login
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Interfaces TypeScript
export interface User {
  id: string;
  email: string;
  name: string;
  role: string;
  created_at: string;
  updated_at: string;
}

export interface Product {
  id: string;
  barcode: string;
  name: string;
  brand: string;
  category: string;
  price: string;
  esg_score: number;
  stock_quantity: number;
  is_active: boolean;
  is_available: boolean;
  image_url?: string;
  created_at: string;
  updated_at: string;
}

export interface CartItem {
  id: string;
  product_id: string;
  product: Product;
  quantity: number;
  price: string;
  total: string;
  created_at: string;
}

export interface ScanEvent {
  id: string;
  barcode?: string;
  product_id?: string;
  product?: Product;
  confidence: number;
  scan_duration_ms: number;
  successful: boolean;
  recognition_method: string;
  created_at: string;
}

export interface EsgScore {
  environmental: number;
  social: number;
  governance: number;
  total: number;
  level: string;
}

// Serviços de autenticação
export const authService = {
  // Login
  async login(email: string, password: string): Promise<{ success: boolean; user?: User; token?: string; message?: string }> {
    try {
      const response: AxiosResponse = await api.post('/api/v1/auth/login', {
        email,
        password,
      });
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Erro ao fazer login');
    }
  },

  // Registro
  async register(userData: any): Promise<{ success: boolean; user?: User; token?: string; message?: string }> {
    try {
      const response: AxiosResponse = await api.post('/api/v1/auth/register', userData);
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Erro ao registrar usuário');
    }
  },

  // Logout
  async logout(): Promise<{ success: boolean }> {
    try {
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user_data');
      return { success: true };
    } catch (error) {
      throw new Error('Erro ao fazer logout');
    }
  },

  // Verificar token
  async verifyToken(): Promise<{ success: boolean; user?: User }> {
    try {
      const response: AxiosResponse = await api.get('/api/v1/auth/verify');
      return response.data;
    } catch (error) {
      throw new Error('Token inválido');
    }
  },
};

// Serviços de produtos
export const productService = {
  // Buscar produtos
  async getProducts(search: string = '', category: string = ''): Promise<{ success: boolean; data?: Product[]; message?: string }> {
    try {
      const response: AxiosResponse = await api.get('/api/v1/products', {
        params: { search, category },
      });
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Erro ao buscar produtos');
    }
  },

  // Buscar produto por ID
  async getProductById(id: string): Promise<{ success: boolean; data?: Product; message?: string }> {
    try {
      const response: AxiosResponse = await api.get(`/api/v1/products/${id}`);
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Erro ao buscar produto');
    }
  },

  // Reconhecer produto por imagem
  async recognizeProduct(imageFile: File): Promise<{ success: boolean; data?: Product; message?: string }> {
    try {
      const formData = new FormData();
      formData.append('image', imageFile);

      const response: AxiosResponse = await api.post('/api/v1/products/recognize', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Erro ao reconhecer produto');
    }
  },
};

// Serviços de carrinho
export const cartService = {
  // Adicionar produto ao carrinho
  async addToCart(productId: string, quantity: number = 1): Promise<{ success: boolean; data?: CartItem; message?: string }> {
    try {
      const response: AxiosResponse = await api.post('/api/v1/cart/add', {
        product_id: productId,
        quantity,
      });
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Erro ao adicionar ao carrinho');
    }
  },

  // Remover produto do carrinho
  async removeFromCart(productId: string): Promise<{ success: boolean; message?: string }> {
    try {
      const response: AxiosResponse = await api.delete(`/api/v1/cart/remove/${productId}`);
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Erro ao remover do carrinho');
    }
  },

  // Atualizar quantidade
  async updateQuantity(productId: string, quantity: number): Promise<{ success: boolean; data?: CartItem; message?: string }> {
    try {
      const response: AxiosResponse = await api.put(`/api/v1/cart/update/${productId}`, {
        quantity,
      });
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Erro ao atualizar quantidade');
    }
  },

  // Buscar carrinho
  async getCart(): Promise<{ success: boolean; data?: CartItem[]; message?: string }> {
    try {
      const response: AxiosResponse = await api.get('/api/v1/cart');
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Erro ao buscar carrinho');
    }
  },

  // Limpar carrinho
  async clearCart(): Promise<{ success: boolean; message?: string }> {
    try {
      const response: AxiosResponse = await api.delete('/api/v1/cart/clear');
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Erro ao limpar carrinho');
    }
  },
};

// Serviços ESG
export const esgService = {
  // Calcular score ESG
  async calculateEsgScore(products: Product[]): Promise<{ success: boolean; data?: EsgScore; message?: string }> {
    try {
      const response: AxiosResponse = await api.post('/api/v1/esg/calculate', { products });
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Erro ao calcular score ESG');
    }
  },

  // Buscar dashboard ESG
  async getEsgDashboard(): Promise<{ success: boolean; data?: any; message?: string }> {
    try {
      const response: AxiosResponse = await api.get('/api/v1/esg/dashboard');
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Erro ao buscar dashboard ESG');
    }
  },

  // Tokenizar compra
  async tokenizePurchase(purchaseData: any): Promise<{ success: boolean; data?: any; message?: string }> {
    try {
      const response: AxiosResponse = await api.post('/api/v1/esg/tokenize', purchaseData);
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Erro ao tokenizar compra');
    }
  },
};

// Serviços de scanner
export const scannerService = {
  // Escanear produto
  async scanProduct(imageFile: File, storeId?: string): Promise<{ success: boolean; data?: any; message?: string }> {
    try {
      const formData = new FormData();
      formData.append('image', imageFile);
      if (storeId) {
        formData.append('store_id', storeId);
      }

      const response: AxiosResponse = await api.post('/api/v1/scanner/scan', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Erro ao escanear produto');
    }
  },

  // Escanear código de barras
  async scanBarcode(barcode: string, storeId?: string): Promise<{ success: boolean; data?: any; message?: string }> {
    try {
      const response: AxiosResponse = await api.post('/api/v1/scanner/scan-barcode', {
        barcode,
        store_id: storeId,
      });
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Erro ao escanear código de barras');
    }
  },

  // Histórico de escaneamentos
  async getScanHistory(limit: number = 20, offset: number = 0): Promise<{ success: boolean; data?: ScanEvent[]; message?: string }> {
    try {
      const response: AxiosResponse = await api.get('/api/v1/scanner/history', {
        params: { limit, offset },
      });
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Erro ao buscar histórico');
    }
  },

  // Estatísticas de escaneamento
  async getScanStats(): Promise<{ success: boolean; data?: any; message?: string }> {
    try {
      const response: AxiosResponse = await api.get('/api/v1/scanner/stats');
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Erro ao buscar estatísticas');
    }
  },
};

// Health check
export const healthService = {
  async checkHealth(): Promise<{ status: string; service: string; version: string }> {
    try {
      const response: AxiosResponse = await api.get('/health');
      return response.data;
    } catch (error) {
      throw new Error('Serviço indisponível');
    }
  },
};

export default api;


