import wxpy

# 初始化机器人，扫码登陆
bot = wxpy.Bot()
# 搜索名称含有 "元宵大师" 的男性杭州好友
my_friend = bot.friends().search('alphazz3', sex=wxpy.MALE, city="杭州")[0]
my_friend.send("hello")
# my_friend.send_image('myplot.png') # 发送图片