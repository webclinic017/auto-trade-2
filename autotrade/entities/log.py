from dataclasses import dataclass
from datetime import datetime
from logging import INFO

from dataclasses import dataclass
from autotrade.entities.base_entity import BaseEntity

@dataclass
class LogData(BaseEntity):
    """
    Log data is used for recording log messages on GUI or in log files.
    """

    msg: str = ''
    level: int = INFO
# StarQuant field
    timestamp: str = ''

    def __post_init__(self):
        """"""
        self.time = datetime.now()

    def deserialize(self, msg: str):
        v = msg.split('|')
        try:
            self.msg = v[0]
            self.timestamp = v[1]
        except Exception as e:
            print(e)
            pass

LogEntity = LogData