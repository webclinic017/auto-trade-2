import backtrader as bt
import pyautogui

class AutoGuiBroker(bt.brokers.BackBroker):
    ''' 
    '''
    def __init__(self):
        super().__init__()
        
        anchor_loc = pyautogui.locateCenterOnScreen('./loc_pic/anchor.png')
        assert(anchor_loc is not None)

        # calc button loc positions
        self.buy_but = (anchor_loc[0]-50,anchor_loc[1]+50)
        self.sell_but = (anchor_loc[0]-180,anchor_loc[1]+50)
        self.market_tab = (anchor_loc[0]-210,anchor_loc[1]+100)
        self.num_input = (anchor_loc[0]-50,anchor_loc[1]+175)
    
    def submit(self, order, check=True):
        super().submit(order, check)
        
        # click market anyway
        pyautogui.click(self.market_tab)
        size = str(abs(order.size))
        if 0==order.ordtype:
            # buy order
            pyautogui.click(self.buy_but)
            pyautogui.click(self.num_input)
            pyautogui.press('backspace',presses=5)
            pyautogui.write(size)
            pyautogui.press('enter')
        else:
            # sell order
            pyautogui.click(self.sell_but)
            pyautogui.click(self.num_input)
            pyautogui.press('backspace',presses=5)
            pyautogui.write(size)
            pyautogui.press('enter')
