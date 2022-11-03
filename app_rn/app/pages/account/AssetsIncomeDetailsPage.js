import * as React from 'react';
import {Button, View, Text} from 'react-native';

// 某个 Goods 的 AssetsIncome
export default function AssetsIncomeDetailsPage({navigation}) {
  return (
    <View style={{flex: 1, alignItems: 'center', justifyContent: 'center'}}>
      <Text>AssetsIncomeDetailsPage</Text>
      <Button title="Go to Home" onPress={() => navigation.navigate('Home')} />
    </View>
  );
}
