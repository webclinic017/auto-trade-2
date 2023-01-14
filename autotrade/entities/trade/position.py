from dataclasses import dataclass
from datetime import datetime
from typing import Any

from autotrade.common.constant import (ACTIVE_STATUSES, Direction, Exchange, 
Offset, OrderFlag, OrderStatus, OrderType, Status,Interval,
SYMBOL_TYPE,ORDERFALG_2VT, ORDERSTATUS_2VT,DIRECTION_CTP2VT)
from autotrade.common.utils import extract_full_symbol, generate_vt_symbol
from autotrade.entities.base_entity import BaseEntity

@dataclass
class PositionData(BaseEntity):
    """
    Positon data is used for tracking each individual position holding.
    """

    symbol: str = ""
    exchange: Exchange = Exchange.SHFE
    direction: Direction = Direction.LONG

    volume: float = 0
    frozen: float = 0
    price: float = 0
    pnl: float = 0
    yd_volume: float = 0
# StarQuant field
    key: str = ""
    account: str = ""
    api: str = ""
    full_symbol: str = ""
    realized_pnl: float = 0
    timestamp: str = ""

    def __post_init__(self):
        """"""
        self.vt_symbol = f"{self.symbol}.{self.exchange.value}"
        self.vt_positionid = f"{self.vt_symbol}.{self.direction}"

    def deserialize(self, msg: str):
        v = msg.split('|')
        try:
            self.key = v[0]
            self.account = v[1]
            self.api = v[2]
            self.full_symbol = v[3]
            self.symbol, self.exchange = extract_full_symbol(self.full_symbol)
            self.vt_symbol = f"{self.symbol}.{self.exchange.value}"
            self.direction = DIRECTION_CTP2VT[v[4]]
            self.price = float(v[5])
            self.vt_positionid = f"{self.vt_symbol}.{self.direction}"
            self.volume = abs(int(v[6]))
            self.yd_volume = abs(int(v[7]))
            self.freezed_size = abs(int(v[8]))
            self.realized_pnl = float(v[9])
            self.pnl = float(v[10])
            self.timestamp = v[11]
        except Exception as e:
            print(e)
            pass

PositionEntity = PositionData