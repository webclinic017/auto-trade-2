import axios from 'axios';
import {Alert} from 'react-native';
import DeviceStorage from '../common/utils/asyncStorage';
import apiSign from './apisign/apiSign';

function getToken() {
  return new Promise((resolve, reject) => {
    DeviceStorage.get('token')
      .then(value => {
        resolve({token: value || ''});
      })
      .catch(error => {
        resolve({token: ''});
      });
  });
}

axios.defaults.baseURL = '';

//请求拦截器
axios.interceptors.request.use(
  function (config) {
    console.log('request >>>: ' + config);
    return getToken()
      .then(tokenObj => {
        console.log('token: ' + tokenObj.token);
        config = config ? config : {};
        // let timestamp = 0;
        /*
        header: {
          'Content-Type': 'application/x-www-form-urlencoded'
          // 'Content-Type': 'application/json'
        }
        */
        if (
          config.method === 'post' ||
          config.headers['Content-Type'] === 'application/x-www-form-urlencoded'
        ) {
          let newParams = {};
          let sign = apiSign(config.data || {});
          newParams.sign = sign;
          newParams.token = tokenObj.token;
          config.data = JSON.stringify(newParams);
        }
        console.log('request handled>>>: ' + config);
        return config;
      })
      .catch(error => {
        console.log('token error: ' + error);
      });
    // // 添加响应头等等设置
    // config.headers.userToken = 'token dummy';
    // return config;
  },
  function (error) {
    console.log('request error: ' + error);
    return Promise.reject(error); // 请求出错
  },
);

//返回拦截器
axios.interceptors.response.use(
  function (response) {
    console.log('response >>>: ' + response);
    let {config, status} = response;
    let {code, msg, data} = response.data;
    if (status === 200) {
      if (code === 0) {
        return response.data;
      } else {
        return Promise.reject(msg);
      }
    } else {
      return Promise.reject('请求失败');
    }
  },
  function (error) {
    console.log('response error: ' + error);
    return Promise.reject(error);
  },
);

const defaultData = {};
const defatltUrl = '';

function post(url = defatltUrl, data = defaultData) {
  return axios({
    method: 'POST',
    url,
    data,
  });
}

function get(url = defatltUrl, data = defaultData) {
  return axios({
    method: 'GET',
    url,
    data,
  });
}

const httpBloc = {
  post,
  get,
};

export default httpBloc;
