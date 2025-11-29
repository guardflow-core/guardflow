/**
 * Teste de conexão com o backend
 */

import { mockApi } from '../services/mockApi';

export const testConnection = async (): Promise<{ success: boolean; data?: any; error?: string }> => {
  try {
    console.log('🔍 Testando conexão com o backend...');
    
    const response = await mockApi.health();
    console.log('✅ Conexão com backend estabelecida:', response);
    
    return {
      success: true,
      data: response.data,
    };
  } catch (error: any) {
    console.error('❌ Erro ao conectar com backend:', error);
    return {
      success: false,
      error: error.message,
    };
  }
};

export default testConnection;


