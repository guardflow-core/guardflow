import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface PaymentMethod {
  id: string;
  type: 'pix' | 'credit_card' | 'debit_card' | 'cash';
  name: string;
  is_active: boolean;
  is_default: boolean;
}

interface PaymentTransaction {
  id: string;
  amount: number;
  currency: string;
  method: string;
  status: 'pending' | 'completed' | 'failed' | 'cancelled';
  description?: string;
  created_at: string;
  completed_at?: string;
  failure_reason?: string;
}

interface PaymentState {
  methods: PaymentMethod[];
  currentTransaction: PaymentTransaction | null;
  transactionHistory: PaymentTransaction[];
  isProcessing: boolean;
  error: string | null;
  totalSpent: number;
  totalTransactions: number;
}

const initialState: PaymentState = {
  methods: [],
  currentTransaction: null,
  transactionHistory: [],
  isProcessing: false,
  error: null,
  totalSpent: 0,
  totalTransactions: 0,
};

const paymentSlice = createSlice({
  name: 'payment',
  initialState,
  reducers: {
    addPaymentMethod: (state, action: PayloadAction<PaymentMethod>) => {
      const method = action.payload;
      
      if (method.is_default) {
        state.methods.forEach(m => m.is_default = false);
      }
      
      state.methods.push(method);
    },

    removePaymentMethod: (state, action: PayloadAction<string>) => {
      state.methods = state.methods.filter(method => method.id !== action.payload);
    },

    setDefaultPaymentMethod: (state, action: PayloadAction<string>) => {
      state.methods.forEach(method => {
        method.is_default = method.id === action.payload;
      });
    },

    startPayment: (state, action: PayloadAction<{ amount: number; method: string; description?: string }>) => {
      const { amount, method, description } = action.payload;
      
      state.currentTransaction = {
        id: `txn_${Date.now()}`,
        amount,
        currency: 'BRL',
        method,
        status: 'pending',
        description,
        created_at: new Date().toISOString(),
      };
      
      state.isProcessing = true;
      state.error = null;
    },

    paymentSuccess: (state, action: PayloadAction<PaymentTransaction>) => {
      const transaction = action.payload;
      
      if (state.currentTransaction) {
        state.currentTransaction.status = 'completed';
        state.currentTransaction.completed_at = new Date().toISOString();
        
        state.transactionHistory.unshift(transaction);
        
        state.totalSpent += transaction.amount;
        state.totalTransactions += 1;
      }
      
      state.isProcessing = false;
      state.error = null;
    },

    paymentFailure: (state, action: PayloadAction<string>) => {
      if (state.currentTransaction) {
        state.currentTransaction.status = 'failed';
        state.currentTransaction.failure_reason = action.payload;
      }
      
      state.isProcessing = false;
      state.error = action.payload;
    },

    cancelPayment: (state) => {
      if (state.currentTransaction) {
        state.currentTransaction.status = 'cancelled';
      }
      
      state.isProcessing = false;
      state.currentTransaction = null;
    },

    clearError: (state) => {
      state.error = null;
    },

    clearCurrentTransaction: (state) => {
      state.currentTransaction = null;
    },

    resetPayment: (state) => {
      state.methods = [];
      state.currentTransaction = null;
      state.transactionHistory = [];
      state.isProcessing = false;
      state.error = null;
      state.totalSpent = 0;
      state.totalTransactions = 0;
    },
  },
});

export const { 
  addPaymentMethod, 
  removePaymentMethod, 
  setDefaultPaymentMethod,
  startPayment, 
  paymentSuccess, 
  paymentFailure, 
  cancelPayment,
  clearError,
  clearCurrentTransaction,
  resetPayment
} = paymentSlice.actions;

export default paymentSlice.reducer;