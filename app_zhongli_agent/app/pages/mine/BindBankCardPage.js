import * as React from 'react';
import {Button, View, Text} from 'react-native';

// 银行卡
export default function BindBankCardPage({navigation}) {
  return (
    <View style={{flex: 1, alignItems: 'center', justifyContent: 'center'}}>
      <Text>BindBankCardPage</Text>
      <Button title="Go to Home" onPress={() => navigation.navigate('Home')} />
    </View>
  );
}
