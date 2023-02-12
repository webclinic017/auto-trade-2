CREATE DATABASE khouse;

-- tick 表:
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


-- tick 表 SQL 简单加工:
select 
    date, 
    code, 
    last as tick_price_close,
    toInt32(volume - ifNull(any(volume) OVER (PARTITION BY code ORDER BY date ASC ROWS BETWEEN 1 PRECEDING AND 1 PRECEDING), 0)) AS tick_volume, 
    round(100 * change_rate, 3)  as close_chg_rate
from khouse.ticks
order by date ASC,  code


-- 1 分钟特征表:
-- drop table khouse.tick_factor_m1
create table if not exists khouse.tick_kline_m1
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

-- 窗口视图：
-- 函数兼容问题，函数名更换试试：
-- TUMBLE --> tumble
-- TUMBLE_START --> tumbleStart
set allow_experimental_window_view = 1;

CREATE WINDOW VIEW IF NOT EXISTS tick_kline_m1_wv TO khouse.tick_kline_m1  WATERMARK=INTERVAL '2' SECOND  AS
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


WATCH tick_kline_m1_wv