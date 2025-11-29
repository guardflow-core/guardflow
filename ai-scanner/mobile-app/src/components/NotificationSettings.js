/**
 * GuardFlow Notification Settings Component
 * Componente para configuração de notificações
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Switch,
  TouchableOpacity,
  ScrollView,
  Alert,
  Modal,
  TextInput,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import notificationManager from '../services/notificationManager';

const NotificationSettings = ({ visible, onClose }) => {
  const [preferences, setPreferences] = useState({
    enabled: true,
    sound: true,
    vibration: true,
    badge: true,
    categories: {
      transactions: true,
      promotions: true,
      esg: true,
      system: true,
      security: true,
    },
    quietHours: {
      enabled: false,
      start: '22:00',
      end: '08:00',
    },
  });
  const [stats, setStats] = useState(null);
  const [showTimeModal, setShowTimeModal] = useState(false);
  const [timeType, setTimeType] = useState('start');
  const [tempTime, setTempTime] = useState('');

  useEffect(() => {
    if (visible) {
      loadSettings();
    }
  }, [visible]);

  const loadSettings = async () => {
    try {
      const currentPreferences = notificationManager.getPreferences();
      setPreferences(currentPreferences);
      
      const currentStats = notificationManager.getStats();
      setStats(currentStats);
    } catch (error) {
      console.error('Erro ao carregar configurações:', error);
    }
  };

  const updatePreference = async (key, value) => {
    const newPreferences = { ...preferences, [key]: value };
    setPreferences(newPreferences);
    
    try {
      await notificationManager.updatePreferences({ [key]: value });
    } catch (error) {
      console.error('Erro ao atualizar preferência:', error);
      Alert.alert('Erro', 'Falha ao salvar configuração');
    }
  };

  const updateCategoryPreference = async (category, value) => {
    const newCategories = { ...preferences.categories, [category]: value };
    const newPreferences = { ...preferences, categories: newCategories };
    setPreferences(newPreferences);
    
    try {
      await notificationManager.updatePreferences({ categories: newCategories });
    } catch (error) {
      console.error('Erro ao atualizar categoria:', error);
      Alert.alert('Erro', 'Falha ao salvar configuração');
    }
  };

  const updateQuietHours = async (key, value) => {
    const newQuietHours = { ...preferences.quietHours, [key]: value };
    const newPreferences = { ...preferences, quietHours: newQuietHours };
    setPreferences(newPreferences);
    
    try {
      await notificationManager.updatePreferences({ quietHours: newQuietHours });
    } catch (error) {
      console.error('Erro ao atualizar horário silencioso:', error);
      Alert.alert('Erro', 'Falha ao salvar configuração');
    }
  };

  const testNotification = async () => {
    try {
      await notificationManager.sendLocalNotification({
        title: 'Teste de Notificação',
        body: 'Esta é uma notificação de teste do GuardFlow',
        categoryId: 'system',
        priority: 'default',
      });
      
      Alert.alert('Sucesso', 'Notificação de teste enviada!');
    } catch (error) {
      Alert.alert('Erro', 'Falha ao enviar notificação de teste');
    }
  };

  const clearHistory = async () => {
    Alert.alert(
      'Limpar Histórico',
      'Tem certeza que deseja limpar todo o histórico de notificações?',
      [
        { text: 'Cancelar', style: 'cancel' },
        {
          text: 'Limpar',
          style: 'destructive',
          onPress: async () => {
            await notificationManager.clearHistory();
            await loadSettings();
            Alert.alert('Sucesso', 'Histórico limpo com sucesso');
          }
        }
      ]
    );
  };

  const markAllAsRead = async () => {
    await notificationManager.markAllAsRead();
    await loadSettings();
    Alert.alert('Sucesso', 'Todas as notificações foram marcadas como lidas');
  };

  const handleTimeChange = (time) => {
    if (!/^\d{2}:\d{2}$/.test(time)) {
      Alert.alert('Erro', 'Formato inválido. Use HH:MM (ex: 22:00)');
      return;
    }
    
    updateQuietHours(timeType, time);
    setShowTimeModal(false);
  };

  const openTimeModal = (type) => {
    setTimeType(type);
    setTempTime(preferences.quietHours[type]);
    setShowTimeModal(true);
  };

  const getCategoryIcon = (category) => {
    const icons = {
      transactions: 'card',
      promotions: 'pricetag',
      esg: 'leaf',
      system: 'settings',
      security: 'shield-checkmark',
    };
    return icons[category] || 'notifications';
  };

  const getCategoryName = (category) => {
    const names = {
      transactions: 'Transações',
      promotions: 'Promoções',
      esg: 'ESG e Sustentabilidade',
      system: 'Sistema',
      security: 'Segurança',
    };
    return names[category] || category;
  };

  const getCategoryDescription = (category) => {
    const descriptions = {
      transactions: 'Confirmações de pagamento e recibos',
      promotions: 'Ofertas especiais e descontos',
      esg: 'Conquistas ESG e dicas sustentáveis',
      system: 'Atualizações e manutenção do app',
      security: 'Alertas de segurança e autenticação',
    };
    return descriptions[category] || '';
  };

  return (
    <Modal
      visible={visible}
      animationType="slide"
      presentationStyle="pageSheet"
    >
      <View style={styles.container}>
        {/* Header */}
        <View style={styles.header}>
          <TouchableOpacity onPress={onClose} style={styles.closeButton}>
            <Ionicons name="close" size={24} color="#007AFF" />
          </TouchableOpacity>
          <Text style={styles.title}>Notificações</Text>
          <TouchableOpacity onPress={testNotification} style={styles.testButton}>
            <Ionicons name="play-circle" size={24} color="#007AFF" />
          </TouchableOpacity>
        </View>

        <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
          {/* Configurações gerais */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Geral</Text>
            
            <View style={styles.settingItem}>
              <View style={styles.settingInfo}>
                <Ionicons name="notifications" size={24} color="#007AFF" />
                <View style={styles.settingText}>
                  <Text style={styles.settingLabel}>Notificações</Text>
                  <Text style={styles.settingDescription}>
                    Receber notificações do GuardFlow
                  </Text>
                </View>
              </View>
              <Switch
                value={preferences.enabled}
                onValueChange={(value) => updatePreference('enabled', value)}
                trackColor={{ false: '#E5E5E7', true: '#007AFF' }}
                thumbColor={preferences.enabled ? '#FFFFFF' : '#F4F3F4'}
              />
            </View>

            <View style={styles.settingItem}>
              <View style={styles.settingInfo}>
                <Ionicons name="volume-high" size={24} color="#FF9500" />
                <View style={styles.settingText}>
                  <Text style={styles.settingLabel}>Som</Text>
                  <Text style={styles.settingDescription}>
                    Tocar som nas notificações
                  </Text>
                </View>
              </View>
              <Switch
                value={preferences.sound}
                onValueChange={(value) => updatePreference('sound', value)}
                disabled={!preferences.enabled}
                trackColor={{ false: '#E5E5E7', true: '#007AFF' }}
                thumbColor={preferences.sound ? '#FFFFFF' : '#F4F3F4'}
              />
            </View>

            <View style={styles.settingItem}>
              <View style={styles.settingInfo}>
                <Ionicons name="phone-portrait" size={24} color="#34C759" />
                <View style={styles.settingText}>
                  <Text style={styles.settingLabel}>Vibração</Text>
                  <Text style={styles.settingDescription}>
                    Vibrar ao receber notificações
                  </Text>
                </View>
              </View>
              <Switch
                value={preferences.vibration}
                onValueChange={(value) => updatePreference('vibration', value)}
                disabled={!preferences.enabled}
                trackColor={{ false: '#E5E5E7', true: '#007AFF' }}
                thumbColor={preferences.vibration ? '#FFFFFF' : '#F4F3F4'}
              />
            </View>

            <View style={styles.settingItem}>
              <View style={styles.settingInfo}>
                <Ionicons name="ellipse" size={24} color="#FF3B30" />
                <View style={styles.settingText}>
                  <Text style={styles.settingLabel}>Badge</Text>
                  <Text style={styles.settingDescription}>
                    Mostrar contador no ícone do app
                  </Text>
                </View>
              </View>
              <Switch
                value={preferences.badge}
                onValueChange={(value) => updatePreference('badge', value)}
                disabled={!preferences.enabled}
                trackColor={{ false: '#E5E5E7', true: '#007AFF' }}
                thumbColor={preferences.badge ? '#FFFFFF' : '#F4F3F4'}
              />
            </View>
          </View>

          {/* Categorias */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Categorias</Text>
            
            {Object.entries(preferences.categories).map(([category, enabled]) => (
              <View key={category} style={styles.settingItem}>
                <View style={styles.settingInfo}>
                  <Ionicons 
                    name={getCategoryIcon(category)} 
                    size={24} 
                    color="#007AFF" 
                  />
                  <View style={styles.settingText}>
                    <Text style={styles.settingLabel}>
                      {getCategoryName(category)}
                    </Text>
                    <Text style={styles.settingDescription}>
                      {getCategoryDescription(category)}
                    </Text>
                  </View>
                </View>
                <Switch
                  value={enabled}
                  onValueChange={(value) => updateCategoryPreference(category, value)}
                  disabled={!preferences.enabled}
                  trackColor={{ false: '#E5E5E7', true: '#007AFF' }}
                  thumbColor={enabled ? '#FFFFFF' : '#F4F3F4'}
                />
              </View>
            ))}
          </View>

          {/* Horário silencioso */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Horário Silencioso</Text>
            
            <View style={styles.settingItem}>
              <View style={styles.settingInfo}>
                <Ionicons name="moon" size={24} color="#5856D6" />
                <View style={styles.settingText}>
                  <Text style={styles.settingLabel}>Ativar</Text>
                  <Text style={styles.settingDescription}>
                    Silenciar notificações em horários específicos
                  </Text>
                </View>
              </View>
              <Switch
                value={preferences.quietHours.enabled}
                onValueChange={(value) => updateQuietHours('enabled', value)}
                disabled={!preferences.enabled}
                trackColor={{ false: '#E5E5E7', true: '#007AFF' }}
                thumbColor={preferences.quietHours.enabled ? '#FFFFFF' : '#F4F3F4'}
              />
            </View>

            {preferences.quietHours.enabled && (
              <>
                <TouchableOpacity
                  style={styles.timeButton}
                  onPress={() => openTimeModal('start')}
                >
                  <View style={styles.settingInfo}>
                    <Ionicons name="time" size={24} color="#FF9500" />
                    <View style={styles.settingText}>
                      <Text style={styles.settingLabel}>Início</Text>
                      <Text style={styles.settingDescription}>
                        Horário de início do silêncio
                      </Text>
                    </View>
                  </View>
                  <Text style={styles.timeValue}>{preferences.quietHours.start}</Text>
                </TouchableOpacity>

                <TouchableOpacity
                  style={styles.timeButton}
                  onPress={() => openTimeModal('end')}
                >
                  <View style={styles.settingInfo}>
                    <Ionicons name="time" size={24} color="#34C759" />
                    <View style={styles.settingText}>
                      <Text style={styles.settingLabel}>Fim</Text>
                      <Text style={styles.settingDescription}>
                        Horário de fim do silêncio
                      </Text>
                    </View>
                  </View>
                  <Text style={styles.timeValue}>{preferences.quietHours.end}</Text>
                </TouchableOpacity>
              </>
            )}
          </View>

          {/* Estatísticas */}
          {stats && (
            <View style={styles.section}>
              <Text style={styles.sectionTitle}>Estatísticas</Text>
              
              <View style={styles.statsContainer}>
                <View style={styles.statItem}>
                  <Text style={styles.statNumber}>{stats.total}</Text>
                  <Text style={styles.statLabel}>Total</Text>
                </View>
                <View style={styles.statItem}>
                  <Text style={styles.statNumber}>{stats.unread}</Text>
                  <Text style={styles.statLabel}>Não Lidas</Text>
                </View>
                <View style={styles.statItem}>
                  <Text style={styles.statNumber}>{stats.read}</Text>
                  <Text style={styles.statLabel}>Lidas</Text>
                </View>
              </View>

              {stats.unread > 0 && (
                <TouchableOpacity
                  style={styles.actionButton}
                  onPress={markAllAsRead}
                >
                  <Ionicons name="checkmark-done" size={20} color="#007AFF" />
                  <Text style={styles.actionButtonText}>
                    Marcar Todas como Lidas
                  </Text>
                </TouchableOpacity>
              )}

              <TouchableOpacity
                style={[styles.actionButton, styles.dangerButton]}
                onPress={clearHistory}
              >
                <Ionicons name="trash" size={20} color="#FF3B30" />
                <Text style={[styles.actionButtonText, styles.dangerText]}>
                  Limpar Histórico
                </Text>
              </TouchableOpacity>
            </View>
          )}
        </ScrollView>

        {/* Modal de horário */}
        <Modal
          visible={showTimeModal}
          transparent={true}
          animationType="fade"
        >
          <View style={styles.modalOverlay}>
            <View style={styles.timeModal}>
              <Text style={styles.timeModalTitle}>
                {timeType === 'start' ? 'Horário de Início' : 'Horário de Fim'}
              </Text>
              
              <TextInput
                style={styles.timeInput}
                value={tempTime}
                onChangeText={setTempTime}
                placeholder="HH:MM"
                keyboardType="numeric"
                maxLength={5}
              />
              
              <View style={styles.timeModalButtons}>
                <TouchableOpacity
                  style={[styles.timeModalButton, styles.cancelButton]}
                  onPress={() => setShowTimeModal(false)}
                >
                  <Text style={styles.cancelButtonText}>Cancelar</Text>
                </TouchableOpacity>
                
                <TouchableOpacity
                  style={[styles.timeModalButton, styles.confirmButton]}
                  onPress={() => handleTimeChange(tempTime)}
                >
                  <Text style={styles.confirmButtonText}>Confirmar</Text>
                </TouchableOpacity>
              </View>
            </View>
          </View>
        </Modal>
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F2F2F7',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingTop: 60,
    paddingBottom: 20,
    backgroundColor: '#FFFFFF',
    borderBottomWidth: 1,
    borderBottomColor: '#E5E5E7',
  },
  closeButton: {
    padding: 4,
  },
  title: {
    fontSize: 18,
    fontWeight: '600',
    color: '#000000',
  },
  testButton: {
    padding: 4,
  },
  content: {
    flex: 1,
  },
  section: {
    backgroundColor: '#FFFFFF',
    marginTop: 20,
    paddingVertical: 8,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#000000',
    paddingHorizontal: 20,
    paddingVertical: 12,
    backgroundColor: '#F2F2F7',
  },
  settingItem: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#F2F2F7',
  },
  settingInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  settingText: {
    marginLeft: 12,
    flex: 1,
  },
  settingLabel: {
    fontSize: 16,
    fontWeight: '500',
    color: '#000000',
  },
  settingDescription: {
    fontSize: 14,
    color: '#8E8E93',
    marginTop: 2,
  },
  timeButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#F2F2F7',
  },
  timeValue: {
    fontSize: 16,
    color: '#007AFF',
    fontWeight: '500',
  },
  statsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#F2F2F7',
  },
  statItem: {
    alignItems: 'center',
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
  actionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 12,
    paddingHorizontal: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#F2F2F7',
  },
  actionButtonText: {
    fontSize: 16,
    color: '#007AFF',
    marginLeft: 8,
  },
  dangerButton: {
    borderBottomWidth: 0,
  },
  dangerText: {
    color: '#FF3B30',
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  timeModal: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 20,
    width: 280,
  },
  timeModalTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#000000',
    textAlign: 'center',
    marginBottom: 20,
  },
  timeInput: {
    borderWidth: 1,
    borderColor: '#E5E5E7',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
    textAlign: 'center',
    marginBottom: 20,
  },
  timeModalButtons: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  timeModalButton: {
    flex: 1,
    paddingVertical: 12,
    borderRadius: 8,
    marginHorizontal: 4,
  },
  cancelButton: {
    backgroundColor: '#F2F2F7',
  },
  cancelButtonText: {
    fontSize: 16,
    color: '#8E8E93',
    textAlign: 'center',
  },
  confirmButton: {
    backgroundColor: '#007AFF',
  },
  confirmButtonText: {
    fontSize: 16,
    color: '#FFFFFF',
    fontWeight: '500',
    textAlign: 'center',
  },
});

export default NotificationSettings;
