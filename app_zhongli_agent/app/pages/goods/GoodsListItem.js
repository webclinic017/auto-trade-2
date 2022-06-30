import * as React from 'react';
import {
  View,
  Text,
  Image,
  TouchableOpacity,
  StyleSheet,
  Dimensions,
} from 'react-native';

import pxToDp from '../../common/utils/todp';

const GoodsListItem = ({navigation, item, onItemClick}) => {
  const onItemClickIntern = () =>
    item.status === 1
      ? navigation.navigate('ProjectDetail', {
          id: item.id,
          numbers: item.numbers,
          saleNumber: item.sale_number,
        })
      : '';

  return (
    <TouchableOpacity
      key={item.id}
      onPress={onItemClick()}
      style={styles.homeRow}>
      <Image style={styles.homeRowImg} source={{uri: item.thumb}} />
      <View style={styles.homeRowRight}>
        <Text numberOfLines={2} style={styles.homeRowTitle}>
          {item.title}
        </Text>
        {item.status === 1 || item.numbers <= 0 ? (
          <View style={styles.homeRowInfor}>
            <Text style={styles.homeRowInforText}>已售 {item.sale_number}</Text>
            <Text style={styles.homeRowInforText}>剩余 {item.numbers}</Text>
          </View>
        ) : (
          <View style={styles.homeRowInfor}>
            <Text style={styles.homeRowInforText}>售罄</Text>
          </View>
        )}
        <Text style={styles.money}>
          ¥<Text style={styles.moneyText}>{item.once_money}</Text>/张
        </Text>
        {item.status === 1 ? null : (
          <Image
            style={styles.shouyao}
            source={require('../../images/home/shouyao.png')}
          />
        )}
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  homeRow: {
    marginTop: pxToDp(30),
    flexDirection: 'row',
    alignItems: 'flex-start',
    justifyContent: 'space-between',
  },
  homeRowImg: {
    width: pxToDp(200),
    height: pxToDp(200),
    borderRadius: pxToDp(10),
  },
  homeRowRight: {
    width: pxToDp(460),
    borderBottomWidth: pxToDp(1),
    borderBottomColor: '#EEEEEE',
    height: pxToDp(200),
    position: 'relative',
  },
  shouyao: {
    position: 'absolute',
    width: pxToDp(150),
    height: pxToDp(117),
    right: 0,
    bottom: pxToDp(31),
  },
  homeRowTitle: {
    lineHeight: pxToDp(40),
    fontSize: pxToDp(30),
    color: '#333333',
  },
  homeRowInfor: {
    flexDirection: 'row',
    marginTop: pxToDp(5),
  },
  homeRowInforText: {
    fontSize: pxToDp(26),
    color: '#A6ABBB',
    marginRight: pxToDp(20),
  },
  money: {
    marginTop: pxToDp(25),
    color: '#FF3B3B',
    fontSize: pxToDp(26),
  },
  moneyText: {
    fontSize: pxToDp(36),
  },
});

export default GoodsListItem;
