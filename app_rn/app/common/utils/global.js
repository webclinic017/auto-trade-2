import {Platform} from 'react-native';
import pxToDp from './todp';
import MD5 from 'react-native-md5';

global.all = {
  // url: 'https://www.zlby.xyz/', //线上
  url: 'https://www.zlby.xyz/', //线上
  // url: "http://api-test.zlby.xyz/",//测试
  version: '1.0.0',
  Data: function (Obj) {
    let re = new RegExp('[\u4E00-\u9FA5]+');
    let obj = {...Obj};
    obj['keys'] = 'zlby2019';
    var newkey = Object.keys(obj).sort();
    var newObj = {};
    for (var i = 0; i < newkey.length; i++) {
      newObj[newkey[i]] = obj[newkey[i]];
    }
    let _string = '';
    for (let i in newObj) {
      if (re.test(newObj[i])) {
        let text = escape(newObj[i]);
        let _text = text.replace(/%/g, '\\');
        _string += i + '=' + _text.toLowerCase() + '&';
      } else {
        _string += i + '=' + newObj[i] + '&';
      }
    }
    let signText = _string.slice(0, _string.length - 1);
    console.log(signText);
    Obj['sign'] = MD5.hex_md5(signText);
    let _Data = '';
    for (let i in Obj) {
      _Data += i + '=' + Obj[i] + '&';
    }
    console.log(Obj);
    return _Data.slice(0, _Data.length - 1);
  },
  formatDateTime: function (inputTime) {
    var date = new Date(inputTime * 1000);
    var y = date.getFullYear();
    var m = date.getMonth() + 1;
    m = m < 10 ? '0' + m : m;
    var d = date.getDate();
    d = d < 10 ? '0' + d : d;
    var h = date.getHours();
    h = h < 10 ? '0' + h : h;
    var minute = date.getMinutes();
    var second = date.getSeconds();
    minute = minute < 10 ? '0' + minute : minute;
    second = second < 10 ? '0' + second : second;
    return y + '-' + m + '-' + d + ' ' + h + ':' + minute + ':' + second;
  },
  formatDateTimeNone: function (inputTime) {
    var date = new Date(inputTime * 1000);
    var y = date.getFullYear();
    var m = date.getMonth() + 1;
    m = m < 10 ? '0' + m : m;
    var d = date.getDate();
    d = d < 10 ? '0' + d : d;
    return y + '-' + m + '-' + d;
  },
  formatDateTimeOther: function (inputTime) {
    var date = new Date(inputTime * 1000);
    var y = date.getFullYear();
    var m = date.getMonth() + 1;
    m = m < 10 ? '0' + m : m;
    var d = date.getDate();
    d = d < 10 ? '0' + d : d;
    var h = date.getHours();
    h = h < 10 ? '0' + h : h;
    var minute = date.getMinutes();
    var second = date.getSeconds();
    minute = minute < 10 ? '0' + minute : minute;
    second = second < 10 ? '0' + second : second;
    return m + '-' + d + ' ' + h + ':' + minute + ':' + second;
  },
};
