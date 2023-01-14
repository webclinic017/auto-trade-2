from dataclasses import dataclass
from autotrade.entities.base_entity import BaseEntity

@dataclass
class AccountData(BaseEntity):
    """
    Account data contains information about balance, frozen and
    available.
    """

    accountid: str = ""

    balance: float = 0
    frozen: float = 0
# StarQuant field

    yd_balance: float = 0
    netliquid: float = 0
    commission: float = 0
    margin: float = 0
    closed_pnl: float = 0
    open_pnl: float = 0
    timestamp: str = ""

    def __post_init__(self):
        """"""
        self.available = self.balance - self.frozen
        self.vt_accountid = f"{self.gateway_name}.{self.accountid}"

    def deserialize(self, msg: str):
        v = msg.split('|')
        try:
            self.accountid = v[0]
            self.vt_accountid = f"{self.gateway_name}.{self.accountid}"
            self.yd_balance = float(v[1])
            self.netliquid = float(v[2])
            self.available = float(v[3])
            self.commission = float(v[4])
            self.margin = float(v[5])
            self.closed_pnl = float(v[6])
            self.open_pnl = float(v[7])
            self.balance = float(v[8])
            self.frozen = float(v[9])
            self.timestamp = v[10]
        except Exception as e:
            print(e)
            pass

AccountEntity = AccountData