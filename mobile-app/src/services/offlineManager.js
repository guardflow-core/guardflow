/**
 * GuardFlow Offline Manager
 * Gerenciador de modo offline com sincronização automática
 */

import AsyncStorage from '@react-native-async-storage/async-storage';
import NetInfo from '@react-native-netinfo/netinfo';
import { Alert } from 'react-native';

class OfflineManager {
  constructor() {
    this.isOnline = true;
    this.syncQueue = [];
    this.listeners = [];
    this.syncInProgress = false;
    this.lastSyncTime = null;
    this.offlineData = {
      products: [],
      cart: [],
      transactions: [],
      userProfile: null,
      settings: {},
    };
    
    this.init();
  }

  async init() {
    try {
      // Monitorar estado da conexão
      this.unsubscribeNetInfo = NetInfo.addEventListener(state => {
        const wasOnline = this.isOnline;
        this.isOnline = state.isConnected;
        
        if (!wasOnline && this.isOnline) {
          // Voltou online - sincronizar dados
          this.handleBackOnline();
        } else if (wasOnline && !this.isOnline) {
          // Ficou offline
          this.handleGoOffline();
        }
        
        // Notificar listeners
        this.notifyListeners({
          isOnline: this.isOnline,
          connectionType: state.type,
          isInternetReachable: state.isInternetReachable,
        });
      });

      // Carregar dados offline salvos
      await this.loadOfflineData();
      
      // Carregar fila de sincronização
      await this.loadSyncQueue();
      
      // Verificar se há dados para sincronizar
      if (this.isOnline && this.syncQueue.length > 0) {
        this.startSync();
      }
      
    } catch (error) {
      console.error('Erro ao inicializar OfflineManager:', error);
    }
  }

  // Adicionar listener para mudanças de conectividade
  addConnectionListener(callback) {
    this.listeners.push(callback);
    
    // Retornar função para remover listener
    return () => {
      this.listeners = this.listeners.filter(listener => listener !== callback);
    };
  }

  // Notificar todos os listeners
  notifyListeners(connectionInfo) {
    this.listeners.forEach(callback => {
      try {
        callback(connectionInfo);
      } catch (error) {
        console.error('Erro ao notificar listener:', error);
      }
    });
  }

  // Verificar se está online
  getConnectionStatus() {
    return {
      isOnline: this.isOnline,
      lastSyncTime: this.lastSyncTime,
      pendingSync: this.syncQueue.length,
      syncInProgress: this.syncInProgress,
    };
  }

  // Salvar dados para uso offline
  async saveOfflineData(key, data) {
    try {
      this.offlineData[key] = data;
      await AsyncStorage.setItem(`offline_${key}`, JSON.stringify(data));
      return true;
    } catch (error) {
      console.error(`Erro ao salvar dados offline (${key}):`, error);
      return false;
    }
  }

  // Obter dados offline
  async getOfflineData(key) {
    try {
      if (this.offlineData[key]) {
        return this.offlineData[key];
      }
      
      const data = await AsyncStorage.getItem(`offline_${key}`);
      if (data) {
        this.offlineData[key] = JSON.parse(data);
        return this.offlineData[key];
      }
      
      return null;
    } catch (error) {
      console.error(`Erro ao obter dados offline (${key}):`, error);
      return null;
    }
  }

  // Carregar todos os dados offline
  async loadOfflineData() {
    try {
      const keys = ['products', 'cart', 'transactions', 'userProfile', 'settings'];
      
      for (const key of keys) {
        const data = await this.getOfflineData(key);
        if (data) {
          this.offlineData[key] = data;
        }
      }
      
      // Carregar timestamp da última sincronização
      const lastSync = await AsyncStorage.getItem('last_sync_time');
      if (lastSync) {
        this.lastSyncTime = new Date(lastSync);
      }
      
    } catch (error) {
      console.error('Erro ao carregar dados offline:', error);
    }
  }

