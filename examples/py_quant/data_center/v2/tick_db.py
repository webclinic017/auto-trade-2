from clickhouse_driver import Client,connect
import pandahouse as ph
import pandas as pd
import numpy as np
import time


'''
数据的存储和获取

CREATE DATABASE khouse;

tick 表:

create table khouse.ticks
(
    date DateTime('Asia/Shanghai'),
    code String,
    tick_price_close Float32,
    tick_volume Int32,
    close_chg_rate Float32
)
ENGINE = AggregatingMergeTree()
ORDER BY (date, code)


tick 表 SQL 简单加工:

select 
    date, 
    code, 
    last as tick_price_close,
    toInt32(volume - ifNull(any(volume) OVER (PARTITION BY code ORDER BY date ASC ROWS BETWEEN 1 PRECEDING AND 1 PRECEDING), 0)) AS tick_volume, 
    round(100 * change_rate, 3)  as close_chg_rate
from khouse.ticks
order by date ASC,  code


1 分钟特征表:
drop table khouse.tick_factor_m1
create table if not exists khouse.tick_factor_m1
(
    date DateTime('Asia/Shanghai'),
    code String,
    m1_price_open Float32,
    m1_price_close Float32,
    m1_price_high Float32,
    m1_price_low Float32,
    m1_price_avg Float32,
    m1_volume Int32,
    m1_chg_ptp Float32,
    m1_chg_avg Float32,
    m1_price_std Float32,
    m1_price_skew Float32,
    m1_price_kurt Float32
)
ENGINE = AggregatingMergeTree()
ORDER BY (date, code)

窗口视图：

函数兼容问题，函数名更换试试：
TUMBLE --> tumble
TUMBLE_START --> tumbleStart

set allow_experimental_window_view = 1;

CREATE WINDOW VIEW IF NOT EXISTS tick_m1_wv TO khouse.tick_factor_m1  WATERMARK=INTERVAL '2' SECOND  AS
SELECT 
    code, 
    TUMBLE_START(date_id), 
    any(tick_price_close) as m1_price_open, 
    anyLast(tick_price_close) as m1_price_close, 
    max(tick_price_close) as m1_price_high,
    min(tick_price_close) as m1_price_low, 
    0.5 * (m1_price_open + m1_price_close) as m1_price_avg, 
    sum(tick_volume) as m1_volume,
    max(close_chg_rate) - min(close_chg_rate) as m1_chg_ptp,
    avg(close_chg_rate) as m1_chg_avg,
    stddevPop(tick_price_close) as m1_price_std,
    skewPop(tick_price_close) as m1_price_skew,
    kurtPop(tick_price_close) as m1_price_kurt
FROM khouse.ticks
GROUP BY TUMBLE(date, INTERVAL '1' MINUTE) as date_id, code
ORDER BY date_id, code

WATCH tick_m1_wv
'''

connection = dict(database="khouse",
                  host="http://localhost:8123",
                  user='default',
                  password='')

client = Client(host='localhost', port=9000)
# conn = connect(
#     host='localhost', 
#     port=9000, 
#     user='default', 
#     password=''
# )

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

def create_tb_ticks():
    """
    ticks 表:

    :param code:
    :param start_time:
    :param end_time:
    :return:
    """
    sql = \
    """
    create table khouse.ticks
    (
        date DateTime('Asia/Shanghai'),
        code String,
        tick_price_close Float32,
        tick_volume Int32,
        close_chg_rate Float32
    )
    ENGINE = AggregatingMergeTree()
    ORDER BY (date, code)
    """
    return from_table(sql)


def tick_1m_process(code, start_time, end_time):
    """
    tick 表 SQL 简单加工:

    :param code:
    :param start_time:
    :param end_time:
    :return:
    """
    sql = \
    """
    select 
        date, 
        code, 
        last as tick_price_close,
        toInt32(volume - ifNull(any(volume) OVER (PARTITION BY code ORDER BY date ASC ROWS BETWEEN 1 PRECEDING AND 1 PRECEDING), 0)) AS tick_volume, 
        round(100 * change_rate, 3)  as close_chg_rate
    from khouse.ticks
    order by date ASC,  code
    """
    # sql = "select * from khouse.stock_daily_price where code == '{}' and date between '{}' and '{}'" \
    #     .format(code, start_time, end_time)
    return from_table(sql)

def create_tb_tick_factor_1m():
    """
    tick_factor_1m 表:

    :param code:
    :param start_time:
    :param end_time:
    :return:
    """
    sql = \
    """
create table if not exists khouse.tick_factor_m1
(
    date DateTime('Asia/Shanghai'),
    code String,
    m1_price_open Float32,
    m1_price_close Float32,
    m1_price_high Float32,
    m1_price_low Float32,
    m1_price_avg Float32,
    m1_volume Int32,
    m1_chg_ptp Float32,
    m1_chg_avg Float32,
    m1_price_std Float32,
    m1_price_skew Float32,
    m1_price_kurt Float32
)
ENGINE = AggregatingMergeTree()
ORDER BY (date, code)
    """
    return from_table(sql)

def create_tick_1m_wv():
    """
    tick_1m_wv 窗口视图:

    :param code:
    :param start_time:
    :param end_time:
    :return:
    """
