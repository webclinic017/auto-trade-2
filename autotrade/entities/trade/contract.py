from dataclasses import dataclass
from datetime import datetime
from typing import Any

from autotrade.common.constant import (ACTIVE_STATUSES, Direction, Exchange, 
Offset, OrderFlag, OrderStatus, OrderType, Status,Interval,Product,
OptionType, SYMBOL_TYPE,EXCHANGE_CTP2VT,PRODUCT_CTP2VT,PRODUCT_VT2SQ,
OPTIONTYPE_CTP2VT, ORDERFALG_2VT, ORDERSTATUS_2VT)
from autotrade.common.utils import extract_full_symbol, generate_vt_symbol, generate_full_symbol
from autotrade.entities.base_entity import BaseEntity

from autotrade.api3.ctp_constant import THOST_FTDC_PT_Net

@dataclass
class ContractData(BaseEntity):
    """
    Contract data contains basic information about each contract traded.
    """

    symbol: str = ""
    exchange: Exchange = Exchange.SHFE
    name: str = ""
    product: Product = Product.FUTURES
    size: int = 1
    pricetick: float = 0

    min_volume: float = 1           # minimum trading volume of the contract
    stop_supported: bool = False    # whether server supports stop order
    net_position: bool = False      # whether gateway uses net position volume

    option_strike: float = 0
    option_underlying: str = ""     # vt_symbol of underlying contract
    option_type: OptionType = None
    option_expiry: datetime = None

    # StarQuant field
    full_symbol: str = ""
    long_margin_ratio: float = 0
    short_margin_ratio: float = 0

    def __post_init__(self):
        """"""
        self.vt_symbol = f"{self.symbol}.{self.exchange.value}"

    def deserialize(self, msg: str):
        v = msg.split('|')
        try:
            self.symbol = v[0]
            self.exchange = EXCHANGE_CTP2VT[v[1]]
            self.vt_symbol = f"{self.symbol}.{self.exchange.value}"
            self.name = v[2]
            self.product = PRODUCT_CTP2VT.get(v[3], None)
            st = PRODUCT_VT2SQ[self.product]
            self.full_symbol = generate_full_symbol(
                self.exchange, self.symbol, st)
            self.size = int(v[4])
            self.pricetick = float(v[5])
            if v[6] == THOST_FTDC_PT_Net:
                self.net_position = True
            self.long_margin_ratio = float(v[7])
            self.short_margin_ratio = float(v[8])
            if self.product == Product.OPTION:
                self.option_underlying = v[9]
                self.option_type = OPTIONTYPE_CTP2VT.get(v[10], None)
                self.option_strike = float(v[11])
                self.option_expiry = datetime.strptime(v[12], "%Y%m%d")
        except Exception as e:
            print(e)
            pass

# product = PRODUCT_CTP2VT.get(data["ProductClass"], None)
# if product:
# OPTIONTYPE_CTP2VT.get(data["OptionsType"], None),

@dataclass
class QryContractRequest:
    """
    qry security
    """
    sym_type: SYMBOL_TYPE = SYMBOL_TYPE.FULL
    content: str = ''

    def serialize(self):
        msg = str(self.sym_type.value) + '|' + self.content
        return msg

ContractEntity = ContractData