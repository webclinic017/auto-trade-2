-- clickhouse-client -u default --password -m

-- 1.
-- DROP TABLE khouse.test_tick;
CREATE TABLE khouse.test_tick (
  code String,
  time DateTime('Asia/Shanghai'),
  price Float64,
  volume Int32
) 
ENGINE = AggregatingMergeTree()
ORDER BY (time,code);

-- DROP DICTIONARY khouse.test_tick_dict;
-- CREATE DICTIONARY khouse.test_tick_dict (
--   id Int64,
--   code String,
--   time DateTime,
--   price Float64,
--   volume Int32
-- )
-- PRIMARY KEY id
-- SOURCE(CLICKHOUSE(
--     -- db = 'khouse',
--     table 'test_tick'
-- ))
-- LIFETIME(MIN 0 MAX 0)
-- -- LIFETIME(TTL=120)
-- LAYOUT(FLAT());

-- DROP VIEW khouse.test_tick_dict_mv;
-- CREATE MATERIALIZED VIEW khouse.test_tick_dict_mv TO khouse.test_tick_dict
-- AS
--     SELECT
--         code,
--         time,
--         price,
--         volume
--     FROM
--         khouse.test_tick;


-- DROP table khouse.test_tick_kline_1m;
create table if not exists khouse.test_tick_kline_1m
(
    code String,
    date DateTime('Asia/Shanghai'),
    open Float32,
    high Float32,
    low Float32,
    close Float32,
    volume Int32
)
ENGINE = AggregatingMergeTree()
ORDER BY (date, code);

-- DROP table khouse.test_tick_kline_5m;
create table if not exists khouse.test_tick_kline_5m
(
    code String,
    date DateTime('Asia/Shanghai'),
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
    code, 
    TUMBLE_START(date_id) as date, 
    any(price) as open, 
    max(price) as high,
    min(price) as low, 
    anyLast(price) as close, 
    sum(volume) as volume
FROM khouse.test_tick
GROUP BY TUMBLE(time, INTERVAL '1' MINUTE) as date_id, code
ORDER BY date_id, code;

WATCH khouse.test_tick_kline_1m_wv;

-- or
-- CREATE WINDOW VIEW khouse.test_tick_kline_1m_wv TO khouse.test_tick_kline_m1 WATERMARK=INTERVAL '2' SECOND AS
-- SELECT
--   code,
--   floor(date / toIntervalMinute('1') ) * toIntervalMinute('1') as date,
--   first(price) as open,
--   max(price) as high,
--   min(price) as low,
--   last(price) as close,
--   sum(volume) as volume
-- FROM khouse.test_tick_dict
-- GROUP BY code, floor(date / toIntervalMinute('1'));

-- or
-- DROP VIEW khouse.test_tick_kline_1m_mv;
CREATE MATERIALIZED VIEW khouse.test_tick_kline_1m_mv TO khouse.test_tick_kline_1m AS
SELECT 
    code, 
    -- toStartOfMinute(time) AS date, 
    TUMBLE_START(date_id) as date, 
    any(price) as open, 
    max(price) AS high, 
    min(price) AS low, 
    -- sum(price) / count(*) AS close, 
    anyLast(price) as close, 
    sum(volume) AS volume
FROM khouse.test_tick
GROUP BY code, TUMBLE(time, INTERVAL '1' MINUTE)  as date_id
ORDER BY date_id, code;

SELECT * FROM khouse.test_tick_kline_1m_mv

-- DROP VIEW khouse.test_tick_kline_5m_mv;
CREATE MATERIALIZED VIEW khouse.test_tick_kline_5m_mv TO khouse.test_tick_kline_5m AS
SELECT 
    code, 
    -- toStartOfMinute(time) AS date, 
    TUMBLE_START(date_id) as date, 
    any(price) as open, 
    max(price) AS high, 
    min(price) AS low, 
    -- sum(price) / count(*) AS close, 
    anyLast(price) as close, 
    sum(volume) AS volume
FROM khouse.test_tick
GROUP BY code, TUMBLE(time, INTERVAL '5' MINUTE)  as date_id
ORDER BY date_id, code;