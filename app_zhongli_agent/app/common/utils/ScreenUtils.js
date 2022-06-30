import {
  Dimensions,
  Platform,
  NativeModules,
  DeviceInfo,
  StatusBar,
} from 'react-native';

const X_WIDTH = 375;
const X_HEIGHT = 812;

const {height: D_HEIGHT, width: D_WIDTH} = Dimensions.get('window');

const {PlatformConstants = {}} = NativeModules;
const {minor = 0} = PlatformConstants.reactNativeVersion || {};

const {width, height} = Dimensions.get('window');
const screenWidth = width;
const screenHeight = height;

function isIphoneX() {
  if (Platform.OS === 'web') return false;
  if (minor >= 50) {
    return DeviceInfo.isIPhoneX_deprecated;
  }
  return (
    Platform.OS === 'ios' &&
    ((D_HEIGHT === X_HEIGHT && D_WIDTH === X_WIDTH) ||
      (D_HEIGHT === X_WIDTH && D_WIDTH === X_HEIGHT))
  );
}

const STATUSBAR_HEIGHT =
  Platform.OS === 'ios' ? (isIphoneX() ? 44 : 20) : StatusBar.currentHeight;

module.exports = {
  isIphoneX,
  STATUSBAR_HEIGHT,
  screenWidth,
  screenHeight,
};
