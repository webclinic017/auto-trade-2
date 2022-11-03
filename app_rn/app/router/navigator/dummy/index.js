/**
 * 页面路由、入口、跟随系统主题
 */
import * as React from 'react';
import {useColorScheme} from 'react-native'; //获取系统当前主题
import {createStackNavigator} from '@react-navigation/stack';
// 底部菜单栏主题参考： https://reactnavigation.org/docs/themes/#basic-usage
import {
  DarkTheme,
  DefaultTheme,
  NavigationContainer,
} from '@react-navigation/native';
import BTN from './bottomTabNavigator';
import LoginPage from './loginPage';
import DetailPage from './detailsPage';
import SearchPage from './searchPage';
import {ThemeProvider} from 'react-native-elements'; //react native element 主题配置：参考https://reactnativeelements.com/docs/customization

//创建页面栈
const Stack = createStackNavigator();

function App() {
  //获取系统配色
  const ColorScheme = useColorScheme();
  //修改底部菜单栏背景颜色为白色
  const lightTheme = {
    ...DefaultTheme,
    colors: {
      ...DefaultTheme.colors,
      background: '#fff',
    },
  };
  return (
    <ThemeProvider useDark={ColorScheme === 'dark'}>
      <NavigationContainer
        theme={ColorScheme === 'dark' ? DarkTheme : lightTheme}>
        <Stack.Navigator initialRoute>
          <Stack.Screen
            component={LoginPage}
            options={{title: '登录', headerShown: false}}
          />
          <Stack.Screen
            component={BTN}
            options={{title: '首页', headerShown: false}}
          />

          <Stack.Screen component={DetailPage} />

          {/* 搜索页面 */}
          <Stack.Screen options={{headerShown: false}} component={SearchPage} />
        </Stack.Navigator>
      </NavigationContainer>
    </ThemeProvider>
  );
}

export default App;
