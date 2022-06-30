import * as React from 'react';
import {Button, View, Text} from 'react-native';

// 我的
export default function MinePage({navigation}) {
  return (
    <View style={{flex: 1, alignItems: 'center', justifyContent: 'center'}}>
      <Text>MinePage</Text>
      <Button title="Go to Home" onPress={() => navigation.navigate('Home')} />
    </View>
  );
}
