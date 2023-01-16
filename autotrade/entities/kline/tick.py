from dataclasses import dataclass
from pandas import Timestamp
import pandas as pd
from datetime import datetime

from autotrade.common.constant import Exchange,Interval
from autotrade.api3.ctp_constant import THOST_FTDC_PT_Net
from autotrade.common.utils import generate_full_symbol, extract_full_symbol, generate_vt_symbol
from autotrade.entities.base_entity import BaseEntity

""" 期货
localtime (本机写入TICK的时间),
InstrumentID (合约名),
TradingDay (交易日),
ActionDay (业务日期),
UpdateTime （时间）,
UpdateMillisec（时间毫秒）,
LastPrice （最新价）,
Volume（成交量） ,
HighestPrice （最高价）,
LowestPrice（最低价） ,
OpenPrice（开盘价） ,
ClosePrice（收盘价）,
AveragePrice（均价）,
AskPrice1（申卖价一）,
AskVolume1（申卖量一）,
BidPrice1（申买价一）,
BidVolume1（申买量一）,
UpperLimitPrice（涨停板价）
LowerLimitPrice（跌停板价）
OpenInterest（持仓量）,
Turnover（成交金额）,
PreClosePrice (昨收盘),
PreOpenInterest (昨持仓),
PreSettlementPrice (上次结算价),
"""


@dataclass
class TickData(BaseEntity):
    """
    Tick data contains information about:
        * last trade in market
        * orderbook snapshot
        * intraday market statistics.
    """

    symbol: str = ""
    exchange: Exchange = Exchange.SHFE
    datetime: datetime = datetime(2019, 1, 1)

    name: str = ""
    volume: float = 0
    last_price: float = 0
    last_volume: float = 0
    limit_up: float = 0
    limit_down: float = 0

    open_price: float = 0
    high_price: float = 0
    low_price: float = 0
    pre_close: float = 0

    bid_price_1: float = 0
    bid_price_2: float = 0
    bid_price_3: float = 0
    bid_price_4: float = 0
    bid_price_5: float = 0

    ask_price_1: float = 0
    ask_price_2: float = 0
    ask_price_3: float = 0
    ask_price_4: float = 0
    ask_price_5: float = 0

    bid_volume_1: float = 0
    bid_volume_2: float = 0
    bid_volume_3: float = 0
    bid_volume_4: float = 0
    bid_volume_5: float = 0

    ask_volume_1: float = 0
    ask_volume_2: float = 0
    ask_volume_3: float = 0
    ask_volume_4: float = 0
    ask_volume_5: float = 0

    # StarQuant unique field
    depth: int = 0
    open_interest: float = 0

    def __post_init__(self):
        """"""

        self.vt_symbol = f"{self.symbol}.{self.exchange.value}"
        self.timestamp = Timestamp(self.datetime)
        self.full_symbol = generate_full_symbol(self.exchange, self.symbol)

    def deserialize(self, msg: str):
        try:
            v = msg.split('|')
            self.full_symbol = v[0]
            self.timestamp = pd.to_datetime(v[1])
            self.datetime = self.timestamp.to_pydatetime()
            self.symbol, self.exchange = extract_full_symbol(self.full_symbol)
            self.vt_symbol = generate_vt_symbol(self.symbol, self.exchange)
            self.last_price = float(v[2])
            self.volume = int(v[3])

            if (len(v) < 17):
                self.depth = 1
                self.bid_price_1 = float(v[4])
                self.bid_volume_1 = int(v[5])
                self.ask_price_1 = float(v[6])
                self.ask_volume_1 = int(v[7])
                self.open_interest = int(v[8])
                self.open_price = float(v[9])
                self.high_price = float(v[10])
                self.low_price = float(v[11])
                self.pre_close = float(v[12])
                self.limit_up = float(v[13])
                self.limit_down = float(v[14])
            else:
                self.depth = 5
                self.bid_price_1 = float(v[4])
                self.bid_volume_1 = int(v[5])
                self.ask_price_1 = float(v[6])
                self.ask_volume_1 = int(v[7])
                self.bid_price_2 = float(v[8])
                self.bid_volume_2 = int(v[9])
                self.ask_price_2 = float(v[10])
                self.ask_volume_2 = int(v[11])
                self.bid_price_3 = float(v[12])
                self.bid_volume_3 = int(v[13])
                self.ask_price_3 = float(v[14])
                self.ask_volume_3 = int(v[15])
                self.bid_price_4 = float(v[16])
                self.bid_volume_4 = int(v[17])
                self.ask_price_4 = float(v[18])
                self.ask_volume_4 = int(v[19])
                self.bid_price_5 = float(v[20])
                self.bid_volume_5 = int(v[21])
                self.ask_price_5 = float(v[22])
                self.ask_volume_5 = int(v[23])
                self.open_interest = int(v[24])
                self.open_price = float(v[25])
                self.high_price = float(v[26])
                self.low_price = float(v[27])
                self.pre_close = float(v[28])
                self.limit_up = float(v[29])
                self.limit_down = float(v[30])
        except Exception as e:
            print(e)
            pass

TickEntity = TickData