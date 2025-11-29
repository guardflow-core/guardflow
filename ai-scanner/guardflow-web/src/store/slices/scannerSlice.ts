import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface ScannedProduct {
  id: string;
  barcode: string;
  name: string;
  description?: string;
  price: number;
  category: string;
  brand?: string;
  image_url?: string;
  weight?: number;
  volume?: number;
  ncm_code?: string;
  esg_score: number;
  is_organic: boolean;
  is_vegan: boolean;
  confidence: number;
  scanned_at: string;
}

interface ScannerState {
  isScanning: boolean;
  scannedProducts: ScannedProduct[];
  currentProduct: ScannedProduct | null;
  scanHistory: ScannedProduct[];
  totalScanned: number;
  successRate: number;
  lastScanTime: string | null;
  error: string | null;
}

const initialState: ScannerState = {
  isScanning: false,
  scannedProducts: [],
  currentProduct: null,
  scanHistory: [],
  totalScanned: 0,
  successRate: 0,
  lastScanTime: null,
  error: null,
};

const scannerSlice = createSlice({
  name: 'scanner',
  initialState,
  reducers: {
    startScanning: (state) => {
      state.isScanning = true;
      state.error = null;
    },

    stopScanning: (state) => {
      state.isScanning = false;
    },

    scanSuccess: (state, action: PayloadAction<ScannedProduct>) => {
      const product = action.payload;
      
      state.scannedProducts.push(product);
      state.scanHistory.push(product);
      state.currentProduct = product;
      
      state.totalScanned += 1;
      state.lastScanTime = new Date().toISOString();
      
      const successfulScans = state.scanHistory.filter(p => p.confidence > 0.7).length;
      state.successRate = state.scanHistory.length > 0 
        ? successfulScans / state.scanHistory.length 
        : 0;
    },

    scanError: (state, action: PayloadAction<string>) => {
      state.error = action.payload;
      state.isScanning = false;
    },

    clearError: (state) => {
      state.error = null;
    },

    clearCurrentProduct: (state) => {
      state.currentProduct = null;
    },

    clearScannedProducts: (state) => {
      state.scannedProducts = [];
    },

    clearScanHistory: (state) => {
      state.scanHistory = [];
      state.totalScanned = 0;
      state.successRate = 0;
    },

    addToCart: (state, action: PayloadAction<{ productId: string; quantity: number }>) => {
      state.currentProduct = null;
    },
  },
});

export const { 
  startScanning, 
  stopScanning, 
  scanSuccess, 
  scanError, 
  clearError, 
  clearCurrentProduct, 
  clearScannedProducts, 
  clearScanHistory,
  addToCart
} = scannerSlice.actions;

export default scannerSlice.reducer;