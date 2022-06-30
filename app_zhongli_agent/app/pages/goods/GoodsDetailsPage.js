import * as React from 'react';
import {Button, View, Text} from 'react-native';

export default function GoodsDetailsPage({navigation}) {
  return (
    <View style={{flex: 1, alignItems: 'center', justifyContent: 'center'}}>
      <Text>GoodsDetailsPage</Text>
      <Button
        title="Go to GoodsDetails"
        onPress={() => navigation.navigate('GoodsDetails')}
      />
    </View>
  );
}
