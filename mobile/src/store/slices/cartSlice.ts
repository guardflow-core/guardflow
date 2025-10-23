import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface CartItem {
  productId: string;
  name: string;
  price: number;
  quantity: number;
  imageUrl?: string;
}

interface CartState {
  items: CartItem[];
  totalAmount: number;
  loading: boolean;
  error: string | null;
}

const initialState: CartState = {
  items: [],
  totalAmount: 0,
  loading: false,
  error: null,
};

const cartSlice = createSlice({
  name: 'cart',
  initialState,
  reducers: {
    addItemToCart: (state, action: PayloadAction<CartItem>) => {
      const existingItem = state.items.find(item => item.productId === action.payload.productId);
      if (existingItem) {
        existingItem.quantity += action.payload.quantity;
      } else {
        state.items.push(action.payload);
      }
      state.totalAmount = state.items.reduce((sum, item) => sum + item.price * item.quantity, 0);
    },
    removeItemFromCart: (state, action: PayloadAction<string>) => {
      state.items = state.items.filter(item => item.productId !== action.payload);
      state.totalAmount = state.items.reduce((sum, item) => sum + item.price * item.quantity, 0);
    },
    updateItemQuantity: (state, action: PayloadAction<{ productId: string; quantity: number }>) => {
      const item = state.items.find(item => item.productId === action.payload.productId);
      if (item) {
        item.quantity = action.payload.quantity;
      }
      state.totalAmount = state.items.reduce((sum, item) => sum + item.price * item.quantity, 0);
    },
    clearCart: (state) => {
      state.items = [];
      state.totalAmount = 0;
    },
    cartLoading: (state) => {
      state.loading = true;
      state.error = null;
    },
    cartError: (state, action: PayloadAction<string>) => {
      state.loading = false;
      state.error = action.payload;
    },
    cartLoaded: (state) => {
      state.loading = false;
    }
  },
});

export const { addItemToCart, removeItemFromCart, updateItemQuantity, clearCart, cartLoading, cartError, cartLoaded } = cartSlice.actions;
export default cartSlice.reducer;