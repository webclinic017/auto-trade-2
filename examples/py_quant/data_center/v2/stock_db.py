import pandahouse as ph
import time

'''
数据的存储和获取
CREATE TABLE stock.stock_daily_price
(
    `date`   Date,
    `code`   String,
    `open`   Float32,
    `high`   Float32,
    `low`    Float32,
    `close`  Float32,
    `volume` Float64,
    `amount` Float64
--     `adj_factor` Int32,
--     `st_status` Int16,
--     `trade_status` Int16
) ENGINE = ReplacingMergeTree()
      ORDER BY (javaHash(code), date)
'''

connection = dict(database="stock",
                  host="http://localhost:8123",
                  user='default',
                  password='sykent')


def to_table(data, table):
    """
    插入数据到表
    :param data:
    :param table:
    :return:
    """
    affected_rows = ph.to_clickhouse(data, table=table, connection=connection)
    return affected_rows


def from_table(sql):
    """
    查询表
    :param sql:
    :return: dataframe
    """
    last_time = time.time()
    df = ph.read_clickhouse(sql, connection=connection)
    print("db-> 耗时: {}  sql: {}".format((time.time() - last_time) * 1000, sql))
    return df


def stock_daily(code, start_time, end_time):
    """
    获取某股票，某时间段的日行情数据
    select *
    from stock_daily_price
    where code == '000001' and date between '2022-03-30' and '2022-07-29'
    :param code:
    :param start_time:
    :param end_time:
    :return:
    """
    sql = "select * from stock.stock_daily_price where code == '{}' and date between '{}' and '{}'" \
        .format(code, start_time, end_time)
    return from_table(sql)


def all_stock_daily(start_time, end_time):
    """
    获取所有股票某时间段的日行情数据
    select *
    from stock.stock_daily_price
    where date between '2022-03-30' and '2022-07-29'
    :param start_time:
    :param end_time:
    :return:
    """
    sql = "select * from stock.stock_daily_price where date between '{}' and '{}'" \
        .format(start_time, end_time)
    return from_table(sql)
