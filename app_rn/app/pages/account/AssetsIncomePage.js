import * as React from 'react';
import {Button, View, Text} from 'react-native';

// 资产收益 只有代理商才显示
export default function AssetsSettlementWardPage({navigation}) {
  return (
    <View style={{flex: 1, alignItems: 'center', justifyContent: 'center'}}>
      <Text>AssetsIncomePage</Text>
      <Button title="Go to Home" onPress={() => navigation.navigate('Home')} />
    </View>
  );
}
