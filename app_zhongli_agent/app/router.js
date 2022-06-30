import * as React from 'react';
import {Button, View, Text} from 'react-native';
import {NavigationContainer} from '@react-navigation/native';
import {createNativeStackNavigator} from '@react-navigation/native-stack';
import {createBottomTabNavigator} from '@react-navigation/bottom-tabs';
import MaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons';

import HomePage from './pages/home/HomePage';

function DummyPage({navigation, route}) {
  const {name} = route;
  return (
    <View style={{flex: 1, alignItems: 'center', justifyContent: 'center'}}>
      <Text>Dummy {name} Page</Text>
      <Button title="Go to Home" onPress={() => navigation.navigate('Home')} />
    </View>
  );
}

const Tab = createBottomTabNavigator();

const Home = () => (
  <Tab.Navigator
    initialRouteName="Goods"
    screenOptions={{
      headerShown: false,
      tabBarActiveTintColor: '#e91e63',
    }}>
    <Tab.Screen
      name="Goods"
      component={HomePage}
      options={{
        tabBarLabel: '首页',
        tabBarIcon: ({color, size}) => (
          <MaterialCommunityIcons name="home" color={color} size={size} />
        ),
      }}
    />
    <Tab.Screen
      name="Order"
      component={DummyPage}
      options={{
        tabBarLabel: '订单',
        tabBarIcon: ({color, size}) => (
          <MaterialCommunityIcons name="bell" color={color} size={size} />
        ),
      }}
    />
    <Tab.Screen
      name="Discovery"
      component={DummyPage}
      options={{
        tabBarLabel: '发现',
        tabBarIcon: ({color, size}) => (
          <MaterialCommunityIcons name="home" color={color} size={size} />
        ),
      }}
    />
    <Tab.Screen
      name="First"
      component={DummyPage}
      options={{
        tabBarLabel: '我的',
        tabBarIcon: ({color, size}) => (
          <MaterialCommunityIcons name="account" color={color} size={size} />
        ),
      }}
    />
  </Tab.Navigator>
);

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen
          name="Home"
          component={Home}
          options={{headerShown: false}}
        />
        <Stack.Screen name="dummy" component={DummyPage} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
