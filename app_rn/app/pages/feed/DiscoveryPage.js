import * as React from 'react';
import {Button, View, Text} from 'react-native';

/*
    - 发现
      - 图文广告
      - 新闻公告
      - 视频
      - 产品出售（暂定）
*/
export default function DiscoveryPage({navigation}) {
  return (
    <View style={{flex: 1, alignItems: 'center', justifyContent: 'center'}}>
      <Text>DiscoveryPage</Text>
      <Button title="Go to Home" onPress={() => navigation.navigate('Home')} />
    </View>
  );
}
