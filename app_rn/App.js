import 'react-native-gesture-handler'; // react navigation的必要配置
import * as React from 'react';
import {View} from 'react-native';
// import {View} from './app/components/Themed';
import Navigation from './app/router/navigator';
import {Provider} from 'react-redux';
// import store from './app/store';

const App = () => {
  return (
    <View style={{flex: 1}}>
      {/* <Provider store={store}>
        <Navigation />
      </Provider> */}
    </View>
  );
};

export default App;
