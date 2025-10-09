/**
 * Teste de conexão com o backend
 */

import { healthService } from './api';

export const testConnection = async () => {
  try {
    console.log('🔍 Testando conexão com o backend...');
    
    const response = await healthService.checkHealth();
    console.log('✅ Conexão com backend estabelecida:', response);
    
    return {
      success: true,
      data: response,
    };
  } catch (error) {
    console.error('❌ Erro ao conectar com backend:', error);
    return {
      success: false,
      error: error.message,
    };
  }
};

export default testConnection;


