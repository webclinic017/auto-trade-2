import datetime

from backtrader import TimeFrame
from backtrader import date2num, num2date
from backtrader.feed import DataBase


class ClickhouseFeed(DataBase):
    params = (
        # object of class clickhouse_driver.Client
        ('client', None),


        # Note:
        #  set fields order as u want, cause the field has been ordered before selecting from clickhouse
        #  1. default order t0,o1,h2,l3,c4,v5,op-1
        #  2. < 0 column not present
        #  3. >=0 numeric index to the column after selected from clickhouse
        ('datetime', 0),
        ('open', 1), ('high', 2), ('low', 3), ('close', 4), ('volume', 5), ('openinterest', -1),
    )

    def __init__(self):
        super(ClickhouseFeed, self).__init__()


    def get_client(self):
        self.p.client = Client(host="localhost", port=19090,
                               user="default", compression="lz4",
                               settings={"use_numpy": False, 'max_block_size': 100000})
        return self.p.client

    def start(self):
        self.p.client: Client
        if not self.p.client:
            self.get_client()

        table_name = self.p.dataname

        # ck: short name for clickhouse
        self.ckfield = list(filter(
            lambda x: getattr(self.params, x) is not None and getattr(self.params, x) >= 0,
            self.getlinealiases()))

        def sort_key(field):
            return getattr(self.params, field)

        self.ckfield.sort(key=sort_key)

        # Note: 'timestamp' key field cannot be renamed in ck,
        #  deal with it here by replacing with 'datetime', u may not do that in ur case
        # ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'turnover', 'b1_p'...]
        self.ckfield[getattr(self.params, 'datetime')] = 'timestamp'
        self.sql = f"select {','.join(self.ckfield)} " \
                   f"from {table_name} " \
                   f"where symbol like 'sh%' and " \
                   f"timestamp between '{self.p.fromdate}' and '{self.p.todate}' "
        self.rows_gen = self.p.client.execute_iter(self.sql)

    def _load(self):
        if not self.rows_gen:
            return False
        try:
            row = next(self.rows_gen)
        except StopIteration:
            return False

        # Note: 取出来的datetime时间戳不能带有tzinfo信息(如果带有则需要删除),
        #       否则date2num后时间不正确
        self.lines.datetime[0] = date2num(row[self.p.datetime].replace(tzinfo=None))

        for ck_field in (x for x in self.ckfield if x != 'timestamp'):
            line_index = getattr(self.params, ck_field)
            line = getattr(self.lines, ck_field)
            line[0] = row[line_index]

        return True

    def stop(self):
        print('stop')
        self.p.client: Client
        self.p.client.disconnect()

