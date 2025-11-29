/**
 * GuardFlow Advanced Biometric Authentication
 * Utilitário avançado para autenticação biométrica com recursos estendidos
 */

import * as LocalAuthentication from 'expo-local-authentication';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Alert } from 'react-native';

class AdvancedBiometricAuth {
  constructor() {
    this.isSupported = false;
    this.availableTypes = [];
    this.isEnrolled = false;
    this.securityLevel = null;
    this.init();
  }

  async init() {
    try {
      // Verificar se o dispositivo suporta autenticação biométrica
      this.isSupported = await LocalAuthentication.hasHardwareAsync();
      
      if (this.isSupported) {
        // Verificar tipos de autenticação disponíveis
        this.availableTypes = await LocalAuthentication.supportedAuthenticationTypesAsync();
        
        // Verificar se há biometrias cadastradas
        this.isEnrolled = await LocalAuthentication.isEnrolledAsync();
        
        // Verificar nível de segurança
        this.securityLevel = await LocalAuthentication.getEnrolledLevelAsync();
      }
    } catch (error) {
      console.error('Erro ao inicializar autenticação biométrica:', error);
    }
  }

  // Verificar se a autenticação biométrica está disponível
  async isAvailable() {
    await this.init();
    return this.isSupported && this.isEnrolled;
  }

  // Obter tipos de autenticação disponíveis
  getAvailableTypes() {
    const types = [];
    
    if (this.availableTypes.includes(LocalAuthentication.AuthenticationType.FINGERPRINT)) {
      types.push({
        type: 'fingerprint',
        name: 'Impressão Digital',
        icon: '👆',
        description: 'Use sua impressão digital para autenticar'
      });
    }
    
    if (this.availableTypes.includes(LocalAuthentication.AuthenticationType.FACIAL_RECOGNITION)) {
      types.push({
        type: 'face',
        name: 'Reconhecimento Facial',
        icon: '😊',
        description: 'Use seu rosto para autenticar'
      });
    }
    
    if (this.availableTypes.includes(LocalAuthentication.AuthenticationType.IRIS)) {
      types.push({
        type: 'iris',
        name: 'Íris',
        icon: '👁️',
        description: 'Use sua íris para autenticar'
      });
    }

    return types;
  }

  // Obter nível de segurança
  getSecurityLevel() {
    switch (this.securityLevel) {
      case LocalAuthentication.SecurityLevel.NONE:
        return { level: 'none', name: 'Nenhum', color: '#f44336' };
      case LocalAuthentication.SecurityLevel.SECRET:
        return { level: 'secret', name: 'Baixo', color: '#ff9800' };
      case LocalAuthentication.SecurityLevel.BIOMETRIC_WEAK:
        return { level: 'weak', name: 'Médio', color: '#2196f3' };
      case LocalAuthentication.SecurityLevel.BIOMETRIC_STRONG:
        return { level: 'strong', name: 'Alto', color: '#4caf50' };
      default:
        return { level: 'unknown', name: 'Desconhecido', color: '#9e9e9e' };
    }
  }

  // Autenticar com biometria
  async authenticate(options = {}) {
    const {
      reason = 'Confirme sua identidade para continuar',
      fallbackEnabled = true,
      cancelLabel = 'Cancelar',
      fallbackLabel = 'Usar senha',
      requireConfirmation = false,
    } = options;

    try {
      if (!await this.isAvailable()) {
        return {
          success: false,
          error: 'Autenticação biométrica não disponível',
          errorCode: 'BIOMETRIC_NOT_AVAILABLE'
        };
      }

      const result = await LocalAuthentication.authenticateAsync({
        promptMessage: reason,
        cancelLabel,
        fallbackLabel,
        disableDeviceFallback: !fallbackEnabled,
        requireConfirmation,
      });

      // Log da tentativa de autenticação
      await this.logAuthAttempt(result.success);

      return {
        success: result.success,
        error: result.error,
        warning: result.warning,
        errorCode: this.getErrorCode(result.error),
      };
    } catch (error) {
      await this.logAuthAttempt(false, error.message);
      
      return {
        success: false,
        error: error.message,
        errorCode: 'AUTHENTICATION_ERROR'
      };
    }
  }

  // Obter código de erro padronizado
  getErrorCode(error) {
    if (!error) return null;
    
    const errorMap = {
      'UserCancel': 'USER_CANCELLED',
      'UserFallback': 'USER_FALLBACK',
      'SystemCancel': 'SYSTEM_CANCELLED',
      'PasscodeNotSet': 'PASSCODE_NOT_SET',
      'BiometryNotAvailable': 'BIOMETRY_NOT_AVAILABLE',
      'BiometryNotEnrolled': 'BIOMETRY_NOT_ENROLLED',
      'BiometryLockout': 'BIOMETRY_LOCKOUT',
    };
    
    return errorMap[error] || 'UNKNOWN_ERROR';
  }

  // Autenticação rápida para login
  async quickAuth(userId) {
    if (!await this.isBiometricEnabled(userId)) {
      return { success: false, error: 'Biometria não habilitada' };
    }

    return await this.authenticate({
      reason: 'Entre no GuardFlow com sua biometria',
      fallbackEnabled: true,
    });
  }

  // Autenticação para transações
  async transactionAuth(amount, description) {
    return await this.authenticate({
      reason: `Confirme a transação de R$ ${amount.toFixed(2)}\n${description}`,
      fallbackEnabled: false,
      requireConfirmation: true,
    });
  }

