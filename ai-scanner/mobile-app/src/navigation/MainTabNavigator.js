/**
 * Main Tab Navigator
 * QuickFlow Mobile App
 */

import React from 'react';
import {createBottomTabNavigator} from '@react-navigation/bottom-tabs';
import {useSelector} from 'react-redux';
import Icon from 'react-native-vector-icons/MaterialIcons';

// Navigators
import ShoppingNavigator from './ShoppingNavigator';
import RewardsNavigator from './RewardsNavigator';
import ProfileNavigator from './ProfileNavigator';

// Screens
import ScannerScreen from '../screens/shopping/ScannerScreen';

// Styles
import {colors, typography} from '../styles';

const Tab = createBottomTabNavigator();

const MainTabNavigator = () => {
  const {gstBalance, nftCount} = useSelector(state => ({
    gstBalance: state.tokens.gstBalance,
    nftCount: state.nfts.collection.length,
  }));

  const getTabBarIcon = (routeName, focused, color, size) => {
    let iconName;

    switch (routeName) {
      case 'Shopping':
        iconName = 'shopping-cart';
        break;
      case 'Scanner':
        iconName = 'camera-alt';
        break;
      case 'Rewards':
        iconName = 'stars';
        break;
      case 'Profile':
        iconName = 'person';
        break;
      default:
        iconName = 'help';
    }

    return <Icon name={iconName} size={size} color={color} />;
  };

  const getTabBarBadge = (routeName) => {
    switch (routeName) {
      case 'Rewards':
        return gstBalance > 0 ? gstBalance.toString() : null;
      case 'Profile':
        return nftCount > 0 ? nftCount.toString() : null;
      default:
        return null;
    }
  };

  return (
    <Tab.Navigator
      screenOptions={({route}) => ({
        headerShown: false,
        tabBarIcon: ({focused, color, size}) =>
          getTabBarIcon(route.name, focused, color, size),
        tabBarBadge: getTabBarBadge(route.name),
        tabBarActiveTintColor: colors.primary.green,
        tabBarInactiveTintColor: colors.gray.medium,
        tabBarStyle: {
          backgroundColor: colors.white,
          borderTopWidth: 1,
          borderTopColor: colors.gray.light,
          paddingBottom: 5,
          paddingTop: 5,
          height: 60,
        },
        tabBarLabelStyle: {
          fontSize: typography.sizes.xs,
          fontFamily: typography.fonts.medium,
          marginTop: -5,
        },
        tabBarItemStyle: {
          paddingVertical: 5,
        },
      })}
      initialRouteName="Scanner">
      
      <Tab.Screen
        name="Shopping"
        component={ShoppingNavigator}
        options={{
          title: 'Compras',
        }}
      />
      
      <Tab.Screen
        name="Scanner"
        component={ScannerScreen}
        options={{
          title: 'Scanner',
          tabBarIconStyle: {
            backgroundColor: colors.primary.green,
            borderRadius: 25,
            padding: 8,
          },
        }}
      />
      
      <Tab.Screen
        name="Rewards"
        component={RewardsNavigator}
        options={{
          title: 'Recompensas',
        }}
      />
      
      <Tab.Screen
        name="Profile"
        component={ProfileNavigator}
        options={{
          title: 'Perfil',
        }}
      />
    </Tab.Navigator>
  );
};

export default MainTabNavigator;



