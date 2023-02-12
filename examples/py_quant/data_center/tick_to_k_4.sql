-- chaptgpt
-- 1. 使用全局字典实现存储 tick 数据，并合成 1 分钟 k 线数据

-- ClickHouse 的全局字典功能可以在多个表间共享字典数据，避免重复的数据存储。
-- 如果需要使用全局字典实现存储 tick 数据并合成 1 分钟 k 线数据，需要进行以下步骤：

-- 创建存储 tick 数据的表：
CREATE TABLE tick_data (
    `symbol` String,
    `datetime` DateTime,
    `price` Float64,
    `volume` UInt64
) ENGINE = MergeTree(datetime, (symbol, datetime), 8192)

-- 创建存储 k 线数据的表：
CREATE TABLE k_line (
    `symbol` String,
    `datetime` DateTime,
    `open` Float64,
    `high` Float64,
    `low` Float64,
    `close` Float64,
    `volume` UInt64
) ENGINE = MergeTree(datetime, (symbol, datetime), 8192)

-- 创建全局字典：
CREATE DICTIONARY global_dict_symbol (
    `symbol` String,
    `id` UInt64
) PRIMARY KEY symbol
    SOURCE(CLICKHOUSE_DICT_SRC(
        db = 'system',
        table = 'one',
        dict_key_column = 'symbol',
        dict_value_column = 'id'
    ))

-- 创建存储 symbol ID 和合成 k 线所需信息的表：
CREATE TABLE symbol_tmp (
    `id` UInt64,
    `symbol` String,
    `datetime` DateTime,
    `price` Float64,
    `volume` UInt64
) ENGINE = Memory()

-- 将 tick 数据加载到 symbol_tmp 表中：
INSERT INTO symbol_tmp
SELECT dictGetUInt64('global_dict_symbol', symbol), symbol, datetime, price, volume
FROM tick_data

-- 使用窗口视图合成 k 线数据：
INSERT INTO k_line
SELECT
    symbol,
    floor(datetime / 60) * 60 AS datetime,
    first(price) OVER w1 AS open,
    max(price) OVER w1


-- 2. clickhouse 使用全局字典和物化视图实现存储 tick 数据，并合成 1 分钟 k 线数据

-- 在 ClickHouse 中，您可以使用全局字典和物化视图来存储 "Tick" 数据并合成 1 分钟 K 线数据。
-- 以下是一个实现此功能的代码示例：

CREATE DICTIONARY tick_data_dict (
    symbol String,
    datetime DateTime,
    price Float64,
    volume UInt64
) 
PRIMARY KEY symbol, datetime
SOURCES(
    mysql(
        host: 'localhost',
        port: 3306,
        user: 'root',
        password: 'password',
        database: 'tick_data'
    )
)

CREATE MATERIALIZED VIEW tick_data_mv TO tick_data_dict
AS
    SELECT
        symbol,
        datetime,
        price,
        volume
    FROM
        tick_data

WITH MinuteData AS (
    SELECT
        symbol,
        floor(toUInt32(datetime) / 60) AS minute_time,
        min(price) AS open,
        max(price) AS high,
        avg(price) AS close,
        sum(volume) AS volume
    FROM
        tick_data_dict
    GROUP BY
        symbol,
        floor(toUInt32(datetime) / 60)
)

SELECT * FROM MinuteData

-- 此代码将创建一个全局字典 "tick_data_dict"，并从 MySQL 数据库中读取数据进行存储。
-- 然后，它创建了一个物化视图 "tick_data_mv"，该物化视图从字典 "tick_data_dict" 中选择相关数据，以方便查询。
-- 最后，该代码使用 "GROUP BY" 语句对数据进行分组，以生成每分钟的 K 线数据。

-- 请注意，此代码假定您已经在 MySQL 数据库中创建了名为 "tick_data" 的表，
-- 并且已经根据您的具体需求调整了数据结构。您可以通过调整该代码中的 SELECT 语句来根据您


-- 3. clickhouse 使用全局字典和窗口视图实现存储 tick 数据，并合成 1 分钟 k 线数据

-- ClickHouse 是一个列式存储数据库，可以通过全局字典和窗口视图来实现存储 tick 数据，并合成 1 分钟 k 线数据。

-- 首先，我们需要创建一个表来存储原始的 tick 数据，如下：
CREATE TABLE tick_data (
  datetime DateTime,
  code String,
  price Float64,
  volume Int32
) ENGINE = MergeTree()
ORDER BY (code, datetime);

