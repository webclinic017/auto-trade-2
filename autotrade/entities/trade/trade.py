from dataclasses import dataclass
from datetime import datetime
from typing import Any

from autotrade.common.constant import (ACTIVE_STATUSES, Direction, Exchange, 
Offset, OrderFlag, OrderStatus, OrderType, Status,Interval,
SYMBOL_TYPE,ORDERFALG_2VT, ORDERSTATUS_2VT)
from autotrade.common.utils import extract_full_symbol, generate_vt_symbol
from autotrade.entities.base_entity import BaseEntity

@dataclass
class TradeData(BaseEntity):
    """
    Trade data contains information of a fill of an order. One order
    can have several trade fills.
    """

    symbol: str = ""
    exchange: Exchange = Exchange.SHFE
    orderid: str = ""
    tradeid: str = ""
    direction: Direction = ""

    offset: Offset = Offset.NONE
    price: float = 0
    volume: float = 0
    time: str = ""

# StarQuant field
    server_order_id: int = -1
    client_order_id: int = -1
    clientID: int = -1
    localNo: str = ""
    orderNo: str = ""
    full_symbol: str = ""
    fill_flag: OrderFlag = OrderFlag.OPEN
    commission: float = 0.0
    account: str = ""
    api: str = ""

    datetime: datetime = datetime(1990, 1, 1)

# Backtest use
    commission: float = 0.0
    slippage: float = 0.0
    turnover: float = 0.0
    long_pos: int = 0
    long_price: float = 0
    long_pnl: float = 0
    short_pos: int = 0
    short_price: float = 0
    short_pnl: float = 0

    def __post_init__(self):
        """"""
        self.vt_symbol = f"{self.symbol}.{self.exchange.value}"
        self.vt_orderid = f"{self.gateway_name}.{self.orderid}"
        self.vt_tradeid = f"{self.gateway_name}.{self.tradeid}"

    def deserialize(self, msg: str):
        v = msg.split('|')
        try:
            self.server_order_id = int(v[0])
            self.client_order_id = int(v[1])
            self.clientID = int(v[2])
            self.localNo = v[3]
            self.orderid = self.localNo
            self.vt_orderid = f"{self.gateway_name}.{self.orderid}"
            self.orderNo = v[4]
            self.tradeid = v[5]
            self.vt_tradeid = f"{self.gateway_name}.{self.tradeid}"
            self.time = v[6]
            self.full_symbol = v[7]
            self.symbol, self.exchange = extract_full_symbol(self.full_symbol)
            self.vt_symbol = f"{self.symbol}.{self.exchange.value}"

            self.price = float(v[8])
            quantity = int(v[9])
            self.volume = abs(quantity)
            self.direction = Direction.LONG if quantity > 0 else Direction.SHORT
            self.fill_flag = OrderFlag(int(v[10]))
            self.offset = ORDERFALG_2VT[self.fill_flag]

            self.commission = float(v[11])
            self.account = v[12]
            self.api = v[13]
        except Exception as e:
            print(e)
            pass

TradeEntity = TradeData
BacktestTradeData = TradeData
BacktestTradeEntity = TradeData