  // Adicionar operação à fila de sincronização
  async addToSyncQueue(operation) {
    try {
      const syncItem = {
        id: `sync_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        timestamp: new Date().toISOString(),
        operation: operation.type,
        data: operation.data,
        endpoint: operation.endpoint,
        method: operation.method || 'POST',
        priority: operation.priority || 'normal', // high, normal, low
        retries: 0,
        maxRetries: operation.maxRetries || 3,
      };
      
      this.syncQueue.push(syncItem);
      await this.saveSyncQueue();
      
      // Se estiver online, tentar sincronizar imediatamente
      if (this.isOnline && !this.syncInProgress) {
        this.startSync();
      }
      
      return syncItem.id;
    } catch (error) {
      console.error('Erro ao adicionar à fila de sincronização:', error);
      return null;
    }
  }

  // Salvar fila de sincronização
  async saveSyncQueue() {
    try {
      await AsyncStorage.setItem('sync_queue', JSON.stringify(this.syncQueue));
    } catch (error) {
      console.error('Erro ao salvar fila de sincronização:', error);
    }
  }

  // Carregar fila de sincronização
  async loadSyncQueue() {
    try {
      const queue = await AsyncStorage.getItem('sync_queue');
      if (queue) {
        this.syncQueue = JSON.parse(queue);
      }
    } catch (error) {
      console.error('Erro ao carregar fila de sincronização:', error);
    }
  }

  // Iniciar sincronização
  async startSync() {
    if (this.syncInProgress || !this.isOnline || this.syncQueue.length === 0) {
      return;
    }

    this.syncInProgress = true;
    
    try {
      // Ordenar por prioridade e timestamp
      this.syncQueue.sort((a, b) => {
        const priorityOrder = { high: 3, normal: 2, low: 1 };
        const aPriority = priorityOrder[a.priority] || 2;
        const bPriority = priorityOrder[b.priority] || 2;
        
        if (aPriority !== bPriority) {
          return bPriority - aPriority;
        }
        
        return new Date(a.timestamp) - new Date(b.timestamp);
      });

      const itemsToSync = [...this.syncQueue];
      
      for (const item of itemsToSync) {
        if (!this.isOnline) {
          break; // Parar se ficou offline durante a sincronização
        }
        
        try {
          await this.syncItem(item);
          
          // Remover item da fila após sucesso
          this.syncQueue = this.syncQueue.filter(qItem => qItem.id !== item.id);
          
        } catch (error) {
          console.error(`Erro ao sincronizar item ${item.id}:`, error);
          
          // Incrementar contador de tentativas
          const queueItem = this.syncQueue.find(qItem => qItem.id === item.id);
          if (queueItem) {
            queueItem.retries++;
            
            // Remover se excedeu tentativas máximas
            if (queueItem.retries >= queueItem.maxRetries) {
              this.syncQueue = this.syncQueue.filter(qItem => qItem.id !== item.id);
              console.warn(`Item ${item.id} removido da fila após ${queueItem.retries} tentativas`);
            }
          }
        }
      }
      
      // Salvar fila atualizada
      await this.saveSyncQueue();
      
      // Atualizar timestamp da última sincronização
      this.lastSyncTime = new Date();
      await AsyncStorage.setItem('last_sync_time', this.lastSyncTime.toISOString());
      
    } catch (error) {
      console.error('Erro durante sincronização:', error);
    } finally {
      this.syncInProgress = false;
    }
  }

  // Sincronizar item individual
  async syncItem(item) {
    const { endpoint, method, data } = item;
    
    // Simular chamada de API
    // Em produção, usaria o cliente HTTP real
    const response = await fetch(endpoint, {
      method,
      headers: {
        'Content-Type': 'application/json',
        // Adicionar headers de autenticação aqui
      },
      body: method !== 'GET' ? JSON.stringify(data) : undefined,
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    const result = await response.json();
    
    // Processar resultado baseado no tipo de operação
    await this.processSyncResult(item, result);
    
    return result;
  }

  // Processar resultado da sincronização
  async processSyncResult(item, result) {
    switch (item.operation) {
      case 'create_transaction':
        // Atualizar transação local com ID do servidor
        if (result.id) {
          const transactions = await this.getOfflineData('transactions') || [];
          const updatedTransactions = transactions.map(t => 
            t.localId === item.data.localId ? { ...t, id: result.id, synced: true } : t
          );
          await this.saveOfflineData('transactions', updatedTransactions);
        }
        break;
        
      case 'update_cart':
        // Sincronizar carrinho
        if (result.cart) {
          await this.saveOfflineData('cart', result.cart);
        }
        break;
        
      case 'update_profile':
        // Atualizar perfil do usuário
        if (result.profile) {
          await this.saveOfflineData('userProfile', result.profile);
        }
        break;
        
      default:
        console.log(`Resultado da sincronização (${item.operation}):`, result);
    }
  }

  // Lidar com volta online
  async handleBackOnline() {
    console.log('Dispositivo voltou online - iniciando sincronização');
    
    // Notificar usuário se há dados para sincronizar
    if (this.syncQueue.length > 0) {
      Alert.alert(
        'Sincronizando dados',
        `Sincronizando ${this.syncQueue.length} operações pendentes...`,
        [{ text: 'OK' }]
      );
    }
    
    // Iniciar sincronização
    await this.startSync();
    
    // Baixar dados atualizados do servidor
    await this.downloadLatestData();
  }

  // Lidar com ficar offline
  handleGoOffline() {
    console.log('Dispositivo ficou offline - modo offline ativado');
    
    Alert.alert(
      'Modo Offline',
      'Você está offline. Suas ações serão sincronizadas quando a conexão for restabelecida.',
      [{ text: 'OK' }]
    );
  }

  // Baixar dados mais recentes do servidor
  async downloadLatestData() {
    try {
      // Baixar produtos atualizados
      // Em produção, faria chamadas reais para API
      const mockProducts = [
        { id: '1', name: 'Produto 1', price: 10.00, barcode: '1234567890' },
        { id: '2', name: 'Produto 2', price: 15.50, barcode: '0987654321' },
      ];
      await this.saveOfflineData('products', mockProducts);
      
      // Baixar configurações atualizadas
      const mockSettings = {
        theme: 'light',
        notifications: true,
        biometric: false,
      };
      await this.saveOfflineData('settings', mockSettings);
      
    } catch (error) {
      console.error('Erro ao baixar dados atualizados:', error);
    }
  }

  // Operações offline para produtos
  async getProducts() {
    const products = await this.getOfflineData('products');
    return products || [];
  }

  async searchProducts(query) {
    const products = await this.getProducts();
    return products.filter(product => 
      product.name.toLowerCase().includes(query.toLowerCase()) ||
      product.barcode.includes(query)
    );
  }

  // Operações offline para carrinho
  async getCart() {
    const cart = await this.getOfflineData('cart');
    return cart || [];
  }

  async addToCart(product, quantity = 1) {
    const cart = await this.getCart();
    const existingItem = cart.find(item => item.id === product.id);
    
    if (existingItem) {
      existingItem.quantity += quantity;
    } else {
      cart.push({ ...product, quantity });
    }
    
    await this.saveOfflineData('cart', cart);
    
    // Adicionar à fila de sincronização se online
    if (this.isOnline) {
      await this.addToSyncQueue({
        type: 'update_cart',
        endpoint: '/api/v1/cart/sync',
        data: { cart },
        priority: 'normal',
      });
    }
    
    return cart;
  }

  async removeFromCart(productId) {
    const cart = await this.getCart();
    const updatedCart = cart.filter(item => item.id !== productId);
    
    await this.saveOfflineData('cart', updatedCart);
    
    if (this.isOnline) {
      await this.addToSyncQueue({
        type: 'update_cart',
        endpoint: '/api/v1/cart/sync',
        data: { cart: updatedCart },
        priority: 'normal',
      });
    }
    
    return updatedCart;
  }

  // Operações offline para transações
  async createTransaction(transactionData) {
    const transactions = await this.getOfflineData('transactions') || [];
    
    const localTransaction = {
      ...transactionData,
      localId: `local_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      timestamp: new Date().toISOString(),
      synced: false,
    };
    
    transactions.push(localTransaction);
    await this.saveOfflineData('transactions', transactions);
    
    // Adicionar à fila de sincronização
    await this.addToSyncQueue({
      type: 'create_transaction',
      endpoint: '/api/v1/transactions',
      data: localTransaction,
      priority: 'high',
    });
    
    return localTransaction;
  }

  async getTransactions() {
    const transactions = await this.getOfflineData('transactions');
    return transactions || [];
  }

  // Limpar dados offline
  async clearOfflineData() {
    try {
      const keys = ['products', 'cart', 'transactions', 'userProfile', 'settings'];
      
      for (const key of keys) {
        await AsyncStorage.removeItem(`offline_${key}`);
        this.offlineData[key] = key === 'cart' || key === 'transactions' ? [] : 
                               key === 'settings' ? {} : null;
      }
      
      // Limpar fila de sincronização
      this.syncQueue = [];
      await AsyncStorage.removeItem('sync_queue');
      await AsyncStorage.removeItem('last_sync_time');
      this.lastSyncTime = null;
      
      return true;
    } catch (error) {
      console.error('Erro ao limpar dados offline:', error);
      return false;
    }
  }

  // Obter estatísticas do modo offline
  getOfflineStats() {
    return {
      isOnline: this.isOnline,
      lastSyncTime: this.lastSyncTime,
      pendingOperations: this.syncQueue.length,
      syncInProgress: this.syncInProgress,
      offlineDataSize: {
        products: this.offlineData.products?.length || 0,
        cart: this.offlineData.cart?.length || 0,
        transactions: this.offlineData.transactions?.length || 0,
      },
      highPriorityPending: this.syncQueue.filter(item => item.priority === 'high').length,
    };
  }

  // Cleanup
  destroy() {
    if (this.unsubscribeNetInfo) {
      this.unsubscribeNetInfo();
    }
    this.listeners = [];
  }
}

export default new OfflineManager();
