import * as React from 'react';
import {Button, View, Text} from 'react-native';

export default function ObligatoryContractPage({navigation}) {
  return (
    <View style={{flex: 1, alignItems: 'center', justifyContent: 'center'}}>
      <Text>ObligatoryContractPage</Text>
      <Button title="Go to Home" onPress={() => navigation.navigate('Home')} />
    </View>
  );
}
