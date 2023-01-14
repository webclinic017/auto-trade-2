from dataclasses import dataclass,field
from datetime import datetime
from typing import Any

from autotrade.common.constant import (ACTIVE_STATUSES, Direction, Exchange, 
Offset, OrderFlag, OrderStatus, OrderType, Status,Interval, StopOrderStatus,
SYMBOL_TYPE,ORDERFALG_2VT, ORDERSTATUS_2VT)
from autotrade.common.utils import extract_full_symbol, generate_vt_symbol
from autotrade.entities.base_entity import BaseEntity




@dataclass
class OrderEntity(BaseEntity):
    """
    Order data contains information for tracking lastest status 
    of a specific order.
    """

    symbol: str = ""
    exchange: Exchange = Exchange.SHFE
    orderid: str = ""

    type: OrderType = OrderType.LMT
    direction: Direction = Direction.LONG
    offset: Offset = Offset.NONE
    price: float = 0
    volume: int = 0
    traded: int = 0
    status: Status = Status.SUBMITTING
    time: str = ""

# StarQuant unique field
    api: str = ""
    account: str = ""
    clientID: int = -1
    client_order_id: int = -1
    tag: str = ""

    full_symbol: str = ""
    flag: OrderFlag = OrderFlag.OPEN
    server_order_id: int = -1
    broker_order_id: int = -1
    orderNo: str = ""
    localNo: str = ""
    create_time: str = ""
    update_time: str = ""
    orders_status: OrderStatus = OrderStatus.SUBMITTED
    orderfield: Any = None

    def __post_init__(self):
        """"""
        if self.full_symbol:
            self.symbol, self.exchange = extract_full_symbol(self.full_symbol)
        self.vt_symbol = f"{self.symbol}.{self.exchange.value}"
        self.vt_orderid = f"{self.gateway_name}.{self.orderid}"
        self.tag = str(self.type.value)

    def is_active(self):
        """
        Check if the order is active.
        """
        if self.status in ACTIVE_STATUSES:
            return True
        else:
            return False

    def create_cancel_request(self):
        """
        Create cancel request object from order.
        """
        req = CancelRequest(
            clientID=self.clientID,
            client_order_id=self.client_order_id,
            server_order_id=self.server_order_id
        )
        return req

    def deserialize(self, msg: str):
        v = msg.split('|')
        try:
            self.api = v[0]
            self.account = v[1]
            self.clientID = int(v[2])
            self.client_order_id = int(v[3])
            self.tag = v[4]
            self.type = OrderType(int(v[4].split(':')[0]))
            self.full_symbol = v[5]
            self.symbol, self.exchange = extract_full_symbol(self.full_symbol)
            self.vt_symbol = generate_vt_symbol(self.symbol, self.exchange)
            self.price = float(v[6])
            self.volume = int(v[7])
            if self.volume < 0:
                self.direction = Direction.SHORT
                self.volume = -1 * self.volume
            self.traded = abs(int(v[8]))
            self.flag = OrderFlag(int(v[9]))
            self.offset = ORDERFALG_2VT[self.flag]
            self.server_order_id = int(v[10])
            self.broker_order_id = int(v[11])
            self.orderNo = v[12]
            self.localNo = v[13]
            self.orderid = self.localNo
            self.vt_orderid = f"{self.gateway_name}.{self.orderid}"
            self.create_time = v[14]
            self.update_time = v[15]
            self.time = self.update_time
            self.order_status = OrderStatus(int(v[16]))
            self.status = ORDERSTATUS_2VT[self.order_status]
        except Exception as e:
            print(e)
            pass

    def serialize(self):
        msg = str(self.api
                  + '|' + self.account
                  + '|' + str(self.clientID)
                  + '|' + str(self.client_order_id)
                  + '|' + self.tag)
        if (self.orderfield):
            msg = msg + '|' + self.orderfield.serialize()
        return msg

@dataclass
class CtpOrderField(object):

    InstrumentID: str = ''
    OrderPriceType: str = ''
    Direction: str = ''
    CombOffsetFlag: str = ''
    CombHedgeFlag: str = ''
    LimitPrice: float = 0.0
    VolumeTotalOriginal: int = 0
    TimeCondition: str = ''
    GTDDate: str = ''
    VolumeCondition: str = ''
    MinVolume: int = 0
    ContingentCondition: str = ''
    StopPrice: float = 0.0
    ForceCloseReason: str = '0'
    IsAutoSuspend: int = 0
    UserForceClose: int = 0
    IsSwapOrder: int = 0
    BusinessUnit: str = ''
    CurrencyID: str = ''

    def serialize(self):
        msg = str(self.InstrumentID
                  + '|' + self.OrderPriceType
                  + '|' + self.Direction
                  + '|' + self.CombOffsetFlag
                  + '|' + self.CombHedgeFlag
                  + '|' + str(self.LimitPrice)
                  + '|' + str(self.VolumeTotalOriginal)
                  + '|' + self.TimeCondition
                  + '|' + self.GTDDate
                  + '|' + self.VolumeCondition
                  + '|' + str(self.MinVolume)
                  + '|' + self.ContingentCondition
                  + '|' + str(self.StopPrice)
                  + '|' + self.ForceCloseReason
                  + '|' + str(self.IsAutoSuspend)
                  + '|' + str(self.UserForceClose)
                  + '|' + str(self.IsSwapOrder)
                  + '|' + self.BusinessUnit
                  + '|' + self.CurrencyID)
        return msg


@dataclass
class PaperOrderField(object):

    order_type: OrderType = OrderType.MKT
    full_symbol: str = ''
    order_flag: OrderFlag = OrderFlag.OPEN
    limit_price: float = 0.0
    stop_price: float = 0.0
    order_size: int = 0

    def serialize(self):
        msg = str(str(self.order_type.value)
                  + '|' + self.full_symbol
                  + '|' + str(self.order_flag.value)
                  + '|' + str(self.order_size)
                  + '|' + str(self.limit_price)
                  + '|' + str(self.stop_price))
        return msg

@dataclass
class SubscribeRequest:
    """
    subscribe
    """
    sym_type: SYMBOL_TYPE = SYMBOL_TYPE.FULL
    content: str = ''

    def serialize(self):
        msg = str(self.sym_type.value) + '|' + self.content
        return msg


@dataclass
class CancelRequest:
    """
    Request sending to specific gateway for canceling an existing order.
    """
    clientID: int = 0
    client_order_id: int = 0
    server_order_id: int = 0

    def serialize(self):
        msg = str(self.clientID) + '|' + str(self.client_order_id) + \
            '|' + str(self.server_order_id)
        return msg


OrderRequest = OrderEntity
OrderCancelRequest = CancelRequest
CancelAllRequest = SubscribeRequest

@dataclass
class StopOrder:
    full_symbol: str
    direction: Direction
    offset: Offset
    price: float
    volume: float
    stop_orderid: str
    strategy_name: str
    lock: bool = False
    vt_orderids: list = field(default_factory=list)
    status: StopOrderStatus = StopOrderStatus.WAITING

@dataclass
class HistoryRequest:
    """
    Request sending to specific gateway for querying history data.
    """

    symbol: str
    exchange: Exchange
    start: datetime
    end: datetime = None
    interval: Interval = None

    def __post_init__(self):
        """"""
        self.vt_symbol = f"{self.symbol}.{self.exchange.value}"