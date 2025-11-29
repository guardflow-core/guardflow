/**
 * Main App Navigator
 * GuardFlow Mobile App
 */

import React from 'react';
import {createStackNavigator} from '@react-navigation/stack';
import {useSelector} from 'react-redux';

// Navigators
import AuthNavigator from './AuthNavigator';
import MainTabNavigator from './MainTabNavigator';
import OnboardingNavigator from './OnboardingNavigator';

// Screens
import SplashScreen from '../screens/SplashScreen';

const Stack = createStackNavigator();

const AppNavigator = () => {
  const {isAuthenticated, isFirstTime, isLoading} = useSelector(state => ({
    isAuthenticated: state.auth.isAuthenticated,
    isFirstTime: state.user.isFirstTime,
    isLoading: state.auth.isLoading,
  }));

  if (isLoading) {
    return <SplashScreen />;
  }

  return (
    <Stack.Navigator
      screenOptions={{
        headerShown: false,
        gestureEnabled: false,
      }}>
      {isFirstTime ? (
        <Stack.Screen
          name="Onboarding"
          component={OnboardingNavigator}
          options={{
            animationTypeForReplace: 'push',
          }}
        />
      ) : !isAuthenticated ? (
        <Stack.Screen
          name="Auth"
          component={AuthNavigator}
          options={{
            animationTypeForReplace: 'push',
          }}
        />
      ) : (
        <Stack.Screen
          name="Main"
          component={MainTabNavigator}
          options={{
            animationTypeForReplace: 'push',
          }}
        />
      )}
    </Stack.Navigator>
  );
};

export default AppNavigator;



