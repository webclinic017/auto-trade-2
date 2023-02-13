-- clickhouse-client -u default --password -m

-- 1.
-- DROP TABLE khouse.test_tick;
CREATE TABLE khouse.test_tick (
  datetime DateTime,
  code String,
  price Float64,
  volume Int32
) ENGINE = MergeTree()
ORDER BY (code, datetime);

-- DROP DICTIONARY khouse.test_tick_dict;
CREATE DICTIONARY khouse.test_tick_dict (
  id Int64,
  code String,
  date DateTime,
  price Float64,
  volume Int32
)
PRIMARY KEY id
SOURCE(CLICKHOUSE(
    -- db = 'khouse',
    table 'test_tick'
))
LIFETIME(MIN 0 MAX 0)
-- LIFETIME(TTL=120)
LAYOUT(FLAT());

-- DROP VIEW khouse.test_tick_dict_mv;
CREATE MATERIALIZED VIEW khouse.test_tick_dict_mv TO khouse.test_tick_dict
AS
    SELECT
        code,
        date,
        price,
        volume
    FROM
        khouse.test_tick;

-- DROP table khouse.test_tick_kline_m1;
create table if not exists khouse.test_tick_kline_1m
(
    date DateTime('Asia/Shanghai'),
    code String,
    open Float32,
    high Float32,
    low Float32,
    close Float32,
    volume Int32
)
ENGINE = AggregatingMergeTree()
ORDER BY (date, code);

set allow_experimental_window_view=1;

-- DROP VIEW khouse.test_tick_kline_1m_wv;
CREATE WINDOW VIEW IF NOT EXISTS khouse.test_tick_kline_1m_wv TO khouse.test_tick_kline_1m  WATERMARK=INTERVAL '2' SECOND  AS
SELECT 
    TUMBLE_START(w_id) as date, 
    code, 
    any(price) as open, 
    max(price) as high,
    min(price) as low, 
    anyLast(price) as close, 
    sum(volume) as volume
FROM khouse.test_tick
GROUP BY TUMBLE(datetime, INTERVAL '1' MINUTE) as w_id, code
ORDER BY w_id, code;

WATCH khouse.test_tick_kline_1m_wv;

-- or
CREATE WINDOW VIEW khouse.test_tick_kline_1m_wv TO khouse.test_tick_kline_m1 WATERMARK=INTERVAL '2' SECOND AS
SELECT
  code,
  floor(date / toIntervalMinute('1') ) * toIntervalMinute('1') as date,
  first(price) as open,
  max(price) as high,
  min(price) as low,
  last(price) as close,
  sum(volume) as volume
FROM khouse.test_tick_dict
GROUP BY code, floor(date / toIntervalMinute('1'));
-- or 