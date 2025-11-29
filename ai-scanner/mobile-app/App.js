/**
 * GuardFlow Mobile App
 * Agiliza aí suas compras! Sistema de Checkout Inteligente
 * Powered by GuardPass
 */

import React from 'react';
import {SafeAreaProvider} from 'react-native-safe-area-context';
import {Provider} from 'react-redux';
import {PersistGate} from 'redux-persist/integration/react';
import {NavigationContainer} from '@react-navigation/native';
import Toast from 'react-native-toast-message';

// Store
import {store, persistor} from './src/store';

// Navigation
import AppNavigator from './src/navigation/AppNavigator';

// Components
import LoadingScreen from './src/components/common/LoadingScreen';
import ErrorBoundary from './src/components/common/ErrorBoundary';

// Services
import {initializeApp} from './src/services/app/appService';

// Styles
import {toastConfig} from './src/styles/toastConfig';

class App extends React.Component {
  componentDidMount() {
    initializeApp();
  }

  render() {
    return (
      <ErrorBoundary>
        <SafeAreaProvider>
          <Provider store={store}>
            <PersistGate loading={<LoadingScreen />} persistor={persistor}>
              <NavigationContainer>
                <AppNavigator />
                <Toast config={toastConfig} />
              </NavigationContainer>
            </PersistGate>
          </Provider>
        </SafeAreaProvider>
      </ErrorBoundary>
    );
  }
}

export default App;
