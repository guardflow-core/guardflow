/**
 * GuardFlow Offline Status Component
 * Componente para mostrar status de conectividade e sincronização
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Animated,
  Dimensions,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import offlineManager from '../services/offlineManager';

const { width } = Dimensions.get('window');

const OfflineStatus = ({ style }) => {
  const [connectionStatus, setConnectionStatus] = useState({
    isOnline: true,
    lastSyncTime: null,
    pendingSync: 0,
    syncInProgress: false,
  });
  const [showDetails, setShowDetails] = useState(false);
  const [slideAnim] = useState(new Animated.Value(-100));

  useEffect(() => {
    // Obter status inicial
    updateConnectionStatus();

    // Adicionar listener para mudanças de conectividade
    const removeListener = offlineManager.addConnectionListener((info) => {
      updateConnectionStatus();
      
      // Mostrar banner quando ficar offline/online
      if (!info.isOnline) {
        showBanner();
      } else if (info.isOnline && connectionStatus.pendingSync > 0) {
        showBanner();
      }
    });

    return () => {
      removeListener();
    };
  }, []);

  const updateConnectionStatus = () => {
    const status = offlineManager.getConnectionStatus();
    setConnectionStatus(status);
  };

  const showBanner = () => {
    Animated.sequence([
      Animated.timing(slideAnim, {
        toValue: 0,
        duration: 300,
        useNativeDriver: true,
      }),
      Animated.delay(3000),
      Animated.timing(slideAnim, {
        toValue: -100,
        duration: 300,
        useNativeDriver: true,
      }),
    ]).start();
  };

  const handlePress = () => {
    setShowDetails(!showDetails);
    updateConnectionStatus();
  };

  const formatLastSync = (lastSyncTime) => {
    if (!lastSyncTime) return 'Nunca';
    
    const now = new Date();
    const sync = new Date(lastSyncTime);
    const diffMs = now - sync;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);
    
    if (diffMins < 1) return 'Agora mesmo';
    if (diffMins < 60) return `${diffMins}min atrás`;
    if (diffHours < 24) return `${diffHours}h atrás`;
    return `${diffDays}d atrás`;
  };

  const getStatusColor = () => {
    if (!connectionStatus.isOnline) return '#FF3B30';
    if (connectionStatus.syncInProgress) return '#FF9500';
    if (connectionStatus.pendingSync > 0) return '#FF9500';
    return '#34C759';
  };

  const getStatusIcon = () => {
    if (!connectionStatus.isOnline) return 'cloud-offline';
    if (connectionStatus.syncInProgress) return 'sync';
    if (connectionStatus.pendingSync > 0) return 'cloud-upload';
    return 'cloud-done';
  };

  const getStatusText = () => {
    if (!connectionStatus.isOnline) return 'Offline';
    if (connectionStatus.syncInProgress) return 'Sincronizando...';
    if (connectionStatus.pendingSync > 0) return `${connectionStatus.pendingSync} pendente${connectionStatus.pendingSync > 1 ? 's' : ''}`;
    return 'Online';
  };

  return (
    <>
      {/* Banner de status (aparece temporariamente) */}
      <Animated.View
        style={[
          styles.banner,
          {
            backgroundColor: getStatusColor(),
            transform: [{ translateY: slideAnim }],
          },
        ]}
      >
        <View style={styles.bannerContent}>
          <Ionicons name={getStatusIcon()} size={16} color="#FFFFFF" />
          <Text style={styles.bannerText}>
            {connectionStatus.isOnline 
              ? connectionStatus.pendingSync > 0 
                ? `Sincronizando ${connectionStatus.pendingSync} operações...`
                : 'Conectado e sincronizado'
              : 'Modo offline ativado'
            }
          </Text>
        </View>
      </Animated.View>

      {/* Indicador de status (sempre visível) */}
      <TouchableOpacity
        style={[styles.statusIndicator, style]}
        onPress={handlePress}
        activeOpacity={0.7}
      >
        <View style={styles.statusContent}>
          <View style={[styles.statusDot, { backgroundColor: getStatusColor() }]} />
          <Text style={styles.statusText}>{getStatusText()}</Text>
          <Ionicons 
            name={showDetails ? 'chevron-up' : 'chevron-down'} 
            size={16} 
            color="#8E8E93" 
          />
        </View>

        {/* Detalhes expandidos */}
        {showDetails && (
          <View style={styles.detailsContainer}>
            <View style={styles.detailRow}>
              <Text style={styles.detailLabel}>Status:</Text>
              <View style={styles.detailValue}>
                <Ionicons name={getStatusIcon()} size={16} color={getStatusColor()} />
                <Text style={[styles.detailText, { color: getStatusColor() }]}>
                  {connectionStatus.isOnline ? 'Online' : 'Offline'}
                </Text>
              </View>
            </View>

            <View style={styles.detailRow}>
              <Text style={styles.detailLabel}>Última Sync:</Text>
              <Text style={styles.detailText}>
                {formatLastSync(connectionStatus.lastSyncTime)}
              </Text>
            </View>

            {connectionStatus.pendingSync > 0 && (
              <View style={styles.detailRow}>
                <Text style={styles.detailLabel}>Pendentes:</Text>
                <Text style={[styles.detailText, { color: '#FF9500' }]}>
                  {connectionStatus.pendingSync} operações
                </Text>
              </View>
            )}

            {connectionStatus.syncInProgress && (
              <View style={styles.detailRow}>
                <Text style={styles.detailLabel}>Sincronização:</Text>
                <View style={styles.detailValue}>
                  <Ionicons name="sync" size={16} color="#FF9500" />
                  <Text style={[styles.detailText, { color: '#FF9500' }]}>
                    Em andamento...
                  </Text>
                </View>
              </View>
            )}

            {/* Botão de sincronização manual */}
            {connectionStatus.isOnline && connectionStatus.pendingSync > 0 && !connectionStatus.syncInProgress && (
              <TouchableOpacity
                style={styles.syncButton}
                onPress={() => {
                  offlineManager.startSync();
                  updateConnectionStatus();
                }}
              >
                <Ionicons name="refresh" size={16} color="#007AFF" />
                <Text style={styles.syncButtonText}>Sincronizar Agora</Text>
              </TouchableOpacity>
            )}
          </View>
        )}
      </TouchableOpacity>
    </>
  );
};

