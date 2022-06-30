import * as React from 'react';
import {Button, View, Text} from 'react-native';

// 修改信息
export default function UpdateProfilePage({navigation}) {
  return (
    <View style={{flex: 1, alignItems: 'center', justifyContent: 'center'}}>
      <Text>UpdateProfilePage</Text>
      <Button title="Go to Home" onPress={() => navigation.navigate('Home')} />
    </View>
  );
}
