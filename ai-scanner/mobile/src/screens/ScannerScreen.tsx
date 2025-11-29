import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Alert, FlatList } from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { AppDispatch, RootState } from '../store';
import { startScan, scanSuccess, scanFailure, stopScan } from '../store/slices/scannerSlice';
import { addItemToCart } from '../store/slices/cartSlice';
import { MaterialCommunityIcons } from '@expo/vector-icons';

const ScannerScreen: React.FC = () => {
  const dispatch: AppDispatch = useDispatch();
  const { isScanning, lastScannedProduct, scanHistory, error } = useSelector((state: RootState) => state.scanner);
  const [scanningMode, setScanningMode] = useState<'barcode' | 'qr'>('barcode');

  const handleStartScan = () => {
    dispatch(startScan());
    // Simulate scanning process
    setTimeout(() => {
      const mockProduct = {
        id: Date.now().toString(),
        name: 'Produto Escaneado',
        barcode: '1234567890123',
        confidence: 0.95,
        imageUrl: undefined,
      };
      dispatch(scanSuccess(mockProduct));
    }, 2000);
  };

  const handleStopScan = () => {
    dispatch(stopScan());
  };

  const handleAddToCart = (product: any) => {
    dispatch(addItemToCart({
      productId: product.id,
      name: product.name,
      price: Math.random() * 50 + 10, // Mock price
      quantity: 1,
    }));
    Alert.alert('Sucesso', 'Produto adicionado ao carrinho!');
  };

  const renderScanHistoryItem = ({ item }: { item: any }) => (
    <View style={styles.historyItem}>
      <MaterialCommunityIcons name="barcode" size={24} color="#666" />
      <View style={styles.historyItemContent}>
        <Text style={styles.historyItemName}>{item.name}</Text>
        <Text style={styles.historyItemBarcode}>{item.barcode}</Text>
      </View>
      <TouchableOpacity
        style={styles.addToCartButton}
        onPress={() => handleAddToCart(item)}
      >
        <MaterialCommunityIcons name="cart-plus" size={20} color="#fff" />
      </TouchableOpacity>
    </View>
  );

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Scanner de Produtos</Text>
        <View style={styles.modeSelector}>
          <TouchableOpacity
            style={[styles.modeButton, scanningMode === 'barcode' && styles.modeButtonActive]}
            onPress={() => setScanningMode('barcode')}
          >
            <Text style={[styles.modeButtonText, scanningMode === 'barcode' && styles.modeButtonTextActive]}>
              Código de Barras
            </Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.modeButton, scanningMode === 'qr' && styles.modeButtonActive]}
            onPress={() => setScanningMode('qr')}
          >
            <Text style={[styles.modeButtonText, scanningMode === 'qr' && styles.modeButtonTextActive]}>
              QR Code
            </Text>
          </TouchableOpacity>
        </View>
      </View>

      <View style={styles.scannerArea}>
        {isScanning ? (
          <View style={styles.scanningContainer}>
            <MaterialCommunityIcons name="barcode-scan" size={80} color="#2196F3" />
            <Text style={styles.scanningText}>Escaneando...</Text>
            <TouchableOpacity style={styles.stopButton} onPress={handleStopScan}>
              <Text style={styles.stopButtonText}>Parar</Text>
            </TouchableOpacity>
          </View>
        ) : (
          <View style={styles.idleContainer}>
            <MaterialCommunityIcons name="camera" size={80} color="#ccc" />
            <Text style={styles.idleText}>
              {scanningMode === 'barcode' ? 'Posicione o código de barras na câmera' : 'Posicione o QR Code na câmera'}
            </Text>
            <TouchableOpacity style={styles.startButton} onPress={handleStartScan}>
              <MaterialCommunityIcons name="play" size={24} color="#fff" />
              <Text style={styles.startButtonText}>Iniciar Escaneamento</Text>
            </TouchableOpacity>
          </View>
        )}

        {error && (
          <View style={styles.errorContainer}>
            <MaterialCommunityIcons name="alert-circle" size={24} color="#f44336" />
            <Text style={styles.errorText}>{error}</Text>
          </View>
        )}
      </View>

      {lastScannedProduct && (
        <View style={styles.lastScannedContainer}>
          <Text style={styles.lastScannedTitle}>Último Produto Escaneado</Text>
          <View style={styles.lastScannedItem}>
            <MaterialCommunityIcons name="barcode" size={24} color="#4CAF50" />
            <View style={styles.lastScannedContent}>
              <Text style={styles.lastScannedName}>{lastScannedProduct.name}</Text>
              <Text style={styles.lastScannedBarcode}>{lastScannedProduct.barcode}</Text>
            </View>
            <TouchableOpacity
              style={styles.addToCartButton}
              onPress={() => handleAddToCart(lastScannedProduct)}
            >
              <MaterialCommunityIcons name="cart-plus" size={20} color="#fff" />
            </TouchableOpacity>
          </View>
        </View>
      )}

      {scanHistory.length > 0 && (
        <View style={styles.historyContainer}>
          <Text style={styles.historyTitle}>Histórico de Escaneamentos</Text>
          <FlatList
            data={scanHistory}
            renderItem={renderScanHistoryItem}
            keyExtractor={(item) => item.id}
            style={styles.historyList}
          />
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: '#fff',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    textAlign: 'center',
    marginBottom: 15,
  },
  modeSelector: {
    flexDirection: 'row',
    backgroundColor: '#f0f0f0',
    borderRadius: 8,
    padding: 4,
  },
  modeButton: {
    flex: 1,
    padding: 10,
    borderRadius: 6,
    alignItems: 'center',
  },
  modeButtonActive: {
    backgroundColor: '#2196F3',
  },
  modeButtonText: {
    color: '#666',
    fontWeight: 'bold',
  },
  modeButtonTextActive: {
    color: '#fff',
  },
  scannerArea: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  scanningContainer: {
    alignItems: 'center',
  },
  scanningText: {
    fontSize: 18,
    color: '#2196F3',
    marginTop: 20,
    marginBottom: 20,
  },
  stopButton: {
    backgroundColor: '#f44336',
    paddingHorizontal: 30,
    paddingVertical: 15,
    borderRadius: 8,
  },
  stopButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  idleContainer: {
    alignItems: 'center',
  },
  idleText: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    marginTop: 20,
    marginBottom: 30,
  },
  startButton: {
    backgroundColor: '#4CAF50',
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 30,
    paddingVertical: 15,
    borderRadius: 8,
  },
  startButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
    marginLeft: 8,
  },
  errorContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#ffebee',
    padding: 15,
    borderRadius: 8,
    marginTop: 20,
  },
  errorText: {
    color: '#f44336',
    marginLeft: 8,
    flex: 1,
  },
  lastScannedContainer: {
    backgroundColor: '#fff',
    padding: 20,
    borderTopWidth: 1,
    borderTopColor: '#e0e0e0',
  },
  lastScannedTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
  },
  lastScannedItem: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 15,
    backgroundColor: '#f9f9f9',
    borderRadius: 8,
  },
  lastScannedContent: {
    flex: 1,
    marginLeft: 15,
  },
  lastScannedName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
  },
  lastScannedBarcode: {
    fontSize: 14,
    color: '#666',
    marginTop: 4,
  },
  addToCartButton: {
    backgroundColor: '#4CAF50',
    padding: 10,
    borderRadius: 6,
    marginLeft: 10,
  },
  historyContainer: {
    backgroundColor: '#fff',
    padding: 20,
    borderTopWidth: 1,
    borderTopColor: '#e0e0e0',
  },
  historyTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
  },
  historyList: {
    maxHeight: 200,
  },
  historyItem: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 15,
    backgroundColor: '#f9f9f9',
    borderRadius: 8,
    marginBottom: 10,
  },
  historyItemContent: {
    flex: 1,
    marginLeft: 15,
  },
  historyItemName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
  },
  historyItemBarcode: {
    fontSize: 14,
    color: '#666',
    marginTop: 4,
  },
});

export default ScannerScreen;
