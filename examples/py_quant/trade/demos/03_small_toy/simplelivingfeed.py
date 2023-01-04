import backtrader as bt
import requests
import datetime
import time

class SimpleLivingData(bt.feed.DataBase):
    params = (
        ('sleeptime', 10),
        ('symbol', 'ixic'),
    )
    
    def __init__(self, symbol, **kwargs):
        '''symbol: ixic hkHSI'''
        super().__init__(**kwargs)
        
        self.symbol = symbol
        
        # used to stop feed when no more new data from web
        self.last_dt = datetime.datetime.now()
        
    def start(self):
        super().start()
        # add filter adjust time
        self.resample(timeframe=self.p.timeframe, compression=self.p.compression)

    def stop(self):
        pass
    
    def islive(self):
        ''' tell cerebro this is a living feed'''
        return True

    def _load(self):
        # request data
        msg = self._req_data()
        if msg is None:
            # No more data
            return False
        
        # fill the lines
        self.lines.datetime[0] = self.date2num(msg['datetime'])
        self.lines.open[0] = msg['open']
        self.lines.high[0] = msg['high']
        self.lines.low[0] = msg['low']
        self.lines.close[0] = msg['close']
        self.lines.volume[0] = msg['volume']
        self.lines.openinterest[0] = -1

        # Say success
        return True

    
    def _req_data(self):
        '''internal function used to request data from the web
            base on the self.symbol it will fetch different data source'''
        
        # sleep some time
        time.sleep(self.p.sleeptime)
        
        msg = dict()
        if self.symbol == 'ixic':
            # ixic
            ret = requests.get('https://hq.sinajs.cn/list=gb_ixic')
            lstr = ret.text.split(',')

            dt = datetime.datetime.strptime(lstr[3],'%Y-%m-%d %H:%M:%S')
            if self.last_dt == dt:
                return None
            else:
                self.last_dt = dt
            msg['datetime'] = dt
            msg['open'] = float(lstr[5])
            msg['high'] = float(lstr[6])
            msg['low'] = float(lstr[7])
            msg['close'] = float(lstr[1])
            msg['volume'] = int(lstr[10])
            
        elif self.symbol == 'hkHSI':
            # hkHSI
            ret = requests.get('https://hq.sinajs.cn/list=rt_hkHSI')
            lstr = ret.text.split(',')
            
            dt = datetime.datetime.strptime(lstr[17]+' '+lstr[18], '%Y/%m/%d %H:%M:%S')
            if self.last_dt == dt:
                return None
            else:
                self.last_dt = dt
            msg['datetime'] = dt
            msg['open'] = float(lstr[2])
            msg['high'] = float(lstr[4])
            msg['low'] = float(lstr[5])
            msg['close'] = float(lstr[6])
            msg['volume'] = int(float(lstr[11]))
        
        return msg
        