import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface CartItem {
  id: string;
  product_id: string;
  product_name: string;
  product_barcode?: string;
  product_image?: string;
  quantity: number;
  unit_price: number;
  total_price: number;
  weight?: number;
  volume?: number;
  esg_score: number;
  is_organic: boolean;
  is_vegan: boolean;
  added_at: string;
}

interface CartState {
  items: CartItem[];
  totalItems: number;
  totalAmount: number;
  totalWeight: number;
  totalVolume: number;
  averageESGScore: number;
  organicItems: number;
  veganItems: number;
  isOpen: boolean;
}

const initialState: CartState = {
  items: [],
  totalItems: 0,
  totalAmount: 0,
  totalWeight: 0,
  totalVolume: 0,
  averageESGScore: 0,
  organicItems: 0,
  veganItems: 0,
  isOpen: false,
};

const cartSlice = createSlice({
  name: 'cart',
  initialState,
  reducers: {
    addItem: (state, action: PayloadAction<Omit<CartItem, 'id' | 'added_at'>>) => {
      const newItem: CartItem = {
        ...action.payload,
        id: `${action.payload.product_id}_${Date.now()}`,
        added_at: new Date().toISOString(),
      };

      const existingItem = state.items.find(item => item.product_id === newItem.product_id);
      
      if (existingItem) {
        existingItem.quantity += newItem.quantity;
        existingItem.total_price = existingItem.quantity * existingItem.unit_price;
      } else {
        state.items.push(newItem);
      }

      // Recalcular totais
      const totals = calculateTotals(state.items);
      Object.assign(state, totals);
    },

    removeItem: (state, action: PayloadAction<string>) => {
      state.items = state.items.filter(item => item.id !== action.payload);
      const totals = calculateTotals(state.items);
      Object.assign(state, totals);
    },

    updateQuantity: (state, action: PayloadAction<{ id: string; quantity: number }>) => {
      const { id, quantity } = action.payload;
      const item = state.items.find(item => item.id === id);
      
      if (item) {
        if (quantity <= 0) {
          state.items = state.items.filter(item => item.id !== id);
        } else {
          item.quantity = quantity;
          item.total_price = item.quantity * item.unit_price;
        }
      }

      const totals = calculateTotals(state.items);
      Object.assign(state, totals);
    },

    clearCart: (state) => {
      state.items = [];
      state.totalItems = 0;
      state.totalAmount = 0;
      state.totalWeight = 0;
      state.totalVolume = 0;
      state.averageESGScore = 0;
      state.organicItems = 0;
      state.veganItems = 0;
    },

    toggleCart: (state) => {
      state.isOpen = !state.isOpen;
    },

    openCart: (state) => {
      state.isOpen = true;
    },

    closeCart: (state) => {
      state.isOpen = false;
    },
  },
});

// Função para calcular totais
const calculateTotals = (items: CartItem[]) => {
  const totalItems = items.reduce((sum, item) => sum + item.quantity, 0);
  const totalAmount = items.reduce((sum, item) => sum + item.total_price, 0);
  const totalWeight = items.reduce((sum, item) => sum + (item.weight || 0) * item.quantity, 0);
  const totalVolume = items.reduce((sum, item) => sum + (item.volume || 0) * item.quantity, 0);
  const averageESGScore = items.length > 0 
    ? items.reduce((sum, item) => sum + item.esg_score, 0) / items.length 
    : 0;
  const organicItems = items.filter(item => item.is_organic).length;
  const veganItems = items.filter(item => item.is_vegan).length;

  return {
    totalItems,
    totalAmount,
    totalWeight,
    totalVolume,
    averageESGScore,
    organicItems,
    veganItems,
  };
};

export const { 
  addItem, 
  removeItem, 
  updateQuantity, 
  clearCart, 
  toggleCart, 
  openCart, 
  closeCart 
} = cartSlice.actions;

export default cartSlice.reducer;