import React from 'react';
import {Button, Text, View, StyleSheet} from 'react-native';
import {createStackNavigator} from '@react-navigation/stack';
import {NavigationContainer} from '@react-navigation/native';
import {createNativeStackNavigator} from '@react-navigation/native-stack';
import {createBottomTabNavigator} from '@react-navigation/bottom-tabs';

function SettingsScreen({navigation}) {
  return (
    <View style={{flex: 1, alignItems: 'center', justifyContent: 'center'}}>
      <Text>Settings Screen</Text>
      <Button
        title="Go to Profile"
        onPress={() => navigation.navigate('Profile')}
      />
    </View>
  );
}

function ProfileScreen({navigation}) {
  React.useEffect(
    () => navigation.addListener('focus', () => alert('Screen was focused')),
    [navigation],
  );

  React.useEffect(
    () => navigation.addListener('blur', () => alert('Screen was unfocused')),
    [navigation],
  );

  return (
    <View style={{flex: 1, alignItems: 'center', justifyContent: 'center'}}>
      <Text>Profile Screen</Text>
      <Button
        title="Go to Settings"
        onPress={() => navigation.navigate('Settings')}
      />
    </View>
  );
}

function HomeScreen({navigation}) {
  return (
    <View style={{flex: 1, alignItems: 'center', justifyContent: 'center'}}>
      <Text>Home Screen</Text>
      <Button
        title="Go to Details"
        onPress={() => navigation.navigate('Details')}
      />
    </View>
  );
}

function DetailsScreen({navigation}) {
  return (
    <View style={{flex: 1, alignItems: 'center', justifyContent: 'center'}}>
      <Text>Details Screen</Text>
      <Button
        title="Go to Details... again"
        onPress={() => navigation.push('Details')}
      />
    </View>
  );
}

// const HomeTab1 = createBottomTabNavigator();
// const HomeStack1 = createNativeStackNavigator();
// const OrderStack1 = createNativeStackNavigator();
// const MineStack1 = createNativeStackNavigator();

// const HomeTabN1 = () => (
//   <HomeTab1.Navigator screenOptions={{headerShown: false}}>
//     <HomeTab1.Screen name="First">
//       {() => (
//         <HomeStack1.Navigator>
//           <HomeStack1.Screen name="Home" component={HomePage} />
//           <HomeStack1.Screen name="GoodsDetails" component={DummyPage} />
//           <HomeStack1.Screen name="ConfirmOrder" component={DummyPage} />
//         </HomeStack1.Navigator>
//       )}
//     </HomeTab1.Screen>
//     <HomeTab1.Screen name="Second">
//       {() => (
//         <OrderStack1.Navigator>
//           <OrderStack1.Screen name="Order" component={DummyPage} />
//           <OrderStack1.Screen name="OrderDeteils" component={DummyPage} />
//           <OrderStack1.Screen name="assetIncome" component={DummyPage} />
//           <OrderStack1.Screen name="signContractModal" component={DummyPage} />
//           <OrderStack1.Screen name="ObligatoryContract" component={DummyPage} />
//           <OrderStack1.Screen name="ProxyAgreement" component={DummyPage} />
//         </OrderStack1.Navigator>
//       )}
//     </HomeTab1.Screen>
//     <HomeTab1.Screen name="Three">
//       {() => (
//         <OrderStack1.Navigator>
//           <OrderStack1.Screen name="图文广告" component={DummyPage} />
//           <OrderStack1.Screen name="新闻公告" component={DummyPage} />
//           <OrderStack1.Screen name="视频" component={DummyPage} />
//           <OrderStack1.Screen name="产品出售（暂定）" component={DummyPage} />
//         </OrderStack1.Navigator>
//       )}
//     </HomeTab1.Screen>
//     <HomeTab1.Screen name="Four">
//       {() => (
//         <MineStack1.Navigator>
//           <MineStack1.Screen name="Mine" component={DummyPage} />
//           <MineStack1.Screen name="RealName" component={DummyPage} />
//           <MineStack1.Screen name="陪护系统结算" component={DummyPage} />
//           <MineStack1.Screen name="智慧病房结算" component={DummyPage} />
//           <MineStack1.Screen name="bindBankCard" component={DummyPage} />
//           <MineStack1.Screen name="recommendFrieds" component={DummyPage} />
//           <MineStack1.Screen name="updateProfile" component={DummyPage} />
//           <MineStack1.Screen name="assetsIncome" component={DummyPage} />
//           <MineStack1.Screen name="RealName" component={DummyPage} />
//           <MineStack1.Screen name="login" component={DummyPage} />
//           <MineStack1.Screen name="register" component={DummyPage} />
//           <MineStack1.Screen name="resetPassword" component={DummyPage} />
//         </MineStack1.Navigator>
//       )}
//     </HomeTab1.Screen>
//   </HomeTab1.Navigator>
// );

// const DummyTab = createBottomTabNavigator();
// const DummySettingsStack = createNativeStackNavigator();
// const DummyHomeStack = createNativeStackNavigator();

// const DummyTabN = () => (
//   <DummyTab.Navigator screenOptions={{headerShown: false}}>
//     <DummyTab.Screen name="First">
//       {() => (
//         <DummySettingsStack.Navigator>
//           <DummySettingsStack.Screen
//             name="Settings"
//             component={SettingsScreen}
//           />
//           <DummySettingsStack.Screen name="Profile" component={ProfileScreen} />
//         </DummySettingsStack.Navigator>
//       )}
//     </DummyTab.Screen>
//     <DummyTab.Screen name="Second">
//       {() => (
//         <DummyHomeStack.Navigator>
//           <DummyHomeStack.Screen name="Home" component={HomeScreen} />
//           <DummyHomeStack.Screen name="Details" component={DetailsScreen} />
//         </DummyHomeStack.Navigator>
//       )}
//     </DummyTab.Screen>
//   </DummyTab.Navigator>
// );

const Root = createStackNavigator();

const Screen1 = ({navigation, route}) => (
  <View style={styles.screen}>
    <Text style={styles.title}>Screen 1</Text>
    <Button
      title="Go to Screen 2"
      onPress={() => {
        navigation.push('Screen2');
      }}
    />
  </View>
);

const Screen2 = ({navigation, route}) => (
  <View style={styles.screen}>
    <Text style={styles.title}>Screen 2</Text>
    <Button
      title="Go back"
      onPress={() => {
        navigation.pop();
      }}
    />
  </View>
);

export default function App() {
  return (
    <NavigationContainer>
      <Root.Navigator>
        <Root.Screen name="Screen1" component={Screen1} />
        <Root.Screen name="Screen2" component={Screen2} />
      </Root.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  screen: {
    marginTop: 40,
    alignItems: 'center',
  },
  title: {
    padding: 20,
    fontSize: 42,
  },
});
