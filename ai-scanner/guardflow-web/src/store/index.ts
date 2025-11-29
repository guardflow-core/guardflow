import { configureStore } from '@reduxjs/toolkit';
import { persistStore, persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';
import { combineReducers } from '@reduxjs/toolkit';

// Importar slices
import authSlice from './slices/authSlice';
import userSlice from './slices/userSlice';
import productSlice from './slices/productSlice';
import cartSlice from './slices/cartSlice';
import esgSlice from './slices/esgSlice';
import themeSlice from './slices/themeSlice';
import scannerSlice from './slices/scannerSlice';
import paymentSlice from './slices/paymentSlice';
import analyticsSlice from './slices/analyticsSlice';

// Configuração do persist
const persistConfig = {
  key: 'root',
  storage,
  whitelist: ['auth', 'user', 'theme', 'cart'], // Apenas estes slices serão persistidos
};

// Combinar reducers
const rootReducer = combineReducers({
  auth: authSlice,
  user: userSlice,
  product: productSlice,
  cart: cartSlice,
  esg: esgSlice,
  theme: themeSlice,
  scanner: scannerSlice,
  payment: paymentSlice,
  analytics: analyticsSlice,
});

// Reducer persistido
const persistedReducer = persistReducer(persistConfig, rootReducer);

// Configurar store
export const store = configureStore({
  reducer: persistedReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST', 'persist/REHYDRATE'],
      },
    }),
  devTools: process.env.NODE_ENV !== 'production',
});

// Persistor
export const persistor = persistStore(store);

// Tipos
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;