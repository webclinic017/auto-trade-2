

from autotrade.entities import PositionEntity
from autotrade.common.constant import Fill

# Gets the open PL on a per-share basis, ignoring the size of the position.
def open_pt(last_trade:float,  avg_price:float, side: bool) -> float:
    pass

def open_pt(last_trade:float,  avg_price:float, position_size: int) -> float:
    pass

# Gets the open PL considering all the shares held in a position.
def open_pl(last_trade:float,  avg_price:float, position_size_multiplier: int) -> float:
    pass

# Gets the closed PL on a per-share basis, ignoring how many shares are held.
def close_pt(existing: PositionEntity, adjust:Fill) -> float:
    pass

# Gets the closed PL on a position basis, the PL that is registered to the account for the entire shares transacted.
def close_pl(existing:PositionEntity, adjust:Fill, position_size_multiplier: int) -> float:
    pass
