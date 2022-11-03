## 属性分类

### 1.宽高

```
width  //宽
height //高
```

### 2.背景颜色(backgroundColor)

```
backgroundColor
opacity //透明度
```

### 3.边框(border)

```
//边框圆角设置
borderTopLeftRadius  //左上角圆角
borderTopRightRadius //右上角的圆角
borderBottomLeftRadius //左下角的圆角
borderBottomRightRadius //右下角的圆角
borderRadius //所有角的圆角

//边框宽度
borderLeftWidth  //左边边框宽度
borderRightWidth //右边边框宽度
borderTopWidth //顶部边框宽度
borderBottomWidth //底部边框宽度
borderWidth  //所有边框宽度

//边框颜色
borderColor //边框颜色
```

### 4.外边距(margin)

```
marginBottom  //距下外边距
marginLeft  //距左外边距
marginRight  //距右外边距
marginTop  //距上外边距
marginVertical  //垂直外边距(也就是距上,距下边距)
marginHorizontal //水平外边距(距左,距右边距)
margin //所有边距
```

### 5.内边距

paddingBottom  //距下内边距
paddingLeft  //距左内边距
paddingRight  //距右内边距
paddingTop  //距上内边距
paddingVertical//垂直内边距
paddingHorizontal  //水平内边距
padding //所有内边距

### 6.文字

```
color  //文字颜色
textAlign  //对其方式 ('left','right','auto','center','justify')
fontSize //字体大小
fontStyle //字体风格 正常:'normal', 斜体:'italic'
fontWeight //字体粗细 加粗:'bold', '100', '200' 
letterSpacing //字符间距
lineHeight //行间距
textDecorationLine //字体装饰线 下划线:'underline', 删除线:'line-through',下划线删除线:'underline line-through'
textDecorationStyle //字体装饰线风格 单线:'solid' 双线:'double' 虚线:'dotted','dashed'
textDecorationColor //字体装饰线颜色
```

### 7.图像

```
//图像变换
scaleX //水平方向缩放
scaleY //垂直方向缩放
rotation //旋转
translateX //水平方向平移
translateY //水平方向平移
resizemode  //拉伸图片 'cover' ,'strech','contain'
```
## 属性简单测试

测试demo
设置样式部分代码

```
const styles1 = StyleSheet.create({
//最外层View  
superView: {    
  justifyContent: 'center',   
  backgroundColor: 'red',    
  width: 300,    
  height: 400,    
  alignItems:'center',    
  margin:50  },  
//顶部View  
topView: {    
  backgroundColor: 'green',    
  width: 200,    
  height: 250,    
  marginTop:20,   
  borderWidth:2,    
  borderTopLeftRadius:30,    
  borderColor:'cyan',    
  alignItems:'center'  
},  
//底部View  
bottomView: {    
  backgroundColor: 'blue',    
  width: 200,    
  height: 100,    
  margin: 10 
},  
//底部View的文字样式  
bottomText:{    
  backgroundColor:'gray',    
  margin:10,    
  padding: 10,    
  color:'black',    
  textAlign:'justify',    
  fontSize:18,    
  fontStyle:'italic',    
  fontWeight:'100',    
  letterSpacing:2,    
  lineHeight:20,    
  textDecorationLine:'underline',    
  textDecorationStyle:'dashed',    
  textDecorationColor:'yellow'  },  
//图片样式  
imageStyle:{    
  width:100,    
  height:100,    
  borderRadius:20,    
  opacity:0.7  
}
});
```