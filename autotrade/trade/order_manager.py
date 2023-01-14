from multiprocessing import Lock
from typing import List

from autotrade.common.singleton import Singleton
from autotrade.common.sql_logger import SQLogger
from autotrade.entities import OrderEntity
from autotrade.entities import PositionEntity
from autotrade.common.constant import Fill


class OrderManager(Singleton):

    logger:SQLogger
    # _count = [0]
    _count:int = 0
    orders_:map[int, OrderEntity]
    fills_:map[int, int];       #signed filled size
    cancels_:map[int, bool] ;    # if cancelled
    wlock:Lock;

    def reset():
        pass

    def track_order(order:OrderEntity): 
        """
          put order under track
        """
        pass

    def got_order(orderid: int):
        
        """
        order acknowledged
        """
        pass

    def got_fill(fill: Fill):
        pass

    def got_cancled_order(orderid: int):
        pass

    def retrieve_order_from_server_orderId(orderid: int) -> OrderEntity:
        pass

    def retrieve_order_from_source_and_client_orderid(source: int,orderid: int) -> OrderEntity:
        pass

    def retrieve_order_from_orderno(orderno: str) -> OrderEntity:
        pass

    def retrieve_order_from_account_and_broker_orderid(account: str,orderid: int) -> OrderEntity:
        pass

    def retrieve_order_from_account_and_localno(account: str,orderno: str) -> OrderEntity:
        pass

    def retrieve_order_from_matchno(fno: str) -> OrderEntity:
        pass

    def retrieve_order_list_by_symbol(fullsymbol: str) -> List[OrderEntity]:
        pass

    def retrieve_non_filled_order_list() -> List[OrderEntity]:
        pass

    def retrieve_non_filled_order_list_by_symbol(fullsymbol: str) -> List[OrderEntity]:
        pass

    def retrieve_non_filled_orderid_list() -> List[int]:
        pass

    def retrieve_non_filled_orderid_list_by_symbol(fullsymbol: str) -> List[int]:
        pass

    def is_empty() -> bool:
        pass

    def is_tracked(orderid: int) -> bool:
        pass

    def is_completed(orderid: int) -> bool:
        """
        either filled or canceled
        """
        pass
    def has_pending_orders() -> bool:
        """
        is all orders either filled or canceled?
        """
        pass