/**
 * Scanner Screen - Core do GuardFlow
 * Tela principal de escaneamento de produtos
 */

import React, {useState, useEffect, useRef} from 'react';
import {
  View,
  StyleSheet,
  Text,
  TouchableOpacity,
  Alert,
  Animated,
  Dimensions,
} from 'react-native';
import {Camera, useCameraDevices} from 'react-native-vision-camera';
import {useSelector, useDispatch} from 'react-redux';
import Icon from 'react-native-vector-icons/MaterialIcons';
import {runOnJS} from 'react-native-reanimated';

// Components
import ScannerOverlay from '../../components/scanner/ScannerOverlay';
import ProductDetectedModal from '../../components/scanner/ProductDetectedModal';
import CartSummary from '../../components/shopping/CartSummary';

// Services
import {detectProduct} from '../../services/camera/visionService';
import {addToCart} from '../../store/slices/cartSlice';
import {earnGSTTokens} from '../../store/slices/tokensSlice';

// Styles
import {colors, spacing, typography, shadows} from '../../styles';

const {width, height} = Dimensions.get('window');

const ScannerScreen = ({navigation}) => {
  const dispatch = useDispatch();
  const devices = useCameraDevices();
  const device = devices.back;
  
  // State
  const [hasPermission, setHasPermission] = useState(false);
  const [isActive, setIsActive] = useState(true);
  const [detectedProduct, setDetectedProduct] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [showProductModal, setShowProductModal] = useState(false);
  
  // Redux state
  const {cartItems, cartTotal} = useSelector(state => ({
    cartItems: state.cart.items,
    cartTotal: state.cart.total,
  }));
  
  // Animation
  const scanLineAnim = useRef(new Animated.Value(0)).current;
  const pulseAnim = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    checkCameraPermission();
    startScanAnimation();
  }, []);

  const checkCameraPermission = async () => {
    try {
      const permission = await Camera.requestCameraPermission();
      setHasPermission(permission === 'authorized');
    } catch (error) {
      console.error('Camera permission error:', error);
      Alert.alert('Erro', 'Não foi possível acessar a câmera');
    }
  };

  const startScanAnimation = () => {
    // Animação da linha de scan
    Animated.loop(
      Animated.sequence([
        Animated.timing(scanLineAnim, {
          toValue: 1,
          duration: 2000,
          useNativeDriver: true,
        }),
        Animated.timing(scanLineAnim, {
          toValue: 0,
          duration: 0,
          useNativeDriver: true,
        }),
      ])
    ).start();

    // Animação de pulso
    Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, {
          toValue: 1.1,
          duration: 1000,
          useNativeDriver: true,
        }),
        Animated.timing(pulseAnim, {
          toValue: 1,
          duration: 1000,
          useNativeDriver: true,
        }),
      ])
    ).start();
  };

  const frameProcessor = (frame) => {
    'worklet';
    
    if (isProcessing) return;
    
    // Processar frame com IA para detectar produtos
    const products = detectProduct(frame);
    
    if (products && products.length > 0) {
      runOnJS(handleProductDetected)(products[0]);
    }
  };

  const handleProductDetected = async (product) => {
    if (isProcessing) return;
    
    setIsProcessing(true);
    setDetectedProduct(product);
    setShowProductModal(true);
    
    // Feedback háptico
    // HapticFeedback.trigger('impactMedium');
    
    // Som de sucesso
    // SoundPlayer.playSoundFile('scan_success', 'wav');
    
    setTimeout(() => {
      setIsProcessing(false);
    }, 1000);
  };

  const handleAddToCart = () => {
    if (!detectedProduct) return;

    // Adicionar ao carrinho
    dispatch(addToCart({
      id: detectedProduct.id,
      barcode: detectedProduct.barcode,
      name: detectedProduct.name,
      brand: detectedProduct.brand,
      price: detectedProduct.price,
      image: detectedProduct.image,
      esgScore: detectedProduct.esgScore,
      quantity: 1,
    }));

    // Ganhar tokens GST baseado no ESG score
    const gstReward = Math.floor(detectedProduct.esgScore / 10);
    if (gstReward > 0) {
      dispatch(earnGSTTokens({
        amount: gstReward,
        reason: 'sustainable_purchase',
        productId: detectedProduct.id,
      }));
    }

    setShowProductModal(false);
    setDetectedProduct(null);
    
    // Toast de sucesso
    // Toast.show({
    //   type: 'success',
    //   text1: 'Produto adicionado!',
    //   text2: `+${gstReward} GST tokens ganhos`,
    // });
  };

  const handleSkipProduct = () => {
    setShowProductModal(false);
    setDetectedProduct(null);
  };

  const toggleFlashlight = () => {
    // Implementar toggle da lanterna
  };

  const openCart = () => {
    navigation.navigate('Cart');
  };

  if (!hasPermission) {
    return (
      <View style={styles.permissionContainer}>
        <Icon name="camera-alt" size={64} color={colors.gray.medium} />
        <Text style={styles.permissionText}>
          Precisamos de acesso à câmera para escanear produtos
        </Text>
        <TouchableOpacity style={styles.permissionButton} onPress={checkCameraPermission}>
          <Text style={styles.permissionButtonText}>Permitir Câmera</Text>
        </TouchableOpacity>
      </View>
    );
  }

  if (!device) {
    return (
      <View style={styles.errorContainer}>
        <Text style={styles.errorText}>Câmera não disponível</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Camera */}
      <Camera
        style={styles.camera}
        device={device}
        isActive={isActive}
        frameProcessor={frameProcessor}
        frameProcessorFps={5}
      />

      {/* Scanner Overlay */}
      <ScannerOverlay
        scanLineAnim={scanLineAnim}
        pulseAnim={pulseAnim}
        isProcessing={isProcessing}
      />

      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity style={styles.headerButton} onPress={() => navigation.goBack()}>
          <Icon name="arrow-back" size={24} color={colors.white} />
        </TouchableOpacity>
        
        <Text style={styles.headerTitle}>Escaneie Produtos</Text>
        
        <TouchableOpacity style={styles.headerButton} onPress={toggleFlashlight}>
          <Icon name="flash-on" size={24} color={colors.white} />
        </TouchableOpacity>
      </View>

      {/* Instructions */}
      <View style={styles.instructions}>
        <Text style={styles.instructionText}>
          Aponte a câmera para o código de barras do produto
        </Text>
        <Text style={styles.instructionSubtext}>
          A IA identificará automaticamente o produto
        </Text>
      </View>

      {/* Cart Summary */}
      {cartItems.length > 0 && (
        <View style={styles.cartSummaryContainer}>
          <CartSummary
            itemCount={cartItems.length}
            total={cartTotal}
            onPress={openCart}
          />
        </View>
      )}

      {/* Product Detected Modal */}
      <ProductDetectedModal
        visible={showProductModal}
        product={detectedProduct}
        onAddToCart={handleAddToCart}
        onSkip={handleSkipProduct}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.black,
  },
  camera: {
    flex: 1,
  },
  permissionContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: colors.background,
    paddingHorizontal: spacing.xl,
  },
  permissionText: {
    fontSize: typography.sizes.lg,
    color: colors.text.primary,
    textAlign: 'center',
    marginVertical: spacing.lg,
    fontFamily: typography.fonts.medium,
  },
  permissionButton: {
    backgroundColor: colors.primary.green,
    paddingHorizontal: spacing.xl,
    paddingVertical: spacing.md,
    borderRadius: 8,
    marginTop: spacing.md,
  },
  permissionButtonText: {
    color: colors.white,
    fontSize: typography.sizes.base,
    fontFamily: typography.fonts.semiBold,
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: colors.background,
  },
  errorText: {
    fontSize: typography.sizes.lg,
    color: colors.secondary.error,
    fontFamily: typography.fonts.medium,
  },
  header: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingTop: 50,
    paddingHorizontal: spacing.md,
    paddingBottom: spacing.md,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
  },
  headerButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  headerTitle: {
    color: colors.white,
    fontSize: typography.sizes.lg,
    fontFamily: typography.fonts.semiBold,
  },
  instructions: {
    position: 'absolute',
    bottom: 120,
    left: spacing.md,
    right: spacing.md,
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    padding: spacing.md,
    borderRadius: 8,
  },
  instructionText: {
    color: colors.white,
    fontSize: typography.sizes.base,
    fontFamily: typography.fonts.medium,
    textAlign: 'center',
    marginBottom: spacing.xs,
  },
  instructionSubtext: {
    color: colors.white,
    fontSize: typography.sizes.sm,
    fontFamily: typography.fonts.regular,
    textAlign: 'center',
    opacity: 0.8,
  },
  cartSummaryContainer: {
    position: 'absolute',
    bottom: spacing.md,
    left: spacing.md,
    right: spacing.md,
  },
});

export default ScannerScreen;



