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
import {isIphoneX} from '../utils/ScreenUtils';
import Video from 'react-native-video';
const {width, height} = Dimensions.get('window'); //获取手机的宽和高
const STATUSBAR_HEIGHT =
  Platform.OS === 'ios' ? (isIphoneX() ? 44 : 20) : StatusBar.currentHeight;

const styles = StyleSheet.create({
  videoContainer: {
    width,
    backgroundColor: '#000',
    alignItems: 'center',
    flex: 1,
    position: 'relative',
  },
  header: {
    position: 'absolute',
    top: 0,
    left: 0,
    height: pxToDp(100) + STATUSBAR_HEIGHT,
    paddingTop: STATUSBAR_HEIGHT,
    width,
    zIndex: 9,
    flexDirection: 'row',
    alignItems: 'center',
  },
  back: {
    // width: pxToDp(18),
    // height: pxToDp(32),
    marginRight: pxToDp(40),
    width: pxToDp(100),
    height: '100%',
    justifyContent: 'center',
  },
  backImg: {
    marginLeft: pxToDp(34),
    width: pxToDp(18),
    height: pxToDp(32),
  },
  title: {
    fontSize: pxToDp(30),
    color: '#fff',
  },
  backgroundVideo: {
    width: '100%',
    height: pxToDp(500),
  },
});

export default class VideoC extends Component {
  constructor(props) {
    super(props);
    this.player = null;
    this.state = {
      rate: 1,
      volume: 1,
      muted: false,
      resizeMode: 'contain',
      duration: 0.0,
      currentTime: 0.0,
      paused: true,
    };
  }
  componentDidMount() {}
  componentWillUnmount() {}
  render() {
    return (
      <View style={styles.videoContainer}>
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
        <View style={styles.header}>
          <TouchableOpacity
            onPress={() => this.props.navigation.goBack()}
            style={styles.back}>
            <Image
              source={require('../images/back.png')}
              style={styles.backImg}
            />
          </TouchableOpacity>
          <Text style={styles.title}>
            西部信息港：智能健康手环和智慧健康检测...
          </Text>
        </View>
        <Video
          source={{
            uri: 'http://vd3.bdstatic.com/mda-jm0fvpxwe57qwk3y/hd/mda-jm0fvpxwe57qwk3y.mp4?playlist=%5B%22hd%22%5D',
          }} // 视频的URL地址，或者本地地址，都可以.
          //source={require('./music.mp3')} // 还可以播放音频，和视频一样
          //source={{uri:'http://......'}}
          ref="player"
          rate={1} // 控制暂停/播放，0 代表暂停paused, 1代表播放normal.
          volume={1.0} // 声音的放声音的放大倍数大倍数，0 代表没有声音，就是静音muted, 1 代表正常音量 normal，更大的数字表示放大的倍数
          muted={false} // true代表静音，默认为false.
          paused={false} // true代表暂停，默认为false
          resizeMode="contain" // 视频的自适应伸缩铺放行为，contain、stretch、cover
          repeat={false} // 是否重复播放
          playInBackground={false} // 当app转到后台运行的时候，播放是否暂停
          playWhenInactive={false} // [iOS] Video continues to play when control or notification center are shown. 仅适用于IOS
          onLoadStart={this.loadStart} // 当视频开始加载时的回调函数
          onLoad={this.setDuration} // 当视频加载完毕时的回调函数
          onProgress={this.setTime} //  进度控制，每250ms调用一次，以获取视频播放的进度
          onEnd={this.onEnd} // 当视频播放完毕后的回调函数
          onError={this.videoError} // 当视频不能加载，或出错后的回调函数
          style={styles.backgroundVideo}
        />
      </View>
    );
  }
}
