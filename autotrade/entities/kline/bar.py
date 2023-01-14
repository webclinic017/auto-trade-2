from dataclasses import dataclass
import pandas as pd
from datetime import datetime

from autotrade.common.constant import Exchange,Interval
from autotrade.api3.ctp_constant import THOST_FTDC_PT_Net
from autotrade.common.utils import generate_full_symbol, extract_full_symbol, generate_vt_symbol
from autotrade.entities.base_entity import BaseEntity



@dataclass
class BarEntity(BaseEntity):
    """
    Candlestick bar data of a certain trading period.
    """

    symbol: str = ''
    exchange: Exchange = Exchange.SHFE
    datetime: datetime = datetime(2019, 1, 1)

    interval: Interval = None
    volume: float = 0
    open_price: float = 0
    high_price: float = 0
    low_price: float = 0
    close_price: float = 0

    adj_close_price: float = 0.0
    open_interest: int = 0

    def __post_init__(self):
        """"""
        self.vt_symbol = f"{self.symbol}.{self.exchange.value}"
        self.full_symbol = generate_full_symbol(self.exchange, self.symbol)
        self.bar_start_time = pd.Timestamp(self.datetime)