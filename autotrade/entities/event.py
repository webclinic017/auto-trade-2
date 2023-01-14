from pandas import Timestamp
import pandas as pd
from dataclasses import dataclass, field
from datetime import datetime
from logging import INFO
from typing import Any, Callable

from autotrade.common.constant import (EventType, MSG_TYPE, Exchange, Interval,
                       OrderType, Direction, Offset, Status, OrderFlag, OrderStatus, ACTIVE_STATUSES, StopOrderStatus,
                       DIRECTION_CTP2VT, ORDERFALG_2VT, ORDERSTATUS_2VT,
                       Product, OptionType, SYMBOL_TYPE,
                       OPTIONTYPE_CTP2VT, PRODUCT_CTP2VT, PRODUCT_VT2SQ, EXCHANGE_CTP2VT)
from ..api3.ctp_constant import THOST_FTDC_PT_Net
from autotrade.common.utils import generate_full_symbol, extract_full_symbol, generate_vt_symbol

from autotrade.entities.kline.tick import TickEntity
from autotrade.entities.kline.bar import BarEntity
from autotrade.entities.trade.order import OrderEntity
from autotrade.entities.trade.position import PositionEntity
from autotrade.entities.trade.trade import TradeEntity
from autotrade.entities.trade.contract import ContractEntity
from autotrade.entities.trade.account import AccountEntity
from autotrade.entities.log import LogEntity

class Event(object):
    """
    Base Event class for event-driven system
    """

    def __init__(self,
                 type: EventType = EventType.HEADER,
                 data: Any = None,
                 des: str = '',
                 src: str = '',
                 msgtype: MSG_TYPE = MSG_TYPE.MSG_TYPE_BASE
                 ):

        self.event_type = type
        self.data = data
        self.destination = des
        self.source = src
        self.msg_type = msgtype

    @property
    def type(self):
        return self.event_type.name

    def serialize(self):
        msg = self.destination + '|' + self.source + \
            '|' + str(self.msg_type.value)
        if self.data:
            if type(self.data) == str:
                msg = msg + '|' + self.data
            else:
                try:
                    msg = msg + '|' + self.data.serialize()
                except Exception as e:
                    print(e)
                    pass
        return msg

    def deserialize(self, msg: str):
        v = msg.split('|', 3)
        try:
            self.destination = v[0]
            self.source = v[1]
            msg2type = MSG_TYPE(int(v[2]))
            if msg2type in [MSG_TYPE.MSG_TYPE_TICK, MSG_TYPE.MSG_TYPE_TICK_L1, MSG_TYPE.MSG_TYPE_TICK_L5]:
                self.event_type = EventType.TICK
                self.data = TickEntity(gateway_name=self.source)
                self.data.deserialize(v[3])
            elif msg2type == MSG_TYPE.MSG_TYPE_RTN_ORDER:
                self.event_type = EventType.ORDERSTATUS
                self.data = OrderEntity(gateway_name=self.source)
                self.data.deserialize(v[3])
            elif msg2type == MSG_TYPE.MSG_TYPE_RTN_TRADE:
                self.event_type = EventType.FILL
                self.data = TradeEntity(gateway_name=self.source)
                self.data.deserialize(v[3])
            elif msg2type == MSG_TYPE.MSG_TYPE_RSP_POS:
                self.event_type = EventType.POSITION
                self.data = PositionEntity(gateway_name=self.source)
                self.data.deserialize(v[3])
            elif msg2type == MSG_TYPE.MSG_TYPE_BAR:
                self.event_type = EventType.BAR
                self.data = BarEntity(gateway_name=self.source)
                self.data.deserialize(v[3])
            elif msg2type == MSG_TYPE.MSG_TYPE_RSP_ACCOUNT:
                self.event_type = EventType.ACCOUNT
                self.data = AccountEntity(gateway_name=self.source)
                self.data.deserialize(v[3])
            elif msg2type == MSG_TYPE.MSG_TYPE_RSP_CONTRACT:
                self.event_type = EventType.CONTRACT
                self.data = ContractEntity(gateway_name=self.source)
                self.data.deserialize(v[3])
            elif v[2].startswith('11'):
                self.event_type = EventType.ENGINE_CONTROL
                self.msg_type = msg2type
                if len(v) > 3:
                    self.data = v[3]
            elif v[2].startswith('12'):
                self.event_type = EventType.STRATEGY_CONTROL
                self.msg_type = msg2type
                if len(v) > 3:
                    self.data = v[3]
            elif v[2].startswith('14'):
                self.event_type = EventType.RECORDER_CONTROL
                self.msg_type = msg2type
                if len(v) > 3:
                    self.data = v[3]
            elif v[2].startswith('3'):  # msg2type == MSG_TYPE.MSG_TYPE_INFO:
                self.event_type = EventType.INFO
                self.msg_type = msg2type
                self.data = LogEntity(gateway_name=self.source)
                self.data.deserialize(v[3])
            else:
                self.event_type = EventType.HEADER
                self.msg_type = msg2type
        except Exception as e:
            print(e)
            pass