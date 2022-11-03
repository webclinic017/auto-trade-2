/**
 * @format
 */

import {AppRegistry} from 'react-native';
// import App from './App';
import App from './app/router';
// import AppRN from './AppRN';
import {name as appName} from './app.json';

AppRegistry.registerComponent(appName, () => App);
