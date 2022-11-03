import React, {Component} from 'react';
import {
  View,
  Image,
  Dimensions,
  Text,
  TouchableOpacity,
  StyleSheet,
  StatusBar,
  Platform,
} from 'react-native';
import Swiper from 'react-native-swiper';
import pxToDp from '../utils/todp';
const {width, height} = Dimensions.get('window'); //获取手机的宽和高

const styles = StyleSheet.create({
  wrapper: {
    position: 'absolute',
    top: 0,
    left: 0,
    zIndex: 2,
    width,
    height: height,
  },
  container: {
    flex: 1, //必写
    position: 'relative',
    backgroundColor: '#fff',
    zIndex: 1,
  },
  image: {
    width, //等于width:width
    position: 'absolute',
    bottom: 0,
    height,
    zIndex: 3,
  },
  btn: {
    zIndex: 11,
    position: 'absolute',
    bottom: pxToDp(90),
    width: pxToDp(500),
    height: pxToDp(80),
    left: pxToDp(125),
    borderRadius: pxToDp(40),
    backgroundColor: '#f35d5b',
    justifyContent: 'center',
    alignItems: 'center',
  },
  btnText: {
    color: '#fff',
    fontSize: pxToDp(28),
  },
});

export default class WelcomPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      beginUsename: '',
      beginToken: '',
    };
  }
  componentDidMount() {
    this.timer = setTimeout(() => {
      this.props.navigation.navigate('AppRouter');
    }, 3000);
  }
  componentWillUnmount() {
    this.timer && clearTimeout(this.timer); //同时为真的才执行卸载
  }
  render() {
    return (
      <View style={styles.container}>
        {Platform.OS == 'ios' ? (
          <StatusBar
            backgroundColor="rgba(0,0,0,0)"
            barStyle="dark-content"
            animated={true}
            translucent={true}
          />
        ) : (
          <StatusBar
            backgroundColor="rgba(0,0,0,0.4)"
            animated={true}
            translucent={true}
          />
        )}
        <Swiper
          style={styles.wrapper}
          showsButtons={false} //为false时不显示控制按钮
          paginationStyle={{
            //小圆点位置
            bottom: 70,
          }}
          loop={false} //如果设置为false，那么滑动到最后一张时，再次滑动将不会滑到第一张图片。
          autoplay={true} //自动轮播
          autoplayTimeout={2} //每隔2秒切换
        >
          <Image
            style={styles.image}
            source={require('../images/welcome.png')}
          />
        </Swiper>
      </View>
    );
  }
}
