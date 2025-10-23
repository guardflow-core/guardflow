import { createSlice, PayloadAction } from '@reduxjs/toolkit';

type PaymentStatus = 'idle' | 'processing' | 'success' | 'failed';

interface PaymentState {
  status: PaymentStatus;
  transactionId: string | null;
  amount: number | null;
  method: string | null;
  error: string | null;
}

const initialState: PaymentState = {
  status: 'idle',
  transactionId: null,
  amount: null,
  method: null,
  error: null,
};

const paymentSlice = createSlice({
  name: 'payment',
  initialState,
  reducers: {
    initiatePayment: (state, action: PayloadAction<{ amount: number; method: string }>) => {
      state.status = 'processing';
      state.amount = action.payload.amount;
      state.method = action.payload.method;
      state.error = null;
      state.transactionId = null;
    },
    paymentSuccess: (state, action: PayloadAction<string>) => {
      state.status = 'success';
      state.transactionId = action.payload;
    },
    paymentFailed: (state, action: PayloadAction<string>) => {
      state.status = 'failed';
      state.error = action.payload;
      state.transactionId = null;
    },
    resetPayment: (state) => {
      state.status = 'idle';
      state.transactionId = null;
      state.amount = null;
      state.method = null;
      state.error = null;
    },
  },
});

export const { initiatePayment, paymentSuccess, paymentFailed, resetPayment } = paymentSlice.actions;
export default paymentSlice.reducer;