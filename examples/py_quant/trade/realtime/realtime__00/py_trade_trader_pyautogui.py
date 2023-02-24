import pyautogui
import time

# 获取基本信息
# 屏幕大小
size = pyautogui.size()
print(size)
# 鼠标位置
mouse_pos = pyautogui.position()
print(mouse_pos)
# 判断点是否在屏幕内
print(pyautogui.onScreen(100,100))

# 鼠标移动
size = pyautogui.size()
# 把鼠标移动到（10，10）的位置，周期1秒
pyautogui.moveTo(10,10,duration=1)
# 把鼠标移动到画面中央，周期0.5秒
pyautogui.moveTo(size.width/2,size.height/2,duration=0.5)
# 鼠标相对移动，周期1秒
pyautogui.moveRel(100,0,duration=1)

# 实时捕捉鼠标位置
last_pos = pyautogui.position()
try:
    while True:
        # 新位置
        new_pos = pyautogui.position()
        # 鼠标位于左上角时终止
        if new_pos == (0,0):
            break
        if new_pos != last_pos:
            print(new_pos)
            last_pos = new_pos
except KeyboardInterrupt:
    print('\n Exit.')

# 鼠标移动加点击
# 系统准备时间
time.sleep(2)
# 取得帮助菜单位置
help_pos =  pyautogui.locateOnScreen('help.png')
print(help_pos)
goto_pos = pyautogui.center(help_pos)
# 移动鼠标
pyautogui.moveTo(goto_pos,duration=1)
# 点击
pyautogui.click()
# 再移动鼠标
pyautogui.moveRel(0,650,duration=1)
# 再点击
pyautogui.click()

# 键盘输入
# 系统准备时间
time.sleep(2)
# 点击一次编译器
pyautogui.click(button='left')
# 输入[I like Python]
pyautogui.typewrite('I like Python')
# 输入回车，然后继续输入内容
pyautogui.typewrite('\nI like python too',0.25)
# 输入【good】，然后将头文字改为大写G，最后在行尾写个句号
pyautogui.typewrite(['enter','g','o','o','d','left','left','left','backspace','G','end','.','ctrl','w'],0.25)

# 组合键的处理
# 系统准备时间
time.sleep(2)
# 每个动作间隔0.5秒
pyautogui.PAUSE = 0.5
# pyautogui.FAILSAFE = True
# 记事本打出时间
pyautogui.press('f5')
# 打入三行内容
pyautogui.typewrite('\nhello')
pyautogui.typewrite('\nhello')
pyautogui.typewrite('\nhello')
# 按下Ctrl键
pyautogui.keyDown('ctrl')
# 按下a键，拷贝
pyautogui.press('a')
# 按下c键，复制
pyautogui.press('c')
# 松开ctrl键
pyautogui.keyUp('ctrl')
# 鼠标点击记事本下方
pyautogui.click(600,600)
# 输入两个空行
pyautogui.typewrite('\n\n')
# 粘贴
pyautogui.hotkey('ctrl','v')
