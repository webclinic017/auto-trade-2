import React, {Component} from 'react';
import {
  View,
  Image,
  Dimensions,
  StyleSheet,
  DeviceEventEmitter,
  StatusBar,
  Text,
  TouchableOpacity,
  Platform,
} from 'react-native';

import pxToDp from '../utils/todp';
import {isIphoneX} from '../utils/ScreenUtils';
import {WebView} from 'react-native-webview';

const {width, height} = Dimensions.get('window'); //获取手机的宽和高
const STATUSBAR_HEIGHT =
  Platform.OS === 'ios' ? (isIphoneX() ? 44 : 20) : StatusBar.currentHeight;
export default class Webview extends Component {
  constructor(props) {
    super(props);
    this.state = {
      backButtonEnabled: '',
      forwardButtonEnabled: '',
      url: '',
      status: '',
      loading: '',
    };
  }
  _onNavigationStateChange = navState => {
    console.log(navState);
    this.setState(
      {
        backButtonEnabled: navState.canGoBack,
        forwardButtonEnabled: navState.canGoForward,
        url: navState.url,
        status: navState.title,
        loading: navState.loading,
      },
      () => {
        console.log(this.state.status);
      },
    );
  };
  goBack() {
    if (this.state.backButtonEnabled) {
      this.WebView.goBack();
    } else {
      DeviceEventEmitter.emit('realname');
      this.props.navigation.goBack();
    }
  }
  render() {
    const {params} = this.props.navigation.state;
    return (
      <View style={styles.webview}>
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
            style={{
              width: pxToDp(100),
              height: pxToDp(100),
              alignItems: 'center',
              justifyContent: 'center',
            }}
            onPress={() => this.goBack()}>
            <Image
              source={require('../images/back.png')}
              style={{
                width: pxToDp(16),
                height: pxToDp(28),
                marginLeft: pxToDp(30),
              }}
            />
          </TouchableOpacity>
          <Text style={styles.headerText}>{this.state.status}</Text>
          <View style={styles.block}></View>
        </View>
        <WebView
          ref={s => (this.WebView = s)}
          canGoBack={true}
          scalesPageToFit={false}
          source={{uri: params.url}}
          javaScriptEnabled={true}
          style={{width, height}}
          startInLoadingState={true}
          onNavigationStateChange={this._onNavigationStateChange}
        />
      </View>
    );
  }
}

const styles = StyleSheet.create({
  webview: {
    width,
    backgroundColor: '#fff',
    alignItems: 'center',
    flex: 1,
  },
  header: {
    width,
    height: pxToDp(100) + STATUSBAR_HEIGHT,
    paddingTop: STATUSBAR_HEIGHT,
    borderBottomWidth: 0,
    borderBottomColor: '#dedede',
    backgroundColor: '#559cf8',
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  headerText: {
    fontSize: pxToDp(38),
    color: '#fff',
    textAlign: 'center',
  },
  block: {
    width: pxToDp(100),
    height: pxToDp(100),
  },
});
