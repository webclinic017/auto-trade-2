import * as React from 'react';
import {
  Button,
  View,
  Text,
  Image,
  TouchableOpacity,
  FlatList,
  RefreshControl,
  Animated,
  Linking,
  Modal,
  StyleSheet,
  Platform,
  StatusBar,
  Dimensions,
  NetInfo,
} from 'react-native';

import pxToDp from '../../common/utils/todp';
import {STATUSBAR_HEIGHT} from '../../common/utils/ScreenUtils';
const {width, height} = Dimensions.get('window');

import Toast from '../../common/components/toast';
import Loading from '../../common/components/loading';

import HttpUtils from '../../common/utils/HttpUtils';

import GoodsListItem from '../goods/GoodsListItem';

// 首页 商品列表
export default function HomePage({navigation}) {
  //更新
  const {isShow, setIsShow} = React.useState(false);
  const {upgradeType, setUpgradeType} = React.useState(0);

  //toast
  const toastEl = React.useRef(null);
  const loadingEl = React.useRef(null);

  //data
  const {data, setData} = React.useState(null);
  const {page, setPage} = React.useState(1);
  const {isRefresh, setIsRefresh} = React.useState(false);
  const {hasMore, setHasMore} = React.useState(false);

  const _onRefresh = () => {
    if (!(isRefresh || false)) {
      setPage(1);
      getData();
    }
  };
  const _onLoadMore = () => {
    if (hasMore || false) {
      setPage(page + 1);
      getData();
    }
  };

  function _createEmptyView() {
    return (
      // <View style={{width:"100%",height:"100%",justifyContent:"center",alignItems:"center"}}>
      //    <Text style={{fontSize:PxToDp(30),color:global.all.fontColor,marginTop:PxToDp(30)}}>暂无商品！</Text>
      <View />
    );
  }

  const getData = () => {
    NetInfo.isConnected.fetch().done(isConnected => {
      if (isConnected) {
        let params = {
          page: page,
        };
        this.refs.loading.show();
        HttpUtils.post('qc_goods_list', global.all.Data(params))
          .then(result => {
            this.refs.loading.hide();
            console.log(result);
            if (result.code == '0') {
              let newData = result.data.info;
              if (page == 1) {
                if (newData == null || newData.length < 10) {
                  setHasMore(false);
                  setData(newData || []);
                } else {
                  setHasMore(true);
                  setData(newData || []);
                }
              } else {
                if (newData.length < 10) {
                  setHasMore(false);
                  setData((data || []).concat(newData));
                } else {
                  setHasMore(true);
                  setData((data || []).concat(newData));
                }
              }
            } else {
              toastEl.show(result.msg, 1000);
            }
          })
          .catch(error => {
            this.refs.loading.hide();
            console.log(error);
          });
      } else {
        this.refs.toast.show('网络似乎出错了', 1000);
      }
    });
  };

  const goSearch = () => {
    navigation.navigate('Search');
  };

  const goShare = () => {
    let User = this.props.User;
    if (!User) {
      navigation.navigate('Login');
      return false;
    }
    navigation.navigate('Share');
  };

  const goUpgrade = () => {
    if (Platform.OS === 'ios') {
      let url = 'http://itunes.apple.com/app/id1526275481';
      Linking.openURL(url).catch(err =>
        console.error('An error occurred', err),
      );
    } else {
      let url = 'http://d.firim.vip/m2l9';
      Linking.openURL(url).catch(err =>
        console.error('An error occurred', err),
      );
    }
  };

  return (
    <View style={styles.container}>
      {Platform.OS === 'ios' ? (
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
        <Text style={styles.headText}>首页</Text>
        <TouchableOpacity onPress={() => goSearch()} style={styles.search}>
          <Image
            style={styles.searchIcon}
            source={require('../../images/search.png')}
          />
          <Text style={styles.Input}>请输入您要搜索的内容</Text>
        </TouchableOpacity>
      </View>
      <TouchableOpacity onPress={() => goShare()} style={styles.banner}>
        <Image
          style={styles.bannerImg}
          source={require('../../images/home/homeBanner1.png')}
        />
      </TouchableOpacity>

      <View style={styles.homeCon}>
        <Text style={styles.homeConTitle}>推荐产品</Text>
        <View style={styles.homeContent}>
          <FlatList
            data={data}
            ListEmptyComponent={_createEmptyView.bind(this)}
            onRefresh={() => _onRefresh()}
            refreshing={isRefresh || false}
            onEndReached={() => _onLoadMore()}
            onEndReachedThreshold={0.1}
            renderItem={({item}) => GoodsListItem({navigation, item})}
          />
        </View>
      </View>

      {/* <Toast ref={toastEl} /> */}
      {/* <Loading ref={loadingEl} /> */}
      <Modal visible={isShow || false} transparent={true} animationType="fade">
        <View style={styles.version}>
          <View style={styles.versionCon}>
            <Text style={styles.versionTitle}>
              版本更新啦！优化使用体验更人性化！
            </Text>
            <Text style={styles.versionTitle}>立即更新</Text>
            <View style={styles.versionAllBtn}>
              {upgradeType == 0 ? (
                <TouchableOpacity
                  style={styles.versionBtn}
                  onPress={() => setIsShow(false)}>
                  <Text style={styles.versionBtnText}>忽略</Text>
                </TouchableOpacity>
              ) : null}
              <TouchableOpacity
                style={[styles.versionBtn, {borderRightWidth: 0}]}
                onPress={() => goUpgrade()}>
                <Text style={[styles.versionBtnText, {color: '#1876FF'}]}>
                  升级
                </Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>
      {/* <Button
        title="Go to GoodsDetails"
        onPress={() => navigation.navigate('GoodsDetails')}
      /> */}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    width: '100%',
    backgroundColor: '#fff',
    alignItems: 'center',
    flex: 1,
  },
  goBack: {
    width: pxToDp(150),
    height: pxToDp(100),
    justifyContent: 'center',
  },
  goBackImg: {
    width: pxToDp(18),
    height: pxToDp(32),
    marginLeft: pxToDp(30),
    tintColor: '#333',
  },
  headerTitle: {
    fontSize: pxToDp(36),
    color: '#333',
  },
  Home: {
    width: '100%',
    backgroundColor: '#fff',
    alignItems: 'center',
    flex: 1,
  },
  header: {
    marginTop: STATUSBAR_HEIGHT + pxToDp(20),
    height: pxToDp(64),
    width: pxToDp(690),
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  headText: {
    fontWeight: 'bold',
    color: '#333333',
    fontSize: pxToDp(40),
  },
  search: {
    width: pxToDp(555),
    height: pxToDp(64),
    flexDirection: 'row',
    alignItems: 'center',
    borderWidth: pxToDp(1),
    borderColor: 'rgba(0, 0, 0, 0.09)',
    borderRadius: pxToDp(30),
  },
  searchIcon: {
    marginLeft: pxToDp(40),
    width: pxToDp(33),
    height: pxToDp(33),
    marginRight: pxToDp(26),
  },
  Input: {
    fontSize: pxToDp(30),
    color: '#A6ABBB',
  },
  banner: {
    marginTop: pxToDp(50),
    width: pxToDp(690),
    height: pxToDp(240),
  },
  bannerImg: {
    width: pxToDp(690),
    height: pxToDp(240),
  },
  homeCon: {
    width: pxToDp(690),
    marginTop: pxToDp(60),
  },
  homeContent: {
    marginTop: pxToDp(30),
    width: pxToDp(690),
    height: height - pxToDp(600) - STATUSBAR_HEIGHT,
  },
  homeConTitle: {
    fontSize: pxToDp(34),
    color: '#333333',
    fontWeight: 'bold',
  },
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
  version: {
    width,
    height,
    backgroundColor: 'rgba(0,0,0,0.7)',
    alignItems: 'center',
    justifyContent: 'center',
  },
  versionCon: {
    position: 'relative',
    width: pxToDp(650),
    paddingTop: pxToDp(50),
    height: pxToDp(355),
    backgroundColor: '#fff',
    borderRadius: pxToDp(20),
    alignItems: 'center',
  },
  versionTitle: {
    width: pxToDp(650),
    textAlign: 'center',
    marginTop: pxToDp(20),
    fontSize: pxToDp(32),
    color: '#9494A0',
  },
  versionAllBtn: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    height: pxToDp(118),
    width: pxToDp(650),
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    borderTopWidth: pxToDp(1),
    borderTopColor: '#D1D1DA',
  },
  versionBtn: {
    width: pxToDp(325),
    alignItems: 'center',
    height: pxToDp(118),
    justifyContent: 'center',
    borderRightWidth: pxToDp(1),
    borderRightColor: '#D1D1DA',
  },
  versionBtnText: {
    fontSize: pxToDp(36),
    color: '#9494A0',
  },
});
