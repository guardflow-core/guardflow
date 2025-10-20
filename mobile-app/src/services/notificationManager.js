/**
 * GuardFlow Notification Manager
 * Gerenciador de push notifications e notificações locais
 */

import * as Notifications from 'expo-notifications';
import * as Device from 'expo-device';
import { Platform } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Configurar comportamento das notificações
Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: true,
  }),
});

class NotificationManager {
  constructor() {
    this.expoPushToken = null;
    this.notificationListener = null;
    this.responseListener = null;
    this.isInitialized = false;
    this.notificationQueue = [];
    this.notificationHistory = [];
    this.preferences = {
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
    };
  }

  async init() {
    if (this.isInitialized) return;

    try {
      // Carregar preferências salvas
      await this.loadPreferences();

      // Registrar para push notifications
      await this.registerForPushNotifications();

      // Configurar listeners
      this.setupListeners();

      // Configurar canais de notificação (Android)
      await this.setupNotificationChannels();

      // Carregar histórico de notificações
      await this.loadNotificationHistory();

      this.isInitialized = true;
      console.log('NotificationManager inicializado com sucesso');

    } catch (error) {
      console.error('Erro ao inicializar NotificationManager:', error);
    }
  }

  async registerForPushNotifications() {
    if (!Device.isDevice) {
      console.warn('Push notifications só funcionam em dispositivos físicos');
      return;
    }

    // Verificar permissões existentes
    const { status: existingStatus } = await Notifications.getPermissionsAsync();
    let finalStatus = existingStatus;

    // Solicitar permissões se necessário
    if (existingStatus !== 'granted') {
      const { status } = await Notifications.requestPermissionsAsync();
      finalStatus = status;
    }

    if (finalStatus !== 'granted') {
      console.warn('Permissão para notificações negada');
      return;
    }

    // Obter token do Expo
    try {
      this.expoPushToken = (await Notifications.getExpoPushTokenAsync()).data;
      console.log('Expo Push Token:', this.expoPushToken);

      // Salvar token para envio ao servidor
      await AsyncStorage.setItem('expo_push_token', this.expoPushToken);

      // Enviar token para o servidor (em produção)
      // await this.sendTokenToServer(this.expoPushToken);

    } catch (error) {
      console.error('Erro ao obter Expo Push Token:', error);
    }

    // Configurações específicas do Android
    if (Platform.OS === 'android') {
      await Notifications.setNotificationChannelAsync('default', {
        name: 'default',
        importance: Notifications.AndroidImportance.MAX,
        vibrationPattern: [0, 250, 250, 250],
        lightColor: '#FF231F7C',
      });
    }
  }

  setupListeners() {
    // Listener para notificações recebidas
    this.notificationListener = Notifications.addNotificationReceivedListener(
      this.handleNotificationReceived.bind(this)
    );

    // Listener para interações com notificações
    this.responseListener = Notifications.addNotificationResponseReceivedListener(
      this.handleNotificationResponse.bind(this)
    );
  }

  async setupNotificationChannels() {
    if (Platform.OS !== 'android') return;

    const channels = [
      {
        id: 'transactions',
        name: 'Transações',
        description: 'Notificações sobre transações e pagamentos',
        importance: Notifications.AndroidImportance.HIGH,
        sound: 'default',
        vibrationPattern: [0, 250, 250, 250],
      },
      {
        id: 'promotions',
        name: 'Promoções',
        description: 'Ofertas e promoções especiais',
        importance: Notifications.AndroidImportance.DEFAULT,
        sound: 'default',
      },
      {
        id: 'esg',
        name: 'ESG',
        description: 'Informações sobre impacto ESG e sustentabilidade',
        importance: Notifications.AndroidImportance.DEFAULT,
        sound: 'default',
      },
      {
        id: 'system',
        name: 'Sistema',
        description: 'Atualizações do sistema e manutenção',
        importance: Notifications.AndroidImportance.LOW,
      },
      {
        id: 'security',
        name: 'Segurança',
        description: 'Alertas de segurança e autenticação',
        importance: Notifications.AndroidImportance.MAX,
        sound: 'default',
        vibrationPattern: [0, 500, 250, 500],
      },
    ];

    for (const channel of channels) {
      await Notifications.setNotificationChannelAsync(channel.id, channel);
    }
  }

