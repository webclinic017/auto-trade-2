import * as React from 'react';
import {Button, View, Text} from 'react-native';

export default function GoodsSearchPage({navigation}) {
  return (
    <View style={{flex: 1, alignItems: 'center', justifyContent: 'center'}}>
      <Text>GoodsSearchPage</Text>
      <Button title="Go to Home" onPress={() => navigation.navigate('Home')} />
    </View>
  );
}
