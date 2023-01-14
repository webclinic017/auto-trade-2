from dataclasses import dataclass, field


@dataclass
class BaseEntity:
    """
    Any Entity object needs a gateway_name as source 
    and should inherit base data.
    """

    gateway_name: str = ''

    def serialize(self):
        pass

    def deserialize(self, msg):
        pass