const styles = StyleSheet.create({
  banner: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    zIndex: 1000,
    paddingTop: 44, // Status bar height
    paddingBottom: 8,
    paddingHorizontal: 16,
  },
  bannerContent: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  bannerText: {
    color: '#FFFFFF',
    fontSize: 14,
    fontWeight: '500',
    marginLeft: 8,
  },
  statusIndicator: {
    backgroundColor: '#FFFFFF',
    borderRadius: 8,
    padding: 12,
    marginHorizontal: 16,
    marginVertical: 8,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 1,
    },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  statusContent: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginRight: 8,
  },
  statusText: {
    flex: 1,
    fontSize: 14,
    fontWeight: '500',
    color: '#000000',
  },
  detailsContainer: {
    marginTop: 12,
    paddingTop: 12,
    borderTopWidth: 1,
    borderTopColor: '#F2F2F7',
  },
  detailRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  detailLabel: {
    fontSize: 14,
    color: '#8E8E93',
    fontWeight: '500',
  },
  detailValue: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  detailText: {
    fontSize: 14,
    color: '#000000',
    marginLeft: 4,
  },
  syncButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#F2F2F7',
    borderRadius: 6,
    padding: 8,
    marginTop: 8,
  },
  syncButtonText: {
    fontSize: 14,
    color: '#007AFF',
    fontWeight: '500',
    marginLeft: 4,
  },
});

export default OfflineStatus;
