#import time
#from collections import deque
from datetime import datetime

import backtrader as bt
from backtrader.feed import DataBase
from backtrader.utils.py3 import queue, with_metaclass

from .akdatastore import AKDataStore

class MetaAkDataFeed(DataBase.__class__):
    def __init__(cls, name, bases, dct):
        '''Class has already been created ... register'''
        # Initialize the class
        super(MetaAkDataFeed, cls).__init__(name, bases, dct)

        # Register with the store
        AKDataStore.DataCls = cls

class AkDataFeed(with_metaclass(MetaAkDataFeed, DataBase)):
    """
    Akshare data Trading Library Data Feed.
    Params:
      - ``historical`` (default: ``False``)
        If set to ``True`` the data feed will stop after doing the first
        download of data.
        The standard data feed parameters ``fromdate`` and ``todate`` will be
        used as reference.
      - ``backfill_start`` (default: ``True``)
        Perform backfilling at the start. The maximum possible historical data
        will be fetched in a single request.

    Changes From Ed's pacakge

        - Added option to send some additional fetch_ohlcv_params. Some exchanges (e.g Bitmex)
          support sending some additional fetch parameters.
        - Added drop_newest option to avoid loading incomplete candles where exchanges
          do not support sending ohlcv params to prevent returning partial data

    """

    params = (
        ('historical', False),      # only historical download
        ('backfill_start', False),  # do backfilling at the start
        ('fetch_ohlcv_params', {}),
        ('ohlcv_limit', 20),
        ('drop_newest', False),
        ('debug', False)
    )

    _store = AKDataStore
    _use_utc = False

    # States for the Finite State Machine in _load
    _ST_LIVE, _ST_HISTORBACK, _ST_OVER = range(3)

    # def __init__(self, exchange, symbol, ohlcv_limit=None, config={}, retries=5):
    def __init__(self, **kwargs):
        # self.store = CCXTStore(exchange, config, retries)
        self.store = self._store(**kwargs)
        self._data = queue.Queue()  # data queue for price data
        self._last_id = ''          # last processed trade id for ohlcv
        self._last_ts = self.utc_to_ts(datetime.utcnow()) if self._use_utc else datetime.now().timestamp() # last processed timestamp for ohlcv
        self._last_update_bar_time = 0

    def utc_to_ts(self, dt):
        fromdate = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute)
        epoch = datetime(1970, 1, 1)
        return int((fromdate - epoch).total_seconds() * 1000)

    def start(self, ):
        DataBase.start(self)
        if self.p.fromdate:
            self._state = self._ST_HISTORBACK
            self.put_notification(self.DELAYED)
            self._update_bar(self.p.fromdate)
        else:
            self._state = self._ST_LIVE
            self.put_notification(self.LIVE)

    def _load(self):
        """ 
        return True  代表从数据源获取数据成功
        return False 代表因为某种原因(比如历史数据源全部数据已经输出完毕)数据源关闭
        return None  代表暂时无法从数据源获取最新数据,但是以后会有(比如实时数据源中最新的bar还未生成) 
        """
        if self._state == self._ST_OVER:
            return False
        #
        while True:
            if self._state == self._ST_LIVE:
                #===========================================
                # 其实这段代码最好放到独立的工作线程中做,这里纯粹偷懒
                # 每隔一分钟就更新一次bar
                nts = datetime.now().timestamp()
                if nts - self._last_update_bar_time > 60:
                    self._last_update_bar_time = nts
                    self._update_bar(livemode=True)
                #===========================================
                return self._load_bar()
            elif self._state == self._ST_HISTORBACK:
                ret = self._load_bar()
                if ret:
                    return ret
                else:
                    # End of historical data
                    if self.p.historical:  # only historical
                        self.put_notification(self.DISCONNECTED)
                        self._state = self._ST_OVER
                        return False  # end of historical
                    else:
                        self._state = self._ST_LIVE
                        self.put_notification(self.LIVE)
                        continue

    def _update_bar(self, fromdate=None, livemode=False):
        """Fetch OHLCV data into self._data queue"""
        #想要获取哪个时间粒度下的bar
        tf = self.store.get_timeframe(self._timeframe, self._compression)
        #从哪个时间点开始获取bar
        if fromdate:
            self._last_ts = self.utc_to_ts(fromdate) 
            # if self._use_utc else datetime.now()
        #每次获取bar数目的最高限制
        limit = max(3, self.p.ohlcv_limit) #最少不能少于三个,原因:每次头bar时间重复要忽略,尾bar未完整要去掉,只保留中间的,所以最少三个
        #
        while True:
            #先获取数据长度
            dlen = self._data.qsize()
            #
            bars = sorted(self.store.fetch_ohlcv(self.p.dataname, timeframe=tf, since=self._last_ts, limit=limit, params=self.p.fetch_ohlcv_params))
            # Check to see if dropping the latest candle will help with
            # exchanges which return partial data
            if self.p.drop_newest and len(bars) > 0:
                del bars[-1]
            #
            for bar in bars:
                #获取的bar不能有空值
                if None in bar:
                    continue
                #bar的时间戳
                tstamp = bar[0]
                #通过时间戳判断bar是否为新的bar
                if tstamp > self._last_ts:
                    self._data.put(bar) #将新的bar保存到队列中
                    self._last_ts = tstamp
                    #print(datetime.utcfromtimestamp(tstamp//1000))
            #如果数据长度没有增长,那证明已经是当前最后一根bar,退出
            if dlen == self._data.qsize():
                break
            #实时模式下,就没必须判断是否是最后一根bar,减少网络通信
            if livemode:
                break

    def _load_bar(self):
        try:
            bar = self._data.get(block=False) #不阻塞
        except queue.Empty:
            return None  # no data in the queue
        tstamp, open_, high, low, close, volume = bar
        dtime = datetime.utcfromtimestamp(tstamp // 1000)
        self.lines.datetime[0] = bt.date2num(dtime)
        self.lines.open[0] = open_
        self.lines.high[0] = high
        self.lines.low[0] = low
        self.lines.close[0] = close
        self.lines.volume[0] = volume
        return True

    def haslivedata(self):
        return self._state == self._ST_LIVE and not self._data.empty()

    def islive(self):
        return not self.p.historical