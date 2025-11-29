import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface ScannedProduct {
  id: string;
  name: string;
  barcode: string;
  imageUrl?: string;
  confidence: number;
}

interface ScannerState {
  lastScannedProduct: ScannedProduct | null;
  scanHistory: ScannedProduct[];
  isScanning: boolean;
  error: string | null;
}

const initialState: ScannerState = {
  lastScannedProduct: null,
  scanHistory: [],
  isScanning: false,
  error: null,
};

const scannerSlice = createSlice({
  name: 'scanner',
  initialState,
  reducers: {
    startScan: (state) => {
      state.isScanning = true;
      state.error = null;
    },
    scanSuccess: (state, action: PayloadAction<ScannedProduct>) => {
      state.isScanning = false;
      state.lastScannedProduct = action.payload;
      state.scanHistory.unshift(action.payload); // Add to the beginning
      if (state.scanHistory.length > 10) { // Keep history limited
        state.scanHistory.pop();
      }
    },
    scanFailure: (state, action: PayloadAction<string>) => {
      state.isScanning = false;
      state.error = action.payload;
    },
    stopScan: (state) => {
      state.isScanning = false;
    },
    clearScanHistory: (state) => {
      state.scanHistory = [];
    },
  },
});

export const { startScan, scanSuccess, scanFailure, stopScan, clearScanHistory } = scannerSlice.actions;
export default scannerSlice.reducer;