/**
 * GuardFlow Biometric Setup Component
 * Componente para configuração de autenticação biométrica
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Alert,
  Switch,
  ActivityIndicator,
  ScrollView,
  Dimensions,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import biometricAuth from '../utils/biometricAuth';
import advancedBiometricAuth from '../utils/biometricAuthAdvanced';

const { width } = Dimensions.get('window');

const BiometricSetup = ({ userId, onSetupComplete }) => {
  const [loading, setLoading] = useState(true);
  const [biometricAvailable, setBiometricAvailable] = useState(false);
  const [biometricEnabled, setBiometricEnabled] = useState(false);
  const [biometricTypes, setBiometricTypes] = useState([]);
  const [securityLevel, setSecurityLevel] = useState(null);
  const [deviceInfo, setDeviceInfo] = useState(null);
  const [usageStats, setUsageStats] = useState(null);

  useEffect(() => {
    initializeBiometric();
  }, [userId]);

  const initializeBiometric = async () => {
    setLoading(true);
    try {
      // Verificar disponibilidade
      const available = await advancedBiometricAuth.isAvailable();
      setBiometricAvailable(available);

      if (available) {
        // Obter tipos disponíveis
        const types = advancedBiometricAuth.getAvailableTypes();
        setBiometricTypes(types);

        // Obter nível de segurança
        const security = advancedBiometricAuth.getSecurityLevel();
        setSecurityLevel(security);

        // Verificar se está habilitado
        const enabled = await advancedBiometricAuth.isBiometricEnabled(userId);
        setBiometricEnabled(enabled);

        // Obter estatísticas de uso
        const stats = await advancedBiometricAuth.getUsageStats(userId);
        setUsageStats(stats);
      }

      // Obter informações do dispositivo (fallback)
      const info = await biometricAuth.getDeviceInfo();
      setDeviceInfo(info);

    } catch (error) {
      console.error('Erro ao inicializar biometria:', error);
      Alert.alert('Erro', 'Falha ao verificar configurações biométricas');
    } finally {
      setLoading(false);
    }
  };

  const handleToggleBiometric = async (enabled) => {
    setLoading(true);
    try {
      if (enabled) {
        // Habilitar biometria
        const result = await advancedBiometricAuth.enableBiometric(userId);
        if (result.success) {
          setBiometricEnabled(true);
          Alert.alert(
            'Sucesso!',
            'Autenticação biométrica habilitada com sucesso.',
            [{ text: 'OK', onPress: () => onSetupComplete?.(true) }]
          );
          await initializeBiometric(); // Recarregar dados
        } else {
          Alert.alert('Erro', result.error || 'Falha ao habilitar biometria');
        }
      } else {
        // Desabilitar biometria
        Alert.alert(
          'Desabilitar Biometria',
          'Tem certeza que deseja desabilitar a autenticação biométrica?',
          [
            { text: 'Cancelar', style: 'cancel' },
            {
              text: 'Desabilitar',
              style: 'destructive',
              onPress: async () => {
                const result = await advancedBiometricAuth.disableBiometric(userId);
                if (result.success) {
                  setBiometricEnabled(false);
                  onSetupComplete?.(false);
                  await initializeBiometric(); // Recarregar dados
                }
              }
            }
          ]
        );
      }
    } catch (error) {
      console.error('Erro ao alterar configuração biométrica:', error);
      Alert.alert('Erro', 'Falha ao alterar configuração');
    } finally {
      setLoading(false);
    }
  };

  const testBiometric = async () => {
    try {
      const result = await advancedBiometricAuth.authenticate({
        reason: 'Teste de autenticação biométrica',
        fallbackEnabled: true,
      });

      if (result.success) {
        Alert.alert('Sucesso!', 'Autenticação biométrica funcionando corretamente.');
      } else {
        Alert.alert('Falha', result.error || 'Falha na autenticação biométrica');
      }
    } catch (error) {
      Alert.alert('Erro', 'Erro ao testar biometria');
    }
  };

  const getBiometricIcon = (type) => {
    switch (type) {
      case 'fingerprint':
        return 'finger-print';
      case 'face':
        return 'scan';
      case 'iris':
        return 'eye';
      default:
        return 'shield-checkmark';
    }
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#007AFF" />
        <Text style={styles.loadingText}>Verificando configurações biométricas...</Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
      {/* Header */}
      <View style={styles.header}>
        <Ionicons name="shield-checkmark" size={48} color="#007AFF" />
        <Text style={styles.title}>Autenticação Biométrica</Text>
        <Text style={styles.subtitle}>
          Configure o login rápido e seguro com sua biometria
        </Text>
      </View>

      {!biometricAvailable ? (
        /* Biometria não disponível */
        <View style={styles.unavailableContainer}>
          <Ionicons name="warning" size={64} color="#FF9500" />
          <Text style={styles.unavailableTitle}>Biometria não disponível</Text>
          <Text style={styles.unavailableText}>
            Seu dispositivo não suporta autenticação biométrica ou não há biometrias cadastradas.
          </Text>
          
          {deviceInfo && (
            <View style={styles.deviceInfoContainer}>
              <Text style={styles.deviceInfoTitle}>Informações do Dispositivo:</Text>
              <Text style={styles.deviceInfoText}>
                • Suporte: {deviceInfo.available ? 'Sim' : 'Não'}
              </Text>
              <Text style={styles.deviceInfoText}>
                • Tipo: {deviceInfo.biometryType || 'Não detectado'}
              </Text>
              <Text style={styles.deviceInfoText}>
                • Chaves: {deviceInfo.keysExist ? 'Existem' : 'Não existem'}
              </Text>
            </View>
          )}
        </View>
      ) : (
        /* Biometria disponível */
        <View style={styles.availableContainer}>
          {/* Toggle principal */}
          <View style={styles.toggleContainer}>
            <View style={styles.toggleInfo}>
              <Text style={styles.toggleTitle}>Login Biométrico</Text>
              <Text style={styles.toggleSubtitle}>
                Use sua biometria para fazer login rapidamente
              </Text>
            </View>
            <Switch
              value={biometricEnabled}
              onValueChange={handleToggleBiometric}
              trackColor={{ false: '#E5E5E7', true: '#007AFF' }}
              thumbColor={biometricEnabled ? '#FFFFFF' : '#F4F3F4'}
              disabled={loading}
            />
          </View>

          {/* Tipos de biometria disponíveis */}
          <View style={styles.typesContainer}>
            <Text style={styles.sectionTitle}>Tipos Disponíveis</Text>
            {biometricTypes.map((type, index) => (
              <View key={index} style={styles.typeItem}>
                <View style={styles.typeIcon}>
                  <Ionicons 
                    name={getBiometricIcon(type.type)} 
                    size={24} 
                    color="#007AFF" 
                  />
                </View>
                <View style={styles.typeInfo}>
                  <Text style={styles.typeName}>{type.name}</Text>
                  <Text style={styles.typeDescription}>{type.description}</Text>
                </View>
              </View>
            ))}
          </View>

          {/* Nível de segurança */}
          {securityLevel && (
            <View style={styles.securityContainer}>
              <Text style={styles.sectionTitle}>Nível de Segurança</Text>
              <View style={styles.securityItem}>
                <View style={[styles.securityIndicator, { backgroundColor: securityLevel.color }]} />
                <Text style={styles.securityText}>{securityLevel.name}</Text>
              </View>
            </View>
          )}

          {/* Estatísticas de uso */}
          {biometricEnabled && usageStats && (
            <View style={styles.statsContainer}>
              <Text style={styles.sectionTitle}>Estatísticas de Uso</Text>
              <View style={styles.statsGrid}>
                <View style={styles.statItem}>
                  <Text style={styles.statNumber}>{usageStats.total}</Text>
                  <Text style={styles.statLabel}>Total</Text>
                </View>
                <View style={styles.statItem}>
                  <Text style={styles.statNumber}>{usageStats.successful}</Text>
                  <Text style={styles.statLabel}>Sucessos</Text>
                </View>
                <View style={styles.statItem}>
                  <Text style={styles.statNumber}>{usageStats.successRate}%</Text>
                  <Text style={styles.statLabel}>Taxa</Text>
                </View>
                <View style={styles.statItem}>
                  <Text style={styles.statNumber}>{usageStats.recentUsage}</Text>
                  <Text style={styles.statLabel}>Semana</Text>
                </View>
              </View>
            </View>
          )}

          {/* Botão de teste */}
          {biometricEnabled && (
            <TouchableOpacity style={styles.testButton} onPress={testBiometric}>
              <Ionicons name="play-circle" size={24} color="#FFFFFF" />
              <Text style={styles.testButtonText}>Testar Biometria</Text>
            </TouchableOpacity>
          )}

          {/* Informações de segurança */}
          <View style={styles.securityInfoContainer}>
            <Ionicons name="information-circle" size={20} color="#8E8E93" />
            <Text style={styles.securityInfoText}>
              Suas informações biométricas são armazenadas com segurança no seu dispositivo e nunca são enviadas para nossos servidores.
            </Text>
          </View>
        </View>
      )}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F2F2F7',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F2F2F7',
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
    color: '#8E8E93',
    textAlign: 'center',
  },
  header: {
    alignItems: 'center',
    paddingVertical: 32,
    paddingHorizontal: 20,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#000000',
    marginTop: 16,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 16,
    color: '#8E8E93',
    marginTop: 8,
    textAlign: 'center',
    lineHeight: 22,
  },
  unavailableContainer: {
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 32,
  },
  unavailableTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#FF9500',
    marginTop: 16,
    textAlign: 'center',
  },
  unavailableText: {
    fontSize: 16,
    color: '#8E8E93',
    marginTop: 12,
    textAlign: 'center',
    lineHeight: 22,
  },
  deviceInfoContainer: {
    marginTop: 24,
    padding: 16,
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    width: '100%',
  },
  deviceInfoTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#000000',
    marginBottom: 8,
  },
  deviceInfoText: {
    fontSize: 14,
    color: '#8E8E93',
    marginBottom: 4,
  },
  availableContainer: {
    paddingHorizontal: 20,
  },
  toggleContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: '#FFFFFF',
    padding: 16,
    borderRadius: 12,
    marginBottom: 20,
  },
  toggleInfo: {
    flex: 1,
    marginRight: 16,
  },
  toggleTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#000000',
  },
  toggleSubtitle: {
    fontSize: 14,
    color: '#8E8E93',
    marginTop: 4,
  },
  typesContainer: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 16,
    marginBottom: 20,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#000000',
    marginBottom: 12,
  },
  typeItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#F2F2F7',
  },
  typeIcon: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#F2F2F7',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  typeInfo: {
    flex: 1,
  },
  typeName: {
    fontSize: 16,
    fontWeight: '500',
    color: '#000000',
  },
  typeDescription: {
    fontSize: 14,
    color: '#8E8E93',
    marginTop: 2,
  },
  securityContainer: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 16,
    marginBottom: 20,
  },
  securityItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  securityIndicator: {
    width: 12,
    height: 12,
    borderRadius: 6,
    marginRight: 8,
  },
  securityText: {
    fontSize: 16,
    color: '#000000',
  },
  statsContainer: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 16,
    marginBottom: 20,
  },
  statsGrid: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  statItem: {
    alignItems: 'center',
    flex: 1,
  },
  statNumber: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#007AFF',
  },
  statLabel: {
    fontSize: 12,
    color: '#8E8E93',
    marginTop: 4,
  },
  testButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#007AFF',
    padding: 16,
    borderRadius: 12,
    marginBottom: 20,
  },
  testButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#FFFFFF',
    marginLeft: 8,
  },
  securityInfoContainer: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    backgroundColor: '#F2F2F7',
    padding: 16,
    borderRadius: 12,
    marginBottom: 20,
  },
  securityInfoText: {
    fontSize: 14,
    color: '#8E8E93',
    marginLeft: 8,
    flex: 1,
    lineHeight: 20,
  },
});

export default BiometricSetup;
