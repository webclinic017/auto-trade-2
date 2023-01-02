import pyautogui
import time

op = pyautogui.confirm('Buy or Sell?', buttons=['Buy','Sell'])

anchor_loc = pyautogui.locateCenterOnScreen('./loc_pic/anchor.png')
if anchor_loc is None:
    print('anchor not found!')
    exit()

print('anchor loc:{}'.format(anchor_loc))
# calc button loc positions

buy_but = (anchor_loc[0]-50,anchor_loc[1]+50)
sell_but = (anchor_loc[0]-180,anchor_loc[1]+50)
market_tab = (anchor_loc[0]-210,anchor_loc[1]+100)
num_input = (anchor_loc[0]-50,anchor_loc[1]+175)

# get focus first
pyautogui.click(anchor_loc)
print('get focus first')
pyautogui.click(market_tab)
print('market clicked')

if op=='Buy':
    pyautogui.click(buy_but)
    print('buy clicked')
    pyautogui.click(num_input)
    pyautogui.press('backspace',presses=3)
    pyautogui.write('1')
    pyautogui.press('enter')

elif op=='Sell':
    pyautogui.click(sell_but)
    print('sell clicked')
    pyautogui.click(num_input)
    pyautogui.press('backspace',presses=3)
    pyautogui.write('1')
    pyautogui.press('enter')
