import AsyncStorage from 'react-native';

export default class DeviceStorage {
  static save = async (key, value) => {
    try {
      const result = await AsyncStorage.setItem(key, value);
      console.log('save result', result);
    } catch (e) {
      console.log('error', e);
      // saving error
    }
  };
  static get = async key => {
    try {
      const value = await AsyncStorage.getItem(key);
      //console.log('--value-',value)
      return JSON.parse(value);
    } catch (e) {
      console.log('error', e);
      // error reading value
    }
  };
}
