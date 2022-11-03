import React, {Component} from 'react';
import {
  View,
  Image,
  Dimensions,
  Modal,
  Text,
  ActivityIndicator,
  StyleSheet,
} from 'react-native';
import pxToDp from '../utils/todp';
const {width, height} = Dimensions.get('window'); //获取手机的宽和高

const styles = StyleSheet.create({
  loadingCon: {
    width: '100%',
    height: '100%',
    backgroundColor: 'rgba(0,0,0,0.4)',
    alignItems: 'center',
    justifyContent: 'center',
  },
});

export default class RealName extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isShow: false,
    };
  }
  componentDidMount() {}
  componentWillUnmount() {}
  show() {
    this.setState({isShow: true});
  }
  hide() {
    this.setState({isShow: false});
  }
  render() {
    return (
      <Modal
        visible={this.state.isShow}
        transparent={true}
        animationType="fade">
        <View style={styles.loadingCon}>
          <ActivityIndicator
            size="large"
            color="#fff"
            hidesWhenStopped={false}
          />
        </View>
      </Modal>
    );
  }
}
