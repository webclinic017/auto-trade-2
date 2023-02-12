-- chatgpt
-- 使用 clickhouse 全局字典和物化视图存储和读取 tick 数据，并合成 1 分钟 k 线

-- 首先需要创建一个存储 tick 数据的表：
CREATE TABLE IF NOT EXISTS tick (
    date Date,
    time Time,
    code String,
    price Float64,
    volume UInt64
) ENGINE = MergeTree(date, (code, time), 8192);

-- 然后使用全局字典存储 code 列：
CREATE DICTIONARY IF NOT EXISTS code_dict 
(
    code String
) 
PRIMARY KEY code
LAYOUT(FLAT());

-- 接下来创建物化视图：
CREATE MATERIALIZED VIEW IF NOT EXISTS k_line_1m
ENGINE = AggregatingMergeTree(date, (code, intDiv(toUInt32(time), 60)), 8192)
AS 
SELECT 
    date,
    intDiv(toUInt32(time), 60) * 60 AS time,
    code,
    dictionaryGet(code_dict, code, 'unkown_code') AS code_name,
    -- first(price) AS open
    min(price) AS low
    max(price) AS high
    -- last(price) AS close
    avg(price) AS avg_price,
    sum(volume) AS volume
FROM tick_data
GROUP BY date, intDiv(toUInt32(time), 60), code;

-- 最后，可以通过读取 k_line_1m 表来获取合成的 1 分钟 k 线数据。
SELECT * FROM k_line_1m;

-- 注意：以上代码只是示例，实际使用还需要根据需求进行修改。