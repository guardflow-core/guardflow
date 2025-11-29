/**
 * Redux Store Configuration
 * GuardFlow Mobile App
 */

import {configureStore} from '@reduxjs/toolkit';
import {
  persistStore,
  persistReducer,
  FLUSH,
  REHYDRATE,
  PAUSE,
  PERSIST,
  PURGE,
  REGISTER,
} from 'redux-persist';
import AsyncStorage from '@react-native-async-storage/async-storage';
import {combineReducers} from '@reduxjs/toolkit';

// Slices
import authSlice from './slices/authSlice';
import userSlice from './slices/userSlice';
import cartSlice from './slices/cartSlice';
import tokensSlice from './slices/tokensSlice';
import nftsSlice from './slices/nftsSlice';
import productsSlice from './slices/productsSlice';
import scannerSlice from './slices/scannerSlice';
import paymentsSlice from './slices/paymentsSlice';
import rewardsSlice from './slices/rewardsSlice';
import settingsSlice from './slices/settingsSlice';

// Middleware
import {apiMiddleware} from './middleware/apiMiddleware';
import {blockchainMiddleware} from './middleware/blockchainMiddleware';
import {analyticsMiddleware} from './middleware/analyticsMiddleware';

// Root Reducer
const rootReducer = combineReducers({
  auth: authSlice,
  user: userSlice,
  cart: cartSlice,
  tokens: tokensSlice,
  nfts: nftsSlice,
  products: productsSlice,
  scanner: scannerSlice,
  payments: paymentsSlice,
  rewards: rewardsSlice,
  settings: settingsSlice,
});

// Persist Configuration
const persistConfig = {
  key: 'root',
  version: 1,
  storage: AsyncStorage,
  whitelist: [
    'auth',
    'user', 
    'tokens',
    'nfts',
    'settings'
  ], // Only persist these slices
  blacklist: [
    'scanner',
    'cart' // Don't persist temporary data
  ]
};

const persistedReducer = persistReducer(persistConfig, rootReducer);

// Store Configuration
export const store = configureStore({
  reducer: persistedReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
      },
    })
    .concat(apiMiddleware)
    .concat(blockchainMiddleware)
    .concat(analyticsMiddleware),
  devTools: __DEV__,
});

export const persistor = persistStore(store);

// Types
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;