#     函数兼容问题，函数名更换试试：
#     TUMBLE --> tumble
#     TUMBLE_START --> tumbleStart
    sql = \
    """
set allow_experimental_window_view = 1;

CREATE WINDOW VIEW IF NOT EXISTS tick_m1_wv TO khouse.tick_factor_m1  WATERMARK=INTERVAL '2' SECOND  AS
SELECT 
    code, 
    TUMBLE_START(date_id), 
    any(tick_price_close) as m1_price_open, 
    anyLast(tick_price_close) as m1_price_close, 
    max(tick_price_close) as m1_price_high,
    min(tick_price_close) as m1_price_low, 
    0.5 * (m1_price_open + m1_price_close) as m1_price_avg, 
    sum(tick_volume) as m1_volume,
    max(close_chg_rate) - min(close_chg_rate) as m1_chg_ptp,
    avg(close_chg_rate) as m1_chg_avg,
    stddevPop(tick_price_close) as m1_price_std,
    skewPop(tick_price_close) as m1_price_skew,
    kurtPop(tick_price_close) as m1_price_kurt
FROM khouse.ticks
GROUP BY TUMBLE(date, INTERVAL '1' MINUTE) as date_id, code
ORDER BY date_id, code
    """
    # sql = "select * from khouse.stock_daily_price where code == '{}' and date between '{}' and '{}'" \
    #     .format(code, start_time, end_time)
    return from_table(sql)

def all_ticks(start_time, end_time):
    """
    获取所有股票某时间段的 tick 行情数据
    select *
    from khouse.ticks
    where date between '2022-03-30' and '2022-07-29'
    :param start_time:
    :param end_time:
    :return:
    """
    sql = "select * from khouse.ticks where date between '{}' and '{}'" \
        .format(start_time, end_time)
    return from_table(sql)

def all_ticks_1m(start_time, end_time):
    """
    获取所有股票某时间段的 tick 行情数据
    select *
    from khouse.tick_factor_m1
    where date between '2022-03-30' and '2022-07-29'
    :param start_time:
    :param end_time:
    :return:
    """
    sql = "select * from khouse.tick_factor_m1 where date between '{}' and '{}'" \
        .format(start_time, end_time)
    return from_table(sql)

def create_demo_wv():
    # Create a window view
    query = '''
    CREATE TEMPORARY WINDOW table_name
    ON database_name
    AS
    SELECT column1, column2, column3
    FROM table_name
    ORDER BY timestamp
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    '''
    client.execute(query)

def gen_mock_kline(days,start_price,colName,startDate,seed=None): 
    periods = days*24
    np.random.seed(seed)
    steps = np.random.normal(loc=0, scale=0.0018, size=periods)
    steps[0]=0
    P = start_price+np.cumsum(steps)
    P = [round(i,4) for i in P]

    fxDF = pd.DataFrame({ 
        'ticker':np.repeat( [colName], periods ),
        'date':np.tile( pd.date_range(startDate, periods=periods, freq='H'), 1 ),
        'price':(P)})
    fxDF.index = pd.to_datetime(fxDF.date)
    fxDF = fxDF.price.resample('D').ohlc()
    return fxDF

def gen_mock_tick(days=1,start_price=1.0,code="000001",start_date="2023-02-09 09:30:00",seed=None): 
    freq = 'S'
    periods = days*2*60*60
    np.random.seed(seed)
    steps = np.random.normal(loc=0, scale=0.0018, size=periods)
    steps[0]=0
    P = start_price+ np.cumsum(steps)
    P = [round(i,4) for i in P]

    fxDF = pd.DataFrame({ 
        'date':np.tile(pd.date_range(start_date, periods=periods, freq=freq), 1),
        'code':np.repeat( [code], periods ),
        'price':(P),
        'tick_volume': np.random.randint(low=1000, high=8000, size=periods, dtype='l'),
        'close_chg_rate':(P)},
    )
    first = fxDF['price'][0]
    fxDF['close_chg_rate'] = fxDF['price'].apply(lambda x:  x/ first -1 )
    fxDF.index = pd.to_datetime(fxDF.date)
    return fxDF

def mock_ticks_insert():
    """
    mock insert ticks 行情数据, tick_wv(Window View) 会有变化 
    :param start_time:
    :param end_time:
    :return:
    """
    # df = pd.DataFrame(
    #     { 
    #     "date":["2023-02-08 15:00:00"],
    #     "code":["688787"],
    #     "tick_price_close":[189.6],
    #     "tick_volume":[48665.0],
    #     "close_chg_rate":[20.0],
    #     }
    # )
    df = gen_mock_tick(1)
    # net_df 的列名可能和数据库列名不一样，修改列名对应数据库的列名
    df.columns = ['date', 'code', 'tick_price_close', 'tick_volume', 'close_chg_rate']
    # 修改 index 为 date 去掉默认的 index 便于直接插入数据库
    df["date"] = pd.to_datetime(df["date"])
    df.set_index(['date'], inplace=True)

    print(df)
    return
    return to_table(data=df, table="ticks")

def create_tick_tb_and_wv():
    # 创建
    # create_tb_ticks()
    # create_tb_tick_factor_1m()
    # create_tick_1m_wv()

    # watch 窗口试图
    # watch_ticks_1m_wv2()

    # 模拟插入数据
    # mock_ticks_insert()
    pass

def watch_ticks_1m_wv2():
    """
    WATCH tick_m1_wv 窗口视图 行情数据
    WATCH tick_m1_wv
    :param start_time:
    :param end_time:
    :return:
    """

    sql = "WATCH tick_m1_wv"

    return from_table(sql)

def watch_ticks_1m_wv2():
    """
    WATCH tick_m1_wv 窗口视图 行情数据
    WATCH tick_m1_wv
    :param start_time:
    :param end_time:
    :return:
    """

    sql = "WATCH tick_m1_wv"

    return client.execute(sql)


if __name__ == '__main__':
    mock_ticks_insert()
    # create_tick_tb_and_wv()
    pass