import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface Product {
  id: string;
  name: string;
  description?: string;
  price: number;
  category: string;
  barcode?: string;
  ncm_code?: string;
  image_url?: string;
  is_active: boolean;
  store_id?: string;
  esg_score: number;
  is_organic: boolean;
  is_vegan: boolean;
}

interface ProductState {
  products: Product[];
  selectedProduct: Product | null;
  loading: boolean;
  error: string | null;
  filters: {
    category: string;
    minPrice: number;
    maxPrice: number;
    search: string;
  };
}

const initialState: ProductState = {
  products: [],
  selectedProduct: null,
  loading: false,
  error: null,
  filters: {
    category: '',
    minPrice: 0,
    maxPrice: 1000,
    search: '',
  },
};

const productSlice = createSlice({
  name: 'product',
  initialState,
  reducers: {
    fetchProductsStart: (state) => {
      state.loading = true;
      state.error = null;
    },
    fetchProductsSuccess: (state, action: PayloadAction<Product[]>) => {
      state.products = action.payload;
      state.loading = false;
    },
    fetchProductsFailure: (state, action: PayloadAction<string>) => {
      state.error = action.payload;
      state.loading = false;
    },
    selectProduct: (state, action: PayloadAction<string | null>) => {
      state.selectedProduct = action.payload
        ? state.products.find((p) => p.id === action.payload) || null
        : null;
    },
    clearSelectedProduct: (state) => {
      state.selectedProduct = null;
    },
    setFilters: (state, action: PayloadAction<Partial<ProductState['filters']>>) => {
      state.filters = { ...state.filters, ...action.payload };
    },
    clearFilters: (state) => {
      state.filters = {
        category: '',
        minPrice: 0,
        maxPrice: 1000,
        search: '',
      };
    },
  },
});

export const {
  fetchProductsStart,
  fetchProductsSuccess,
  fetchProductsFailure,
  selectProduct,
  clearSelectedProduct,
  setFilters,
  clearFilters,
} = productSlice.actions;

export default productSlice.reducer;