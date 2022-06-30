import MD5 from 'react-native-md5';

function apiSign(
  params,
  startWrapper = 'medical_agent',
  endWrapper = 'medical_agent',
) {
  let data = params;
  let str = '';
  data = ksort(data);
  for (let i in data) {
    if (data[i] !== '') {
      str += i + data[i];
    }
  }
  data.sign = MD5.hex_md5(startWrapper + str + endWrapper);
  return data;
}

function ksort(o) {
  let sorted = {};
  const keys = Object.keys(o).sort();
  keys.forEach(key => {
    sorted[key] = o[key];
  });
  return sorted;
}

export default apiSign;
