import { configureStore } from '@reduxjs/toolkit';
import { persistStore, persistReducer } from 'redux-persist';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { combineReducers } from '@reduxjs/toolkit';

// Importar slices
import authSlice from './slices/authSlice';
import userSlice from './slices/userSlice';
import productSlice from './slices/productSlice';
import cartSlice from './slices/cartSlice';
import scannerSlice from './slices/scannerSlice';
import esgSlice from './slices/esgSlice';
import paymentSlice from './slices/paymentSlice';

// Configuração do persist
const persistConfig = {
  key: 'root',
  storage: AsyncStorage,
  whitelist: ['auth', 'user', 'cart'], // Apenas estes slices serão persistidos
};

// Combinar reducers
const rootReducer = combineReducers({
  auth: authSlice,
  user: userSlice,
  product: productSlice,
  cart: cartSlice,
  scanner: scannerSlice,
  esg: esgSlice,
  payment: paymentSlice,
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
  devTools: __DEV__,
});

// Persistor
export const persistor = persistStore(store);

// Tipos
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