-- 接着，创建一个全局字典来存储每个合约的实时价格：
CREATE DICTIONARY last_price (
  code String,
  price Float64
) PRIMARY KEY code
SOURCE(CLICKHOUSE_DICT_SOURCES=tick_data)
LIFETIME(TTL=30);
-- 全局字典从 tick_data 表中获取数据，并设置了生存期为 30 秒。

-- 最后，我们创建一个窗口视图来从 tick 数据合成 1 分钟 k 线数据：
set allow_experimental_window_view=1;
CREATE WINDOW VIEW wv_kline_1min_wv AS
SELECT
  code,
  floor(datetime / interval 1 minute) * interval 1 minute as datetime,
  first(price) as open,
  max(price) as high,
  min(price) as low,
  last(price) as close,
  sum(volume) as volume
FROM tick_data
GROUP BY code, floor(datetime / interval 1 minute);
-- 窗口视图在查询 tick_data 表时，通过 GROUP BY 和 floor 函数来合成每个合约的 1 分钟 k 线数据。

-- 这样，我们就可以在 ClickHouse 中存储实时 tick 数据，并实时合成 1 分钟 k 线数据了。


-- 在 ClickHouse 中，全局字典是一种常用的数据压缩方式，可以用来存储变量的值和对应的编号，从而减小存储空间和提高查询性能。

-- 在存储 tick 数据时，可以将交易代码、交易时间等数据压缩为编号，使用全局字典存储。

-- 合成 1 分钟 k 线数据时，可以使用 ClickHouse 的窗口视图进行数据处理，对
-- 每个 1 分钟的数据窗口计算最高价、最低价、开盘价、收盘价等指标，生成 1 分钟 k 线数据。

-- 以下是一个简单的实现代码：
CREATE DICTIONARY stock_dict (symbol String, id UInt64)
PRIMARY KEY symbol
LAYOUT FLAT();

INSERT INTO stock_dict (symbol) VALUES ('AAPL'), ('GOOG'), ('TSLA'), ('AMZN');

CREATE TABLE tick_data (
  symbol_id UInt64,
  time DateTime,
  price Float32,
  volume UInt32
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(time)
ORDER BY (symbol_id, time);

INSERT INTO tick_data
SELECT
  id,
  '2022-01-01 10:00:00' + number * 300 AS time,
  rand(),
  rand()
FROM
  numbers(100)
JOIN stock_dict
ON
  symbol = 'AAPL';

set allow_experimental_window_view=1；
CREATE WINDOW VIEW kline_data AS
SELECT
  symbol_id,
  toStartOfMinute(time) AS time,
  any(price) AS open,
  max(price) AS high,
  min(price) AS low,
  avg(price) AS close,
  sum(volume) AS volume
FROM
  tick_data
GROUP BY
  symbol_id,
  time;

SELECT * FROM kline_data;
-- 这是一个简单的实现，如需要获取实际的实现代码，请考虑根据具体需求实现

-- 继续说
-- 在 ClickHouse 中，您可以使用全局字典来优化存储频繁出现的数据项。
-- 在全局字典中，您可以将数据映射到整数编号，以节省存储空间。

-- 在存储 tick 数据时，您可以使用全局字典将合约代码，交易所编号等信息映射到整数编号。
-- 在此之后，您可以在窗口视图中对数据进行聚合，并生成一分钟 k 线数据。

-- 以下是一段示例代码：
CREATE DICTIONARY dict_exchange (
    id       UInt32,
    name     String
) PRIMARY KEY id
LAYOUT(DENSE)
TO dict.txt;

CREATE DICTIONARY dict_symbol (
    id       UInt32,
    name     String
) PRIMARY KEY id
LAYOUT(DENSE)
TO dict.txt;

CREATE TABLE tick_data (
    datetime         DateTime,
    exchange         UInt32,
    symbol           UInt32,
    last_price       Float32,
    volume           UInt32
) ENGINE=MergeTree(datetime, (exchange, symbol), 8192);

CREATE MATERIALIZED VIEW mv_1min_kline AS
SELECT 
    datetime, 
    exchange, 
    symbol, 
    last_price, 
    volume, 
    toDateTime(floor((toUInt32(datetime) - toUInt32('1970-01-01 00:00:00')) / 60) * 60) AS kline_time
FROM tick_data
GROUP BY 
    exchange, 
    symbol, 
    kline_time
-- 在上面的代码中，我们首先创建了两个全局字典，分别存储交易所编号和合约代码。
-- 然后，我们创建了一个 tick_data 表，其中存储了原始的 tick 数据。
-- 最后，我们创建了一个窗口视图 mv_1min_kline



