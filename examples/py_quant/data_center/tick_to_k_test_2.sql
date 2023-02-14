-- chatgpt

-- 1. clickhouse 字典和窗口视图实现存储和读取 tick 数据， 并合成 1 分钟 k 线

-- 存储 Tick 数据：
-- 首先需要创建一个存储 Tick 数据的表，例如：
CREATE TABLE test2_tick (
  tick_time DateTime,
  code String,
  price Float32,
  volume Int64
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(tick_time)
ORDER BY (code, tick_time);

-- 然后，需要创建一个全局字典，以存储股票代码的映射关系：
-- CREATE DICTIONARY test2_tick_dict (code String)
-- PRIMARY KEY code
-- LIFETIME(MINUTE)
-- SOURCE(CLICKHOUSE_DICT_SOURCES=['host=127.0.0.1:9000']);

-- 读取并合成 1 分钟 k 线：

-- 使用窗口视图，可以对每个股票的 Tick 数据按照时间分组，
-- 并计算每个分组的最高价、最低价、开盘价、收盘价和交易量：
WITH test2_kline_window AS (
  SELECT 
    tick_time,
    code,
    argMin(tick_time, price) AS low,
    argMax(tick_time, price) AS high,
    first(price) AS open,
    last(price) AS close,
    sum(volume) AS volume
  FROM test2_tick
  WINDOW BY code, chunk(1, 0)
)
SELECT 
  date_trunc('minute', tick_time) AS kline_time,
  code,
  low,
  high,
  open,
  close,
  volume
FROM test2_kline_window;

-- 最后，使用全局字典将股票代码映射为股票名称：
-- WITH kline_window AS (
--   SELECT 
--     tick_time,
--     code,
--     argMin(tick_time, price) AS low,
--     argMax(tick_time, price) AS high,
--     first(price) AS open,
--     last(price) AS close,
--     sum(volume) AS volume
--   FROM test_tick
--   WINDOW BY code, chunk(1, 0)
-- ), code_mapped AS (
--   SELECT
--     kline_time,
--     stock_dict.get(code) AS name,
--     low,
--     high,
--     open,
--     close,
--     volume
--   )