  async handleNotificationReceived(notification) {
    console.log('Notificação recebida:', notification);

    // Adicionar ao histórico
    const historyItem = {
      id: notification.request.identifier,
      title: notification.request.content.title,
      body: notification.request.content.body,
      data: notification.request.content.data,
      receivedAt: new Date().toISOString(),
      read: false,
    };

    this.notificationHistory.unshift(historyItem);
    await this.saveNotificationHistory();

    // Atualizar badge
    await this.updateBadgeCount();
  }

  async handleNotificationResponse(response) {
    console.log('Resposta à notificação:', response);

    const { notification, actionIdentifier } = response;
    const notificationData = notification.request.content.data || {};

    // Marcar como lida
    await this.markAsRead(notification.request.identifier);

    // Processar ação baseada no tipo
    switch (notificationData.type) {
      case 'transaction':
        // Navegar para detalhes da transação
        this.handleTransactionNotification(notificationData);
        break;
      
      case 'promotion':
        // Navegar para promoção
        this.handlePromotionNotification(notificationData);
        break;
      
      case 'esg':
        // Navegar para dashboard ESG
        this.handleESGNotification(notificationData);
        break;
      
      case 'security':
        // Navegar para configurações de segurança
        this.handleSecurityNotification(notificationData);
        break;
      
      default:
        console.log('Tipo de notificação não reconhecido:', notificationData.type);
    }
  }

  // Enviar notificação local
  async sendLocalNotification(options) {
    const {
      title,
      body,
      data = {},
      categoryId = 'default',
      delay = 0,
      sound = true,
      priority = 'default',
    } = options;

    // Verificar se notificações estão habilitadas
    if (!this.preferences.enabled) {
      console.log('Notificações desabilitadas pelo usuário');
      return null;
    }

    // Verificar categoria específica
    if (!this.preferences.categories[categoryId]) {
      console.log(`Categoria ${categoryId} desabilitada pelo usuário`);
      return null;
    }

    // Verificar horário silencioso
    if (this.isQuietHours()) {
      console.log('Horário silencioso ativo - notificação suprimida');
      return null;
    }

    try {
      const notificationId = await Notifications.scheduleNotificationAsync({
        content: {
          title,
          body,
          data: {
            ...data,
            type: categoryId,
            timestamp: new Date().toISOString(),
          },
          sound: sound && this.preferences.sound ? 'default' : false,
          priority: this.getPriority(priority),
        },
        trigger: delay > 0 ? { seconds: delay } : null,
      });

      console.log('Notificação local enviada:', notificationId);
      return notificationId;

    } catch (error) {
      console.error('Erro ao enviar notificação local:', error);
      return null;
    }
  }

  // Notificações específicas do GuardFlow
  async notifyTransactionComplete(transaction) {
    return await this.sendLocalNotification({
      title: 'Transação Concluída',
      body: `Compra de R$ ${transaction.amount.toFixed(2)} realizada com sucesso`,
      categoryId: 'transactions',
      data: {
        transactionId: transaction.id,
        amount: transaction.amount,
      },
      priority: 'high',
    });
  }

  async notifyESGAchievement(achievement) {
    return await this.sendLocalNotification({
      title: '🌱 Conquista ESG!',
      body: achievement.description,
      categoryId: 'esg',
      data: {
        achievementId: achievement.id,
        points: achievement.points,
      },
      priority: 'default',
    });
  }

  async notifyPromotion(promotion) {
    return await this.sendLocalNotification({
      title: '🎉 Oferta Especial!',
      body: promotion.description,
      categoryId: 'promotions',
      data: {
        promotionId: promotion.id,
        discount: promotion.discount,
      },
      priority: 'default',
    });
  }

  async notifySecurityAlert(alert) {
    return await this.sendLocalNotification({
      title: '🔒 Alerta de Segurança',
      body: alert.message,
      categoryId: 'security',
      data: {
        alertId: alert.id,
        severity: alert.severity,
      },
      priority: 'max',
      sound: true,
    });
  }

  async notifySystemUpdate(update) {
    return await this.sendLocalNotification({
      title: 'Atualização Disponível',
      body: `GuardFlow ${update.version} está disponível`,
      categoryId: 'system',
      data: {
        version: update.version,
        features: update.features,
      },
      priority: 'low',
    });
  }

  // Gerenciamento de preferências
  async updatePreferences(newPreferences) {
    this.preferences = { ...this.preferences, ...newPreferences };
    await AsyncStorage.setItem('notification_preferences', JSON.stringify(this.preferences));
  }

