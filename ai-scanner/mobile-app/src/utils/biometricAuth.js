/**
 * GuardFlow Biometric Authentication
 * Utilitário para autenticação biométrica
 */

import ReactNativeBiometrics from 'react-native-biometrics';

class BiometricAuth {
  constructor() {
    this.rnBiometrics = new ReactNativeBiometrics({ allowDeviceCredentials: true });
  }

  // Verificar se biometria está disponível
  async isAvailable() {
    try {
      const { available, biometryType } = await this.rnBiometrics.isSensorAvailable();
      return available;
    } catch (error) {
      console.error('Erro ao verificar biometria:', error);
      return false;
    }
  }

  // Obter tipo de biometria
  async getBiometryType() {
    try {
      const { available, biometryType } = await this.rnBiometrics.isSensorAvailable();
      if (available) {
        return biometryType;
      }
      return null;
    } catch (error) {
      console.error('Erro ao obter tipo de biometria:', error);
      return null;
    }
  }

  // Autenticar com biometria
  async authenticate(reason = 'Autentique-se para continuar') {
    try {
      const { success } = await this.rnBiometrics.simplePrompt({
        promptMessage: reason,
        cancelButtonText: 'Cancelar',
      });

      return { success };
    } catch (error) {
      console.error('Erro na autenticação biométrica:', error);
      return { success: false, error: error.message };
    }
  }

  // Criar chave biométrica
  async createBiometricKey() {
    try {
      const { publicKey } = await this.rnBiometrics.createKeys();
      return { success: true, publicKey };
    } catch (error) {
      console.error('Erro ao criar chave biométrica:', error);
      return { success: false, error: error.message };
    }
  }

  // Verificar se chave biométrica existe
  async biometricKeysExist() {
    try {
      const { keysExist } = await this.rnBiometrics.biometricKeysExist();
      return keysExist;
    } catch (error) {
      console.error('Erro ao verificar chaves biométricas:', error);
      return false;
    }
  }

  // Deletar chaves biométricas
  async deleteBiometricKeys() {
    try {
      await this.rnBiometrics.deleteKeys();
      return { success: true };
    } catch (error) {
      console.error('Erro ao deletar chaves biométricas:', error);
      return { success: false, error: error.message };
    }
  }

  // Assinar com biometria
  async signWithBiometrics(payload) {
    try {
      const { success, signature } = await this.rnBiometrics.createSignature({
        promptMessage: 'Assine com biometria',
        payload: payload,
      });

      if (success) {
        return { success: true, signature };
      } else {
        return { success: false };
      }
    } catch (error) {
      console.error('Erro ao assinar com biometria:', error);
      return { success: false, error: error.message };
    }
  }

  // Verificar assinatura biométrica
  async verifyBiometricSignature(signature, payload) {
    try {
      const { success } = await this.rnBiometrics.verifySignature({
        payload: payload,
        signature: signature,
      });

      return { success };
    } catch (error) {
      console.error('Erro ao verificar assinatura biométrica:', error);
      return { success: false, error: error.message };
    }
  }

  // Obter informações do dispositivo
  async getDeviceInfo() {
    try {
      const { available, biometryType } = await this.rnBiometrics.isSensorAvailable();
      const keysExist = await this.biometricKeysExist();
      
      return {
        available,
        biometryType,
        keysExist,
      };
    } catch (error) {
      console.error('Erro ao obter informações do dispositivo:', error);
      return {
        available: false,
        biometryType: null,
        keysExist: false,
      };
    }
  }
}

// Exportar instância única
export default new BiometricAuth();


