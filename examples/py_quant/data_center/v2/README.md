# 数据

clickhouse 
akshare
## clickhouse 窗口函数

### clickhouse 视图

ClickHouse支持创建普通视图(normal view)、物化视图(materialized view)、实时视图(live view)和窗口视图(window view)，其中实时视图和窗口视图目前还是试验功能，不能保证稳定性。

- Normal View：视图本身并不会存储任何的数据，它们仅仅只是读取了所关联的表格的查询结果而已。一个视图其实保存的是一个 select查询的语句，而不是它查询的结果。

- Materialized View：物化视图和普通视图最大的区别是物化视图实际存储了一份数据。用户查询的时候和表没有区别，更像是一张时刻在预计算的表。在创建物化视图的时候也需要定义存储引擎。

- Live View: 实时视图是一种特殊的视图，类似于ZooKeeper中的注册监听和Redis中的发布订阅，能够将一条SQL查询结果作为监控目标，当 Live view 变化时可以及时感知到。

- Window View：窗口可以按时间窗口聚合数据，类似Flink中的Window，并在窗口结束时输出结果。它将部分聚合结果（预聚合）存储在一个内部(或指定的)表中，以减少延迟，并可以将处理结果推送到指定的表或使用WATCH语句查询推送通知。

通过上面的介绍，我们知道通过窗口视图和时间函数，Clickhouse也拥有了流式数据处理能力。但窗口视图处于实验阶段，需要我们手动开启这项功能，开启的方式有两种：

• 在sql语句中添加一条控制开关： set allow_experimental_window_view = 1

• 在Clickhouse中增加一个用户配置：

• 新建文件：nano /etc/clickhouse-server/users.d/allow_experimental_window_functions.xml

• 写入如下配置：
```xml
  <?xml version="1.0"?>
    <yandex>
    <profiles>
        <default>
            <allow_experimental_window_view>1</allow_experimental_window_view>
        </default>
    </profiles>
    </yandex>
```
其中增加用户配置方案是永久性的，写入后就默认开启此功能。

#### 设计数据表

##### 2.1 原始tick行情数据加工

通常交易所tick行情提供的字段有：

- open：开盘价

- last：最新价

- high：最高价

- low：最低价

- prev_close：昨收价

- volume：累计成交量

- total_turnover：累计成交额

- change_rate：涨跌幅

- ask_price_1-5：卖出价1-5档

- ask_volume_1-5: 卖出量1-5档

- ask_price_1-5：卖出价1-5档

- ask_volume_1-5: 卖出量1-5档

实时处理时通常要使用一个全局字典，将累计成交量、累计成交额转换成切片瞬时成交量和成交金额, 离线处理我们可用 SQL 进行简单的转换。

首先创建一张 tick 数据表(股票代码、交易时间、tick价格、tick成交量、涨跌幅)：

```sql
create table tick.sse50_data
(
    ticker String,
    trade_time DateTime('Asia/Shanghai'),
    tick_price_close Float32,
    tick_volume Int32,
    close_chg_rate Float32
)
ENGINE = AggregatingMergeTree()
ORDER BY (trade_time, ticker)
```

然后使用如下 SQL 进行简单加工，即通过 volume - ifNull(any(volume) OVER (PARTITION BY stock_code ORDER BY trade_time ASC ROWS BETWEEN 1 PRECEDING AND 1 PRECEDING), 0) 语句获得瞬时成交量：

```sql
select 
    stock_code as ticker, 
    trade_time, 
    last as tick_price_close,
    toInt32(volume - ifNull(any(volume) OVER (PARTITION BY stock_code ORDER BY trade_time ASC ROWS BETWEEN 1 PRECEDING AND 1 PRECEDING), 0)) AS tick_volume, 
    round(100 * change_rate, 3)  as close_chg_rate
from tick.sse_50
order by trade_time ASC,  ticker
```

这里我们可以把数据先存储到 data 对象中，后面用来做行情回放，动态写入 tick.sse50_data表中

##### 2.2 设计1分钟窗口视图
首先创建一张1分钟特征表用来存储加工得到的K线特征(包含1分钟开盘价、收盘价、最高价、最低价、平均价、价格标准差、峰度等统计量):

```sql
create table if not exists tick.factor_m1
(
    ticker String,
    trade_timestamp DateTime('Asia/Shanghai'),
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
ORDER BY (trade_timestamp, ticker)
```

然后创建我们的主角，窗口视图：
使用前也需要:
set allow_experimental_window_view = 1;

```sql
CREATE WINDOW VIEW IF NOT EXISTS stock_m1 TO tick.factor_m1  WATERMARK=INTERVAL '2' SECOND  AS
SELECT 
    ticker, 
    tumbleStart(trade_time_id) as trade_timestamp, 
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
FROM tick.sse50_data
GROUP BY tumble(trade_time, INTERVAL '1' MINUTE) as trade_time_id, ticker
ORDER BY trade_time_id, ticker
```

其中 tumble(trade_time, INTERVAL '1' MINUTE) 表示每1分钟执行一次。

#### 三、效果测试

##### 3.1 客户端模拟实时插入

```python
for item in tqdm(data):
    db_client.execute("insert into tick.sse50_data values", [item])
```

3.2 查询
在另一个控制台上查询 tick.factor_m1 表，可以发现数据已经实时写入特征表中了
(K 线与看盘软件有 1 分钟偏移，因为这里时间戳表示该分钟的起始位置)：

图片

通过 WATCH 语句，在控制台中我们能看到 K 线的实时生成：

图片

虽然仍处于实验阶段，但 Clickhouse 窗口视图显示出强大的流式处理能力，
我们可以利用其轻松搭建一个tick级的高频交易系统，
自动提取特征入库，省去手工维护之烦恼。


### other

ClickHouse基于全局字典与物化视图的精确去重方案

clickhouse 具有 bitmap, 但只支持 int, 实测表明 groupBitmap() 这个 agg 比直接的 count(distinct x) 计算要快至少一倍以上, 按之前druid中的测试
经验表明, 全局字典编码后的bitmap的查询性能也远远比普通bitmap好。
通过物化视图对bitmap构建groupBitmapState的中间存储状态, 通过预计算bitmap的并集能减少查询的开销。 并且物化视图的行数远比原始表行数
少, 除了bitmap以外的sum/max/min/avg等计算耗时也呈倍数下降

由于bitmap只支持int类型，所以uid，pid这类long类型的指标需要维护一个全局字典将long类型映射为int类型


```sql

CREATE MATERIALIZED VIEW atsplch_rpt.
ads_screen_unique_indicator_view_local on cluster cluster01
ENGINE = ReplicatedAggregatingMergeTree('/clickhouse/tables/{shard}
/atsplch_rpt/ads_screen_unique_indicator_view_local', '{replica}')
partition by dt
ORDER BY (indicator_id,city_id)
SETTINGS index_granularity = 10
POPULATE
AS SELECT
dt,
indicator_id,
city_id,
groupBitmapState(globalDict('pid_cn', indicator_value)) as
indicator_value_count,
maxState(parseDateTimeBestEffort(create_time)) as create_time
FROM atsplch_rpt.ads_screen_unique_indicator_local
GROUP BY dt,indicator_id,city_id;

```