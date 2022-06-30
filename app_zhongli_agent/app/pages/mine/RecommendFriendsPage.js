import * as React from 'react';
import {Button, View, Text} from 'react-native';

// 推荐好友：只有代理商才展示
export default function RecommendFriendsPage({navigation}) {
  return (
    <View style={{flex: 1, alignItems: 'center', justifyContent: 'center'}}>
      <Text>BindBankCardPage</Text>
      <Button title="Go to Home" onPress={() => navigation.navigate('Home')} />
    </View>
  );
}
