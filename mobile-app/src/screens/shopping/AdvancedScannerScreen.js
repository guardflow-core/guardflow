/**
 * GuardFlow Advanced Scanner Screen
 * Scanner avançado com IA, múltiplos modos e reconhecimento inteligente
 */

import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Alert,
  Dimensions,
  ActivityIndicator,
  Animated,
  Image,
  Modal,
  ScrollView,
  Vibration,
} from 'react-native';
import { Camera } from 'expo-camera';
import { BarCodeScanner } from 'expo-barcode-scanner';
import * as ImagePicker from 'expo-image-picker';
import * as ImageManipulator from 'expo-image-manipulator';
import { Ionicons } from '@expo/vector-icons';
import { useFocusEffect } from '@react-navigation/native';
import AsyncStorage from '@react-native-async-storage/async-storage';

const { width, height } = Dimensions.get('window');

const AdvancedScannerScreen = ({ navigation }) => {
  const [hasPermission, setHasPermission] = useState(null);
  const [scanned, setScanned] = useState(false);
  const [flashMode, setFlashMode] = useState(Camera.Constants.FlashMode.off);
  const [cameraType, setCameraType] = useState(Camera.Constants.Type.back);
  const [isLoading, setIsLoading] = useState(false);
  const [scannerActive, setScannerActive] = useState(true);
  const [scanMode, setScanMode] = useState('barcode'); // barcode, visual, text, auto
  const [scanHistory, setScanHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);
  const [confidence, setConfidence] = useState(0);
  const [autoScanEnabled, setAutoScanEnabled] = useState(true);
  const [scanStats, setScanStats] = useState({
    totalScans: 0,
    successfulScans: 0,
    avgConfidence: 0,
    sessionScans: 0,
  });
  const [aiProcessing, setAiProcessing] = useState(false);
  const [detectedObjects, setDetectedObjects] = useState([]);
  const [showSettings, setShowSettings] = useState(false);
  
  const cameraRef = useRef(null);
  const scanAnimation = useRef(new Animated.Value(0)).current;
  const confidenceAnimation = useRef(new Animated.Value(0)).current;
  const pulseAnimation = useRef(new Animated.Value(1)).current;

  useFocusEffect(
    React.useCallback(() => {
      setScannerActive(true);
      setScanned(false);
      startAnimations();
      loadScanData();
      
      return () => {
        setScannerActive(false);
        stopAnimations();
      };
    }, [])
  );

  useEffect(() => {
    initializeScanner();
  }, []);

  const initializeScanner = async () => {
    try {
      const { status } = await Camera.requestCameraPermissionsAsync();
      setHasPermission(status === 'granted');
      
      if (status === 'granted') {
        await loadScanData();
      }
    } catch (error) {
      console.error('Erro ao inicializar scanner:', error);
    }
  };

  const loadScanData = async () => {
    try {
      const history = await AsyncStorage.getItem('scan_history');
      const stats = await AsyncStorage.getItem('scan_stats');
      
      if (history) {
        setScanHistory(JSON.parse(history));
      }
      
      if (stats) {
        setScanStats(JSON.parse(stats));
      }
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
    }
  };

  const saveScanData = async (newHistory, newStats) => {
    try {
      await AsyncStorage.setItem('scan_history', JSON.stringify(newHistory));
      await AsyncStorage.setItem('scan_stats', JSON.stringify(newStats));
    } catch (error) {
      console.error('Erro ao salvar dados:', error);
    }
  };

  const startAnimations = () => {
    // Animação da linha de scan
    Animated.loop(
      Animated.sequence([
        Animated.timing(scanAnimation, {
          toValue: 1,
          duration: 2000,
          useNativeDriver: true,
        }),
        Animated.timing(scanAnimation, {
          toValue: 0,
          duration: 0,
          useNativeDriver: true,
        }),
      ])
    ).start();

    // Animação de pulso
    Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnimation, {
          toValue: 1.1,
          duration: 1000,
          useNativeDriver: true,
        }),
        Animated.timing(pulseAnimation, {
          toValue: 1,
          duration: 1000,
          useNativeDriver: true,
        }),
      ])
    ).start();
  };

  const stopAnimations = () => {
    scanAnimation.stopAnimation();
    pulseAnimation.stopAnimation();
    confidenceAnimation.stopAnimation();
  };

  const animateConfidence = (targetConfidence) => {
    Animated.timing(confidenceAnimation, {
      toValue: targetConfidence / 100,
      duration: 500,
      useNativeDriver: false,
    }).start();
  };

  const handleBarCodeScanned = async ({ type, data }) => {
    if (!scannerActive || scanned || !autoScanEnabled) return;
    
    await processScannedData('barcode', data, { type });
  };

  const processScannedData = async (mode, data, extra = {}) => {
    if (scanned) return;
    
    setScanned(true);
    setIsLoading(true);
    setAiProcessing(true);
    stopAnimations();

    // Vibração de feedback
    Vibration.vibrate(100);

    try {
      // Simular processamento com IA avançada
      const processingSteps = [
        { step: 'Analisando dados...', delay: 200 },
        { step: 'Processando com IA...', delay: 400 },
        { step: 'Consultando base de produtos...', delay: 600 },
        { step: 'Verificando informações ESG...', delay: 300 },
        { step: 'Calculando confiança...', delay: 200 },
        { step: 'Enriquecendo dados...', delay: 300 },
      ];

      for (const { step, delay } of processingSteps) {
        await new Promise(resolve => setTimeout(resolve, delay));
      }

      // Simular resultado com IA avançada
      const mockConfidence = Math.floor(Math.random() * 30) + 70; // 70-100%
      const mockProduct = generateMockProduct(mode, data, mockConfidence, extra);

      setConfidence(mockConfidence);
      animateConfidence(mockConfidence);

      // Atualizar estatísticas
      const newStats = {
        ...scanStats,
        totalScans: scanStats.totalScans + 1,
        successfulScans: scanStats.successfulScans + 1,
        sessionScans: scanStats.sessionScans + 1,
        avgConfidence: Math.round(((scanStats.avgConfidence * scanStats.totalScans + mockConfidence) / (scanStats.totalScans + 1)) * 10) / 10,
      };
      setScanStats(newStats);

      // Adicionar ao histórico
      const newHistory = [mockProduct, ...scanHistory.slice(0, 49)]; // Manter últimos 50
      setScanHistory(newHistory);

      // Salvar dados
      await saveScanData(newHistory, newStats);

      // Mostrar resultado baseado na confiança
      await showScanResult(mockProduct);

    } catch (error) {
      console.error('Erro no processamento:', error);
      Alert.alert('Erro', 'Falha no reconhecimento. Tente novamente.');
      resetScanner();
    } finally {
      setIsLoading(false);
      setAiProcessing(false);
    }
  };

  const generateMockProduct = (mode, data, confidence, extra) => {
    const brands = ['Coca-Cola', 'Nestlé', 'Unilever', 'P&G', 'Danone', 'Kraft', 'Mondelez'];
    const categories = ['Alimentação', 'Bebidas', 'Limpeza', 'Higiene', 'Snacks'];
    
    return {
      id: `${mode}_${Date.now()}`,
      name: mode === 'barcode' ? 'Produto Escaneado' : 
            mode === 'visual' ? 'Produto Reconhecido' : 'Produto Identificado',
      brand: brands[Math.floor(Math.random() * brands.length)],
      price: Math.round((Math.random() * 50 + 5) * 100) / 100,
      barcode: mode === 'barcode' ? data : `${Math.floor(Math.random() * 9000000000000) + 1000000000000}`,
      confidence,
      esgScore: Math.round((Math.random() * 4 + 6) * 10) / 10,
      category: categories[Math.floor(Math.random() * categories.length)],
      scanMode: mode,
      timestamp: new Date(),
      nutritionalInfo: mode === 'visual' ? {
        calories: Math.floor(Math.random() * 500) + 50,
        protein: Math.floor(Math.random() * 20) + 2,
        carbs: Math.floor(Math.random() * 60) + 10,
        fat: Math.floor(Math.random() * 30) + 1,
      } : null,
      aiAnalysis: {
        objectDetection: mode === 'visual' ? ['produto', 'embalagem', 'rótulo'] : null,
        textRecognition: mode === 'text' ? ['ingredientes', 'informações nutricionais'] : null,
        qualityScore: confidence,
        processingTime: Math.floor(Math.random() * 2000) + 500,
      },
      sustainability: {
        packaging: ['reciclável', 'biodegradável', 'compostável'][Math.floor(Math.random() * 3)],
        carbonFootprint: Math.round((Math.random() * 5 + 1) * 100) / 100,
        waterUsage: Math.round((Math.random() * 10 + 2) * 100) / 100,
      },
    };
  };

  const showScanResult = async (product) => {
    if (product.confidence >= 90) {
      showHighConfidenceResult(product);
    } else if (product.confidence >= 75) {
      showMediumConfidenceResult(product);
    } else {
      showLowConfidenceResult(product);
    }
  };

  const showHighConfidenceResult = (product) => {
    Alert.alert(
      `✅ ${product.name} (${product.confidence}%)`,
      `${product.brand} • ${product.category}\nR$ ${product.price.toFixed(2)}\n🌱 ESG: ${product.esgScore}/10\n♻️ ${product.sustainability.packaging}`,
      [
        {
          text: 'Ver Detalhes',
          onPress: () => showProductDetails(product),
        },
        {
          text: 'Adicionar ao Carrinho',
          onPress: () => {
            navigation.navigate('Cart', { newProduct: product });
          },
        },
        {
          text: 'Continuar',
          onPress: resetScanner,
        },
      ]
    );
  };

  const showMediumConfidenceResult = (product) => {
    Alert.alert(
      `⚠️ ${product.name} (${product.confidence}%)`,
      `Confiança média. Confirme se é o produto correto:\n${product.brand} • R$ ${product.price.toFixed(2)}\n\nProcessado com ${product.scanMode} em ${product.aiAnalysis.processingTime}ms`,
      [
        {
          text: 'Não é este',
          style: 'cancel',
          onPress: resetScanner,
        },
        {
          text: 'Ver Detalhes',
          onPress: () => showProductDetails(product),
        },
        {
          text: 'Confirmar',
          onPress: () => {
            navigation.navigate('Cart', { newProduct: product });
          },
        },
      ]
    );
  };

  const showLowConfidenceResult = (product) => {
    Alert.alert(
      `❌ Confiança Baixa (${product.confidence}%)`,
      'Não foi possível identificar o produto com certeza. Sugestões:\n• Melhorar a iluminação\n• Aproximar a câmera\n• Limpar a lente\n• Tentar modo visual',
      [
        {
          text: 'Tentar Novamente',
          onPress: resetScanner,
        },
        {
          text: 'Modo Visual',
          onPress: () => {
            setScanMode('visual');
            resetScanner();
          },
        },
        {
          text: 'Buscar Manual',
          onPress: () => navigation.navigate('ProductSearch'),
        },
      ]
    );
  };

  const showProductDetails = (product) => {
    Alert.alert(
      `📋 ${product.name}`,
      `Marca: ${product.brand}\nCategoria: ${product.category}\nPreço: R$ ${product.price.toFixed(2)}\nESG Score: ${product.esgScore}/10\n\nSustentabilidade:\n• Embalagem: ${product.sustainability.packaging}\n• Pegada de carbono: ${product.sustainability.carbonFootprint}kg CO₂\n• Uso de água: ${product.sustainability.waterUsage}L\n\nIA Analysis:\n• Confiança: ${product.confidence}%\n• Tempo: ${product.aiAnalysis.processingTime}ms\n• Modo: ${product.scanMode}`,
      [
        {
          text: 'Fechar',
          style: 'cancel',
        },
        {
          text: 'Adicionar ao Carrinho',
          onPress: () => {
            navigation.navigate('Cart', { newProduct: product });
          },
        },
      ]
    );
  };

  const resetScanner = () => {
    setScanned(false);
    setIsLoading(false);
    setConfidence(0);
    confidenceAnimation.setValue(0);
    startAnimations();
  };

  const capturePhoto = async () => {
    if (cameraRef.current) {
      try {
        setIsLoading(true);
        const photo = await cameraRef.current.takePictureAsync({
          quality: 0.8,
          base64: false,
        });
        
        // Processar com manipulação de imagem
        const manipulatedImage = await ImageManipulator.manipulateAsync(
          photo.uri,
          [{ resize: { width: 800 } }],
          { compress: 0.8, format: ImageManipulator.SaveFormat.JPEG }
        );
        
        await processScannedData('visual', manipulatedImage.uri);
      } catch (error) {
        Alert.alert('Erro', 'Falha ao capturar foto');
        setIsLoading(false);
      }
    }
  };

  const pickImageFromGallery = async () => {
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [4, 3],
      quality: 0.8,
    });

    if (!result.canceled) {
      await processScannedData('visual', result.assets[0].uri);
    }
  };

  const toggleFlash = () => {
    setFlashMode(
      flashMode === Camera.Constants.FlashMode.off
        ? Camera.Constants.FlashMode.torch
        : Camera.Constants.FlashMode.off
    );
  };

  const changeScanMode = () => {
    const modes = ['barcode', 'visual', 'text', 'auto'];
    const currentIndex = modes.indexOf(scanMode);
    const nextIndex = (currentIndex + 1) % modes.length;
    setScanMode(modes[nextIndex]);
    resetScanner();
  };

  const getScanModeInfo = () => {
    const modeInfo = {
      barcode: { icon: 'barcode', name: 'Código de Barras', color: '#00FF00' },
      visual: { icon: 'camera', name: 'Reconhecimento Visual', color: '#007AFF' },
      text: { icon: 'text', name: 'Reconhecimento de Texto', color: '#FF9500' },
      auto: { icon: 'scan', name: 'Modo Automático', color: '#5856D6' },
    };
    return modeInfo[scanMode] || modeInfo.barcode;
  };

  if (hasPermission === null) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color="#007AFF" />
        <Text style={styles.loadingText}>Inicializando scanner avançado...</Text>
      </View>
    );
  }

  if (hasPermission === false) {
    return (
      <View style={styles.centerContainer}>
        <Ionicons name="camera-off" size={64} color="#8E8E93" />
        <Text style={styles.errorText}>Acesso à câmera negado</Text>
        <Text style={styles.errorSubtext}>
          Habilite o acesso à câmera nas configurações para usar o scanner avançado
        </Text>
        <TouchableOpacity
          style={styles.retryButton}
          onPress={initializeScanner}
        >
          <Text style={styles.retryButtonText}>Tentar Novamente</Text>
        </TouchableOpacity>
      </View>
    );
  }

  const modeInfo = getScanModeInfo();

  return (
    <View style={styles.container}>
      <Camera
        ref={cameraRef}
        style={styles.camera}
        type={cameraType}
        flashMode={flashMode}
        onBarCodeScanned={scanMode === 'barcode' && !scanned ? handleBarCodeScanned : undefined}
        barCodeScannerSettings={{
          barCodeTypes: [
            BarCodeScanner.Constants.BarCodeType.ean13,
            BarCodeScanner.Constants.BarCodeType.ean8,
            BarCodeScanner.Constants.BarCodeType.upc_a,
            BarCodeScanner.Constants.BarCodeType.upc_e,
            BarCodeScanner.Constants.BarCodeType.code128,
            BarCodeScanner.Constants.BarCodeType.code39,
            BarCodeScanner.Constants.BarCodeType.qr,
          ],
        }}
      >
        {/* Overlay */}
        <View style={styles.overlay}>
          {/* Header */}
          <View style={styles.header}>
            <TouchableOpacity
              style={styles.headerButton}
              onPress={() => navigation.goBack()}
            >
              <Ionicons name="close" size={24} color="white" />
            </TouchableOpacity>
            
            <View style={styles.headerCenter}>
              <Text style={styles.headerTitle}>Scanner Avançado</Text>
              <Text style={[styles.headerSubtitle, { color: modeInfo.color }]}>
                {modeInfo.name}
              </Text>
              {scanStats.sessionScans > 0 && (
                <Text style={styles.headerStats}>
                  {scanStats.sessionScans} scans • {scanStats.avgConfidence}% avg
                </Text>
              )}
            </View>
            
            <TouchableOpacity
              style={styles.headerButton}
              onPress={() => setShowHistory(true)}
            >
              <Ionicons name="time" size={24} color="white" />
              {scanHistory.length > 0 && (
                <View style={styles.badge}>
                  <Text style={styles.badgeText}>{scanHistory.length}</Text>
                </View>
              )}
            </TouchableOpacity>
          </View>

          {/* Controls */}
          <View style={styles.controls}>
            <TouchableOpacity
              style={[styles.controlButton, { backgroundColor: modeInfo.color }]}
              onPress={changeScanMode}
            >
              <Ionicons name={modeInfo.icon} size={20} color="white" />
            </TouchableOpacity>
            
            <TouchableOpacity
              style={styles.controlButton}
              onPress={toggleFlash}
            >
              <Ionicons
                name={flashMode === Camera.Constants.FlashMode.off ? 'flash-off' : 'flash'}
                size={20}
                color="white"
              />
            </TouchableOpacity>
            
            <TouchableOpacity
              style={[styles.controlButton, autoScanEnabled && styles.activeControl]}
              onPress={() => setAutoScanEnabled(!autoScanEnabled)}
            >
              <Ionicons
                name={autoScanEnabled ? 'scan' : 'scan-outline'}
                size={20}
                color="white"
              />
            </TouchableOpacity>
          </View>

          {/* Scanner Area */}
          <View style={styles.scannerArea}>
            <Animated.View
              style={[
                styles.scannerFrame,
                {
                  transform: [{ scale: pulseAnimation }],
                  borderColor: modeInfo.color,
                }
              ]}
            >
              {/* Cantos do frame */}
              <View style={[styles.corner, styles.topLeft, { borderColor: modeInfo.color }]} />
              <View style={[styles.corner, styles.topRight, { borderColor: modeInfo.color }]} />
              <View style={[styles.corner, styles.bottomLeft, { borderColor: modeInfo.color }]} />
              <View style={[styles.corner, styles.bottomRight, { borderColor: modeInfo.color }]} />
              
              {/* Linha de scan animada */}
              {scanMode === 'barcode' && !scanned && (
                <Animated.View
                  style={[
                    styles.scanLine,
                    {
                      backgroundColor: modeInfo.color,
                      transform: [
                        {
                          translateY: scanAnimation.interpolate({
                            inputRange: [0, 1],
                            outputRange: [0, 220],
                          }),
                        },
                      ],
                    },
                  ]}
                />
              )}
              
              {/* Indicador de confiança */}
              {confidence > 0 && (
                <View style={styles.confidenceIndicator}>
                  <Text style={styles.confidenceText}>{confidence}%</Text>
                  <View style={styles.confidenceBar}>
                    <Animated.View
                      style={[
                        styles.confidenceFill,
                        {
                          width: confidenceAnimation.interpolate({
                            inputRange: [0, 1],
                            outputRange: ['0%', '100%'],
                          }),
                          backgroundColor: confidence >= 85 ? '#00FF00' : confidence >= 70 ? '#FF9500' : '#FF3B30',
                        },
                      ]}
                    />
                  </View>
                </View>
              )}
            </Animated.View>
            
            <Text style={styles.instructionText}>
              {scanMode === 'barcode' 
                ? 'Posicione o código de barras dentro do quadro'
                : scanMode === 'visual'
                ? 'Aponte para o produto e toque o botão de captura'
                : scanMode === 'text'
                ? 'Aponte para texto e toque para reconhecer'
                : 'Modo automático: detecta códigos e produtos'
              }
            </Text>
          </View>

          {/* Loading/Processing */}
          {(isLoading || aiProcessing) && (
            <View style={styles.loadingContainer}>
              <ActivityIndicator size="large" color="white" />
              <Text style={styles.loadingText}>
                {aiProcessing ? 'Processando com IA...' : 'Carregando...'}
              </Text>
              {aiProcessing && (
                <Text style={styles.loadingSubtext}>
                  Análise avançada em progresso
                </Text>
              )}
            </View>
          )}

          {/* Footer */}
          <View style={styles.footer}>
            <TouchableOpacity
              style={styles.footerButton}
              onPress={pickImageFromGallery}
            >
              <Ionicons name="images" size={28} color="white" />
              <Text style={styles.footerButtonText}>Galeria</Text>
            </TouchableOpacity>
            
            {(scanMode === 'visual' || scanMode === 'text') && (
              <TouchableOpacity
                style={[styles.footerButton, styles.captureButton]}
                onPress={capturePhoto}
                disabled={isLoading}
              >
                <View style={[styles.captureButtonInner, { backgroundColor: modeInfo.color }]}>
                  <Ionicons name="camera" size={32} color="white" />
                </View>
              </TouchableOpacity>
            )}
            
            <TouchableOpacity
              style={styles.footerButton}
              onPress={() => navigation.navigate('Cart')}
            >
              <Ionicons name="bag" size={28} color="white" />
              <Text style={styles.footerButtonText}>Carrinho</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Camera>

      {/* Modal de Histórico */}
      <Modal
        visible={showHistory}
        animationType="slide"
        presentationStyle="pageSheet"
      >
        <View style={styles.historyModal}>
          <View style={styles.historyHeader}>
            <Text style={styles.historyTitle}>Histórico de Scans</Text>
            <TouchableOpacity onPress={() => setShowHistory(false)}>
              <Ionicons name="close" size={24} color="#007AFF" />
            </TouchableOpacity>
          </View>
          
          <ScrollView style={styles.historyList}>
            {scanHistory.map((item, index) => (
              <View key={index} style={styles.historyItem}>
                <View style={styles.historyItemInfo}>
                  <Text style={styles.historyItemName}>{item.name}</Text>
                  <Text style={styles.historyItemDetails}>
                    {item.brand} • {item.confidence}% • {item.scanMode}
                  </Text>
                  <Text style={styles.historyItemPrice}>
                    R$ {item.price.toFixed(2)} • ESG: {item.esgScore}/10
                  </Text>
                  <Text style={styles.historyItemTime}>
                    {item.timestamp.toLocaleString()}
                  </Text>
                </View>
                <TouchableOpacity
                  style={styles.historyItemButton}
                  onPress={() => {
                    setShowHistory(false);
                    navigation.navigate('Cart', { newProduct: item });
                  }}
                >
                  <Ionicons name="add-circle" size={24} color="#007AFF" />
                </TouchableOpacity>
              </View>
            ))}
            
            {scanHistory.length === 0 && (
              <View style={styles.emptyHistory}>
                <Ionicons name="scan" size={48} color="#8E8E93" />
                <Text style={styles.emptyHistoryText}>Nenhum scan realizado ainda</Text>
              </View>
            )}
          </ScrollView>
        </View>
      </Modal>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: 'black',
  },
  camera: {
    flex: 1,
  },
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.2)',
  },
  centerContainer: {
    flex: 1,
    backgroundColor: 'black',
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 40,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingTop: 50,
    paddingHorizontal: 20,
    paddingBottom: 10,
  },
  headerButton: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: 'rgba(0,0,0,0.6)',
    justifyContent: 'center',
    alignItems: 'center',
    position: 'relative',
  },
  headerCenter: {
    alignItems: 'center',
  },
  headerTitle: {
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold',
  },
  headerSubtitle: {
    fontSize: 12,
    marginTop: 2,
    fontWeight: '500',
  },
  headerStats: {
    color: 'rgba(255,255,255,0.7)',
    fontSize: 10,
    marginTop: 2,
  },
  badge: {
    position: 'absolute',
    top: -2,
    right: -2,
    backgroundColor: '#FF3B30',
    borderRadius: 8,
    minWidth: 16,
    height: 16,
    justifyContent: 'center',
    alignItems: 'center',
  },
  badgeText: {
    color: 'white',
    fontSize: 10,
    fontWeight: 'bold',
  },
  controls: {
    flexDirection: 'row',
    justifyContent: 'center',
    paddingHorizontal: 20,
    paddingBottom: 20,
    gap: 20,
  },
  controlButton: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: 'rgba(0,0,0,0.6)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  activeControl: {
    backgroundColor: 'rgba(0,255,0,0.3)',
  },
  scannerArea: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  scannerFrame: {
    width: 300,
    height: 240,
    position: 'relative',
    borderWidth: 2,
    borderRadius: 12,
  },
  corner: {
    position: 'absolute',
    width: 30,
    height: 30,
    borderWidth: 4,
  },
  topLeft: {
    top: -2,
    left: -2,
    borderRightWidth: 0,
    borderBottomWidth: 0,
    borderTopLeftRadius: 12,
  },
  topRight: {
    top: -2,
    right: -2,
    borderLeftWidth: 0,
    borderBottomWidth: 0,
    borderTopRightRadius: 12,
  },
  bottomLeft: {
    bottom: -2,
    left: -2,
    borderRightWidth: 0,
    borderTopWidth: 0,
    borderBottomLeftRadius: 12,
  },
  bottomRight: {
    bottom: -2,
    right: -2,
    borderLeftWidth: 0,
    borderTopWidth: 0,
    borderBottomRightRadius: 12,
  },
  scanLine: {
    position: 'absolute',
    left: 0,
    right: 0,
    height: 3,
    opacity: 0.9,
    shadowColor: '#00FF00',
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.8,
    shadowRadius: 4,
  },
  confidenceIndicator: {
    position: 'absolute',
    top: -50,
    left: 0,
    right: 0,
    alignItems: 'center',
  },
  confidenceText: {
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 6,
    textShadowColor: 'rgba(0,0,0,0.5)',
    textShadowOffset: { width: 1, height: 1 },
    textShadowRadius: 2,
  },
  confidenceBar: {
    width: 120,
    height: 6,
    backgroundColor: 'rgba(255,255,255,0.3)',
    borderRadius: 3,
    overflow: 'hidden',
  },
  confidenceFill: {
    height: '100%',
    borderRadius: 3,
  },
  instructionText: {
    color: 'white',
    fontSize: 16,
    textAlign: 'center',
    marginTop: 40,
    paddingHorizontal: 40,
    lineHeight: 24,
    textShadowColor: 'rgba(0,0,0,0.5)',
    textShadowOffset: { width: 1, height: 1 },
    textShadowRadius: 2,
  },
  loadingContainer: {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: [{ translateX: -100 }, { translateY: -60 }],
    alignItems: 'center',
    backgroundColor: 'rgba(0,0,0,0.8)',
    padding: 24,
    borderRadius: 16,
    minWidth: 200,
  },
  loadingText: {
    color: 'white',
    fontSize: 16,
    marginTop: 12,
    textAlign: 'center',
    fontWeight: '500',
  },
  loadingSubtext: {
    color: 'rgba(255,255,255,0.7)',
    fontSize: 12,
    marginTop: 4,
    textAlign: 'center',
  },
  footer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
    paddingBottom: 50,
    paddingHorizontal: 40,
  },
  footerButton: {
    alignItems: 'center',
    padding: 8,
  },
  footerButtonText: {
    color: 'white',
    fontSize: 12,
    marginTop: 6,
    fontWeight: '500',
  },
  captureButton: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: 'rgba(255,255,255,0.2)',
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 4,
    borderColor: 'white',
  },
  captureButtonInner: {
    width: 60,
    height: 60,
    borderRadius: 30,
    justifyContent: 'center',
    alignItems: 'center',
  },
  errorText: {
    color: '#8E8E93',
    fontSize: 20,
    textAlign: 'center',
    marginTop: 16,
    fontWeight: '500',
  },
  errorSubtext: {
    color: '#8E8E93',
    fontSize: 14,
    textAlign: 'center',
    marginTop: 8,
    lineHeight: 20,
  },
  retryButton: {
    backgroundColor: '#007AFF',
    paddingHorizontal: 32,
    paddingVertical: 16,
    borderRadius: 12,
    marginTop: 24,
  },
  retryButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },
  loadingText: {
    color: 'white',
    fontSize: 16,
    marginTop: 16,
  },
  historyModal: {
    flex: 1,
    backgroundColor: '#F2F2F7',
  },
  historyHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingTop: 60,
    paddingBottom: 20,
    backgroundColor: 'white',
    borderBottomWidth: 1,
    borderBottomColor: '#E5E5E7',
  },
  historyTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: '#000000',
  },
  historyList: {
    flex: 1,
  },
  historyItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'white',
    paddingHorizontal: 20,
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#F2F2F7',
  },
  historyItemInfo: {
    flex: 1,
  },
  historyItemName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#000000',
  },
  historyItemDetails: {
    fontSize: 14,
    color: '#8E8E93',
    marginTop: 2,
  },
  historyItemPrice: {
    fontSize: 14,
    color: '#007AFF',
    marginTop: 2,
    fontWeight: '500',
  },
  historyItemTime: {
    fontSize: 12,
    color: '#8E8E93',
    marginTop: 4,
  },
  historyItemButton: {
    padding: 8,
  },
  emptyHistory: {
    alignItems: 'center',
    paddingVertical: 60,
  },
  emptyHistoryText: {
    fontSize: 16,
    color: '#8E8E93',
    marginTop: 16,
  },
});

export default AdvancedScannerScreen;