  async loadPreferences() {
    try {
      const saved = await AsyncStorage.getItem('notification_preferences');
      if (saved) {
        this.preferences = { ...this.preferences, ...JSON.parse(saved) };
      }
    } catch (error) {
      console.error('Erro ao carregar preferências:', error);
    }
  }

  getPreferences() {
    return { ...this.preferences };
  }

  // Gerenciamento de histórico
  async loadNotificationHistory() {
    try {
      const history = await AsyncStorage.getItem('notification_history');
      if (history) {
        this.notificationHistory = JSON.parse(history);
      }
    } catch (error) {
      console.error('Erro ao carregar histórico:', error);
    }
  }

  async saveNotificationHistory() {
    try {
      // Manter apenas os últimos 100 itens
      const recentHistory = this.notificationHistory.slice(0, 100);
      await AsyncStorage.setItem('notification_history', JSON.stringify(recentHistory));
      this.notificationHistory = recentHistory;
    } catch (error) {
      console.error('Erro ao salvar histórico:', error);
    }
  }

  getNotificationHistory() {
    return [...this.notificationHistory];
  }

  async markAsRead(notificationId) {
    const notification = this.notificationHistory.find(n => n.id === notificationId);
    if (notification) {
      notification.read = true;
      await this.saveNotificationHistory();
      await this.updateBadgeCount();
    }
  }

  async markAllAsRead() {
    this.notificationHistory.forEach(n => n.read = true);
    await this.saveNotificationHistory();
    await this.updateBadgeCount();
  }

  async clearHistory() {
    this.notificationHistory = [];
    await AsyncStorage.removeItem('notification_history');
    await this.updateBadgeCount();
  }

  // Gerenciamento de badge
  async updateBadgeCount() {
    const unreadCount = this.notificationHistory.filter(n => !n.read).length;
    await Notifications.setBadgeCountAsync(unreadCount);
  }

  // Utilitários
  isQuietHours() {
    if (!this.preferences.quietHours.enabled) return false;

    const now = new Date();
    const currentTime = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
    
    const { start, end } = this.preferences.quietHours;
    
    if (start <= end) {
      return currentTime >= start && currentTime <= end;
    } else {
      return currentTime >= start || currentTime <= end;
    }
  }

  getPriority(priority) {
    const priorityMap = {
      'min': Notifications.AndroidImportance.MIN,
      'low': Notifications.AndroidImportance.LOW,
      'default': Notifications.AndroidImportance.DEFAULT,
      'high': Notifications.AndroidImportance.HIGH,
      'max': Notifications.AndroidImportance.MAX,
    };
    
    return priorityMap[priority] || Notifications.AndroidImportance.DEFAULT;
  }

  // Handlers específicos
  handleTransactionNotification(data) {
    // Implementar navegação para detalhes da transação
    console.log('Navegando para transação:', data.transactionId);
  }

  handlePromotionNotification(data) {
    // Implementar navegação para promoção
    console.log('Navegando para promoção:', data.promotionId);
  }

  handleESGNotification(data) {
    // Implementar navegação para dashboard ESG
    console.log('Navegando para ESG:', data.achievementId);
  }

  handleSecurityNotification(data) {
    // Implementar navegação para configurações de segurança
    console.log('Navegando para segurança:', data.alertId);
  }

  // Cancelar notificações
  async cancelNotification(notificationId) {
    await Notifications.cancelScheduledNotificationAsync(notificationId);
  }

  async cancelAllNotifications() {
    await Notifications.cancelAllScheduledNotificationsAsync();
  }

  // Estatísticas
  getStats() {
    const total = this.notificationHistory.length;
    const unread = this.notificationHistory.filter(n => !n.read).length;
    const byCategory = this.notificationHistory.reduce((acc, n) => {
      const category = n.data?.type || 'unknown';
      acc[category] = (acc[category] || 0) + 1;
      return acc;
    }, {});

    return {
      total,
      unread,
      read: total - unread,
      byCategory,
      expoPushToken: this.expoPushToken,
      isInitialized: this.isInitialized,
    };
  }

  // Cleanup
  destroy() {
    if (this.notificationListener) {
      Notifications.removeNotificationSubscription(this.notificationListener);
    }
    if (this.responseListener) {
      Notifications.removeNotificationSubscription(this.responseListener);
    }
  }
}

export default new NotificationManager();
