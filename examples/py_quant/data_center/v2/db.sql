CREATE DATABASE khouse;

CREATE TABLE khouse.stock_daily_price
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