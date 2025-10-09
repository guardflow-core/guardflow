/**
 * GuardFlow Authentication Service
 * Serviço de autenticação com JWT e biometria
 */

import AsyncStorage from '@react-native-async-storage/async-storage';
import { authService } from './api';
import { BiometricAuth } from '../utils/biometricAuth';

class AuthService {
  constructor() {
    this.isAuthenticated = false;
    this.user = null;
    this.token = null;
  }

  // Login com email e senha
  async login(email, password) {
    try {
      const response = await authService.login(email, password);
      
      if (response.success) {
        // Salvar token e dados do usuário
        await AsyncStorage.setItem('auth_token', response.data.token);
        await AsyncStorage.setItem('user_data', JSON.stringify(response.data.user));
        
        this.isAuthenticated = true;
        this.user = response.data.user;
        this.token = response.data.token;
        
        return {
          success: true,
          user: response.data.user,
          token: response.data.token,
        };
      } else {
        throw new Error(response.message || 'Erro ao fazer login');
      }
    } catch (error) {
      throw new Error(error.message || 'Erro ao fazer login');
    }
  }

  // Registro de usuário
  async register(userData) {
    try {
      const response = await authService.register(userData);
      
      if (response.success) {
        // Salvar token e dados do usuário
        await AsyncStorage.setItem('auth_token', response.data.token);
        await AsyncStorage.setItem('user_data', JSON.stringify(response.data.user));
        
        this.isAuthenticated = true;
        this.user = response.data.user;
        this.token = response.data.token;
        
        return {
          success: true,
          user: response.data.user,
          token: response.data.token,
        };
      } else {
        throw new Error(response.message || 'Erro ao registrar usuário');
      }
    } catch (error) {
      throw new Error(error.message || 'Erro ao registrar usuário');
    }
  }

  // Login com biometria
  async loginWithBiometrics() {
    try {
      // Verificar se biometria está disponível
      const isAvailable = await BiometricAuth.isAvailable();
      if (!isAvailable) {
        throw new Error('Biometria não disponível');
      }

      // Autenticar com biometria
      const biometricResult = await BiometricAuth.authenticate();
      if (!biometricResult.success) {
        throw new Error('Autenticação biométrica falhou');
      }

      // Buscar dados salvos
      const savedUser = await AsyncStorage.getItem('user_data');
      const savedToken = await AsyncStorage.getItem('auth_token');
      
      if (savedUser && savedToken) {
        this.isAuthenticated = true;
        this.user = JSON.parse(savedUser);
        this.token = savedToken;
        
        return {
          success: true,
          user: this.user,
          token: this.token,
        };
      } else {
        throw new Error('Dados de usuário não encontrados');
      }
    } catch (error) {
      throw new Error(error.message || 'Erro na autenticação biométrica');
    }
  }

  // Logout
  async logout() {
    try {
      await AsyncStorage.removeItem('auth_token');
      await AsyncStorage.removeItem('user_data');
      
      this.isAuthenticated = false;
      this.user = null;
      this.token = null;
      
      return { success: true };
    } catch (error) {
      throw new Error('Erro ao fazer logout');
    }
  }

  // Verificar se está autenticado
  async checkAuth() {
    try {
      const token = await AsyncStorage.getItem('auth_token');
      const userData = await AsyncStorage.getItem('user_data');
      
      if (token && userData) {
        // Verificar se o token ainda é válido
        try {
          await authService.verifyToken();
          
          this.isAuthenticated = true;
          this.user = JSON.parse(userData);
          this.token = token;
          
          return {
            isAuthenticated: true,
            user: this.user,
            token: this.token,
          };
        } catch (error) {
          // Token inválido, limpar dados
          await this.logout();
          return { isAuthenticated: false };
        }
      } else {
        this.isAuthenticated = false;
        this.user = null;
        this.token = null;
        return { isAuthenticated: false };
      }
    } catch (error) {
      this.isAuthenticated = false;
      this.user = null;
      this.token = null;
      return { isAuthenticated: false };
    }
  }

  // Obter dados do usuário
  getUser() {
    return this.user;
  }

  // Obter token
  getToken() {
    return this.token;
  }

  // Verificar se está autenticado
  isLoggedIn() {
    return this.isAuthenticated;
  }

  // Atualizar dados do usuário
  async updateUser(userData) {
    try {
      await AsyncStorage.setItem('user_data', JSON.stringify(userData));
      this.user = userData;
      return { success: true };
    } catch (error) {
      throw new Error('Erro ao atualizar dados do usuário');
    }
  }

  // Configurar biometria
  async setupBiometrics() {
    try {
      const isAvailable = await BiometricAuth.isAvailable();
      if (!isAvailable) {
        throw new Error('Biometria não disponível');
      }

      const result = await BiometricAuth.authenticate();
      if (result.success) {
        await AsyncStorage.setItem('biometric_enabled', 'true');
        return { success: true };
      } else {
        throw new Error('Configuração de biometria falhou');
      }
    } catch (error) {
      throw new Error(error.message || 'Erro ao configurar biometria');
    }
  }

  // Verificar se biometria está habilitada
  async isBiometricEnabled() {
    try {
      const enabled = await AsyncStorage.getItem('biometric_enabled');
      return enabled === 'true';
    } catch (error) {
      return false;
    }
  }
}

// Exportar instância única
export default new AuthService();


