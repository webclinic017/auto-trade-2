# app zhongli agent

## React Native 环境

- version: 0.67.4
- https://reactjs.org/docs/hooks-intro.html
- https://github.com/facebook/react-native
- https://www.reactnative.express/app/navigation
- https://reactnative.cn/docs/environment-setup

```bash
# 环境搭建
brew install node
brew install watchman

# 使用nrm工具切换淘宝源
npx nrm use taobao

# 如果之后需要切换回官方源可使用
npx nrm use npm

# yarn
npm install -g yarn

# jdk
brew install adoptopenjdk/openjdk/adoptopenjdk11

# Android 开发环境
# 1. 安装 Android Studio
# 2. 安装 Android SDK
# 3. 配置 ANDROID_HOME 环境变量

# vi ~/.zshrc
# 如果你不是通过Android Studio安装的sdk，则其路径可能不同，请自行确定清楚
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/emulator
export PATH=$PATH:$ANDROID_HOME/tools
export PATH=$PATH:$ANDROID_HOME/tools/bin
export PATH=$PATH:$ANDROID_HOME/platform-tools

# 创建新项目

npx react-native init app_zhongli_agent

# npx react-native init AwesomeProject --version 0.67.4
# npx react-native init AwesomeTSProject --template react-native-template-typescript

# 准备真机

# 编译并运行 React Native 应用
cd app_zhongli_agent
yarn android
# 或者
yarn react-native run-android

# 可能遇到 Android 依赖下载问题，
# 可以开代理
# 也可以尝试阿里云提供的 maven 镜像，
# 将 android/build.gradle 中的 jcenter() 和 google() 分别替换为
# maven { url 'https://maven.aliyun.com/repository/jcenter' }
# 和
# maven { url 'https://maven.aliyun.com/repository/google' }
#（注意有多处需要替换）

# 修改项目
# 现在你已经成功运行了项目，我们可以开始尝试动手改一改了：

# 使用你喜欢的文本编辑器打开 App.js 并随便改上几行
# 按两下 R 键，或是在开发者菜单中选择 Reload，就可以看到你的最新修改。

```

## 项目依赖

```
# https://juejin.cn/post/6970581257973399559
# https://www.jianshu.com/p/4ca887e45bc7

yarn add react-native-elements

yarn add react-native-vector-icons
npx react-native link react-native-vector-icons

yarn add react-native-safe-area-context
npx react-native link react-native-safe-area-context
npx react-native unlink react-native-safe-area-context

yarn add react-native-screens

# 路由及底部菜单栏 React Navigation
yarn add @react-navigation/bottom-tabs

yarn add @react-navigation/native
yarn add @react-navigation/native-stack
yarn add @react-navigation/stack

yarn add react-native-gesture-handler
npx react-native unlink react-native-gesture-handler
yarn add react-native-swiper
yarn add react-navigation

// https://blog.logrocket.com/using-axios-react-native-manage-api-requests/
yarn add axios

yarn add react-native-webview

# https://github.com/arnnis/react-native-toast-notifications#demo
yarn add react-native-toast-notifications

# 图片上传 ，支持图片裁切
yarn add react-native-image-crop-picker 

# 图片预览功能
# yarn add react-native-image-zoom-viewer

# rn 渐变色
yarn add react-native-linear-gradient

yarn add react-native-picker
yarn add react-native-image-picker
yarn add react-native-qrcode-svg
yarn add react-native-video
# yarn add react-native-video-controls
yarn add react-native-svg
yarn add react-native-view-shot

yarn add react-native-md5

yarn add react-redux
yarn add redux
yarn add redux-thunk

# rn操作storage
yarn add @react-native-async-storage/async-storage

# 获取设备唯一的id 啥的功能
yarn add react-native-device-info
```

## 状态管理

仅使用 React hooks 和 Context 管理应用状态：https://segmentfault.com/a/1190000020808696

## 页面

- 首页 HomeTab
    - 首页 Home
      - 商品详情 GoodsDetails
      - 确认订单 ConfirmOrder
    - 订单 Order
      - 资产收益 AssetIncome
      - 签署合同 Modal SignContrctModel
        - 义务合同 ObligatoryContract
        - 委托运营协议 ProxyAgreement
    - 我的 Mine
      - 实名认证：个人认证
      - 陪护系统结算
      - 智慧病房结算
      - 银行卡
      - 推荐好友：只有代理商才展示
      - 修改信息
      - 代理收益：只有代理商才展示
      - 登录，注册，修改密码
    - 发现
      - 图文广告
      - 新闻公告
      - 视频
      - 产品出售（暂定）