  // Autenticação para configurações sensíveis
  async settingsAuth() {
    return await this.authenticate({
      reason: 'Confirme sua identidade para acessar configurações',
      fallbackEnabled: true,
    });
  }

  // Salvar configuração de biometria
  async enableBiometric(userId) {
    try {
      // Primeiro, testar a biometria
      const authResult = await this.authenticate({
        reason: 'Confirme sua biometria para habilitar o login rápido'
      });

      if (!authResult.success) {
        return { success: false, error: 'Falha na autenticação biométrica' };
      }

      await AsyncStorage.setItem(`biometric_enabled_${userId}`, 'true');
      await AsyncStorage.setItem(`biometric_setup_date_${userId}`, new Date().toISOString());
      
      return { success: true };
    } catch (error) {
      console.error('Erro ao habilitar biometria:', error);
      return { success: false, error: error.message };
    }
  }

  // Desabilitar biometria
  async disableBiometric(userId) {
    try {
      await AsyncStorage.removeItem(`biometric_enabled_${userId}`);
      await AsyncStorage.removeItem(`biometric_setup_date_${userId}`);
      await AsyncStorage.removeItem(`biometric_attempts_${userId}`);
      
      return { success: true };
    } catch (error) {
      console.error('Erro ao desabilitar biometria:', error);
      return { success: false, error: error.message };
    }
  }

  // Verificar se biometria está habilitada para o usuário
  async isBiometricEnabled(userId) {
    try {
      const enabled = await AsyncStorage.getItem(`biometric_enabled_${userId}`);
      return enabled === 'true';
    } catch (error) {
      console.error('Erro ao verificar biometria:', error);
      return false;
    }
  }

  // Log de tentativas de autenticação
  async logAuthAttempt(success, error = null) {
    try {
      const timestamp = new Date().toISOString();
      const attempt = {
        timestamp,
        success,
        error,
        deviceInfo: {
          availableTypes: this.availableTypes,
          securityLevel: this.securityLevel,
        }
      };

      const logs = await this.getAuthLogs();
      logs.push(attempt);
      
      // Manter apenas os últimos 50 logs
      const recentLogs = logs.slice(-50);
      
      await AsyncStorage.setItem('biometric_auth_logs', JSON.stringify(recentLogs));
    } catch (error) {
      console.error('Erro ao registrar log de autenticação:', error);
    }
  }

  // Obter logs de autenticação
  async getAuthLogs() {
    try {
      const logs = await AsyncStorage.getItem('biometric_auth_logs');
      return logs ? JSON.parse(logs) : [];
    } catch (error) {
      console.error('Erro ao obter logs:', error);
      return [];
    }
  }

  // Obter estatísticas de uso
  async getUsageStats(userId) {
    try {
      const logs = await this.getAuthLogs();
      const userLogs = logs.filter(log => log.userId === userId);
      
      const total = userLogs.length;
      const successful = userLogs.filter(log => log.success).length;
      const failed = total - successful;
      const successRate = total > 0 ? (successful / total) * 100 : 0;
      
      const lastWeek = new Date();
      lastWeek.setDate(lastWeek.getDate() - 7);
      
      const recentLogs = userLogs.filter(log => 
        new Date(log.timestamp) > lastWeek
      );

      return {
        total,
        successful,
        failed,
        successRate: Math.round(successRate),
        recentUsage: recentLogs.length,
        lastUsed: userLogs.length > 0 ? userLogs[userLogs.length - 1].timestamp : null,
      };
    } catch (error) {
      console.error('Erro ao obter estatísticas:', error);
      return null;
    }
  }

  // Mostrar configuração de biometria
  async showBiometricSetup(userId) {
    const available = await this.isAvailable();
    
    if (!available) {
      Alert.alert(
        'Biometria não disponível',
        'Seu dispositivo não suporta autenticação biométrica ou não há biometrias cadastradas.',
        [{ text: 'OK' }]
      );
      return false;
    }

    const types = this.getAvailableTypes();
    const typeNames = types.map(t => t.name).join(', ');
    
    return new Promise((resolve) => {
      Alert.alert(
        'Habilitar Login Biométrico',
        `Deseja usar ${typeNames} para fazer login mais rapidamente no GuardFlow?`,
        [
          {
            text: 'Não',
            style: 'cancel',
            onPress: () => resolve(false)
          },
          {
            text: 'Sim',
            onPress: async () => {
              const result = await this.enableBiometric(userId);
              resolve(result.success);
            }
          }
        ]
      );
    });
  }

  // Verificar integridade da configuração biométrica
  async verifyIntegrity(userId) {
    try {
      const enabled = await this.isBiometricEnabled(userId);
      const available = await this.isAvailable();
      
      if (enabled && !available) {
        // Biometria estava habilitada mas não está mais disponível
        await this.disableBiometric(userId);
        return {
          valid: false,
          reason: 'Biometria não está mais disponível no dispositivo',
          action: 'disabled'
        };
      }

      return {
        valid: true,
        enabled,
        available
      };
    } catch (error) {
      console.error('Erro na verificação de integridade:', error);
      return {
        valid: false,
        reason: error.message,
        action: 'error'
      };
    }
  }
}

export default new AdvancedBiometricAuth();
