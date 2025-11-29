import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { AppDispatch, RootState } from '../store';
import { scanSuccess } from '../store/slices/scannerSlice';
import { addItemToCart, cartLoading, cartError, cartLoaded } from '../store/slices/cartSlice';
import { fetchESGScoreStart, fetchESGScoreSuccess, fetchESGScoreFailure } from '../store/slices/esgSlice';

interface ScannerCartIntegrationProps {
  onProductAdded?: (product: any) => void;
  onError?: (error: string) => void;
}

const ScannerCartIntegration: React.FC<ScannerCartIntegrationProps> = ({
  onProductAdded,
  onError,
}) => {
  const dispatch: AppDispatch = useDispatch();
  const { lastScannedProduct } = useSelector((state: RootState) => state.scanner);
  const { loading: cartLoading } = useSelector((state: RootState) => state.cart);
  const { loading: esgLoading } = useSelector((state: RootState) => state.esg);

  // Simulate product data fetching and validation
  const fetchProductData = async (barcode: string) => {
    try {
      // Simulate API call to fetch product data
      const response = await new Promise((resolve, reject) => {
        setTimeout(() => {
          // Simulate different products based on barcode
          const mockProducts = {
            '1234567890123': {
              id: 'prod_1',
              name: 'Produto Orgânico A',
              price: 15.99,
              category: 'Alimentos',
              ncm_code: '12345678',
              imageUrl: 'https://example.com/product1.jpg',
            },
            '2345678901234': {
              id: 'prod_2',
              name: 'Produto Sustentável B',
              price: 25.50,
              category: 'Limpeza',
              ncm_code: '23456789',
              imageUrl: 'https://example.com/product2.jpg',
            },
            '3456789012345': {
              id: 'prod_3',
              name: 'Produto Eco-friendly C',
              price: 8.75,
              category: 'Higiene',
              ncm_code: '34567890',
              imageUrl: 'https://example.com/product3.jpg',
            },
          };

          const product = mockProducts[barcode as keyof typeof mockProducts];
          if (product) {
            resolve(product);
          } else {
            reject(new Error('Produto não encontrado'));
          }
        }, 1000);
      });

      return response;
    } catch (error) {
      throw new Error('Erro ao buscar dados do produto');
    }
  };

  // Simulate ESG score calculation
  const calculateESGScore = async (product: any) => {
    try {
      // Simulate ESG calculation based on NCM code and category
      const baseScore = Math.random() * 30 + 60; // Score between 60-90
      const categoryMultiplier = {
        'Alimentos': 1.1,
        'Limpeza': 0.9,
        'Higiene': 1.0,
      };

      const finalScore = baseScore * (categoryMultiplier[product.category as keyof typeof categoryMultiplier] || 1.0);
      
      return {
        productId: product.id,
        score: Math.min(finalScore, 100),
        category: 'Sustentabilidade',
        details: {
          environmental: Math.random() * 20 + 70,
          social: Math.random() * 20 + 70,
          governance: Math.random() * 20 + 70,
        },
      };
    } catch (error) {
      throw new Error('Erro ao calcular score ESG');
    }
  };

  // Handle scanned product integration
  useEffect(() => {
    if (lastScannedProduct) {
      handleScannedProduct(lastScannedProduct);
    }
  }, [lastScannedProduct]);

  const handleScannedProduct = async (scannedProduct: any) => {
    try {
      dispatch(cartLoading());
      
      // Fetch product data
      const productData = await fetchProductData(scannedProduct.barcode);
      
      // Add to cart
      dispatch(addItemToCart({
        productId: productData.id,
        name: productData.name,
        price: productData.price,
        quantity: 1,
        imageUrl: productData.imageUrl,
      }));

      // Calculate ESG score
      dispatch(fetchESGScoreStart());
      const esgScore = await calculateESGScore(productData);
      dispatch(fetchESGScoreSuccess(esgScore));

      dispatch(cartLoaded());
      
      // Notify parent component
      if (onProductAdded) {
        onProductAdded({
          ...productData,
          scannedProduct,
          esgScore,
        });
      }
    } catch (error: any) {
      dispatch(cartError(error.message));
      dispatch(fetchESGScoreFailure(error.message));
      
      if (onError) {
        onError(error.message);
      }
    }
  };

  // Validate product before adding to cart
  const validateProduct = (product: any) => {
    const validations = [
      { check: () => product.name && product.name.length > 0, message: 'Nome do produto inválido' },
      { check: () => product.price && product.price > 0, message: 'Preço inválido' },
      { check: () => product.category && product.category.length > 0, message: 'Categoria inválida' },
    ];

    for (const validation of validations) {
      if (!validation.check()) {
        throw new Error(validation.message);
      }
    }

    return true;
  };

  // Check for duplicate products
  const checkForDuplicates = (productId: string, cartItems: any[]) => {
    const existingItem = cartItems.find(item => item.productId === productId);
    if (existingItem) {
      return {
        isDuplicate: true,
        existingItem,
      };
    }
    return { isDuplicate: false };
  };

  // Auto-sync with backend (simulated)
  const syncWithBackend = async (cartItems: any[]) => {
    try {
      // Simulate backend sync
      const response = await new Promise((resolve) => {
        setTimeout(() => {
          resolve({ success: true, timestamp: new Date().toISOString() });
        }, 500);
      });
      
      return response;
    } catch (error) {
      throw new Error('Erro na sincronização com o backend');
    }
  };

  // Handle offline mode
  const handleOfflineMode = () => {
    // Store actions in local queue for later sync
    const offlineActions = JSON.parse(localStorage.getItem('offlineActions') || '[]');
    offlineActions.push({
      type: 'ADD_TO_CART',
      timestamp: new Date().toISOString(),
      data: lastScannedProduct,
    });
    localStorage.setItem('offlineActions', JSON.stringify(offlineActions));
  };

  // Process offline actions when back online
  const processOfflineActions = async () => {
    try {
      const offlineActions = JSON.parse(localStorage.getItem('offlineActions') || '[]');
      
      for (const action of offlineActions) {
        if (action.type === 'ADD_TO_CART') {
          await handleScannedProduct(action.data);
        }
      }
      
      // Clear processed actions
      localStorage.removeItem('offlineActions');
    } catch (error) {
      console.error('Erro ao processar ações offline:', error);
    }
  };

  return null; // This is a service component, no UI
};

export default ScannerCartIntegration;
