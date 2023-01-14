from abc import ABCMeta, abstractmethod


class RiskManagerBase(metaclass=ABCMeta):
    """
    RiskManager base class
    """
    @abstractmethod
    def order_in_compliance(self, original_order):
        raise NotImplementedError("order_in_compliance should be implemented")