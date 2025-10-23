import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { Provider } from 'react-redux';
import { PersistGate } from 'redux-persist/integration/react';
import { StatusBar } from 'expo-status-bar';
import { store, persistor } from './src/store';
import AppNavigator from './src/navigation/AppNavigator';
import ScannerCartIntegration from './src/components/ScannerCartIntegration';

export default function App() {
  return (
    <Provider store={store}>
      <PersistGate loading={null} persistor={persistor}>
        <NavigationContainer>
          <AppNavigator />
          <ScannerCartIntegration />
          <StatusBar style="auto" />
        </NavigationContainer>
      </PersistGate>
    </Provider>
  );
}
